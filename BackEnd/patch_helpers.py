"""Run this once to patch helpers.py with 5 distinct narrative styles."""
import pathlib

NEW_FALLBACK = r'''

# ── Vietnamese narrative styles ───────────────────────────────────────────────

def _build_vi_classic(n, p, s, t, g) -> str:
    o = _pick([
        f"{n} lớn lên ở {s} với tính cách {p} khiến ai cũng quý mến.",
        f"Ở {s}, không ai không biết {n} — người mang tính cách {p} hiếm thấy.",
        f"Giữa nhịp sống bận rộn của {s}, {n} với bản tính {p} vẫn là điểm tựa cho nhiều người.",
    ])
    c = _pick([
        f"Biến cố ập đến khi {g['challenge']} xảy ra, khiến mọi kế hoạch của {n} đảo lộn.",
        f"Một sự kiện bất ngờ liên quan đến {t} đẩy {n} vào tình huống chưa từng chuẩn bị.",
        f"Không ai ngờ {g['challenge']} lại là thử thách lớn nhất {n} từng đối mặt.",
    ])
    m = _pick([
        f"Dù vấp ngã nhiều lần, {n} không bỏ cuộc vì tính cách {p} không cho phép.",
        f"Những thất bại liên tiếp dạy cho {n} rằng {g['growth']} là điều không thể bỏ qua.",
        f"Càng khó khăn, {n} càng kiên định hơn, từng bước tìm ra hướng đi.",
    ])
    cl = _pick([
        f"Đến cao trào, {n} đưa ra quyết định dứt khoát và trực tiếp đối đầu xung đột.",
        f"Khi mọi người gần như bỏ cuộc, chính {n} đứng ra và thay đổi cục diện.",
        f"Trong khoảnh khắc căng thẳng nhất, {n} chọn hành động thay vì chờ đợi.",
    ])
    e = _pick([
        f"Sau tất cả, {s} dần trở lại bình yên. Câu chuyện ấy nhắc mọi người: {g['message']}.",
        f"Biến cố khép lại, nhưng bài học còn mãi: {g['message']}.",
        f"Từ đó, {n} sống khác đi — sâu sắc hơn. Vì {n} đã hiểu: {g['message']}.",
    ])
    return "\n\n".join([o, c, m, cl, e])


def _build_vi_medias_res(n, p, s, t, g) -> str:
    a = _pick([
        f"Không có thời gian để nghĩ — {n} phải hành động ngay lập tức.",
        f"Đó là lần đầu tiên {n} nhận ra mọi thứ có thể sụp đổ chỉ trong một khoảnh khắc.",
        f"Khi {g['challenge']} bùng phát tại {s}, {n} là người đầu tiên đứng ra đối mặt.",
    ])
    b = _pick([
        f"Ít ai biết rằng {n} — người vốn {p} và điềm tĩnh — đã từng rất sợ khoảnh khắc này.",
        f"Vài tuần trước, {n} chỉ là người {p} sống yên bình ở {s}, không nghĩ mình sẽ phải chọn lựa như vậy.",
        f"Nhưng {n} đã học được điều gì đó từ lâu: {g['growth']}. Và đó là thứ duy nhất có ích lúc này.",
    ])
    st = _pick([
        f"Mọi thứ không diễn ra suôn sẻ. {n} vấp ngã, nghi ngờ, có lúc gần như bỏ cuộc.",
        f"{n} mắc sai lầm — không ít lần. Nhưng mỗi lần ngã, {n} đứng dậy với hiểu biết sâu hơn.",
        f"Hành trình dài và đau hơn {n} nghĩ. Nhưng đó cũng là cách {n} trưởng thành.",
    ])
    r = _pick([
        f"Và rồi, đúng vào lúc tưởng như hết hy vọng, {n} tìm ra lối thoát.",
        f"Cuối cùng, không phải sức mạnh hay may mắn đã giúp {n} — mà là sự kiên trì và tính cách {p}.",
        f"Khi cơn bão qua đi, {n} đứng ở phía bên kia — khác hơn, nhưng vẫn là mình.",
    ])
    rf = _pick([
        f"Nhìn lại, {n} hiểu rằng {t} không phải điều học từ sách — mà phải sống qua. {g['message']}.",
        f"Người ta ở {s} nói nhiều về chuyện đó. Nhưng điều {n} nhớ nhất: {g['message']}.",
        f"Đêm hôm đó ở {s}, {n} ngồi lặng và nhận ra: {g['message']}.",
    ])
    return "\n\n".join([a, b, st, r, rf])


def _build_vi_memoir(n, p, s, t, g) -> str:
    i = _pick([
        f"Người ta thường hỏi {n} bài học lớn nhất trong đời là gì. Câu trả lời luôn bắt đầu từ {s}.",
        f"Có những khoảng thời gian {n} không bao giờ quên — và câu chuyện ở {s} là một trong số đó.",
        f"Nếu phải kể lại, {n} sẽ bắt đầu từ cái ngày mọi thứ còn đơn giản, khi {s} vẫn là thế giới quen thuộc.",
    ])
    pa = _pick([
        f"Hồi đó, {n} còn trẻ và {p} theo kiểu chưa biết {g['challenge']} là gì.",
        f"{n} nhớ rõ lần đầu đối mặt với {g['challenge']} — bối rối, chơi vơi, không sẵn sàng chút nào.",
        f"Trước khi tất cả xảy ra, {n} chỉ là người {p} sống bình thường ở {s} — không hơn, không kém.",
    ])
    tu = _pick([
        f"Nhưng rồi mọi thứ thay đổi. Và {n} không còn có thể làm ngơ trước {t} nữa.",
        f"Cái ngày đó đến mà không báo trước, và {n} hiểu có những thứ không thể né tránh mãi.",
        f"Sự kiện xảy ra nhanh, nhưng bài học đến chậm — và đau.",
    ])
    le = _pick([
        f"Sau này, {n} nhận ra điều quan trọng nhất không phải thành công — mà là {g['growth']}.",
        f"Nhìn lại, {n} thấy rõ: chính {g['challenge']} mới là thứ thay đổi {n} sâu sắc nhất.",
        f"Có những thứ chỉ hiểu được sau khi đã trải qua. Với {n}, đó là {g['growth']}.",
    ])
    cl = _pick([
        f"Và đó là lý do mỗi khi ai nhắc đến {t}, {n} lại nhớ đến {s} và thầm nghĩ: {g['message']}.",
        f"Câu chuyện ấy không có anh hùng — chỉ có một người học cách sống với {t}. {g['message']}.",
        f"Bây giờ mỗi lần trở lại {s}, {n} vẫn nhớ. Và hiểu hơn bao giờ hết: {g['message']}.",
    ])
    return "\n\n".join([i, pa, tu, le, cl])


def _build_vi_dialogue(n, p, s, t, g) -> str:
    op = _pick([
        f'"Mày có chắc không?" — đó là câu hỏi {n} nghe nhiều nhất ở {s} trong những ngày đó.',
        f'"Không ai có thể làm được đâu," người ta nói. {n} nghe nhưng không trả lời.',
        f'"Sao lại là mày?" — câu hỏi đó vang lên lúc {n} bước ra giữa đám đông ở {s}.',
    ])
    co = _pick([
        f"{n} — người vốn {p} và ít nói — hiểu rằng đôi khi hành động nói nhiều hơn lời giải thích.",
        f"Chẳng ai ở {s} thực sự hiểu vì sao {n} lại chọn đứng ở phía khó hơn. Kể cả {n} cũng không chắc.",
        f"Nhưng {n} biết một điều: {g['challenge']} đang diễn ra, và {n} không thể giả vờ như không thấy.",
    ])
    ac = _pick([
        f"Những ngày tiếp theo, {n} hành động trong lặng lẽ — vấp ngã, đứng dậy, rồi lại tiếp tục.",
        f"{n} không giải thích nhiều. Chỉ làm. Và {g['growth']} dần trở thành thứ {n} thực sự hiểu.",
        f"Có lúc mệt mỏi, {n} tự hỏi có nên tiếp tục không. Rồi tự trả lời bằng cách đứng dậy thêm một lần.",
    ])
    cx = _pick([
        f'"Tôi sẽ làm" — {n} nói, và làm thật.',
        f"Không có lời tuyên bố to tát. {n} chỉ làm điều phải làm, đúng lúc cần thiết nhất.",
        f'"Sao lúc đó mày dám?" Người ta hỏi sau này. {n} chỉ cười: "Vì không còn lựa chọn nào khác."',
    ])
    en = _pick([
        f"Câu chuyện kết thúc không bằng hoa và tiếng vỗ tay — mà bằng một câu đơn giản: {g['message']}.",
        f"Và {s} học được một điều từ {n}: {g['message']}.",
        f'{t} với {n} có nghĩa gì? {n} lặng một lúc: "{g["message"]}".',
    ])
    return "\n\n".join([op, co, ac, cx, en])


def _build_vi_atmospheric(n, p, s, t, g) -> str:
    sc = _pick([
        f"{s} — nơi chứa đựng những câu chuyện mà không phải ai cũng dám kể lại.",
        f"Có những nơi mà thời gian dường như đặc hơn, và {s} là một trong số đó.",
        f"Không khí ở {s} hôm đó nặng nề theo cách khó diễn tả — như thể cả nơi này đang chờ điều gì đó.",
    ])
    it = _pick([
        f"Giữa khung cảnh ấy, {n} xuất hiện — {p} và điềm tĩnh hơn bất kỳ ai.",
        f"{n} là người {s} không dễ quên: {p}, ít lời, nhưng hành động luôn nói thay tất cả.",
        f"Ít ai chú ý đến {n} trong những ngày đầu. Nhưng {p} không phải thứ có thể giấu lâu.",
    ])
    cf = _pick([
        f"Rồi {g['challenge']} phá vỡ sự yên tĩnh ấy, và {s} trở nên khác đi theo cách không ai muốn.",
        f"Đúng khi {s} tưởng như đang ngủ yên, {g['challenge']} ập đến — và kéo {n} vào tâm điểm.",
        f"Mưa bắt đầu rơi đêm hôm đó. Và cùng lúc, {g['challenge']} hiện ra trước mắt {n}.",
    ])
    rs = _pick([
        f"Nhưng chính {n} — với tính cách {p} không bao giờ tắt — đã tìm ra lối đi giữa bóng tối đó.",
        f"{g['growth']} không bao giờ đến nhanh — nó đến đúng lúc. Và {n} đã sẵn sàng.",
        f"Khi ánh sáng cuối cùng cũng lọt qua, {n} đứng ở phía bên kia — khác hơn, nhưng vẫn là mình.",
    ])
    cl = _pick([
        f"{s} sau đó vẫn là {s}. Nhưng {n} thì không. Và câu chuyện ấy nhắc nhở: {g['message']}.",
        f"Không phải cổ tích — nhưng là thật. Và thông điệp thật: {g['message']}.",
        f"Người ta nhớ đến {n} không vì chiến thắng, mà vì cách {n} sống giữa khó khăn. {g['message']}.",
    ])
    return "\n\n".join([sc, it, cf, rs, cl])


# ── English narrative styles ──────────────────────────────────────────────────

def _build_en_classic(n, p, s, t, g) -> str:
    o = _pick([
        f"{n} was known in {s} for being {p} — dependable and hard to rattle.",
        f"{n} had lived in {s} long enough to know its rhythms. What {n} did not expect was how fast those rhythms could break.",
        f"People in {s} trusted {n}. A {p} person tends to earn that kind of trust quietly, over time.",
    ])
    c = _pick([
        f"Then came the day {g['challenge']} arrived, and nothing {n} had planned seemed to apply anymore.",
        f"A crisis tied to {t} disrupted {s}, and {n} found themselves at the center of it.",
        f"The incident asked of {n} exactly the kind of response {n} had never rehearsed.",
    ])
    m = _pick([
        f"The path forward was not clean. {n} stumbled, reconsidered, and stumbled again — but kept moving.",
        f"Doubt settled in more than once. But {n}'s {p} nature refused to treat every setback as the final word.",
        f"There were moments when giving up felt reasonable. {n} chose not to — not every time, but enough.",
    ])
    cl = _pick([
        f"At the critical moment, {n} stopped waiting for certainty and acted on what {n} knew was right.",
        f"When the hardest decision came, {n} made it — not because it was easy, but because it was necessary.",
        f"The situation demanded more than anyone wanted to give. {n} gave it anyway.",
    ])
    e = _pick([
        f"Afterward, {s} slowly returned to normal. {n} returned changed, but intact. {g['message']}.",
        f"The crisis ended. The lesson did not. {g['message']}.",
        f"What {n} took away from {s} was a deeper understanding of {t}: {g['message']}.",
    ])
    return "\n\n".join([o, c, m, cl, e])


def _build_en_medias_res(n, p, s, t, g) -> str:
    a = _pick([
        f"There was no time to think. {n} had to move — right now, without a plan.",
        f"The moment {g['challenge']} hit {s}, {n} was already in the middle of it.",
        f"By the time {n} understood what was happening, there was no clean way out — only through.",
    ])
    b = _pick([
        f"Hours earlier, {n} had been just another {p} person living an ordinary day in {s}.",
        f"Not long ago, {t} had been an abstract idea for {n} — something to think about, not live through.",
        f"{n} had learned {g['growth']} somewhere along the way. This was the moment it finally mattered.",
    ])
    st = _pick([
        f"It did not go smoothly. Several attempts failed before {n} found any traction at all.",
        f"{n} made mistakes — real ones. Each one hurt. Each one also taught something.",
        f"The middle of the crisis was the hardest part: no one could promise it would end.",
    ])
    tu = _pick([
        f"And then, without fanfare, the way forward appeared. {n} took it.",
        f"It was not a dramatic victory. It was one steady decision made at the right moment.",
        f"Through exhaustion and doubt and several wrong turns — {n} found the edge of the storm and stepped past it.",
    ])
    rf = _pick([
        f"Looking back later, {n} thought about {t} differently. {g['message']}.",
        f"The people of {s} moved on. But {n} carried the experience forward. {g['message']}.",
        f"The clearest thing {n} remembered afterward was not the conflict but the lesson underneath: {g['message']}.",
    ])
    return "\n\n".join([a, b, st, tu, rf])


def _build_en_memoir(n, p, s, t, g) -> str:
    h = _pick([
        f"If {n} ever had to pick the moment everything changed, it would be a specific afternoon in {s}.",
        f"Years later, {n} would say: 'That was when I finally understood {t}.'",
        f"{n} has been asked many times what {p} really means under pressure. The answer always starts in {s}.",
    ])
    bg = _pick([
        f"Back then, {n} was younger and more certain than the situation deserved.",
        f"Before it all happened, {n} had thought of {t} as something noble and distant — not personal.",
        f"{n} had never faced {g['challenge']} before. No one had said how much it would ask.",
    ])
    ev = _pick([
        f"Then the situation in {s} changed, and {t} stopped being abstract.",
        f"What followed was not a clean story — it was confusing, exhausting, and at times humbling.",
        f"The weeks that followed tested {n} in ways that had nothing to do with being {p}.",
    ])
    ins = _pick([
        f"The real turning point was the slow recognition that {g['growth']}.",
        f"Somewhere in the middle of it, {n} stopped asking whether it was worth it and started asking what it was teaching.",
        f"What {n} learned was not what {n} expected. But it was more useful: {g['growth']}.",
    ])
    en = _pick([
        f"That is why, when people ask {n} about {t}, the answer is never theoretical. {g['message']}.",
        f"{s} gave {n} many things. The most lasting one was this: {g['message']}.",
        f"The memory of {s} has faded in places. But not: {g['message']}.",
    ])
    return "\n\n".join([h, bg, ev, ins, en])


def _build_en_dialogue(n, p, s, t, g) -> str:
    op = _pick([
        f"'Are you sure about this?' someone asked {n} that morning in {s}. {n} was not sure. {n} went anyway.",
        f"'Nobody can fix this,' they said. {n} heard it, nodded once, and got to work.",
        f"'Why you?' The question followed {n} through {s} for days. {n} never had a clean answer.",
    ])
    co = _pick([
        f"{n} — {p} by nature — had not planned to be involved. But {g['challenge']} does not care about plans.",
        f"Being {p} in {s} was usually quiet work. What made this different was that quiet work was no longer enough.",
        f"{n} understood something others had not yet accepted: {g['challenge']} was not going away on its own.",
    ])
    mi = _pick([
        f"The days that followed were not heroic. They were repetitive, difficult, and occasionally absurd.",
        f"{n} tried three approaches before finding one that held. Each failure was its own conversation with reality.",
        f"There were arguments, setbacks, and at least one moment when {n} seriously considered stepping back.",
    ])
    cx = _pick([
        f"At the decisive moment, {n} said: 'I'll handle it' — and did.",
        f"When the outcome finally shifted, it happened quietly — one careful action at a time.",
        f"'How did it end?' people asked later. 'Slowly,' said {n}, 'and then all at once.'",
    ])
    cl = _pick([
        f"The story of {n} and {s} did not make headlines. But it made a point: {g['message']}.",
        f"Someone asked {n} once: 'What does {t} mean to you?' After a pause: '{g['message']}'.",
        f"The last word on all of it was short: {g['message']}.",
    ])
    return "\n\n".join([op, co, mi, cx, cl])


def _build_en_atmospheric(n, p, s, t, g) -> str:
    sc = _pick([
        f"{s} — a place that holds its stories close, rarely sharing them with outsiders.",
        f"There is a particular quality to the light in {s} on difficult days. {n} would come to know it well.",
        f"Not every place carries the weight of its events visibly. {s} is not one of those places.",
    ])
    it = _pick([
        f"Into that landscape arrived {n} — {p}, deliberate, and unaware of what the next weeks would require.",
        f"{n} had come to {s} without expectation. What {s} returned was not what {n} would have asked for.",
        f"A {p} person in a place like {s} does not go unnoticed for long. Nor did {n}.",
    ])
    cf = _pick([
        f"The trouble began the way trouble usually does in quiet places: gradually, and then all at once.",
        f"{g['challenge']} settled over {s} like weather, and {n} was not equipped to simply wait it out.",
        f"What {t} required of {n} became clear in the space of a few difficult days.",
    ])
    rs = _pick([
        f"The resolution was not clean. But {n} brought {p} to the problem and, eventually, that was enough.",
        f"What changed things was not a single decision but a series of small, consistent ones.",
        f"By the time the difficulty passed, {n} had become someone slightly different — changed, but not unrecognizable.",
    ])
    cl = _pick([
        f"{s} returned to itself in time. {n} did not return to who they had been. {g['message']}.",
        f"The landscape of {s} does not carry monuments. It carries memory. And: {g['message']}.",
        f"Somewhere between the beginning and the end, {t} stopped being an idea. {g['message']}.",
    ])
    return "\n\n".join([sc, it, cf, rs, cl])


def build_fallback_story(request: StoryRequest, language: str) -> str:
    """Build a varied story when model output is poor.

    Randomly selects one of 5 distinct narrative styles so stories feel
    genuinely different even when input parameters are similar:
      - Classic 3rd-person narrator
      - In medias res (starts mid-action, then context)
      - Memoir / first-person reflective
      - Dialogue-driven
      - Atmospheric / descriptive setting-first
    """
    guidance = _theme_guidance(request.theme, language)
    n, p, s, t = request.name, request.personality, request.setting, request.theme

    if language == "vi":
        builders = [
            _build_vi_classic,
            _build_vi_medias_res,
            _build_vi_memoir,
            _build_vi_dialogue,
            _build_vi_atmospheric,
        ]
    else:
        builders = [
            _build_en_classic,
            _build_en_medias_res,
            _build_en_memoir,
            _build_en_dialogue,
            _build_en_atmospheric,
        ]

    return _pick(builders)(n, p, s, t, guidance)


def validate_input(data: Dict[str, str]) -> bool:
    """Validate input data."""
    required_fields = ["name", "personality", "setting", "theme"]
    for field in required_fields:
        if field not in data or not isinstance(data[field], str) or len(data[field].strip()) == 0:
            logger.warning(f"Missing or empty field: {field}")
            return False
    return True
'''

p = pathlib.Path(r'c:\Big_Data\AI\Final Term\BackEnd\app\utils\helpers.py')
content = p.read_text(encoding='utf-8')
cut = content.find('\ndef build_fallback_story(')
if cut == -1:
    print('ERROR: marker not found')
else:
    kept = content[:cut]
    p.write_text(kept + NEW_FALLBACK, encoding='utf-8')
    total = (kept + NEW_FALLBACK).count('\n')
    print(f'OK — total lines written: {total}')
