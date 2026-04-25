import logging
import random
import re
from typing import Dict
from app.models.schema import StoryRequest

logger = logging.getLogger(__name__)
RNG = random.SystemRandom()

# Story angle hints to inject diversity into the prompt each request
_VI_STORY_ANGLES = [
    "Câu chuyện bắt đầu bằng một buổi sáng bình thường bỗng thay đổi hoàn toàn.",
    "Câu chuyện xoay quanh một quyết định khó khăn mà nhân vật phải thực hiện một mình.",
    "Câu chuyện khởi đầu bằng một cuộc gặp gỡ bất ngờ thay đổi mọi thứ.",
    "Câu chuyện bắt đầu khi nhân vật phát hiện ra sự thật đằng sau một điều tưởng như quen thuộc.",
    "Câu chuyện mở ra trong khung cảnh một thử thách mà không ai dám đối mặt ngoại trừ nhân vật chính.",
    "Câu chuyện được kể từ khoảnh khắc nhân vật phạm phải một sai lầm không thể quay đầu.",
]

_EN_STORY_ANGLES = [
    "The story begins on an ordinary day that suddenly takes an unexpected turn.",
    "The story centers on a difficult choice the character must face alone.",
    "The story starts with a chance encounter that changes everything.",
    "The story opens when the character uncovers a truth hidden in plain sight.",
    "The story unfolds around a challenge nobody else dared to confront.",
    "The story begins at the moment the character makes a mistake with lasting consequences.",
]

VIETNAMESE_DIACRITIC_PATTERN = re.compile(
    r"[àáạảãăằắặẳẵâầấậẩẫèéẹẻẽêềếệểễìíịỉĩ"
    r"òóọỏõôồốộổỗơờớợởỡùúụủũưừứựửữỳýỵỷỹđ]",
    flags=re.IGNORECASE,
)

VIETNAMESE_HINTS = {
    "va", "cua", "mot", "nguoi", "trong", "lang", "tinh", "cam", "hanh", "phuc",
    "và", "của", "một", "người", "trong", "làng", "tình", "cảm", "hạnh", "phúc",
    "dung", "cam", "dũng", "thong", "minh", "bi an", "hy vong", "phieu luu", "phiêu lưu",
}

ENGLISH_HINTS = {
    "the", "and", "with", "in", "on", "at", "a", "an", "brave", "village",
    "adventure", "mystery", "friendship", "journey", "hope", "future", "forest", "city",
}

VI_COMMON_WORDS = {
    "và", "một", "là", "trong", "nhưng", "không", "đã", "với", "cho", "khi", "người", "câu", "chuyện",
}

EN_COMMON_WORDS = {
    "the", "and", "a", "an", "in", "on", "with", "for", "to", "was", "were", "that", "story", "character",
}

PROMPT_LABEL_PATTERN = re.compile(
    r"(Nhân vật chính|Tính cách|Bối cảnh|Chủ đề|Main character|Personality|Setting|Theme)\s*:",
    flags=re.IGNORECASE,
)


def detect_language(data: Dict[str, str]) -> str:
    """
    Detect whether input is primarily Vietnamese or English.

    Returns:
        "vi" for Vietnamese, "en" for English
    """
    combined_text = " ".join(str(v) for v in data.values()).strip().lower()

    if not combined_text:
        return "en"

    if VIETNAMESE_DIACRITIC_PATTERN.search(combined_text):
        return "vi"

    words = re.findall(r"[a-zA-Z']+", combined_text)
    if not words:
        return "en"

    vi_score = sum(1 for word in words if word in VIETNAMESE_HINTS)
    en_score = sum(1 for word in words if word in ENGLISH_HINTS)

    return "vi" if vi_score > en_score else "en"


def build_prompt(request: StoryRequest, language: str) -> str:
    """
    Build a prompt based on detected language.

    A random story-angle hint is injected each call so the model is guided
    toward a fresh narrative direction even when the user inputs are similar.

    Args:
        request: StoryRequest containing name, personality, setting, theme
        language: Detected language code ("vi" or "en")

    Returns:
        Prompt string in Vietnamese or English
    """
    if language == "vi":
        angle = RNG.choice(_VI_STORY_ANGLES)
        prompt = (
            "Hãy viết một truyện ngắn hoàn chỉnh bằng tiếng Việt (khoảng 180-260 từ), "
            "có mở đầu, cao trào và kết thúc rõ ràng. "
            "Mỗi lần tạo phải là một diễn biến mới, không lặp lại cốt truyện trước đó. "
            "Chủ đề phải là thông điệp xuyên suốt, không biến thành tên nhân vật hay tên đồ vật. "
            f"{angle} "
            f"Nhân vật chính: {request.name}. "
            f"Tính cách: {request.personality}. "
            f"Bối cảnh: {request.setting}. "
            f"Chủ đề: {request.theme}. "
            "Truyện:"
        )
    else:
        angle = RNG.choice(_EN_STORY_ANGLES)
        prompt = (
            "Write a complete short story in English (about 180-260 words) with "
            "a clear beginning, conflict, climax, and ending. "
            "Generate a fresh plot each time, do not reuse previous story flow. "
            "Treat the theme as a central message, not as a character name or an object name. "
            f"{angle} "
            f"Main character: {request.name}. "
            f"Personality: {request.personality}. "
            f"Setting: {request.setting}. "
            f"Theme: {request.theme}. "
            "Story:"
        )

    return prompt


def extract_story_text(generated_text: str, prompt: str) -> str:
    """Extract only story body and remove prompt remnants."""
    text = generated_text.strip()

    if text.startswith(prompt):
        text = text[len(prompt):].strip()
    else:
        text = text.replace(prompt, "", 1).strip()

    # Remove everything before the last explicit story marker.
    markers = list(re.finditer(r"(Truyện|Story)\s*:\s*", text, flags=re.IGNORECASE))
    if markers:
        text = text[markers[-1].end():].strip()

    # Remove common leading labels that some models repeat.
    text = re.sub(r"^(Truyện|Story)\s*:\s*", "", text, flags=re.IGNORECASE)
    return text.strip()


def has_garbled_artifacts(text: str) -> bool:
    """Detect common mojibake-like artifacts and malformed output patterns."""
    if not text:
        return True

    garbled_markers = ["Ã", "Â", "Ð", "Ñ", "?", "Ã¢", "Ã£", "Ã´", "Ã "]
    if any(marker in text for marker in garbled_markers):
        return True

    weird_symbol_ratio = sum(1 for ch in text if ch in "|{}[]<>~") / max(len(text), 1)
    if weird_symbol_ratio > 0.08:
        return True

    return False


def _contains_context(story: str, request: StoryRequest) -> bool:
    """Ensure generated story still references key user-provided context."""
    lowered_story = story.lower()

    # Character name is mandatory for coherence.
    if request.name.lower() not in lowered_story:
        return False

    context_sources = [request.personality, request.setting, request.theme]
    for source in context_sources:
        tokens = [t for t in re.findall(r"\w+", source.lower()) if len(t) >= 4]
        if not tokens:
            continue
        if any(token in lowered_story for token in tokens):
            return True

    return False


def _language_coherence_ok(story: str, language: str) -> bool:
    """Simple lexical checks to reject random multilingual gibberish."""
    words = [w.lower() for w in re.findall(r"\w+", story)]
    if not words:
        return False

    if language == "vi":
        vi_count = sum(1 for w in words if w in VI_COMMON_WORDS)
        return vi_count >= 3

    en_count = sum(1 for w in words if w in EN_COMMON_WORDS)
    return en_count >= 4


def _pick(options: list) -> str:
    """Choose one option using cryptographically strong randomness."""
    return RNG.choice(options)


def _theme_guidance(theme: str, language: str) -> dict:
    """Map a theme to conflict/resolution emphasis so theme stays conceptual."""
    normalized = theme.strip().lower()

    if language == "vi":
        mapping = [
            (("phiêu lưu", "khám phá", "mạo hiểm"), {
                "challenge": "sự sợ hãi trước điều chưa biết",
                "growth": "dám bước ra khỏi vùng an toàn để trưởng thành",
                "message": "mỗi hành trình can đảm đều mở ra một chân trời mới",
            }),
            (("tình bạn", "bạn bè", "đồng đội"), {
                "challenge": "mâu thuẫn và hiểu lầm giữa những người thân thiết",
                "growth": "lắng nghe, tin tưởng và cùng nhau vượt khó",
                "message": "tình bạn bền vững được xây bằng sự thấu hiểu và chân thành",
            }),
            (("gia đình", "tình thân"), {
                "challenge": "khoảng cách giữa các thế hệ và những điều chưa nói ra",
                "growth": "học cách cảm thông và quan tâm đúng cách",
                "message": "gia đình là nơi người ta luôn có thể quay về để được chữa lành",
            }),
            (("hy vọng", "niềm tin"), {
                "challenge": "giai đoạn tưởng như mọi cánh cửa đã khép lại",
                "growth": "giữ vững niềm tin ngay cả khi kết quả chưa rõ ràng",
                "message": "hy vọng nhỏ bé vẫn có thể thắp sáng những ngày tối nhất",
            }),
            (("trưởng thành", "phát triển bản thân"), {
                "challenge": "đối diện sai lầm và trách nhiệm cá nhân",
                "growth": "biết nhận lỗi, sửa đổi và tiếp tục tiến lên",
                "message": "trưởng thành là hành trình hiểu mình và sống có trách nhiệm hơn",
            }),
            (("dũng cảm", "can đảm"), {
                "challenge": "nỗi sợ thất bại và áp lực từ người xung quanh",
                "growth": "chọn điều đúng dù không dễ dàng",
                "message": "dũng cảm không phải không sợ, mà là vẫn bước tiếp dù đang sợ",
            }),
        ]

        for keywords, guidance in mapping:
            if any(keyword in normalized for keyword in keywords):
                return guidance

        return {
            "challenge": f"xung đột gắn với chủ đề {theme}",
            "growth": f"thay đổi nhận thức để hiểu sâu hơn về {theme}",
            "message": f"{theme} là giá trị cần được nuôi dưỡng bằng hành động mỗi ngày",
        }

    mapping = [
        (("adventure", "exploration"), {
            "challenge": "fear of the unknown",
            "growth": "taking meaningful risks beyond comfort",
            "message": "new horizons appear when courage meets curiosity",
        }),
        (("friendship", "friends", "teamwork"), {
            "challenge": "misunderstanding among close companions",
            "growth": "rebuilding trust through empathy and honesty",
            "message": "strong friendship is built through trust and shared effort",
        }),
        (("family", "belonging"), {
            "challenge": "distance and unspoken expectations at home",
            "growth": "learning to communicate with care",
            "message": "belonging grows when people choose to understand one another",
        }),
        (("hope", "faith"), {
            "challenge": "a moment when everything seems lost",
            "growth": "holding on to purpose despite uncertainty",
            "message": "hope can quietly rebuild what fear tries to break",
        }),
        (("growth", "maturity", "coming of age"), {
            "challenge": "facing mistakes and personal responsibility",
            "growth": "accepting lessons and improving with intention",
            "message": "growth begins when people own their choices",
        }),
        (("courage", "bravery"), {
            "challenge": "pressure, doubt, and fear of failure",
            "growth": "choosing what is right over what is easy",
            "message": "courage means moving forward even when fear is present",
        }),
        (("romance", "love"), {
            "challenge": "vulnerability and the fear of rejection",
            "growth": "opening up and expressing honest feelings",
            "message": "love becomes real when two people choose each other in spite of uncertainty",
        }),
        (("mystery", "secrets"), {
            "challenge": "uncovering a truth that changes everything",
            "growth": "facing reality rather than hiding behind comfortable assumptions",
            "message": "the truth, however difficult, is always worth seeking",
        }),
    ]

    for keywords, guidance in mapping:
        if any(keyword in normalized for keyword in keywords):
            return guidance

    return {
        "challenge": f"an emotional conflict linked to the theme of {theme}",
        "growth": f"a personal transformation shaped by {theme}",
        "message": f"{theme} becomes meaningful when expressed through choices",
    }


def is_story_quality_acceptable(story: str, language: str, request: StoryRequest) -> bool:
    """Check if generated text is usable as a complete short story."""
    if not story:
        return False

    normalized = story.strip()

    if len(normalized) < 220:
        return False

    sentence_count = len(re.findall(r"[.!?]+", normalized))
    if sentence_count < 4:
        return False

    if has_garbled_artifacts(normalized):
        return False

    # If prompt labels leaked into output, extraction failed and quality is unreliable.
    if PROMPT_LABEL_PATTERN.search(normalized):
        return False

    if language == "vi" and len(VIETNAMESE_DIACRITIC_PATTERN.findall(normalized)) == 0:
        return False

    if not _language_coherence_ok(normalized, language):
        return False

    if not _contains_context(normalized, request):
        return False

    return True


def build_fallback_story(request: StoryRequest, language: str) -> str:
    """Build a varied story when model output is poor.

    Uses 5-8 options per narrative section and randomises between
    three different paragraph orderings so consecutive requests with
    different inputs produce clearly distinct stories.
    """
    guidance = _theme_guidance(request.theme, language)
    n, p, s, t = request.name, request.personality, request.setting, request.theme

    if language == "vi":
        openings = [
            f"{n} lớn lên ở {s} với tính cách {p} khiến ai cũng quý mến.",
            f"Tại {s}, {n} được biết đến là người {p} hiếm có.",
            f"Giữa {s} náo nhiệt, {n} vẫn giữ được bản tính {p} của mình.",
            f"Không ai ở {s} ngạc nhiên khi {n} lại là người {p} nhất đám.",
            f"{n} chưa bao giờ nghĩ rằng cuộc sống ở {s} lại thay đổi nhanh đến vậy.",
            f"Buổi sáng hôm đó ở {s}, {n} thức dậy với linh cảm rằng mọi thứ sắp khác đi.",
            f"Người ta nói {s} sinh ra những con người {p}, và {n} chính là minh chứng.",
            f"Trong ký ức của nhiều người ở {s}, {n} luôn gắn với hình ảnh {p} và kiên định.",
        ]
        setups = [
            f"Cho đến ngày {n} phải đối mặt với {guidance['challenge']} — thứ chưa ai trong {s} dám nhìn thẳng vào.",
            f"Mọi thứ thay đổi khi một biến cố ập đến, đẩy {n} vào tình huống không lối thoát rõ ràng.",
            f"Rồi một sự kiện liên quan đến {t} xảy ra, buộc {n} phải đưa ra quyết định quan trọng nhất cuộc đời.",
            f"Không ai ngờ chính {n} lại là người đứng giữa tâm bão khi {guidance['challenge']} bùng phát.",
            f"Một cuộc gặp gỡ tình cờ kéo {n} vào vòng xoáy của {guidance['challenge']}.",
            f"Khi tin tức về {guidance['challenge']} lan ra khắp {s}, {n} biết mình không thể đứng ngoài.",
        ]
        middles = [
            f"Không ít lần {n} muốn bỏ cuộc, nhưng tính cách {p} không cho phép điều đó xảy ra.",
            f"Vấp ngã liên tiếp, {n} dần nhận ra rằng {guidance['growth']} mới là con đường duy nhất.",
            f"Giữa lúc khó khăn nhất, {n} tìm thấy sức mạnh từ những người xung quanh.",
            f"Mỗi thất bại là một bài học, và {n} học cách đứng dậy nhanh hơn sau mỗi lần ngã.",
            f"{n} bắt đầu hiểu rằng {guidance['growth']} không phải điểm đến mà là hành trình.",
            f"Dù áp lực ngày càng lớn, {n} không để mất đi bản thân giữa tất cả sóng gió đó.",
        ]
        climaxes = [
            f"Đỉnh điểm đến khi {n} đứng trước lựa chọn cuối cùng và chọn điều đúng dù không dễ dàng.",
            f"Trong khoảnh khắc ai cũng nghĩ đã thua, {n} bước ra và thay đổi cục diện.",
            f"{n} nhận ra rằng giải pháp nằm ngay trong tính cách {p} của mình — và hành động.",
            f"Khi căng thẳng lên đến cực điểm, {n} đưa ra quyết định dứt khoát khiến mọi người sửng sốt.",
            f"Đúng lúc mọi thứ tưởng như sụp đổ, {n} tìm ra một lối thoát không ai nghĩ tới.",
        ]
        endings = [
            f"Nhìn lại hành trình, {n} hiểu rằng {t} không chỉ là một từ — đó là cách sống. {guidance['message']}.",
            f"{s} trở lại bình yên, nhưng {n} đã không còn là người cũ. {guidance['message']}.",
            f"Câu chuyện của {n} trở thành lời nhắc nhở cho {s}: {guidance['message']}.",
            f"Sau tất cả, điều còn lại không phải chiến thắng mà là bài học về {t}: {guidance['message']}.",
            f"Từ đó, {n} sống khác đi — không ồn ào, nhưng sâu sắc hơn. Vì {n} đã hiểu: {guidance['message']}.",
        ]

        structure = RNG.randint(0, 2)
        if structure == 0:
            parts = [_pick(openings), _pick(setups), _pick(middles), _pick(climaxes), _pick(endings)]
        elif structure == 1:
            parts = [_pick(setups), _pick(openings), _pick(middles), _pick(climaxes), _pick(endings)]
        else:
            parts = [_pick(openings), _pick(middles), _pick(setups), _pick(climaxes), _pick(endings)]
        return "\n\n".join(parts)

    # ---------- English ----------
    openings = [
        f"{n} had always been {p} — it was simply who they were in {s}.",
        f"In {s}, everyone knew {n} as someone {p} and steady under pressure.",
        f"Few people in {s} understood {n} fully, but all agreed on one thing: {n} was {p}.",
        f"{n} never planned to stand out in {s}, yet a {p} spirit is hard to hide.",
        f"Life in {s} had shaped {n} into someone {p}, though {n} rarely thought about it.",
        f"On an ordinary morning in {s}, {n} made a small decision that changed everything.",
        f"The people of {s} called {n} {p} — some meant it as a compliment, others as a warning.",
        f"{n} arrived in {s} quietly, carrying nothing but a {p} nature and an open mind.",
    ]
    setups = [
        f"That changed the day {n} encountered {guidance['challenge']} and realized the old approach would not work.",
        f"A sudden crisis involving {t} forced {n} to make a choice no one else dared to make.",
        f"When {guidance['challenge']} arrived, everyone looked away — except {n}.",
        f"An unexpected event tied to {t} pulled {n} into a conflict that felt deeply personal.",
        f"Without warning, {n} found themselves at the center of exactly the kind of situation {s} feared most.",
        f"One afternoon, a stranger arrived in {s} and everything {n} thought was settled became uncertain.",
    ]
    middles = [
        f"The road was not easy. Again and again {n} stumbled, but each failure made the next step clearer.",
        f"{n} began to understand that {guidance['growth']} was not a shortcut — it was the whole point.",
        f"Doubt crept in, but {n}'s {p} character kept pushing forward when logic said to stop.",
        f"Every setback taught {n} something new, and slowly a plan took shape from the wreckage.",
        f"There were moments {n} wanted to walk away. Instead, {n} stayed and learned {guidance['growth']}.",
        f"The hardest part was not the obstacle itself — it was admitting that {guidance['growth']} was necessary.",
    ]
    climaxes = [
        f"At the breaking point, {n} chose action over hesitation and confronted the conflict head-on.",
        f"When the moment came, {n} did not wait for permission — and that made all the difference.",
        f"In the final hour, {n}'s {p} spirit became the one thing {s} needed most.",
        f"No one expected {n} to step forward. But stepping forward was exactly what {n} did.",
        f"The turning point arrived quietly, and {n} met it with a calm that surprised even close friends.",
    ]
    endings = [
        f"Afterward, {s} felt different — lighter somehow. And {n} carried a new understanding of {t}: {guidance['message']}.",
        f"The crisis passed, but its lesson stayed: {guidance['message']}. {n} would not forget it.",
        f"People in {s} talked about it for years — not the conflict, but what {n} did next. {guidance['message']}.",
        f"{n} never became famous for it. But in {s}, the quiet truth remained: {guidance['message']}.",
        f"Looking back, {n} realized that {t} was never about the destination. {guidance['message']}.",
    ]

    structure = RNG.randint(0, 2)
    if structure == 0:
        parts = [_pick(openings), _pick(setups), _pick(middles), _pick(climaxes), _pick(endings)]
    elif structure == 1:
        parts = [_pick(setups), _pick(openings), _pick(middles), _pick(climaxes), _pick(endings)]
    else:
        parts = [_pick(openings), _pick(middles), _pick(setups), _pick(climaxes), _pick(endings)]
    return "\n\n".join(parts)


def validate_input(data: Dict[str, str]) -> bool:
    """
    Validate input data

    Args:
        data: Dictionary containing story parameters

    Returns:
        True if valid, False otherwise
    """
    required_fields = ['name', 'personality', 'setting', 'theme']

    for field in required_fields:
        if field not in data or not isinstance(data[field], str) or len(data[field].strip()) == 0:
            logger.warning(f"Missing or empty field: {field}")
            return False

    return True
