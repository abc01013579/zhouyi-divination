from flask import Flask, render_template, request

from yijing_core import cast_reading

app = Flask(__name__)

VALID_YAO = (6, 7, 8, 9)


@app.route("/", methods=["GET", "POST"])
def index():
    result = None
    error = None
    submitted = []

    if request.method == "POST":
        raw_values = [request.form.get(f"yao{i}", "").strip() for i in range(1, 7)]
        submitted = raw_values

        try:
            yao_list = [int(v) for v in raw_values]
        except ValueError:
            error = "请输入完整的爻值（六个都要填）。"
            yao_list = None

        if yao_list is not None and any(y not in VALID_YAO for y in yao_list):
            error = "爻值必须是 6、7、8 或 9。"
            yao_list = None

        if yao_list is not None:
            result = cast_reading(yao_list)

    return render_template("index.html", result=result, error=error, submitted=submitted)


if __name__ == "__main__":
    app.run(debug=True)
