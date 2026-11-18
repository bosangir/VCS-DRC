# -*- coding: utf-8 -*-
"""Build the key-messages guide (FR, EN) and the combined BGC meeting minutes (EN).
Usage: python build_docs.py <training_root> <logo.png>"""
import sys, os
from docx import Document
from docx.shared import Pt, Cm, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml.ns import qn
from docx.oxml import OxmlElement
sys.path.insert(0, os.path.dirname(__file__))
import guide_text

NAVY = RGBColor(0x12, 0x30, 0x5A); GREY = RGBColor(0x5B, 0x68, 0x76); RED = RGBColor(0xC8, 0x3B, 0x3B)


def base(doc):
    st = doc.styles["Normal"]; st.font.name = "Calibri"; st.font.size = Pt(10.5)
    st.element.rPr.rFonts.set(qn("w:eastAsia"), "Calibri")
    st.paragraph_format.space_after = Pt(4)
    for name, size in [("Title", 22), ("Heading 1", 15), ("Heading 2", 12.5), ("Heading 3", 11)]:
        s = doc.styles[name]; s.font.name = "Calibri"; s.font.size = Pt(size); s.font.color.rgb = NAVY; s.font.bold = True
        s.element.rPr.rFonts.set(qn("w:asciiTheme"), "") if False else None
    for sec in doc.sections:
        sec.top_margin = Cm(1.8); sec.bottom_margin = Cm(1.8); sec.left_margin = Cm(2); sec.right_margin = Cm(2)


def shade(cell, hexcol):
    tcPr = cell._tc.get_or_add_tcPr(); sh = OxmlElement("w:shd")
    sh.set(qn("w:val"), "clear"); sh.set(qn("w:color"), "auto"); sh.set(qn("w:fill"), hexcol); tcPr.append(sh)


def table(doc, cols, rows, widths=None, head="12305A"):
    t = doc.add_table(rows=1, cols=len(cols)); t.style = "Table Grid"; t.alignment = WD_TABLE_ALIGNMENT.CENTER
    for i, c in enumerate(cols):
        cell = t.rows[0].cells[i]; cell.text = ""; r = cell.paragraphs[0].add_run(c); r.bold = True; r.font.color.rgb = RGBColor(255, 255, 255); r.font.size = Pt(10)
        shade(cell, head)
    for k, row in enumerate(rows):
        cells = t.add_row().cells
        for i, v in enumerate(row):
            cells[i].text = ""; p = cells[i].paragraphs[0]; r = p.add_run(str(v)); r.font.size = Pt(9.5)
            if i == 0: r.bold = True
            if k % 2: shade(cells[i], "F2F5F9")
    if widths:
        for row in t.rows:
            for i, w in enumerate(widths): row.cells[i].width = Cm(w)
    doc.add_paragraph()
    return t


def bullets(doc, items, style="List Bullet"):
    for it in items:
        p = doc.add_paragraph(style=style)
        if isinstance(it, tuple):
            r = p.add_run(it[0] + " "); r.bold = True; p.add_run(it[1])
        else:
            p.add_run(it)


def header_block(doc, logo, title, subtitle, meta):
    if logo and os.path.exists(logo):
        doc.add_picture(logo, width=Cm(8)); doc.paragraphs[-1].alignment = WD_ALIGN_PARAGRAPH.LEFT
    p = doc.add_paragraph(style="Title"); p.add_run(title)
    p = doc.add_paragraph(); r = p.add_run(subtitle); r.font.size = Pt(12); r.font.color.rgb = NAVY
    p = doc.add_paragraph(); r = p.add_run(meta); r.italic = True; r.font.size = Pt(9.5); r.font.color.rgb = GREY


def footer(doc, text):
    for sec in doc.sections:
        p = sec.footer.paragraphs[0]; p.text = ""; r = p.add_run(text); r.font.size = Pt(8); r.font.color.rgb = GREY


def guide(L, lang, root, logo):
    doc = Document(); base(doc)
    header_block(doc, logo, L["title"], L["subtitle"], L["meta"])
    doc.add_heading(L["why_h"], 1); bullets(doc, L["why"])
    doc.add_heading(L["five_h"], 1)
    for i, (a, b) in enumerate(L["five"], 1):
        p = doc.add_paragraph(style="List Number"); r = p.add_run(a + " "); r.bold = True; p.add_run(b)
    doc.add_heading(L["roles_h"], 1)
    for role, blocks in L["roles"]:
        doc.add_heading(role, 2)
        for h, items in blocks:
            doc.add_heading(h, 3); bullets(doc, items)
    doc.add_heading(L["seg_h"], 1)
    doc.add_paragraph(L["seg_intro"])
    fig = os.path.join(root, "04_Segment_protocol_demo", f"map_correct_{lang}.png")
    if os.path.exists(fig):
        doc.add_picture(fig, width=Cm(17)); doc.paragraphs[-1].alignment = WD_ALIGN_PARAGRAPH.CENTER
        p = doc.add_paragraph(); r = p.add_run(L["seg_cap"]); r.italic = True; r.font.size = Pt(9); r.font.color.rgb = GREY
    doc.add_heading(L["codes_h"], 2)
    table(doc, L["codes_cols"], L["codes"], [1.4, 7.6, 8])
    p = doc.add_paragraph(); r = p.add_run(L["codes_note"]); r.bold = True
    doc.add_heading(L["alerts_h"], 1)
    table(doc, L["alerts_cols"], L["alerts"], [4, 6, 7])
    doc.add_heading(L["bgc_h"], 1)
    table(doc, L["bgc_cols"], L["bgc"], [6, 7.5, 3.5])
    doc.add_heading(L["open_h"], 1)
    for it in L["open"]:
        p = doc.add_paragraph(style="List Bullet"); a, b = it.split(". ", 1); r = p.add_run(a + ". "); r.bold = True; r.font.color.rgb = RED; p.add_run(b)
    doc.add_heading(L["card_h"], 1)
    p = doc.add_paragraph(); r = p.add_run(L["card_intro"]); r.italic = True
    for it in L["card"]:
        p = doc.add_paragraph(); p.paragraph_format.left_indent = Cm(0.5); r = p.add_run("☐  "); r.font.size = Pt(13); p.add_run(it)
    footer(doc, L["foot"])
    name = {"en": "Key_messages_quality_data_by_role_EN.docx", "fr": "Messages_cles_qualite_donnees_par_role_FR.docx"}[lang]
    out = os.path.join(root, "01_Key_messages_by_role", name); doc.save(out); print("wrote", out)


if __name__ == "__main__":
    root, logo = sys.argv[1], sys.argv[2]
    guide(guide_text.EN, "en", root, logo)
    guide(guide_text.FR, "fr", root, logo)
    try:  # minutes_text.py is internal and is never copied to the public repository
        from minutes_text import minutes
        minutes(root, logo)
    except ImportError:
        print("minutes_text.py not found: minutes not built")
