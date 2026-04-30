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
    "Câu chuyện xoay quanh xung đột trong lòng nhân vật giữa hai cách sống khác nhau.",
    "Câu chuyện bắt đầu từ khoảnh khắc nhân vật nhận ra rằng họ đang sống trong một cái ngoài hoặc những điều giả dối.",
    "Câu chuyện phát triển khi nhân vật tìm cách kết nối lại với thứ họ cho là đã mất.",
    "Câu chuyện dẫn vào một hành trình tự tìm hiểu bản thân thông qua những thử thách bất ngờ.",
]

_EN_STORY_ANGLES = [
    "The story begins on an ordinary day that suddenly takes an unexpected turn.",
    "The story centers on a difficult choice the character must face alone.",
    "The story starts with a chance encounter that changes everything.",
    "The story opens when the character uncovers a truth hidden in plain sight.",
    "The story unfolds around a challenge nobody else dared to confront.",
    "The story begins at the moment the character makes a mistake with lasting consequences.",
    "The story explores the inner conflict between two opposing paths the character could take.",
    "The story begins when the character realizes they have been living a lie or illusion.",
    "The story unfolds as the character attempts to reconnect with something they thought was lost forever.",
    "The story traces the character's journey of self-discovery through unexpected trials and revelations.",
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

    garbled_markers = ["\u00c3", "\u00c2", "\u00d0", "\u00d1", "\ufffd"]
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
    """Build a complete fallback story with varied narrative structures."""
    g = _theme_guidance(request.theme, language)
    n, p, s, t = request.name, request.personality, request.setting, request.theme
    style = RNG.randint(0, 6)

    if language == "vi":
     if style == 0:
         parts = [
          f"Tại {s}, {n} được biết đến là người {p}, nhưng chính điều đó lại khiến mọi người nghĩ {n} sẽ luôn ổn trong mọi hoàn cảnh.",
          f"Biến cố đến khi {g['challenge']} xuất hiện, kéo theo những hiểu lầm và áp lực mà {n} chưa từng chuẩn bị để đối mặt.",
          f"Ban đầu, {n} chọn cách im lặng để tránh va chạm. Nhưng càng lùi lại, mọi chuyện càng trở nên khó kiểm soát hơn.",
          f"Trong khoảnh khắc quyết định, {n} bước ra, chấp nhận rủi ro để làm điều đúng đắn và bảo vệ những gì quan trọng.",
          f"Sau tất cả, {n} hiểu sâu sắc rằng {t} không chỉ là lời nói. {g['message']}."
         ]
     elif style == 1:
         parts = [
          f"Không có nhiều thời gian để suy nghĩ. Khi {g['challenge']} bùng phát ở {s}, {n} phải hành động ngay.",
          f"Ít ai biết người mang tính cách {p} như {n} cũng đã từng hoài nghi chính mình trước áp lực lớn.",
          f"Nhiều nỗ lực đầu tiên thất bại. Mỗi sai lầm đều khiến {n} chậm lại, nhưng cũng giúp nhìn rõ vấn đề hơn.",
          f"Đến lúc mọi thứ tưởng như bế tắc, {n} chọn đối diện sự thật thay vì chạy theo giải pháp dễ dàng.",
          f"Nhìn lại hành trình ấy, {n} hiểu rõ hơn ý nghĩa của {t}: {g['message']}."
         ]
     elif style == 2:
         parts = [
          f"Nhiều năm sau, mỗi lần nhắc đến {s}, {n} vẫn nhớ giai đoạn đã thay đổi cách mình nhìn cuộc sống.",
          f"Khi đó, {n} còn nghĩ rằng chỉ cần chăm chỉ là đủ. Nhưng {g['challenge']} cho thấy mọi chuyện phức tạp hơn nhiều.",
          f"Từng lựa chọn nhỏ trong giai đoạn khó khăn đã buộc {n} học cách chịu trách nhiệm với hậu quả.",
          f"Điều quý giá nhất không phải chiến thắng nhanh, mà là quá trình hiểu bản thân và trưởng thành từng bước.",
          f"Vì vậy với {n}, {t} luôn gắn với một kết luận rõ ràng: {g['message']}."
         ]
     elif style == 3:
         parts = [
          f"'Cậu chắc chứ?' là câu hỏi {n} nghe nhiều nhất khi quyết định can thiệp vào chuyện ở {s}.",
          f"Là người {p}, {n} không thích ồn ào, nhưng cũng không thể làm ngơ khi {g['challenge']} ngày một nghiêm trọng.",
          f"Có những ngày mọi thứ chỉ toàn tranh cãi và mệt mỏi, khiến {n} muốn dừng lại.",
          f"Tuy vậy, mỗi lần chùn bước, {n} lại nhớ lý do ban đầu và tiếp tục hành động bằng những việc cụ thể.",
          f"Đến cuối cùng, chính sự kiên định ấy đã chứng minh rằng {g['message']}."
         ]
     elif style == 4:
         parts = [
          f"Có hai con đường trước mắt {n}: một con đường dễ chịu và một con đường đúng đắn.",
          f"Khi {g['challenge']} xảy ra tại {s}, {n} đã thử chọn đường dễ trước, và cái giá phải trả đến rất nhanh.",
          f"Thất bại khiến {n} buộc phải nhìn thẳng vào giới hạn của mình, thay vì đổ lỗi cho hoàn cảnh.",
          f"Lần tiếp theo, {n} chọn điều khó hơn, chậm hơn, nhưng phù hợp với giá trị mà {t} đại diện.",
          f"Từ đó, {n} không còn băn khoăn phải chọn gì nữa, vì {g['message']}."
         ]
     elif style == 5:
         parts = [
          f"Mọi chuyện ở {s} thay đổi theo từng giai đoạn, và {n} phải học cách thay đổi cùng nó.",
          f"Tuần đầu, {n} nghĩ có thể xử lý nhanh {g['challenge']}. Thực tế thì hoàn toàn ngược lại.",
          f"Mỗi giai đoạn đều buộc {n} điều chỉnh cách tiếp cận: bớt nóng vội, nhiều lắng nghe, và hành động có chiến lược.",
          f"Nhờ vậy, {n} dần hiểu rằng phát triển thật sự không đến từ một khoảnh khắc, mà từ sự bền bỉ lâu dài.",
          f"Khi nhìn lại, bài học còn lại rõ ràng: {g['message']}."
         ]
     else:
         parts = [
          f"Khi {g['challenge']} ảnh hưởng cả {s}, đa số chọn đứng ngoài quan sát. {n} thì không.",
          f"Với tính cách {p}, {n} bắt đầu từ những việc nhỏ, nhưng đủ cụ thể để tạo thay đổi thật.",
          f"Điều bất ngờ là hành động của {n} dần kéo theo người khác cùng tham gia, biến nỗ lực cá nhân thành nỗ lực chung.",
          f"Dù vẫn có mâu thuẫn và thất bại, cộng đồng xung quanh {n} đã học được cách phối hợp và tin nhau hơn.",
          f"Câu chuyện ấy để lại một kết luận bền vững về {t}: {g['message']}."
         ]
     return "\n\n".join(parts)

    if style == 0:
     parts = [
         f"In {s}, {n} was known as someone {p}, a person people trusted when things became uncertain.",
         f"That trust was tested when {g['challenge']} surfaced and turned ordinary routines into daily pressure.",
         f"At first, {n} tried to keep the peace by stepping back, but silence only gave the problem more room to grow.",
         f"At the turning point, {n} chose a difficult but honest action, accepting short-term cost for long-term clarity.",
         f"By the end, {n} understood that {t} is meaningful only when lived through choices: {g['message']}."
     ]
    elif style == 1:
     parts = [
         f"There was no time to plan. As soon as {g['challenge']} hit {s}, {n} had to move.",
         f"Even for someone as {p} as {n}, fear and doubt appeared quickly once consequences became real.",
         f"Several early attempts failed, each one exposing a blind spot and forcing a better approach.",
         f"When the hardest decision arrived, {n} stopped waiting for certainty and acted with intention.",
         f"Looking back, {n} no longer described {t} as an idea, but as practice: {g['message']}."
     ]
    elif style == 2:
     parts = [
         f"Years later, {n} would still remember that period in {s} as a turning point.",
         f"Before it happened, {n} believed effort alone could solve everything. Then {g['challenge']} changed that belief.",
         f"The process was messy: wrong turns, difficult conversations, and responsibility that could not be postponed.",
         f"What mattered most was not a dramatic victory, but steady growth in judgment and character.",
         f"That is why {n} speaks about {t} with quiet certainty now: {g['message']}."
     ]
    elif style == 3:
     parts = [
         f"'Are you sure?' was the question {n} heard repeatedly while stepping into conflict in {s}.",
         f"As someone {p}, {n} preferred calm solutions, but {g['challenge']} made passivity impossible.",
         f"The middle was exhausting, full of friction and setbacks that made quitting look reasonable.",
         f"Still, {n} kept going through small, concrete decisions that rebuilt trust one step at a time.",
         f"In the end, the result was simple and lasting: {g['message']}."
     ]
    elif style == 4:
     parts = [
         f"{n} discovered there were two paths: the easier one and the right one.",
         f"When {g['challenge']} reached {s}, the easy path failed quickly and made the cost visible.",
         f"That failure forced {n} to re-evaluate priorities, not circumstances.",
         f"On the second attempt, {n} chose the harder path aligned with the meaning of {t}.",
         f"From that point on, the lesson remained clear: {g['message']}."
     ]
    elif style == 5:
     parts = [
         f"The situation in {s} changed in waves, and {n} had to change with it.",
         f"In the first phase, {n} rushed to fix {g['challenge']}. The result was incomplete and fragile.",
         f"Over time, the strategy matured: less reaction, more listening, and decisions built for endurance.",
         f"That slower pace transformed not only outcomes but also how {n} understood responsibility.",
         f"The final takeaway was not dramatic, but deeply practical: {g['message']}."
     ]
    else:
     parts = [
         f"When {g['challenge']} affected everyone in {s}, most people watched from a safe distance. {n} stepped in.",
         f"Being {p}, {n} began with small commitments that were visible and consistent.",
         f"Those actions created momentum, and others gradually joined, turning an individual effort into a shared one.",
         f"There were setbacks, but the group learned to coordinate, recover, and continue.",
         f"That collective experience gave {t} a concrete meaning for everyone involved: {g['message']}."
     ]

    return "\n\n".join(parts)


def validate_input(data: Dict[str, str]) -> bool:
    """Validate input data."""
    required_fields = ["name", "personality", "setting", "theme"]
    for field in required_fields:
     if field not in data or not isinstance(data[field], str) or len(data[field].strip()) == 0:
         logger.warning(f"Missing or empty field: {field}")
         return False
    return True

