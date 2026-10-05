from flask import Flask, render_template, request

from dca import calculate_dca
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
        "chosen_text_label": "断辞",
        "no_change": "无变爻，本卦即为最终卦。",
        "error_incomplete": "请输入完整的爻值（六个都要填）。",
        "error_range": "爻值必须是 6、7、8 或 9。",
        "lang_switch_label": "English",
        "lang_switch_target": "en",
        "classics_link_label": "中华典籍",
        "guide_link_label": "如何解卦",
        "journal_link_label": "随笔",
        "balance_plate_link_label": "Shopping List",
        "dca_link_label": "复利计算器",
        "read_link_label": "朗读",
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
        "chosen_text_label": "Reading",
        "no_change": "No changing lines — the original hexagram is the final reading.",
        "error_incomplete": "Please enter all six line values.",
        "error_range": "Line values must be 6, 7, 8, or 9.",
        "lang_switch_label": "中文",
        "lang_switch_target": "zh",
        "classics_link_label": "Chinese Classics",
        "guide_link_label": "How to Read a Hexagram",
        "journal_link_label": "Journal",
        "balance_plate_link_label": "Shopping List",
        "dca_link_label": "DCA Calculator",
        "read_link_label": "Read Aloud",
    },
}

DCA_STRINGS = {
    "zh": {
        "html_lang": "zh",
        "title": "复利计算器",
        "heading": "定投复利计算器",
        "hint": "输入每年投入金额和预期年化收益率，查看 5、10、20、30、40、50、60 年后的复利总额。假设每年年初投入，全年参与复利增长。",
        "amount_label": "每年投入金额",
        "rate_label": "预期年化收益率（%）",
        "submit": "计算",
        "years_col": "年数",
        "contributed_col": "累计投入",
        "total_col": "复利总额",
        "growth_col": "增值部分",
        "error_incomplete": "请输入完整的投入金额和收益率。",
        "lang_switch_label": "English",
        "lang_switch_target": "en",
        "index_link_label": "周易摇卦",
    },
    "en": {
        "html_lang": "en",
        "title": "DCA Calculator",
        "heading": "DCA Compounding Calculator",
        "hint": "Enter a yearly investment amount and an expected annual growth rate to see the compounded total after 5, 10, 20, 30, 40, 50, and 60 years. Assumes each year's contribution is made at the start of that year and compounds through the full year.",
        "amount_label": "Yearly investment amount",
        "rate_label": "Expected annual growth rate (%)",
        "submit": "Calculate",
        "years_col": "Years",
        "contributed_col": "Total contributed",
        "total_col": "Total value",
        "growth_col": "Growth",
        "error_incomplete": "Please enter both the yearly amount and the growth rate.",
        "lang_switch_label": "中文",
        "lang_switch_target": "zh",
        "index_link_label": "Zhouyi Divination",
    },
}

READ_STRINGS = {
    "zh": {
        "html_lang": "zh",
        "title": "朗读",
        "heading": "朗读",
        "hint": "粘贴文字，或打开 PDF / TXT 文件，中文用中文声音读，英文用英文声音读。选中一段只读那一段；把光标放在某处就从那里读起。文字只在本机处理，不上传。",
        "text_placeholder": "在此粘贴文字……",
        "paste": "粘贴",
        "clear": "清空",
        "paste_error": "无法读取剪贴板，请用 Ctrl+V 粘贴。",
        "file_label": "打开 PDF 或 TXT",
        "play": "朗读",
        "pause": "暂停",
        "resume": "继续",
        "stop": "停止",
        "rate_label": "语速",
        "zh_voice_label": "中文声音",
        "en_voice_label": "英文声音",
        "auto_voice": "自动",
        "loading_pdf": "正在读取 PDF：第 {page} / {pages} 页",
        "loaded": "已载入 {name}",
        "no_text": "这个文件里没有可读的文字（可能是扫描图片）。",
        "file_error": "无法读取这个文件。",
        "nothing": "请先粘贴文字或打开文件。",
        "no_speech": "此浏览器不支持朗读。",
        "done": "读完了。",
        "lang_switch_label": "English",
        "lang_switch_target": "en",
        "index_link_label": "周易摇卦",
    },
    "en": {
        "html_lang": "en",
        "title": "Read Aloud",
        "heading": "Read Aloud",
        "hint": "Paste text, or open a PDF / TXT file. Chinese is read with a Chinese voice, English with an English voice. Select a passage to read just that, or click somewhere to start from there. Everything stays on this device; nothing is uploaded.",
        "text_placeholder": "Paste text here…",
        "paste": "Paste",
        "clear": "Clear",
        "paste_error": "Couldn't read the clipboard; paste with Ctrl+V instead.",
        "file_label": "Open PDF or TXT",
        "play": "Read",
        "pause": "Pause",
        "resume": "Resume",
        "stop": "Stop",
        "rate_label": "Speed",
        "zh_voice_label": "Chinese voice",
        "en_voice_label": "English voice",
        "auto_voice": "Automatic",
        "loading_pdf": "Reading PDF: page {page} / {pages}",
        "loaded": "Loaded {name}",
        "no_text": "No readable text in this file (it may be a scanned image).",
        "file_error": "Couldn't read this file.",
        "nothing": "Paste some text or open a file first.",
        "no_speech": "This browser can't read aloud.",
        "done": "Finished.",
        "lang_switch_label": "中文",
        "lang_switch_target": "zh",
        "index_link_label": "Zhouyi Divination",
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


@app.route("/balance-plate")
def balance_plate_page():
    return render_template("balance_plate.html")


@app.route("/dca", methods=["GET", "POST"])
def dca_page():
    result = None
    error = None
    submitted = {}
    lang = resolve_lang(request)
    t = DCA_STRINGS[lang]

    if request.method == "POST":
        submitted = {
            field: request.form.get(field, "").strip() for field in ("amount", "rate")
        }

        try:
            amount = float(submitted["amount"])
            rate = float(submitted["rate"])
        except ValueError:
            error = t["error_incomplete"]
        else:
            result = calculate_dca(amount, rate)

    return render_template(
        "dca.html", result=result, error=error, submitted=submitted, lang=lang, t=t
    )


@app.route("/read")
def read_page():
    lang = resolve_lang(request)
    return render_template("read.html", lang=lang, t=READ_STRINGS[lang])


if __name__ == "__main__":
    app.run(debug=True)
