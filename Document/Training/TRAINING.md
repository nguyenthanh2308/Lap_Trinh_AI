# Story Model Fine-Tuning

This backend can load a local Hugging Face model from `./fine_tuned_model`.
Use `train_story_model.py` to build that folder from the parquet dataset.

## Install Dependencies

```powershell
cd "C:\Big_Data\AI\Final Term"
.\BackEnd\venv\Scripts\python.exe -m pip install -r BackEnd\requirements.txt
```

## Check Dataset Conversion

This verifies parquet loading and prints one training example without loading a model.

```powershell
.\BackEnd\venv\Scripts\python.exe BackEnd\train_story_model.py `
  --train train-00000-of-00001.parquet `
  --test test-00000-of-00001.parquet `
  --max-samples 3 `
  --max-eval-samples 2 `
  --dry-run
```

## Fine-Tune

Start small on CPU. Increase `--max-samples`, `--epochs`, and `--block-size` when
you have enough time or a CUDA GPU.

```powershell
.\BackEnd\venv\Scripts\python.exe BackEnd\train_story_model.py `
  --train train-00000-of-00001.parquet `
  --test test-00000-of-00001.parquet `
  --output BackEnd\fine_tuned_model `
  --base-model gpt2 `
  --max-samples 5000 `
  --epochs 1 `
  --batch-size 1 `
  --gradient-accumulation-steps 8 `
  --checkpoint-steps 50
```

The default `--target-mode synthetic-story` uses each dataset row as a topic seed
and trains on short story targets. Use `--target-mode raw-continuation` only if
the selected dataset column already contains actual stories.

## Checkpoints And Resume

Training saves resumable checkpoints under:

```text
BackEnd\fine_tuned_model\checkpoints\checkpoint-50
BackEnd\fine_tuned_model\checkpoints\checkpoint-100
...
```

By default, the script uses `--resume-from-checkpoint auto`, so if training is
interrupted, run the same command again and it will continue from the latest
checkpoint in `BackEnd\fine_tuned_model\checkpoints`.

To force a fresh run:

```powershell
.\BackEnd\venv\Scripts\python.exe BackEnd\train_story_model.py `
  --train train-00000-of-00001.parquet `
  --test test-00000-of-00001.parquet `
  --output BackEnd\fine_tuned_model `
  --resume-from-checkpoint none
```

To resume from a specific checkpoint:

```powershell
.\BackEnd\venv\Scripts\python.exe BackEnd\train_story_model.py `
  --train train-00000-of-00001.parquet `
  --test test-00000-of-00001.parquet `
  --output BackEnd\fine_tuned_model `
  --resume-from-checkpoint BackEnd\fine_tuned_model\checkpoints\checkpoint-450
```

## Run API With The Fine-Tuned Model

```powershell
cd "C:\Big_Data\AI\Final Term\BackEnd"
.\venv\Scripts\Activate.ps1
uvicorn app.main:app --reload
```

The API reads `MODEL_FOLDER=./fine_tuned_model` by default.
