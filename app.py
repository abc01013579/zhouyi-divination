from flask import Flask, render_template, request

from yijing_core import cast_reading

app = Flask(__name__)

VALID_YAO = (6, 7, 8, 9)

UI_STRINGS = {
    "zh": {
        "html_lang": "zh",
        "title": "周易摇卦",
        "heading": "周易摇卦",
        "hint": "请依次输入六爻的数值（6、7、8 或 9），从初爻（第一爻）到上爻（第六爻）。",
        "coin_guide_title": "如何摇卦：三枚硬币法",
        "coin_guide_intro": "准备三枚硬币，正面记 3 分，反面记 2 分。每一爻投掷三枚硬币一次，将三枚点数相加，得到该爻的数值：",
        "coin_6": "6 = 三个反面（老阴，变爻）",
        "coin_7": "7 = 两反一正（少阳）",
        "coin_8": "8 = 两正一反（少阴）",
        "coin_9": "9 = 三个正面（老阳，变爻）",
        "coin_guide_outro": "从初爻（第一爻）摇到上爻（第六爻），共投掷六次，再将六个数值依次填入下方。",
        "yao_label": "第{}爻",
        "submit": "起卦",
        "print_btn": "打印卦象",
        "original_hexagram": "本卦",
        "changed_hexagram": "变卦",
        "moving_text_label": "爻辞",
        "no_change": "无变爻，本卦即为最终卦。",
        "error_incomplete": "请输入完整的爻值（六个都要填）。",
        "error_range": "爻值必须是 6、7、8 或 9。",
        "lang_switch_label": "English",
        "lang_switch_target": "en",
    },
    "en": {
        "html_lang": "en",
        "title": "Zhouyi Divination",
        "heading": "Zhouyi (I Ching) Divination",
        "hint": "Enter the value of each line (6, 7, 8, or 9) in order, from the first (bottom) line to the sixth (top) line.",
        "coin_guide_title": "How to Cast: Three-Coin Method",
        "coin_guide_intro": "Prepare three coins — heads count 3, tails count 2. Toss all three coins once per line and add the values together to get that line's number:",
        "coin_6": "6 = three tails (old yin, changing line)",
        "coin_7": "7 = two tails, one heads (young yang)",
        "coin_8": "8 = two heads, one tails (young yin)",
        "coin_9": "9 = three heads (old yang, changing line)",
        "coin_guide_outro": "Cast from the first (bottom) line to the sixth (top) line — six tosses in total — then enter the six values below in order.",
        "yao_label": "Line {}",
        "submit": "Cast Hexagram",
        "print_btn": "Print Reading",
        "original_hexagram": "Original Hexagram",
        "changed_hexagram": "Changed Hexagram",
        "moving_text_label": "Changing Line Text",
        "no_change": "No changing lines — the original hexagram is the final reading.",
        "error_incomplete": "Please enter all six line values.",
        "error_range": "Line values must be 6, 7, 8, or 9.",
        "lang_switch_label": "中文",
        "lang_switch_target": "zh",
    },
}


def resolve_lang(request):
    lang = request.values.get("lang", "zh")
    return lang if lang in UI_STRINGS else "zh"


@app.route("/", methods=["GET", "POST"])
def index():
    result = None
    error = None
    submitted = []
    lang = resolve_lang(request)
    t = UI_STRINGS[lang]

    if request.method == "POST":
        raw_values = [request.form.get(f"yao{i}", "").strip() for i in range(1, 7)]
        submitted = raw_values

        try:
            yao_list = [int(v) for v in raw_values]
        except ValueError:
            error = t["error_incomplete"]
            yao_list = None

        if yao_list is not None and any(y not in VALID_YAO for y in yao_list):
            error = t["error_range"]
            yao_list = None

        if yao_list is not None:
            result = cast_reading(yao_list, lang=lang)

    return render_template(
        "index.html", result=result, error=error, submitted=submitted, lang=lang, t=t
    )


if __name__ == "__main__":
    app.run(debug=True)
