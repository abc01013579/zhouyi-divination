# 周易摇卦 (Zhouyi Divination)

A small Flask web app for casting an *I Ching* (Book of Changes) hexagram using the traditional three-coin method, then looking up the resulting hexagram(s) and moving-line text.

**Live:** [shuiming.cc](https://shuiming.cc)

## How it works

1. You toss three coins six times (once per line, bottom to top), scoring heads = 3, tails = 2, and summing each toss to get a value of 6, 7, 8, or 9:
   - **6** — three tails (old yin, a changing line)
   - **7** — two tails, one head (young yang)
   - **8** — two heads, one tail (young yin)
   - **9** — three heads (old yang, a changing line)
2. Enter the six values into the form, from the first line (初爻) to the top line (上爻).
3. The app builds the resulting hexagram (本卦) from the values, and if any lines are "old" (6 or 9) — meaning they change to their opposite — it also derives the transformed hexagram (变卦) and shows the relevant moving-line text (爻辞).

## Project structure

- `app.py` — Flask routes; validates the six submitted yao values and renders the result.
- `yijing_core.py` — Maps the six yin/yang lines to one of the 64 hexagrams and computes the changed hexagram from moving lines.
- `cs001.py` — Hexagram and line-text data (names and classical text for all 64 hexagrams).
- `templates/index.html` — Single-page form and result view.
- `static/style.css` — Styling, including a print stylesheet for the result.
- `render.yaml` — Render.com blueprint for one-click deployment.

## Running locally

```bash
pip install -r requirements.txt
python app.py
```

Then open `http://127.0.0.1:5000`.

## Deployment

Deployed on [Render](https://render.com) (free tier) via the included `render.yaml` blueprint, with a custom domain routed through Cloudflare DNS.
