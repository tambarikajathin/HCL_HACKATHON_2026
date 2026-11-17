"""Build the 6-slide ResearchIQ hackathon deck.

Usage:  python docs/build_presentation.py
Output: docs/ResearchIQ_Presentation.pptx
Edit TEAM_NAME / MEMBERS below before presenting.
"""
from pathlib import Path

from pptx import Presentation
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_CONNECTOR, MSO_SHAPE
from pptx.enum.text import MSO_ANCHOR, PP_ALIGN
from pptx.util import Emu, Inches, Pt

# ------------------------------------------------------------------ edit me
TEAM_NAME = "<Team Name>"
MEMBERS = ["<Member 1>", "<Member 2>", "<Member 3>", "<Member 4>"]
# --------------------------------------------------------------------------

OUT = Path(__file__).with_name("ResearchIQ_Presentation.pptx")
NAVY, BLUE, TEAL = RGBColor(0x14, 0x2B, 0x4C), RGBColor(0x1F, 0x6F, 0xB2), RGBColor(0x0E, 0x9F, 0x8E)
LIGHT, GREY, WHITE = RGBColor(0xEE, 0xF3, 0xF9), RGBColor(0x55, 0x5F, 0x6B), RGBColor(0xFF, 0xFF, 0xFF)
AMBER = RGBColor(0xE0, 0x8A, 0x1E)

prs = Presentation()
prs.slide_width, prs.slide_height = Inches(13.333), Inches(7.5)
BLANK = prs.slide_layouts[6]
W = prs.slide_width


def text(slide, x, y, w, h, content, size=16, bold=False, color=NAVY, align=PP_ALIGN.LEFT,
         anchor=MSO_ANCHOR.TOP, bullets=False):
    """Add a textbox. `content` is a string or a list of lines (list -> one paragraph per line)."""
    tb = slide.shapes.add_textbox(x, y, w, h)
    tf = tb.text_frame
    tf.word_wrap = True
    tf.vertical_anchor = anchor
    lines = content if isinstance(content, list) else [content]
    for i, line in enumerate(lines):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.alignment = align
        p.space_after = Pt(6)
        r = p.add_run()
        r.text = ("•  " + line) if bullets else line
        r.font.size, r.font.bold, r.font.color.rgb = Pt(size), bold, color
    return tb


def box(slide, x, y, w, h, title, body=None, fill=LIGHT, title_color=NAVY, size=13, body_size=11):
    shp = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, x, y, w, h)
    shp.adjustments[0] = 0.12
    shp.fill.solid()
    shp.fill.fore_color.rgb = fill
    shp.line.color.rgb = fill
    tf = shp.text_frame
    tf.word_wrap = True
    tf.vertical_anchor = MSO_ANCHOR.MIDDLE
    for m in ("margin_left", "margin_right"):
        setattr(tf, m, Inches(0.08))
    p = tf.paragraphs[0]
    p.alignment = PP_ALIGN.CENTER
    r = p.add_run()
    r.text = title
    r.font.size, r.font.bold, r.font.color.rgb = Pt(size), True, title_color
    if body:
        p2 = tf.add_paragraph()
        p2.alignment = PP_ALIGN.CENTER
        r2 = p2.add_run()
        r2.text = body
        r2.font.size = Pt(body_size)
        r2.font.color.rgb = WHITE if fill in (BLUE, TEAL, NAVY) else GREY
    return shp


def arrow(slide, x1, y1, x2, y2, color=GREY):
    c = slide.shapes.add_connector(MSO_CONNECTOR.STRAIGHT, x1, y1, x2, y2)
    c.line.color.rgb, c.line.width = color, Pt(1.75)
    c.line._get_or_add_ln().append(_arrow_head())
    return c


def _arrow_head():
    from pptx.oxml.ns import qn
    from lxml import etree
    el = etree.SubElement(etree.Element("dummy"), qn("a:tailEnd"))
    el.set("type", "triangle")
    return el


def header(slide, title, subtitle=None, num=None):
    bar = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, W, Inches(1.05))
    bar.fill.solid()
    bar.fill.fore_color.rgb = NAVY
    bar.line.fill.background()
    text(slide, Inches(0.5), Inches(0.18), Inches(10), Inches(0.7), title, 30, True, WHITE)
    if subtitle:
        text(slide, Inches(0.5), Inches(1.15), Inches(12.3), Inches(0.5), subtitle, 15, False, GREY)
    if num:
        text(slide, Inches(11.8), Inches(0.3), Inches(1.1), Inches(0.5), f"{num} / 6", 14, False, WHITE,
             PP_ALIGN.RIGHT)


# ===================================================== 1. Problem statement
s = prs.slides.add_slide(BLANK)
bg = s.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, W, prs.slide_height)
bg.fill.solid()
bg.fill.fore_color.rgb = NAVY
bg.line.fill.background()
text(s, Inches(0.6), Inches(0.45), Inches(8), Inches(0.9), "ResearchIQ", 44, True, WHITE)
text(s, Inches(0.6), Inches(1.25), Inches(8.5), Inches(0.6),
     "Multimodal, evidence-grounded AI research assistant", 20, False, RGBColor(0xB8, 0xD4, 0xF0))
text(s, Inches(0.6), Inches(2.1), Inches(7.4), Inches(0.5), "Problem statement", 18, True, AMBER)
text(s, Inches(0.6), Inches(2.55), Inches(7.4), Inches(1.6),
     "Researchers must read many papers to compare methods and results. Generic PDF chatbots ignore "
     "tables, figures and charts, mix up papers, and state claims that the papers never make.",
     15, False, WHITE)
text(s, Inches(0.6), Inches(3.95), Inches(7.4), Inches(0.5), "Requirements to be solved", 18, True, AMBER)
text(s, Inches(0.6), Inches(4.4), Inches(7.4), Inches(2.9), [
    "Ingest 8–10 open-access papers on one topic (ours: Retrieval-Augmented Generation)",
    "Understand text, tables, figures, diagrams and charts",
    "Answer, compare and synthesise across papers with paper / page / figure citations",
    "Flag missing or conflicting evidence instead of guessing",
    "Separate author findings from AI interpretation; resist prompt injection",
], 14, False, WHITE, bullets=True)
team = s.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(8.6), Inches(2.1), Inches(4.2), Inches(4.6))
team.fill.solid()
team.fill.fore_color.rgb = BLUE
team.line.fill.background()
text(s, Inches(8.85), Inches(2.3), Inches(3.8), Inches(0.5), "Team", 16, True, RGBColor(0xB8, 0xD4, 0xF0))
text(s, Inches(8.85), Inches(2.75), Inches(3.8), Inches(0.7), TEAM_NAME, 24, True, WHITE)
text(s, Inches(8.85), Inches(3.6), Inches(3.8), Inches(0.5), "Members", 16, True, RGBColor(0xB8, 0xD4, 0xF0))
text(s, Inches(8.85), Inches(4.05), Inches(3.8), Inches(2.5), MEMBERS, 16, False, WHITE)
text(s, Inches(0.6), Inches(6.9), Inches(12), Inches(0.4), "HCL Hackathon 2026", 12, False,
     RGBColor(0xB8, 0xD4, 0xF0))

# ===================================================== 2. Approach
s = prs.slides.add_slide(BLANK)
header(s, "Approach", "Two connected pipelines, direct Python orchestration — no agent frameworks", 2)
cards = [
    ("Structure-aware parsing", "Docling first, PyMuPDF fallback per page, PaddleOCR for scans. One page = one parser, so no duplicate elements."),
    ("Multimodal understanding", "Figures cropped and described once by Qwen2.5-VL (cached). Tables kept as rows + text. Charts read without inventing values."),
    ("Hybrid retrieval", "Dense (OpenAI embeddings in Qdrant) + BM25, merged with Reciprocal Rank Fusion, reranked by a BGE cross-encoder."),
    ("Evidence before answers", "Sufficiency check runs before the LLM. Not enough evidence → explain what is missing instead of answering."),
    ("Verified claims", "Every claim carries source ids. Numbers must appear in cited text; an LLM verifier checks support. Unsupported claims are removed."),
    ("Security by default", "PDF text is data, never instructions: injection-like sentences stripped, input validation, rate limiting, secret redaction."),
]
cw, ch = Inches(3.95), Inches(2.45)
for i, (t, b) in enumerate(cards):
    x = Inches(0.5) + (cw + Inches(0.22)) * (i % 3)
    y = Inches(1.75) + (ch + Inches(0.25)) * (i // 3)
    card = s.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, x, y, cw, ch)
    card.adjustments[0] = 0.06
    card.fill.solid()
    card.fill.fore_color.rgb = LIGHT
    card.line.fill.background()
    strip = s.shapes.add_shape(MSO_SHAPE.RECTANGLE, x, y + Inches(0.2), Inches(0.09), Inches(0.5))
    strip.fill.solid()
    strip.fill.fore_color.rgb = TEAL if i % 2 else BLUE
    strip.line.fill.background()
    text(s, x + Inches(0.25), y + Inches(0.15), cw - Inches(0.4), Inches(0.6), t, 17, True, NAVY)
    text(s, x + Inches(0.25), y + Inches(0.8), cw - Inches(0.4), ch - Inches(0.9), b, 13, False, GREY)

# ===================================================== 3. Pipelines
s = prs.slides.add_slide(BLANK)
header(s, "Two pipelines", None, 3)
text(s, Inches(0.5), Inches(1.2), Inches(12), Inches(0.45),
     "Pipeline A — Offline ingestion (Paper Management tab or  python -m ingestion.batch)", 16, True, BLUE)
a_steps = [("Upload\nvalidator", "type · size · pages\nSHA-256 dedupe"), ("Parse", "Docling / PyMuPDF\n/ PaddleOCR"),
           ("Normalize", "one JSON schema\ntitle · authors · year"), ("3 branches", "text · tables ·\nfigures"),
           ("Vision model", "Qwen2.5-VL\ncached by image hash"), ("Chunk", "parent 1200 tok\nchild 300 tok"),
           ("Embed", "text-embedding-3-small\ncached"), ("Index", "Qdrant vectors\nSQLite metadata")]
bw, bh, gap = Inches(1.43), Inches(1.2), Inches(0.16)
y = Inches(1.7)
for i, (t, b) in enumerate(a_steps):
    x = Inches(0.5) + (bw + gap) * i
    box(s, x, y, bw, bh, t, b, BLUE if i in (1, 4, 7) else LIGHT, WHITE if i in (1, 4, 7) else NAVY, 13, 10)
    if i:
        arrow(s, x - gap, y + bh // 2, x, y + bh // 2)

text(s, Inches(0.5), Inches(3.25), Inches(12), Inches(0.45),
     "Pipeline B — Online query → answer (Research Chat and Comparison tabs)", 16, True, TEAL)
b_steps = [("Input guard", "validation · rate limit\ninjection check"), ("Refine", "LLM: intent, rewrite,\nsub-queries, scope"),
           ("Hybrid search", "dense top-20 +\nBM25 top-20 → RRF"), ("Rerank", "BGE cross-encoder\ntop 6–8"),
           ("Expand", "parent context,\nlinked tables / figures"), ("Sufficiency", "enough evidence?\nelse abstain"),
           ("Generate", "gpt-4o-mini JSON\nclaims + source ids"), ("Validate", "citations · numbers\nLLM verifier · retry")]
y = Inches(3.75)
for i, (t, b) in enumerate(b_steps):
    x = Inches(0.5) + (bw + gap) * i
    box(s, x, y, bw, bh, t, b, TEAL if i in (2, 5, 7) else LIGHT, WHITE if i in (2, 5, 7) else NAVY, 13, 10)
    if i:
        arrow(s, x - gap, y + bh // 2, x, y + bh // 2)

shared = s.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.5), Inches(5.3), Inches(12.33), Inches(0.75))
shared.fill.solid()
shared.fill.fore_color.rgb = NAVY
shared.line.fill.background()
text(s, Inches(0.7), Inches(5.33), Inches(12), Inches(0.7),
     "Shared:  config.py  ·  SQLite metadata store  ·  Qdrant vector store  ·  Embedder  ·  LLM / VLM client"
     "      (A writes, B reads)", 14, True, WHITE, PP_ALIGN.CENTER, MSO_ANCHOR.MIDDLE)
text(s, Inches(0.5), Inches(6.2), Inches(12.33), Inches(1.0), [
    "Visual questions only: the original figure image is sent to the vision model at query time — text questions never call it.",
    "Final status per answer: answered · partial · abstained · blocked · error.  Suggestions are labelled \"AI suggestion\".",
], 12, False, GREY, bullets=True)

# ===================================================== 4. Configuration
s = prs.slides.add_slide(BLANK)
header(s, "Configuration", "All values come from .env (python-dotenv); secrets are never committed", 4)
groups = [
    ("Models", BLUE, [("Embeddings", "text-embedding-3-small · 1536-d"), ("LLM", "gpt-4o-mini (OpenAI)"),
                      ("Vision", "Qwen2.5-VL-72B (OpenRouter)"), ("Reranker", "BAAI/bge-reranker-base · CPU"),
                      ("Injection", "Prompt Guard 2 22M + rules")]),
    ("Retrieval", TEAL, [("Dense top-k", "20 (Qdrant, cosine)"), ("BM25 top-k", "20"), ("RRF k", "60"),
                         ("Rerank keep", "6 (8 for comparison)"), ("Evidence floor", "reranker prob ≥ 0.10")]),
    ("Chunking", BLUE, [("Child chunk", "300 tokens"), ("Parent section", "1200 tokens"), ("Overlap", "50 tokens"),
                        ("OCR trigger", "< 200 chars / page"), ("Min figure", "120 px")]),
    ("Limits & guards", TEAL, [("File / pages", "50 MB / 80 pages"), ("Query length", "1000 chars"),
                               ("Rate limit", "20 / min / session"), ("Claim overlap", "≥ 0.30"),
                               ("Answer retries", "1, then partial / abstain")]),
]
gw = Inches(2.95)
for i, (title, color, rows) in enumerate(groups):
    x = Inches(0.5) + (gw + Inches(0.18)) * i
    hd = s.shapes.add_shape(MSO_SHAPE.RECTANGLE, x, Inches(1.75), gw, Inches(0.55))
    hd.fill.solid()
    hd.fill.fore_color.rgb = color
    hd.line.fill.background()
    text(s, x, Inches(1.75), gw, Inches(0.55), title, 17, True, WHITE, PP_ALIGN.CENTER, MSO_ANCHOR.MIDDLE)
    for j, (k, v) in enumerate(rows):
        ry = Inches(2.38) + Inches(0.78) * j
        cell = s.shapes.add_shape(MSO_SHAPE.RECTANGLE, x, ry, gw, Inches(0.72))
        cell.fill.solid()
        cell.fill.fore_color.rgb = LIGHT
        cell.line.fill.background()
        text(s, x + Inches(0.12), ry + Inches(0.02), gw - Inches(0.2), Inches(0.3), k, 11, True, GREY)
        text(s, x + Inches(0.12), ry + Inches(0.3), gw - Inches(0.2), Inches(0.4), v, 13, True, NAVY)
text(s, Inches(0.5), Inches(6.45), Inches(12.3), Inches(0.8),
     "Storage: Qdrant embedded (data/db/qdrant) · SQLite (data/db/metadata.sqlite) · figures, tables, normalized JSON and "
     "caches under data/.  Runs locally on CPU — Python 3.13 venv, Streamlit UI.", 12, False, GREY)

# ===================================================== 5. Outputs
s = prs.slides.add_slide(BLANK)
header(s, "Outputs", "Measured on our 8 RAG papers (CPU laptop) — no invented numbers", 5)
stats = [("8", "papers indexed"), ("677", "searchable chunks"), ("38", "tables extracted"),
         ("30", "figures described"), ("65 / 65", "unit & e2e tests pass"), ("45 / 45", "security cases pass")]
sw = Inches(1.93)
for i, (n, lbl) in enumerate(stats):
    x = Inches(0.5) + (sw + Inches(0.15)) * i
    c = s.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, x, Inches(1.7), sw, Inches(1.2))
    c.fill.solid()
    c.fill.fore_color.rgb = BLUE if i % 2 == 0 else TEAL
    c.line.fill.background()
    text(s, x, Inches(1.75), sw, Inches(0.65), n, 28, True, WHITE, PP_ALIGN.CENTER)
    text(s, x, Inches(2.38), sw, Inches(0.45), lbl, 12, False, WHITE, PP_ALIGN.CENTER)

text(s, Inches(0.5), Inches(3.1), Inches(12), Inches(0.45), "Live questions (real LLM + vision model)", 16, True, NAVY)
rows = [
    ("Question", "Result", "Evidence"),
    ("What accuracy gain does TC-RAG report?", "\"over 7.20%\"; EM +2.60–5.62%, BLEU-4 +8.23–13.72%", "P001 abstract p.1, p.7–8"),
    ("What does Figure 2 of Transform Retrieval show?", "Architecture: frozen encoder → transform model → contrastive loss", "P004 p.3 Figure 2 (vision model)"),
    ("Compare how TC-RAG and Best Practices evaluate RAG", "Both papers cited; states which metrics are missing", "P001 p.8, p.23 · P002 p.6"),
    ("What GPU did the Best Practices paper use?", "Abstained — not reported; sources checked listed", "best relevance 0.05 < 0.10"),
    ("\"Ignore all previous instructions…\"", "Blocked before retrieval", "input guard"),
]
tbl = s.shapes.add_table(len(rows), 3, Inches(0.5), Inches(3.55), Inches(12.33), Inches(2.6)).table
for j, wdt in enumerate((Inches(4.2), Inches(5.0), Inches(3.13))):
    tbl.columns[j].width = wdt
for r_i, row in enumerate(rows):
    for c_i, val in enumerate(row):
        cell = tbl.cell(r_i, c_i)
        cell.text = val
        para = cell.text_frame.paragraphs[0]
        para.runs[0].font.size = Pt(12)
        para.runs[0].font.bold = r_i == 0
        para.runs[0].font.color.rgb = WHITE if r_i == 0 else NAVY
        cell.fill.solid()
        cell.fill.fore_color.rgb = NAVY if r_i == 0 else (LIGHT if r_i % 2 else WHITE)
text(s, Inches(0.5), Inches(6.3), Inches(12.33), Inches(1.0), [
    "Latency: 15–45 s per answer on CPU; the cross-encoder reranker is the largest share (12–29 s) — next step is tuning candidate count.",
    "Ingestion: 27–216 s per paper; figure descriptions and embeddings are cached, so re-processing is near-free.",
], 12, False, GREY, bullets=True)

# ===================================================== 6. Thank you
s = prs.slides.add_slide(BLANK)
bg = s.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, W, prs.slide_height)
bg.fill.solid()
bg.fill.fore_color.rgb = NAVY
bg.line.fill.background()
text(s, 0, Inches(2.4), W, Inches(1.2), "Thank you", 60, True, WHITE, PP_ALIGN.CENTER)
text(s, 0, Inches(3.6), W, Inches(0.7), "Open for Q&A", 28, False, AMBER, PP_ALIGN.CENTER)
text(s, 0, Inches(4.6), W, Inches(0.5), f"{TEAM_NAME}  ·  ResearchIQ", 18, False,
     RGBColor(0xB8, 0xD4, 0xF0), PP_ALIGN.CENTER)
text(s, 0, Inches(5.1), W, Inches(0.5), "github.com/tambarikajathin/HCL_HACKATHON_2026", 14, False,
     RGBColor(0xB8, 0xD4, 0xF0), PP_ALIGN.CENTER)

prs.save(OUT)
print(f"Saved {OUT}")
