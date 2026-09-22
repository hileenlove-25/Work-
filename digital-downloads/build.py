#!/usr/bin/env python3
"""Build the DigitalByHileen hospitality guides into print-ready PDFs.

Each guide lives in content/<slug>.txt using a small line-based markup:

    key: value          front matter until a line of --- (title, subtitle, tagline, number,
                        inside = "; "-separated cover bullets, disclaimer = contents-page note)
    # Chapter           starts a new chapter on a new page (listed in the contents)
    ## Heading          section heading
    ### Heading         small heading
    - item              bullet
    [ ] item            checkbox item
    > text              tip callout (consecutive lines join)
    ! text              caution callout (consecutive lines join)
    | a | b |           table row (first row is the header)
    :: text             template line kept on its own line; consecutive lines form a boxed card
    ___ label           fill-in line for worksheets (___ alone = blank line)
    @pagebreak          force a page break
    anything else       paragraph (consecutive lines join)

Usage:  python3 build.py            builds every guide plus the bundle
"""
import re
import sys
from pathlib import Path

from pypdf import PdfReader, PdfWriter
from reportlab.lib.colors import HexColor, white
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import LETTER
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import inch
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (
    BaseDocTemplate, CondPageBreak, Frame, KeepTogether, NextPageTemplate, PageBreak,
    PageTemplate, Paragraph, Spacer, Table, TableStyle,
)
from reportlab.platypus.tableofcontents import TableOfContents

ROOT = Path(__file__).parent
CONTENT = ROOT / "content"
OUT = ROOT / "pdf"
BRAND = "DigitalByHileen"

WINE = HexColor("#5B1A2B")
GOLD = HexColor("#C9A227")
CREAM = HexColor("#FBF6EE")
INK = HexColor("#262223")
MUTED = HexColor("#6E6466")
RULE = HexColor("#E4D9CC")
SAGE = HexColor("#EEF3EC")
SAGE_EDGE = HexColor("#6F8F6A")
ROSE = HexColor("#FBEDEA")
ROSE_EDGE = HexColor("#B4533F")

FONT_DIR = ROOT / "fonts"
for name, file in [("Sans", "LiberationSans-Regular"), ("Sans-Bold", "LiberationSans-Bold"),
                   ("Sans-Italic", "LiberationSans-Italic"),
                   ("Sans-BoldItalic", "LiberationSans-BoldItalic"),
                   ("Serif", "DejaVuSerif"), ("Serif-Bold", "DejaVuSerif-Bold"),
                   ("Symbol", "DejaVuSans")]:
    pdfmetrics.registerFont(TTFont(name, FONT_DIR / f"{file}.ttf"))
pdfmetrics.registerFontFamily("Sans", normal="Sans", bold="Sans-Bold",
                              italic="Sans-Italic", boldItalic="Sans-BoldItalic")

PAGE_W, PAGE_H = LETTER
MARGIN = 0.9 * inch

S = {
    "body": ParagraphStyle("body", fontName="Sans", fontSize=10.5, leading=15.5,
                           textColor=INK, spaceAfter=8),
    "chapter_num": ParagraphStyle("chapter_num", fontName="Sans-Bold", fontSize=10,
                                  leading=14, textColor=GOLD, spaceAfter=4),
    "chapter": ParagraphStyle("chapter", fontName="Serif-Bold", fontSize=24, leading=30,
                              textColor=WINE, spaceAfter=18),
    "h2": ParagraphStyle("h2", fontName="Serif-Bold", fontSize=15, leading=20,
                         textColor=WINE, spaceBefore=12, spaceAfter=6, keepWithNext=1),
    "h3": ParagraphStyle("h3", fontName="Sans-Bold", fontSize=11, leading=15,
                         textColor=INK, spaceBefore=8, spaceAfter=4, keepWithNext=1),
    "bullet": ParagraphStyle("bullet", fontName="Sans", fontSize=10.5, leading=15,
                             textColor=INK, leftIndent=16, bulletIndent=4, spaceAfter=3),
    "check": ParagraphStyle("check", fontName="Sans", fontSize=10.5, leading=15,
                            textColor=INK, leftIndent=20, bulletIndent=2, spaceAfter=4,
                            bulletFontName="Symbol"),
    "callout": ParagraphStyle("callout", fontName="Sans", fontSize=10, leading=14.5,
                              textColor=INK),
    "cell": ParagraphStyle("cell", fontName="Sans", fontSize=9.2, leading=12.5,
                           textColor=INK),
    "cell_head": ParagraphStyle("cell_head", fontName="Sans-Bold", fontSize=9.2,
                                leading=12.5, textColor=white),
    "fill_label": ParagraphStyle("fill_label", fontName="Sans-Bold", fontSize=9.5,
                                 leading=12, textColor=MUTED),
    "toc_title": ParagraphStyle("toc_title", fontName="Serif-Bold", fontSize=24,
                                leading=30, textColor=WINE, spaceAfter=18),
    "toc1": ParagraphStyle("toc1", fontName="Sans", fontSize=11.5, leading=22,
                           textColor=INK),
    "small": ParagraphStyle("small", fontName="Sans", fontSize=8.5, leading=12,
                            textColor=MUTED, alignment=TA_CENTER),
}


def inline(text):
    """Escape XML and apply **bold** / *italic* markup."""
    text = text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    text = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", text)
    text = re.sub(r"(?<!\*)\*(?!\s)(.+?)(?<!\s)\*(?!\*)", r"<i>\1</i>", text)
    return text


def parse(path):
    meta, body = {}, []
    lines = path.read_text(encoding="utf-8").splitlines()
    i = 0
    while i < len(lines) and lines[i].strip() != "---":
        if ":" in lines[i]:
            k, v = lines[i].split(":", 1)
            meta[k.strip()] = v.strip()
        i += 1
    return meta, lines[i + 1:]


def callout(text, fill, edge, label):
    p = Paragraph(f"<b>{label}</b>&nbsp;&nbsp;{inline(text)}", S["callout"])
    t = Table([[p]], colWidths=[PAGE_W - 2 * MARGIN])
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), fill),
        ("LINEBEFORE", (0, 0), (0, -1), 3, edge),
        ("LEFTPADDING", (0, 0), (-1, -1), 12), ("RIGHTPADDING", (0, 0), (-1, -1), 12),
        ("TOPPADDING", (0, 0), (-1, -1), 9), ("BOTTOMPADDING", (0, 0), (-1, -1), 9),
    ]))
    return [Spacer(1, 4), t, Spacer(1, 10)]


def template_card(lines):
    cells = [[Paragraph(inline(l), S["callout"]) if l else Spacer(1, 4)] for l in lines]
    t = Table(cells, colWidths=[PAGE_W - 2 * MARGIN])
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), CREAM),
        ("BOX", (0, 0), (-1, -1), 0.8, RULE),
        ("LINEABOVE", (0, 0), (-1, 0), 3, GOLD),
        ("LEFTPADDING", (0, 0), (-1, -1), 14), ("RIGHTPADDING", (0, 0), (-1, -1), 14),
        ("TOPPADDING", (0, 0), (-1, -1), 2), ("BOTTOMPADDING", (0, 0), (-1, -1), 2),
        ("TOPPADDING", (0, 0), (-1, 0), 12), ("BOTTOMPADDING", (0, -1), (-1, -1), 12),
    ]))
    return [KeepTogether([Spacer(1, 4), t]), Spacer(1, 12)]


def table(rows):
    width = PAGE_W - 2 * MARGIN
    ncol = max(len(r) for r in rows)
    rows = [r + [""] * (ncol - len(r)) for r in rows]
    data = [[Paragraph(inline(c), S["cell_head"]) for c in rows[0]]]
    data += [[Paragraph(inline(c), S["cell"]) for c in r] for r in rows[1:]]
    style = [
        ("BACKGROUND", (0, 0), (-1, 0), WINE),
        ("GRID", (0, 0), (-1, -1), 0.5, RULE),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 6), ("RIGHTPADDING", (0, 0), (-1, -1), 6),
        ("TOPPADDING", (0, 0), (-1, -1), 5), ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
    ]
    for r in range(2, len(data), 2):
        style.append(("BACKGROUND", (0, r), (-1, r), CREAM))
    # Empty body rows are worksheet rows: give them room to write in.
    heights = [None] + [28 if not any(c.strip() for c in row) else None for row in rows[1:]]
    t = Table(data, colWidths=[width / ncol] * ncol, rowHeights=heights, repeatRows=1)
    t.setStyle(TableStyle(style))
    return [t, Spacer(1, 12)]


def fill_line(label):
    width = PAGE_W - 2 * MARGIN
    cells = [[Paragraph(inline(label), S["fill_label"]) if label else ""]]
    t = Table(cells, colWidths=[width], rowHeights=[26])
    t.setStyle(TableStyle([
        ("LINEBELOW", (0, 0), (-1, -1), 0.7, MUTED),
        ("VALIGN", (0, 0), (-1, -1), "BOTTOM"),
        ("LEFTPADDING", (0, 0), (-1, -1), 0), ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
    ]))
    return [t]


class GuideDoc(BaseDocTemplate):
    def __init__(self, filename, meta):
        super().__init__(filename, pagesize=LETTER, leftMargin=MARGIN, rightMargin=MARGIN,
                         topMargin=MARGIN, bottomMargin=MARGIN,
                         title=meta["title"], author=BRAND, subject=meta.get("subtitle", ""),
                         creator=BRAND)
        self.meta = meta
        frame = Frame(MARGIN, MARGIN, PAGE_W - 2 * MARGIN, PAGE_H - 2 * MARGIN, id="f")
        self.addPageTemplates([
            PageTemplate("cover", [frame], onPage=self.draw_cover),
            PageTemplate("body", [frame], onPage=self.draw_chrome),
        ])

    def afterFlowable(self, flowable):
        if getattr(flowable, "toc_entry", None):
            self.notify("TOCEntry", (0, flowable.toc_entry, self.page))

    def draw_cover(self, c, doc):
        m = self.meta
        c.saveState()
        c.setFillColor(WINE)
        c.rect(0, 0, PAGE_W, PAGE_H, stroke=0, fill=1)
        c.setFillColor(GOLD)
        c.rect(MARGIN, PAGE_H - 1.6 * inch, 1.1 * inch, 4, stroke=0, fill=1)
        c.setFont("Sans-Bold", 10)
        c.drawString(MARGIN, PAGE_H - 1.3 * inch,
                     f"THE FRONT-OF-HOUSE SERIES  ·  GUIDE {m.get('number', '')}".upper())
        # Title, wrapped to the page width.
        style = ParagraphStyle("ct", fontName="Serif-Bold", fontSize=38, leading=44,
                               textColor=white)
        p = Paragraph(inline(m["title"]), style)
        w, h = p.wrap(PAGE_W - 2 * MARGIN, PAGE_H)
        top = PAGE_H - 2.2 * inch
        p.drawOn(c, MARGIN, top - h)
        sub_style = ParagraphStyle("cs", fontName="Serif", fontSize=15, leading=21,
                                   textColor=HexColor("#F1E3C4"))
        sp = Paragraph(inline(m.get("subtitle", "")), sub_style)
        _, sh = sp.wrap(PAGE_W - 2 * MARGIN - 0.5 * inch, PAGE_H)
        sp.drawOn(c, MARGIN, top - h - 24 - sh)
        # Big watermark number and "inside" list
        c.setFillColor(HexColor("#6A2436"))
        c.setFont("Serif-Bold", 150)
        c.drawRightString(PAGE_W - MARGIN + 10, 1.95 * inch, m.get("number", ""))
        items = [i.strip() for i in m.get("inside", "").split(";") if i.strip()]
        if items:
            y = top - h - 24 - sh - 0.75 * inch
            c.setFillColor(GOLD)
            c.setFont("Sans-Bold", 10)
            c.drawString(MARGIN, y, "INSIDE THIS GUIDE")
            y -= 8
            item_style = ParagraphStyle("ci", fontName="Sans", fontSize=11.5, leading=15,
                                        textColor=white, leftIndent=14, bulletIndent=0,
                                        bulletFontName="Symbol", bulletColor=GOLD)
            for item in items:
                ip = Paragraph(inline(item), item_style, bulletText="✓")
                _, ih = ip.wrap(PAGE_W - 2 * MARGIN - 1.8 * inch, PAGE_H)
                y -= ih + 8
                ip.drawOn(c, MARGIN, y)
        # Bottom band
        c.setFillColor(HexColor("#4A1422"))
        c.rect(0, 0, PAGE_W, 1.7 * inch, stroke=0, fill=1)
        c.setFillColor(GOLD)
        c.rect(0, 1.7 * inch, PAGE_W, 2, stroke=0, fill=1)
        c.setFillColor(white)
        c.setFont("Sans", 11)
        tag = m.get("tagline", "")
        c.drawString(MARGIN, 1.05 * inch, tag)
        c.setFont("Sans-Bold", 12)
        c.setFillColor(GOLD)
        c.drawString(MARGIN, 0.7 * inch, BRAND)
        c.setFont("Sans", 9)
        c.setFillColor(HexColor("#D9C7C9"))
        c.drawRightString(PAGE_W - MARGIN, 0.7 * inch, "Printable · Fillable by hand · Personal use")
        c.restoreState()

    def draw_chrome(self, c, doc):
        c.saveState()
        c.setStrokeColor(RULE)
        c.setLineWidth(0.6)
        c.line(MARGIN, PAGE_H - 0.6 * inch, PAGE_W - MARGIN, PAGE_H - 0.6 * inch)
        c.setFont("Sans", 8)
        c.setFillColor(MUTED)
        c.drawString(MARGIN, PAGE_H - 0.5 * inch, self.meta["title"])
        c.drawRightString(PAGE_W - MARGIN, PAGE_H - 0.5 * inch, BRAND)
        c.line(MARGIN, 0.6 * inch, PAGE_W - MARGIN, 0.6 * inch)
        c.drawCentredString(PAGE_W / 2, 0.42 * inch, str(doc.page))
        c.restoreState()


def build_story(meta, lines):
    story = [NextPageTemplate("body"), PageBreak()]

    toc = TableOfContents()
    toc.levelStyles = [S["toc1"]]
    toc.dotsMinLevel = 0
    story += [Paragraph("Contents", S["toc_title"]), toc]
    if meta.get("disclaimer"):
        story += [Spacer(1, 18)] + callout(meta["disclaimer"], ROSE, ROSE_EDGE, "Please note:")

    chapter_no = 0
    para, kind = [], None  # pending multi-line paragraph/callout
    table_rows = []

    def flush():
        nonlocal para, kind, table_rows
        out = []
        if para:
            text = " ".join(para)
            if kind == "tip":
                out += callout(text, SAGE, SAGE_EDGE, "Try this:")
            elif kind == "warn":
                out += callout(text, ROSE, ROSE_EDGE, "Important:")
            elif kind == "card":
                out += template_card(para)
            else:
                out.append(Paragraph(inline(text), S["body"]))
        if table_rows:
            out += table(table_rows)
        para, kind, table_rows = [], None, []
        return out

    for raw in lines:
        line = raw.rstrip()
        s = line.strip()
        if s.startswith("|"):
            if para:
                story += flush()
            table_rows.append([c.strip() for c in s.strip("|").split("|")])
            continue
        if table_rows:
            story += flush()
        if s.startswith("::"):
            if kind != "card":
                story += flush()
                kind = "card"
            para.append(s[2:].strip())
            continue
        if kind == "card":
            story += flush()
        if not s:
            story += flush()
            continue
        if s.startswith("> ") or s.startswith("! "):
            k = "tip" if s[0] == ">" else "warn"
            if kind != k:
                story += flush()
                kind = k
            para.append(s[2:])
            continue
        if kind in ("tip", "warn"):
            story += flush()

        if s.startswith("# "):
            story += flush()
            chapter_no += 1
            title = s[2:]
            while story and isinstance(story[-1], Spacer):
                story.pop()  # a trailing spacer can spill onto a blank page
            story.append(PageBreak())
            story.append(Paragraph(f"CHAPTER {chapter_no}" if not title.lower().startswith(
                ("worksheet", "bonus", "resources", "your ")) else "TOOLKIT", S["chapter_num"]))
            h = Paragraph(inline(title), S["chapter"])
            h.toc_entry = title
            story.append(h)
        elif s.startswith("## "):
            story += flush()
            story.append(CondPageBreak(1.3 * inch))
            story.append(Paragraph(inline(s[3:]), S["h2"]))
        elif s.startswith("### "):
            story += flush()
            story.append(CondPageBreak(0.9 * inch))
            story.append(Paragraph(inline(s[4:]), S["h3"]))
        elif s.startswith("- "):
            story += flush()
            story.append(Paragraph(inline(s[2:]), S["bullet"], bulletText="•"))
        elif re.match(r"\d+\. ", s):
            story += flush()
            num, rest = s.split(" ", 1)
            story.append(Paragraph(inline(rest), S["bullet"], bulletText=num))
        elif s.startswith("[ ] "):
            story += flush()
            story.append(Paragraph(inline(s[4:]), S["check"], bulletText="☐"))
        elif s.startswith("___"):
            story += flush()
            story += fill_line(s[3:].strip())
        elif s == "@pagebreak":
            story += flush()
            story.append(PageBreak())
        else:
            para.append(s)
    story += flush()
    while isinstance(story[-1], Spacer):
        story.pop()

    story += [PageBreak(), Spacer(1, 2.5 * inch),
              Paragraph(f"Thank you for supporting {BRAND}.", ParagraphStyle(
                  "ty", parent=S["h2"], alignment=TA_CENTER)),
              Spacer(1, 8),
              Paragraph("You deserve a workplace that respects your time, your effort, and your "
                        "dignity. Keep this guide close, share what helps, and look out for the "
                        "people working beside you.", ParagraphStyle(
                            "tyb", parent=S["body"], alignment=TA_CENTER)),
              Spacer(1, 30),
              Paragraph(f"© {BRAND}. For personal use only. Please do not resell or redistribute. "
                        "This guide is educational and is not legal, financial, medical, or "
                        "mental-health advice.", S["small"])]
    return story


def build(path):
    meta, lines = parse(path)
    out = OUT / f"{path.stem}.pdf"
    doc = GuideDoc(str(out), meta)
    doc.multiBuild(build_story(meta, lines))
    pages = len(PdfReader(str(out)).pages)
    print(f"  {out.name}: {pages} pages")
    return out, meta


def bundle_cover(built, path):
    from reportlab.pdfgen.canvas import Canvas
    c = Canvas(str(path), pagesize=LETTER)
    c.setFillColor(WINE)
    c.rect(0, 0, PAGE_W, PAGE_H, stroke=0, fill=1)
    c.setFillColor(GOLD)
    c.rect(MARGIN, PAGE_H - 1.6 * inch, 1.1 * inch, 4, stroke=0, fill=1)
    c.setFont("Sans-Bold", 10)
    c.drawString(MARGIN, PAGE_H - 1.3 * inch, "THE FRONT-OF-HOUSE SERIES  ·  COMPLETE BUNDLE")
    title = Paragraph("The Restaurant Worker's Survival Bundle", ParagraphStyle(
        "bt", fontName="Serif-Bold", fontSize=38, leading=44, textColor=white))
    _, h = title.wrap(PAGE_W - 2 * MARGIN, PAGE_H)
    top = PAGE_H - 2.2 * inch
    title.drawOn(c, MARGIN, top - h)
    sub = Paragraph(f"{len(built)} guides to earn more, protect your peace, and stand up for "
                    "yourself at work", ParagraphStyle(
                        "bs", fontName="Serif", fontSize=15, leading=21,
                        textColor=HexColor("#F1E3C4")))
    _, sh = sub.wrap(PAGE_W - 2 * MARGIN, PAGE_H)
    sub.drawOn(c, MARGIN, top - h - 24 - sh)
    y = top - h - 24 - sh - 0.6 * inch
    for _, meta in built:
        c.setFillColor(GOLD)
        c.setFont("Serif-Bold", 20)
        c.drawString(MARGIN, y - 4, meta["number"])
        p = Paragraph(inline(meta["title"]), ParagraphStyle(
            "bi", fontName="Sans-Bold", fontSize=12.5, leading=16, textColor=white))
        _, ph = p.wrap(PAGE_W - 2 * MARGIN - 0.6 * inch, PAGE_H)
        p.drawOn(c, MARGIN + 0.6 * inch, y - ph + 12)
        y -= max(ph, 16) + 16
    c.setFillColor(HexColor("#4A1422"))
    c.rect(0, 0, PAGE_W, 1.2 * inch, stroke=0, fill=1)
    c.setFillColor(GOLD)
    c.rect(0, 1.2 * inch, PAGE_W, 2, stroke=0, fill=1)
    c.setFont("Sans-Bold", 12)
    c.drawString(MARGIN, 0.55 * inch, BRAND)
    c.setFont("Sans", 9)
    c.setFillColor(HexColor("#D9C7C9"))
    c.drawRightString(PAGE_W - MARGIN, 0.55 * inch, "Printable · Fillable by hand · Personal use")
    c.save()


def build_bundle(built):
    writer = PdfWriter()
    cover = OUT / "_bundle-cover.pdf"
    bundle_cover(built, cover)
    writer.append(str(cover))
    cover.unlink()
    for path, meta in built:
        start = len(writer.pages)
        writer.append(str(path))
        writer.add_outline_item(meta["title"], start)
    writer.add_metadata({"/Title": "The Front-of-House Series: Complete Bundle",
                         "/Author": BRAND})
    out = OUT / "00-front-of-house-complete-bundle.pdf"
    with open(out, "wb") as f:
        writer.write(f)
    print(f"  {out.name}: {len(writer.pages)} pages")


if __name__ == "__main__":
    OUT.mkdir(exist_ok=True)
    files = sorted(CONTENT.glob("*.txt"))
    if len(sys.argv) > 1:
        files = [f for f in files if any(a in f.name for a in sys.argv[1:])]
    built = [build(f) for f in files]
    if len(sys.argv) == 1:
        build_bundle(built)
