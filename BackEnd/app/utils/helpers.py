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
    # Các góc nhìn phi tuyến và đa dạng hơn
    "Câu chuyện bắt đầu ngay giữa hành động, không có lời giới thiệu, chỉ có khoảnh khắc đang xảy ra.",
    "Câu chuyện mở đầu bằng một câu đối thoại cắt ngang im lặng và mọi thứ bắt đầu từ đó.",
    "Câu chuyện được kể ngược, từ kết thúc trở về cái khoảnh khắc khiến mọi thứ thay đổi.",
    "Câu chuyện bắt đầu từ một chi tiết rất nhỏ, một âm thanh, một mùi hương, một vật bỏ quên, rồi mở rộng ra.",
    "Câu chuyện nhìn từ góc độ của người đứng ngoài quan sát nhân vật chính trước khi hiểu toàn cảnh.",
    "Câu chuyện bắt đầu khi nhân vật sắp từ bỏ tất cả và chỉ một điều nhỏ bé ngăn họ lại.",
    "Câu chuyện mở đầu bằng một bí mật mà nhân vật giấu kín và toàn bộ cốt truyện là cách bí mật đó rò rỉ.",
    "Câu chuyện bắt đầu từ một nơi quen thuộc nhưng hôm nay có điều gì đó sai sai mà nhân vật chưa thể xác định.",
    "Câu chuyện diễn ra trong một đêm duy nhất từ hoàng hôn đến bình minh và mọi thứ thay đổi trong khoảng đó.",
    "Câu chuyện mở ra bằng một mất mát và hành trình là tìm lại thứ đã mất dù không phải theo nghĩa đen.",
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
    # Non-linear and diverse openings
    "The story drops straight into the action with no setup, no introduction, just the moment itself.",
    "The story opens with a single line of dialogue that breaks the silence and sets everything in motion.",
    "The story is told in reverse, starting from the aftermath and working back to the decision that caused it.",
    "The story begins with a tiny detail, a sound, a smell, a forgotten object, that slowly opens into something vast.",
    "The story is seen through the eyes of an observer on the edge of the scene before the full picture emerges.",
    "The story begins when the character is about to give up, and only one small thing stops them.",
    "The story opens with a secret the character has been keeping, and the entire plot is how it unravels.",
    "The story starts in a familiar place that feels subtly wrong today in a way the character cannot yet name.",
    "The story spans a single night from dusk to dawn, and everything shifts within those hours.",
    "The story begins with a loss, and the whole journey is about recovering what was lost, though not literally.",
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


def _contains_any(text: str, words: tuple[str, ...]) -> bool:
    return any(word in text for word in words)


def _setting_motif(setting: str) -> str:
    normalized = setting.lower()
    if _contains_any(normalized, ("empty", "abandoned", "deserted", "ghost town")):
        return (
            "streets where traffic lights changed for nobody, glass towers held "
            "only reflections, and every footstep sounded borrowed"
        )
    if _contains_any(normalized, ("city", "urban", "metropolis")):
        return (
            "late trains, locked rooftops, flickering signs, and strangers who "
            "vanished into crosswalk steam"
        )
    if _contains_any(normalized, ("forest", "woods", "jungle")):
        return (
            "wet leaves, broken animal paths, old roots underfoot, and a clearing "
            "that seemed to move when no one watched"
        )
    if _contains_any(normalized, ("school", "classroom", "campus")):
        return (
            "silent corridors after hours, chalk dust in the air, and one room "
            "whose door was never listed on the map"
        )
    if _contains_any(normalized, ("village", "town")):
        return (
            "narrow lanes, familiar windows, whispered news, and a place everyone "
            "claimed not to remember"
        )
    return (
        "a place with one vivid secret, one forbidden corner, and details that "
        "slowly stopped behaving normally"
    )


def _theme_motif(theme: str) -> str:
    normalized = theme.lower()
    if _contains_any(normalized, ("horror", "fear", "terror", "dread")):
        return (
            "a quiet dread that did not jump out, but waited in ordinary sounds "
            "until the familiar became unsafe"
        )
    if _contains_any(normalized, ("mystery", "secret", "detective")):
        return "a missing fact that made every honest answer feel suspicious"
    if _contains_any(normalized, ("romance", "love")):
        return "an affection revealed through risk rather than confession"
    if _contains_any(normalized, ("adventure", "journey", "exploration")):
        return "a risky path that kept changing the farther it was followed"
    if _contains_any(normalized, ("courage", "brave", "bravery")):
        return "a moment when fear stayed, but someone moved anyway"
    if _contains_any(normalized, ("family", "home")):
        return "an old bond tested by something nobody wanted to say aloud"
    return "a pressure that forced the character to act before they fully understood it"


def _personality_gesture(personality: str) -> str:
    normalized = personality.lower()
    if _contains_any(normalized, ("brave", "courage", "daring")):
        return "stepped forward before certainty arrived"
    if _contains_any(normalized, ("quiet", "shy", "reserved")):
        return "noticed the detail everyone louder had missed"
    if _contains_any(normalized, ("clever", "smart", "intelligent")):
        return "solved problems sideways, by questioning the obvious"
    if _contains_any(normalized, ("kind", "gentle", "caring")):
        return "protected someone vulnerable even when it complicated everything"
    if _contains_any(normalized, ("curious", "restless")):
        return "opened the one door that should have been left alone"
    return "made one specific choice that revealed who they were under pressure"



_VI_OPENING_HOOKS = [
    "Hãy mở đầu ngay giữa hành động, không cần giới thiệu nhân vật theo kiểu truyền thống.",
    "Hãy bắt đầu bằng một câu đối thoại hoặc lời độc thoại nội tâm.",
    "Hãy mở đầu bằng một chi tiết cảm quan rất cụ thể: mùi, âm thanh, kết cấu, ánh sáng.",
    "Hãy bắt đầu bằng một câu hỏi mà nhân vật đang tự hỏi mình.",
    "Hãy mở đầu bằng một khoảnh khắc căng thẳng — không phải giải thích, mà là cảm giác.",
]

_EN_OPENING_HOOKS = [
    "Open in the middle of the action. Do not introduce the character in a traditional way.",
    "Start with a line of dialogue or internal monologue, no scene-setting preamble.",
    "Open with a sharp sensory detail: a smell, a sound, a texture, a quality of light.",
    "Begin with a question the character is asking themselves.",
    "Start at the moment of highest tension — show the feeling, not the explanation.",
]


def build_creative_direction(request: StoryRequest, language: str) -> str:
    """Tell the model to transform inputs into imagery instead of repeating them."""
    if language == "vi":
        hook = RNG.choice(_VI_OPENING_HOOKS)
        return (
            "\nHướng sáng tạo: dùng mô tả người dùng như cảm hứng, không bê nguyên "
            "cụm từ vào truyện. Nếu bối cảnh là một cụm như thành phố trống rỗng, "
            "hãy biến nó thành hình ảnh, âm thanh, chi tiết cụ thể. Nếu chủ đề là "
            "kinh dị, hãy tạo cảm giác bất an thay vì viết thẳng chữ kinh dị nhiều lần. "
            f"Tránh văn kiểu bài học đạo đức hoặc dàn ý năm đoạn. {hook}"
        )

    hook = RNG.choice(_EN_OPENING_HOOKS)
    literal_phrases = [
        phrase.strip()
        for phrase in (request.personality, request.setting, request.theme)
        if len(phrase.strip()) >= 4
    ]
    phrase_text = "; ".join(f'"{phrase}"' for phrase in literal_phrases)
    return (
        "\nCreative direction: treat the user's descriptions as raw material, "
        "not wording to paste into the story. Transform setting/theme/personality "
        "into scenes, actions, symbols, and atmosphere. Avoid repeating these exact "
        f"phrases unless absolutely necessary: {phrase_text}. Do not write a moral "
        "essay, lesson, objective, glossary, question-answer, textbook explanation, "
        f"or tutorial. {hook}"
    )



def build_creative_english_fallback(request: StoryRequest) -> str:
    """Fallback that interprets inputs through imagery instead of copying them."""
    n = request.name
    place = _setting_motif(request.setting)
    pressure = _theme_motif(request.theme)
    gesture = _personality_gesture(request.personality)
    style = RNG.randint(0, 4)

    if style == 0:
        parts = [
            f"The first thing {n} noticed was not the silence, but how carefully the world seemed to be holding it.",
            f"A message scratched beneath a stair rail led {n} through {place}.",
            f"Every clue suggested {pressure}, and every sensible instinct said to turn back.",
            f"Instead, {n} {gesture}, following a sound that stopped whenever it was almost understood.",
            f"At dawn, the answer was smaller than a monster and worse than a dream: someone had been waiting for {n} to choose whether the door should stay closed.",
        ]
    elif style == 1:
        parts = [
            f"{n} found the photograph in a place where no photograph should have survived.",
            f"It showed the same corner, the same light, the same impossible stillness of {place}, but with {n} standing in the background.",
            f"The longer {n} looked, the more the scene suggested {pressure}.",
            f"Running would have been easier. Instead, {n} {gesture}, then stepped into the street shown in the picture.",
            f"The figure waiting there wore no face, only {n}'s old hesitation, and it disappeared the moment {n} named what had been avoided.",
        ]
    elif style == 2:
        parts = [
            f"By midnight, {n} understood that the map was lying.",
            f"Each street led back to {place}, but each return changed one small detail: a window open, a shoe in the gutter, a child's song from nowhere.",
            f"The pattern carried {pressure}, not loudly, but with the patience of something certain it would be obeyed.",
            f"{n} {gesture}, marking the changes on the back of a receipt until the lines formed a question.",
            f"When the question was answered, the way out appeared behind the only door {n} had been afraid to open.",
        ]
    elif style == 3:
        parts = [
            f"The call came from {n}'s own number.",
            f"On the other end was breathing, wind, and the distant echo of {place}.",
            f"No voice explained anything, yet the pauses carried {pressure}.",
            f"{n} {gesture}, speaking one sentence into the receiver that had never been admitted aloud.",
            f"Somewhere nearby, a phone rang in answer, and this time {n} walked toward it instead of away.",
        ]
    else:
        parts = [
            f"{n} had been warned not to count the windows.",
            f"That warning made no sense until the buildings around {place} began gaining one new dark square every time {n} looked away.",
            f"What grew behind the glass was not a creature, but {pressure}.",
            f"With no one left to ask, {n} {gesture}, choosing the window that reflected a memory instead of a room.",
            f"The glass broke inward, and the first real sound of morning rushed through like forgiveness with sharp edges.",
        ]

    return "\n\n".join(parts)


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


def build_creative_vietnamese_fallback(request: StoryRequest) -> str:
    """Fallback tiếng Việt dùng imagery thay vì paste literal variables."""
    n = request.name
    place = _setting_motif(request.setting)
    pressure = _theme_motif(request.theme)
    gesture = _personality_gesture(request.personality)
    g = _theme_guidance(request.theme, "vi")
    style = RNG.randint(0, 4)

    if style == 0:
        parts = [
            f"Điều đầu tiên {n} nhận ra không phải là sự im lặng, mà là cách thế giới xung quanh đang cố giữ lấy nó.",
            f"Một mảnh giấy nhỏ kẹp dưới bậc cầu thang dẫn {n} qua {place}.",
            f"Từng manh mối đều gợi lên {pressure}, và từng bản năng lý trí đều bảo quay trở lại.",
            f"Nhưng {n} {gesture}, đi theo một âm thanh cứ dừng lại mỗi khi sắp được hiểu ra.",
            f"Đến lúc bình minh ló dạng, câu trả lời nhỏ hơn một con quái vật nhưng nặng hơn cả một giấc mộng: {g['message']}.",
        ]
    elif style == 1:
        parts = [
            f"{n} tìm thấy tấm ảnh ở một nơi không thể nào còn ảnh tồn tại được.",
            f"Nó chụp cùng một góc phố, cùng thứ ánh sáng, cùng sự tĩnh lặng kỳ lạ của {place} — nhưng có bóng {n} đứng phía sau.",
            f"Càng nhìn lâu, khung cảnh càng gợi lên {pressure}.",
            f"Bỏ chạy lẽ ra dễ hơn. Nhưng {n} {gesture}, rồi bước vào con đường trong tấm ảnh.",
            f"Bóng người đứng đợi không có khuôn mặt — chỉ mang theo sự do dự cũ của {n} — và tan biến ngay khi {n} gọi tên điều mình đã tránh né: {g['message']}.",
        ]
    elif style == 2:
        parts = [
            f"Đến nửa đêm, {n} hiểu ra rằng tấm bản đồ đang nói dối.",
            f"Mỗi con phố đều dẫn trở lại {place}, nhưng mỗi lần quay lại lại thay đổi một chi tiết nhỏ: một ô cửa sổ hé mở, một chiếc giày bên lề đường, một tiếng hát trẻ con từ đâu đó.",
            f"Mạch truyện ẩn chứa {pressure} — không ồn ào, nhưng kiên nhẫn như thứ chắc chắn rằng nó sẽ được tuân theo.",
            f"{n} {gesture}, ghi lại những thay đổi ở mặt sau một tờ hóa đơn cho đến khi các đường nét tạo thành một câu hỏi.",
            f"Khi câu hỏi được trả lời, lối thoát xuất hiện sau chiếc cửa duy nhất mà {n} đã sợ mở ra. Đó là lúc {n} hiểu: {g['message']}.",
        ]
    elif style == 3:
        parts = [
            f"Cuộc gọi đến từ chính số điện thoại của {n}.",
            f"Đầu dây bên kia là hơi thở, gió, và tiếng vang xa xôi của {place}.",
            f"Không có giọng nói nào giải thích bất cứ điều gì, nhưng những khoảng lặng lại mang theo {pressure}.",
            f"{n} {gesture}, nói một câu vào ống nghe mà bấy lâu nay chưa dám thừa nhận.",
            f"Ở đâu đó gần đây, một chiếc điện thoại reo lên để đáp lại — và lần này {n} bước về phía nó thay vì bước ra xa. Bởi vì {g['message']}.",
        ]
    else:
        parts = [
            f"{n} đã được cảnh báo không được đếm những ô cửa sổ.",
            f"Lời cảnh báo đó vô nghĩa cho đến khi những tòa nhà quanh {place} bắt đầu mọc thêm một ô tối mỗi lần {n} nhìn đi chỗ khác.",
            f"Thứ lớn dần sau lớp kính không phải là một sinh vật, mà là {pressure}.",
            f"Không còn ai để hỏi, {n} {gesture}, chọn ô cửa sổ phản chiếu một ký ức thay vì một căn phòng.",
            f"Kính vỡ vào trong, và tiếng ồn đầu tiên của buổi sáng ùa qua như sự tha thứ mang theo những cạnh sắc. {g['message']}.",
        ]

    return "\n\n".join(parts)


def build_fallback_story(request: StoryRequest, language: str) -> str:
    """Build a complete fallback story with varied narrative structures."""
    if language != "vi":
        return build_creative_english_fallback(request)

    return build_creative_vietnamese_fallback(request)



def _dead_code_fallback(g=None, n="", s="", p="", t="", style=0):
    """Dead code - never called. Kept to avoid reparse issues."""
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


def clean_generated_story(story: str) -> str:
    """Light cleanup for model output without forcing it into a template."""
    text = story.strip()
    text = re.sub(r"\n{3,}", "\n\n", text)
    text = re.sub(r"^(Story|Truyen|Truyện)\s*:\s*", "", text, flags=re.IGNORECASE)

    stop_markers = [
        "\nMain character:",
        "\nPersonality:",
        "\nSetting:",
        "\nTheme:",
        "\nStory:",
        "\nPrompt:",
    ]
    for marker in stop_markers:
        index = text.find(marker)
        if index > 0:
            text = text[:index].strip()

    paragraphs = [part.strip() for part in re.split(r"\n\s*\n", text) if part.strip()]
    if len(paragraphs) > 7:
        text = "\n\n".join(paragraphs[:7])

    textbook_pattern = re.compile(
        r"\b(lesson|objective|glossary|section|question|answer|curriculum|"
        r"students|definition|exercise|introduction to)\b",
        flags=re.IGNORECASE,
    )
    sentences = re.findall(r"[^.!?]+[.!?]+|[^.!?]+$", text)
    filtered_sentences = [
        sentence.strip()
        for sentence in sentences
        if sentence.strip() and not textbook_pattern.search(sentence)
    ]
    if filtered_sentences:
        text = " ".join(filtered_sentences)

    return text.strip()


def score_story_candidate(story: str, language: str, request: StoryRequest) -> int:
    """Rank generated candidates by coherence and narrative specificity."""
    text = clean_generated_story(story)
    lowered = text.lower()
    score = 0

    if not text or has_garbled_artifacts(text):
        return -100

    if request.name.lower() in lowered:
        score += 25
    else:
        score -= 30

    context_hits = 0
    for source in (request.personality, request.setting, request.theme):
        tokens = [token for token in re.findall(r"\w+", source.lower()) if len(token) >= 4]
        if any(token in lowered for token in tokens):
            context_hits += 1
    score += context_hits * 12

    for phrase in (request.personality, request.setting, request.theme):
        normalized_phrase = phrase.strip().lower()
        if len(normalized_phrase) >= 4:
            exact_count = lowered.count(normalized_phrase)
            if exact_count:
                score -= 6 * exact_count  # Reduced from 10 to allow more natural phrasing

    sentence_count = len(re.findall(r"[.!?]+", text))
    if 5 <= sentence_count <= 14:
        score += 20
    elif sentence_count >= 4:
        score += 8
    else:
        score -= 20

    word_count = len(re.findall(r"\w+", text))
    if 120 <= word_count <= 320:
        score += 20
    elif 80 <= word_count < 120:
        score += 8
    else:
        score -= 10

    action_words = {
        "found", "ran", "opened", "chose", "left", "returned", "asked", "hid",
        "followed", "broke", "saved", "crossed", "remembered", "decided",
        "tìm", "chạy", "mở", "chọn", "rời", "trở", "hỏi", "giấu", "theo",
        "vỡ", "cứu", "băng", "nhớ", "quyết",
    }
    action_hits = sum(1 for word in re.findall(r"\w+", lowered) if word in action_words)
    score += min(action_hits * 3, 18)

    abstract_words = {
        "meaningful", "journey", "lesson", "truth", "choice", "responsibility",
        "ý", "nghĩa", "bài", "học", "hành", "trình", "lựa", "chọn",
    }
    abstract_hits = sum(1 for word in re.findall(r"\w+", lowered) if word in abstract_words)
    if abstract_hits > 8:  # Reduced from 12 to catch moral-essay tone earlier
        score -= 12

    # Bonus for dialogue (sign of vivid, scene-based writing)
    dialogue_count = len(re.findall(r'["\u201c\u201d\u2018\u2019]', text))
    if dialogue_count >= 2:
        score += 8

    # Bonus for sensory/action verbs beyond the action_words set
    sensory_words = {
        "whispered", "glanced", "breathed", "smelled", "shivered", "echoed",
        "thầm", "nhìn", "thở", "run", "rùng", "vang",
    }
    sensory_hits = sum(1 for word in re.findall(r"\w+", lowered) if word in sensory_words)
    score += min(sensory_hits * 3, 9)

    if PROMPT_LABEL_PATTERN.search(text):
        score -= 35

    textbook_markers = {
        "lesson:", "objective:", "glossary:", "section ", "question:", "answer:",
        "introduction to", "students", "definition", "exercise", "curriculum",
    }
    marker_hits = sum(1 for marker in textbook_markers if marker in lowered)
    score -= marker_hits * 35

    repeated_sentences = re.findall(r"([^.!?]{20,}[.!?])", text)
    if len(repeated_sentences) != len(set(sentence.strip().lower() for sentence in repeated_sentences)):
        score -= 20

    if language == "vi" and len(VIETNAMESE_DIACRITIC_PATTERN.findall(text)) == 0:
        score -= 10

    return score

def validate_input(data: Dict[str, str]) -> bool:
    """Validate input data."""
    required_fields = ["name", "personality", "setting", "theme"]
    for field in required_fields:
     if field not in data or not isinstance(data[field], str) or len(data[field].strip()) == 0:
         logger.warning(f"Missing or empty field: {field}")
         return False
    return True

