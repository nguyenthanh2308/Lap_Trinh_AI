"""
Fine-tune a causal language model for the story generator API.

The script reads parquet rows, converts each row into the same prompt shape used
by the API, and saves a Hugging Face model folder that app.config can load from
MODEL_FOLDER=./fine_tuned_model.

Example:
    python train_story_model.py ^
      --train ..\\train-00000-of-00001.parquet ^
      --test ..\\test-00000-of-00001.parquet ^
      --output .\\fine_tuned_model ^
      --max-samples 5000
"""

from __future__ import annotations

import argparse
import json
import math
import random
import re
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Iterable

import pandas as pd
import torch
from torch.utils.data import DataLoader, Dataset
from transformers import (
    AutoModelForCausalLM,
    AutoTokenizer,
    get_linear_schedule_with_warmup,
)


NAMES = [
    "Minh",
    "Anna",
    "Leo",
    "Maya",
    "Linh",
    "Noah",
    "Iris",
    "Kai",
    "Thao",
    "Eli",
]

PERSONALITIES = [
    "brave and curious",
    "quiet but observant",
    "kind-hearted and stubborn",
    "clever and impatient",
    "gentle but determined",
    "playful and honest",
    "cautious yet loyal",
    "creative and restless",
]

SETTINGS = [
    "a coastal village",
    "an old library",
    "a mountain town",
    "a crowded night market",
    "a futuristic city",
    "a forest after heavy rain",
    "a small train station",
    "a school before sunrise",
]

THEMES = [
    "adventure",
    "friendship",
    "hope",
    "courage",
    "family",
    "mystery",
    "growth",
    "trust",
]


@dataclass
class TrainConfig:
    train: str
    test: str | None
    output: str
    base_model: str
    text_column: str
    target_mode: str
    max_samples: int
    max_eval_samples: int
    max_source_chars: int
    block_size: int
    epochs: int
    batch_size: int
    gradient_accumulation_steps: int
    learning_rate: float
    warmup_ratio: float
    seed: int
    device: str
    checkpoint_steps: int
    resume_from_checkpoint: str
    dry_run: bool


class StoryDataset(Dataset):
    def __init__(self, examples: list[str], tokenizer, block_size: int) -> None:
        self.examples = examples
        self.tokenizer = tokenizer
        self.block_size = block_size

    def __len__(self) -> int:
        return len(self.examples)

    def __getitem__(self, index: int) -> dict[str, torch.Tensor]:
        encoded = self.tokenizer(
            self.examples[index],
            truncation=True,
            max_length=self.block_size,
            padding="max_length",
            return_tensors="pt",
        )
        input_ids = encoded["input_ids"].squeeze(0)
        attention_mask = encoded["attention_mask"].squeeze(0)
        labels = input_ids.clone()
        labels[attention_mask == 0] = -100
        return {
            "input_ids": input_ids,
            "attention_mask": attention_mask,
            "labels": labels,
        }


def parse_args() -> TrainConfig:
    parser = argparse.ArgumentParser(description="Fine-tune story generation model.")
    parser.add_argument("--train", default="../train-00000-of-00001.parquet")
    parser.add_argument("--test", default="../test-00000-of-00001.parquet")
    parser.add_argument("--output", default="./fine_tuned_model")
    parser.add_argument("--base-model", default="gpt2")
    parser.add_argument(
        "--text-column",
        default="auto",
        help="Column to train on. Use auto to prefer story/textbook/text.",
    )
    parser.add_argument(
        "--target-mode",
        default="synthetic-story",
        choices=["synthetic-story", "raw-continuation"],
        help=(
            "synthetic-story turns dataset rows into short story targets using "
            "the row topic; raw-continuation trains directly on the source text."
        ),
    )
    parser.add_argument("--max-samples", type=int, default=5000)
    parser.add_argument("--max-eval-samples", type=int, default=500)
    parser.add_argument("--max-source-chars", type=int, default=1400)
    parser.add_argument("--block-size", type=int, default=384)
    parser.add_argument("--epochs", type=int, default=1)
    parser.add_argument("--batch-size", type=int, default=1)
    parser.add_argument("--gradient-accumulation-steps", type=int, default=8)
    parser.add_argument("--learning-rate", type=float, default=5e-5)
    parser.add_argument("--warmup-ratio", type=float, default=0.03)
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument(
        "--device",
        default="auto",
        choices=["auto", "cpu", "cuda"],
        help="Training device. Auto uses CUDA when available.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Build and print a sample training example without loading a model.",
    )
    parser.add_argument(
        "--checkpoint-steps",
        type=int,
        default=50,
        help="Save a resumable checkpoint every N optimizer steps. Use 0 to disable.",
    )
    parser.add_argument(
        "--resume-from-checkpoint",
        default="auto",
        help=(
            "Checkpoint folder to resume from. Use auto to pick the latest "
            "checkpoint under OUTPUT/checkpoints, or none to start fresh."
        ),
    )
    args = parser.parse_args()
    return TrainConfig(**vars(args))


def set_seed(seed: int) -> None:
    random.seed(seed)
    torch.manual_seed(seed)
    if torch.cuda.is_available():
        torch.cuda.manual_seed_all(seed)


def choose_text_column(columns: Iterable[str], requested: str) -> str:
    available = list(columns)
    if requested != "auto":
        if requested not in available:
            raise ValueError(f"Column '{requested}' not found. Available: {available}")
        return requested

    for candidate in ("story", "textbook", "text", "content"):
        if candidate in available:
            return candidate
    raise ValueError(f"No usable text column found. Available: {available}")


def clean_text(value: object, max_chars: int) -> str:
    text = "" if value is None else str(value)
    text = re.sub(r"<[^>]+>", " ", text)
    text = re.sub(r"\s+", " ", text).strip()
    if len(text) > max_chars:
        text = text[:max_chars].rsplit(" ", 1)[0].strip()
    return text


def build_prompt(name: str, personality: str, setting: str, theme: str) -> str:
    return (
        "Write a complete short story in English (about 180-260 words) with "
        "a clear beginning, conflict, climax, and ending. "
        "Generate a fresh plot each time, do not reuse previous story flow. "
        "Treat the theme as a central message, not as a character name or an object name. "
        f"Main character: {name}. "
        f"Personality: {personality}. "
        f"Setting: {setting}. "
        f"Theme: {theme}. "
        "Story:"
    )


def extract_topic(source_text: str) -> str:
    text = source_text.strip()
    lesson_match = re.search(r"\bLesson\s*:\s*(.{4,140})", text, flags=re.IGNORECASE)
    if lesson_match:
        topic = lesson_match.group(1)
        for separator in ("**", "Objective:", "Question:", ".", " - "):
            if separator in topic:
                topic = topic.split(separator, 1)[0]
        return topic.strip(" -*:")

    heading_match = re.search(r"\*\*([^*]{4,100})\*\*", text)
    if heading_match:
        return heading_match.group(1).strip(" -*:")

    words = re.findall(r"[A-Za-z][A-Za-z'-]*", text)
    topic = " ".join(words[:8]).strip()
    return topic or "an unexpected discovery"


def theme_message(theme: str) -> str:
    messages = {
        "adventure": "courage grows when curiosity becomes action",
        "friendship": "trust is built through choices made under pressure",
        "hope": "even a small light can change the shape of a dark road",
        "courage": "being afraid does not mean standing still",
        "family": "belonging is something people keep choosing",
        "mystery": "truth matters most when it is difficult to face",
        "growth": "mistakes become useful when people learn from them",
        "trust": "trust survives when honesty arrives before pride",
    }
    return messages.get(theme, f"{theme} matters most when it becomes action")


def build_synthetic_story(
    source_text: str,
    name: str,
    personality: str,
    setting: str,
    theme: str,
    rng: random.Random,
) -> str:
    topic = extract_topic(source_text)
    message = theme_message(theme)
    style = rng.randint(0, 3)

    if style == 0:
        parts = [
            f"{name} was known in {setting} for being {personality}, though most days asked very little of that reputation.",
            f"That changed when {name} found a damaged notebook about {topic}. Its pages pointed to a problem nobody in {setting} wanted to discuss.",
            f"At first, {name} treated it like a puzzle. Then the clues began affecting real people, and the choice became harder than simple curiosity.",
            f"The turning point came when {name} stopped waiting for perfect answers and used what the notebook revealed to protect someone else.",
            f"By evening, {setting} felt different. The mystery was not fully gone, but {name} understood the lesson clearly: {message}.",
        ]
    elif style == 1:
        parts = [
            f"There was no time to explain. {name} ran through {setting} with one torn page about {topic} folded in a shaking hand.",
            f"Only an hour earlier, {name} had been trying to ignore the strange signs. Being {personality} helped, but it did not make the fear smaller.",
            f"Each clue led to another wrong turn until {name} realized the page was not a map. It was a warning about what people overlook.",
            f"When the final choice arrived, {name} chose the difficult truth over the comfortable lie.",
            f"Later, people remembered the chase. {name} remembered something quieter: {message}.",
        ]
    elif style == 2:
        parts = [
            f"Years later, {name} would still remember the day {topic} stopped being just a phrase in an old document.",
            f"Back then, {setting} was ordinary, and {name} was simply {personality} enough to ask one extra question.",
            f"That question opened a trail of secrets, small failures, and one apology that arrived almost too late.",
            f"The answer did not make {name} famous. It made {name} kinder, sharper, and less willing to mistake silence for peace.",
            f"Whenever someone asked what changed, {name} gave the same answer: {message}.",
        ]
    else:
        parts = [
            f"'You should leave it alone,' someone told {name} in {setting}.",
            f"{name}, {personality} by nature, almost listened. Then the words {topic} appeared again in a place they could not ignore.",
            f"The search that followed was messy. A friend doubted {name}, a stranger lied, and the easiest path led nowhere useful.",
            f"At the decisive moment, {name} spoke plainly, even though the truth cost more than silence.",
            f"The story ended without applause, but it left a mark: {message}.",
        ]

    return "\n\n".join(parts)


def build_training_example(source_text: str, rng: random.Random, target_mode: str) -> str:
    name = rng.choice(NAMES)
    personality = rng.choice(PERSONALITIES)
    setting = rng.choice(SETTINGS)
    theme = rng.choice(THEMES)
    prompt = build_prompt(name, personality, setting, theme)

    if target_mode == "raw-continuation":
        bridge = (
            f"{name} was {personality} in {setting}. "
            f"What happened next became a story about {theme}. "
        )
        target = f"{bridge}{source_text}"
    else:
        target = build_synthetic_story(
            source_text,
            name,
            personality,
            setting,
            theme,
            rng,
        )

    return f"{prompt}\n{target}"


def load_examples(
    parquet_path: str,
    text_column: str,
    max_samples: int,
    max_source_chars: int,
    seed: int,
    target_mode: str,
) -> list[str]:
    path = Path(parquet_path)
    if not path.exists():
        raise FileNotFoundError(f"Parquet file not found: {path}")

    df = pd.read_parquet(path)
    column = choose_text_column(df.columns, text_column)
    if max_samples > 0 and len(df) > max_samples:
        df = df.sample(n=max_samples, random_state=seed)

    rng = random.Random(seed)
    examples: list[str] = []
    for value in df[column].tolist():
        source_text = clean_text(value, max_source_chars)
        if len(source_text) < 120:
            continue
        examples.append(build_training_example(source_text, rng, target_mode))

    if not examples:
        raise ValueError(f"No training examples built from {path} column '{column}'")
    return examples


def evaluate(model, loader: DataLoader, device: torch.device) -> float:
    if len(loader) == 0:
        return float("nan")

    model.eval()
    losses: list[float] = []
    with torch.no_grad():
        for batch in loader:
            batch = {key: value.to(device) for key, value in batch.items()}
            outputs = model(**batch)
            losses.append(float(outputs.loss.detach().cpu()))
    model.train()
    return sum(losses) / len(losses)


def checkpoint_root(output: str) -> Path:
    return Path(output) / "checkpoints"


def checkpoint_sort_key(path: Path) -> int:
    match = re.search(r"checkpoint-(\d+)$", path.name)
    return int(match.group(1)) if match else -1


def find_latest_checkpoint(output: str) -> Path | None:
    root = checkpoint_root(output)
    if not root.exists():
        return None

    checkpoints = [
        path
        for path in root.iterdir()
        if path.is_dir() and checkpoint_sort_key(path) >= 0
    ]
    if not checkpoints:
        return None
    return max(checkpoints, key=checkpoint_sort_key)


def resolve_checkpoint(config: TrainConfig) -> Path | None:
    requested = config.resume_from_checkpoint.strip()
    if requested.lower() in {"", "none", "false", "no"}:
        return None
    if requested.lower() == "auto":
        return find_latest_checkpoint(config.output)

    checkpoint = Path(requested)
    if not checkpoint.exists():
        raise FileNotFoundError(f"Checkpoint not found: {checkpoint}")
    return checkpoint


def save_checkpoint(
    checkpoint_dir: Path,
    model,
    tokenizer,
    optimizer,
    scheduler,
    config: TrainConfig,
    epoch: int,
    batch_step: int,
    global_step: int,
) -> None:
    checkpoint_dir.mkdir(parents=True, exist_ok=True)
    model.save_pretrained(checkpoint_dir)
    tokenizer.save_pretrained(checkpoint_dir)
    torch.save(
        {
            "optimizer": optimizer.state_dict(),
            "scheduler": scheduler.state_dict(),
            "epoch": epoch,
            "batch_step": batch_step,
            "global_step": global_step,
            "config": asdict(config),
        },
        checkpoint_dir / "training_state.pt",
    )
    print(f"Saved checkpoint: {checkpoint_dir.resolve()}")


def load_training_state(
    checkpoint: Path,
    optimizer,
    scheduler,
    device: torch.device,
) -> tuple[int, int, int]:
    state_path = checkpoint / "training_state.pt"
    if not state_path.exists():
        raise FileNotFoundError(f"Missing training state: {state_path}")

    state = torch.load(state_path, map_location=device)
    optimizer.load_state_dict(state["optimizer"])
    scheduler.load_state_dict(state["scheduler"])
    return (
        int(state.get("epoch", 1)),
        int(state.get("batch_step", 0)),
        int(state.get("global_step", 0)),
    )


def train(config: TrainConfig) -> None:
    set_seed(config.seed)
    device_name = "cuda" if config.device == "auto" and torch.cuda.is_available() else config.device
    if device_name == "auto":
        device_name = "cpu"
    device = torch.device(device_name)

    print(f"Reading training data: {config.train}")
    train_examples = load_examples(
        config.train,
        config.text_column,
        config.max_samples,
        config.max_source_chars,
        config.seed,
        config.target_mode,
    )

    eval_examples: list[str] = []
    if config.test:
        test_path = Path(config.test)
        if test_path.exists():
            eval_examples = load_examples(
                config.test,
                config.text_column,
                config.max_eval_samples,
                config.max_source_chars,
                config.seed + 1,
                config.target_mode,
            )

    if config.dry_run:
        print(f"Built {len(train_examples)} training example(s).")
        if eval_examples:
            print(f"Built {len(eval_examples)} eval example(s).")
        print("\n--- sample training example ---\n")
        print(train_examples[0][:2000])
        return

    resume_checkpoint = resolve_checkpoint(config)
    model_source = str(resume_checkpoint) if resume_checkpoint else config.base_model
    if resume_checkpoint:
        print(f"Resuming model from checkpoint: {resume_checkpoint}")
    else:
        print(f"Loading tokenizer/model: {config.base_model}")

    tokenizer = AutoTokenizer.from_pretrained(model_source)
    if tokenizer.pad_token is None:
        tokenizer.pad_token = tokenizer.eos_token

    model = AutoModelForCausalLM.from_pretrained(model_source)
    model.resize_token_embeddings(len(tokenizer))
    model.to(device)
    model.train()

    train_loader = DataLoader(
        StoryDataset(train_examples, tokenizer, config.block_size),
        batch_size=config.batch_size,
        shuffle=True,
    )
    eval_loader = DataLoader(
        StoryDataset(eval_examples, tokenizer, config.block_size),
        batch_size=config.batch_size,
        shuffle=False,
    )

    update_steps_per_epoch = math.ceil(
        len(train_loader) / max(config.gradient_accumulation_steps, 1)
    )
    total_steps = max(update_steps_per_epoch * config.epochs, 1)
    warmup_steps = int(total_steps * config.warmup_ratio)

    optimizer = torch.optim.AdamW(model.parameters(), lr=config.learning_rate)
    scheduler = get_linear_schedule_with_warmup(
        optimizer,
        num_warmup_steps=warmup_steps,
        num_training_steps=total_steps,
    )

    start_epoch = 1
    resume_batch_step = 0
    global_step = 0
    if resume_checkpoint:
        start_epoch, resume_batch_step, global_step = load_training_state(
            resume_checkpoint,
            optimizer,
            scheduler,
            device,
        )
        print(
            "Loaded checkpoint state: "
            f"epoch={start_epoch}, batch_step={resume_batch_step}, "
            f"global_step={global_step}/{total_steps}"
        )

    print(
        "Training "
        f"{len(train_examples)} examples for {config.epochs} epoch(s) on {device} "
        f"({total_steps} optimizer steps)."
    )

    for epoch in range(start_epoch, config.epochs + 1):
        running_loss = 0.0
        optimizer.zero_grad(set_to_none=True)

        for step, batch in enumerate(train_loader, start=1):
            if epoch == start_epoch and step <= resume_batch_step:
                continue

            batch = {key: value.to(device) for key, value in batch.items()}
            outputs = model(**batch)
            loss = outputs.loss / config.gradient_accumulation_steps
            loss.backward()
            running_loss += float(outputs.loss.detach().cpu())

            should_step = step % config.gradient_accumulation_steps == 0
            is_last_step = step == len(train_loader)
            if should_step or is_last_step:
                torch.nn.utils.clip_grad_norm_(model.parameters(), 1.0)
                optimizer.step()
                scheduler.step()
                optimizer.zero_grad(set_to_none=True)
                global_step += 1

                if global_step % 10 == 0 or global_step == total_steps:
                    avg_loss = running_loss / step
                    print(
                        f"epoch={epoch} step={global_step}/{total_steps} "
                        f"train_loss={avg_loss:.4f}"
                    )

                if (
                    config.checkpoint_steps > 0
                    and global_step > 0
                    and global_step % config.checkpoint_steps == 0
                ):
                    save_checkpoint(
                        checkpoint_root(config.output) / f"checkpoint-{global_step}",
                        model,
                        tokenizer,
                        optimizer,
                        scheduler,
                        config,
                        epoch,
                        step,
                        global_step,
                    )

        if eval_examples:
            eval_loss = evaluate(model, eval_loader, device)
            print(f"epoch={epoch} eval_loss={eval_loss:.4f}")

    output = Path(config.output)
    output.mkdir(parents=True, exist_ok=True)
    model.save_pretrained(output)
    tokenizer.save_pretrained(output)

    (output / "training_config.json").write_text(
        json.dumps(asdict(config), indent=2),
        encoding="utf-8",
    )
    (output / "sample_training_preview.txt").write_text(
        train_examples[0],
        encoding="utf-8",
    )
    print(f"Saved fine-tuned model to: {output.resolve()}")


if __name__ == "__main__":
    train(parse_args())
