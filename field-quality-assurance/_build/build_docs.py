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


MIN = {
 "title": "Minutes: BGC and UNIKIN meetings on data collection and quality assurance",
 "sub": "Combined record of the meetings of 13 and 16 November 2026",
 "meta": "Prepared by UNIKIN from the meeting transcripts. The transcript of 13 November is incomplete: about 28 minutes are missing (from 1 min 13 s to 29 min 5 s), so most of the BGC map walkthrough and any questions asked during it are not recorded here.",
 "att": [
  ("13 November 2026", "Dale Rhoda and Caitlin Clary (BGC); Trésor Zola Matuvanga, Bernard Osang'ir, Germaine Tutonda and John Mbuyi (UNIKIN)."),
  ("16 November 2026 (55 minutes)", "Dale Rhoda (BGC); Bernard Osang'ir, Trésor Zola Matuvanga, Tesky Koba, Fabien Vulu and Germaine Tutonda (UNIKIN). Cait was not present; Dale will share the recording with her."),
 ],
 "purpose": "Review of segment and PSU coverage in the data already collected, UNIKIN's quality monitoring, card date checks, and what to change before the next provinces, including Sankuru.",
 "items": [
  ("1. Segment order and coverage seen on BGC maps (13 Nov)", [
   "Dale showed maps of interview locations against the PSU segments. In the PSU shown, the team went from Segment 1 to 2 to 3 as required, but the eastern side of Segment 3 was not covered, Segments 4 to 10 were skipped, Segments 11 and perhaps 12 should have had some work, and the team came into Segment 13 at the end. Dale rated adherence in that PSU as \"mixed\".",
   "Cait confirmed that the maps covered a selection of PSUs, not all of them.",
   "Trésor asked why, in Segment 2, all visited households were on one side of the road. Bernard said the disposition form recorded Segments 1 and 2 as fully covered but outside the prescribed order. Dale said the coding did not look correct, since no work appears east of the road; it would only be correct if that area were abandoned or a market. Bernard agreed.",
   "Dale suggested that teams submit a form even from areas they find abandoned or without households, so every part of a segment that was checked leaves a record.",
   "Dale concluded that UNIKIN's and BGC's tools together give a good picture of what happened in the field. Bernard said UNIKIN gives feedback to teams every day and that BGC's figures will be useful for the next round.",
  ]),
  ("2. Forms left open during the day (16 Nov)", [
   "Dale: keeping a form open after the first knock, so the team can come back later for a full interview, is acceptable, and he is not asking for field practice to change. But end times then no longer show interview length.",
   "Bernard: this matters because GiveWell (Vicky) asked for the average interview duration. A form open 8 hours for a 4-minute interview gives the wrong picture. UNIKIN will strengthen the practice by recording real interview duration.",
   "Trésor asked whether forms were left open all day in Kongo Central. Dale confirmed that end times were close to the end of each working day.",
  ]),
  ("3. UNIKIN quality monitoring tool (16 Nov)", [
   "Tesky presented the tool in French (this part of the transcript is mostly unreadable). What can be made out: daily submission counts, about 10 automatic alerts, maps of points by health zone, checks of GPS precision and PSU boundaries, and same-day feedback to supervisors and team chiefs by WhatsApp.",
   "Dale said the work was impressive and well ahead of other partners, and asked for the slides to make an English version for Cait.",
  ]),
  ("4. Card dates and corrections (16 Nov)", [
   "Dale: when Cait's HBR tool finds dates to change, BGC changes them on its side, so VCQI results can be compared with original and corrected dates. Both versions should be kept to show GiveWell the value of card checks; a corrected copy can be shared with UNIKIN.",
   "Bernard: UNIKIN's tool only flags inconsistent dates for the enumerator to check against the card; it changes nothing.",
   "Dale suggested extra CAPI checks: doses in a series out of order or with the same date (often a transcription error from the wrong row of the card), and doses due at the same age (6, 10 and 14 weeks; 9 months) with different or missing dates. To avoid alert fatigue, one summary list at the end of the card module may work better than many pop-ups. Supervisors could see each enumerator's share of cards with problems.",
   "Bernard asked whether enumerators should be able to record \"evidence of a dose but no readable date\". Dale: yes, it is common practice (full date, partial or illegible date, or a tick). Track how often each enumerator uses it; a full readable date is much more valuable.",
  ]),
  ("5. Interviews outside PSU boundaries (16 Nov)", [
   "Dale asked whether points outside PSU boundaries were removed. Bernard: no, nothing was removed. The CAPI accepts GPS readings within 15 m only, so some may be GPS error and some enumerators may have gone outside. Dale said that was fine.",
  ]),
  ("6. Whole-PSU canvassing and segment order (16 Nov)", [
   "Trésor explained that in Kongo Central teams were told to canvass whole PSUs in sparsely populated areas to reach the target, which may explain segments not visited in order.",
   "Dale: he approved this by email. If the whole PSU is canvassed, segment order does not matter; order matters only when part of a PSU is worked. He asked for a list of PSUs where this applied, or at least the period, and whether teams returned to the protocol once PSUs became larger.",
   "Bernard: a disposition code has been added for \"whole PSU canvassed without following the order\".",
  ]),
  ("7. Kongo Central analysis set (16 Nov)", [
   "Dale will send a note on which children belong in the analysis: his program finds about 2,545 children against UNIKIN's 2,571. The difference comes from possible duplicate children and children whose caregiver did not consent but still answered. Both teams will agree who is in and who is out.",
  ]),
  ("8. Maniema preliminary report and other updates (16 Nov)", [
   "Bernard asked whether to keep producing UNIKIN's own results alongside BGC's while populating the Maniema preliminary report. Dale: up to UNIKIN; an independent comparison is healthy and can catch errors.",
   "Bernard: the Sankuru shapefile feedback has been shared; card date checks for Maniema continue; the Sankuru and Sud-Ubangi questionnaires were restructured with the same codes and are in the GiveWell folder. Dale agreed to review them with the inception reports and protocols.",
   "Bernard: GiveWell asked which inaccessible areas were forest, insecure and so on. UNIKIN will add detailed reason codes under one overall \"inaccessible\" category. Dale agreed.",
  ]),
 ],
 "dec_h": "Decisions and agreements",
 "dec": [
  "Forms may stay open to return to a household; UNIKIN will record real interview duration.",
  "BGC applies card date corrections on its side; original and corrected data are both kept.",
  "Records outside PSU boundaries are kept and explained, not deleted.",
  "Whole-PSU canvassing is acceptable when the entire PSU is covered; a list of such PSUs or periods goes to BGC.",
  "Partial or illegible dates and tick-only evidence are allowed, with use tracked by enumerator.",
  "Detailed inaccessible reason codes will be added under the overall inaccessible code.",
 ],
 "act_h": "Action points",
 "act_cols": ["#", "Action", "Owner", "Source", "Status (18 Nov)"],
 "act": [
  ("1", "Review the Segment 1 and 2 disposition codes in the PSU shown on 13 Nov and correct them if the area east of the road was not covered", "UNIKIN (Bernard, Germaine)", "13 Nov", "Open"),
  ("2", "Add to the procedure a record for abandoned or empty areas", "UNIKIN", "13 Nov", "In the Sankuru training material"),
  ("3", "Use BGC segment maps alongside UNIKIN's monitoring tool in the next round", "UNIKIN, BGC", "13 Nov", "Planned for Sankuru"),
  ("4", "Send the monitoring tool slides to Dale", "Tesky", "16 Nov", "Open"),
  ("5", "Make an English version of the slides and share them and the recording with Cait", "Dale", "16 Nov", "Open"),
  ("6", "Send the note on the Kongo Central analysis set (2,571 vs about 2,545)", "Dale", "16 Nov", "Open"),
  ("7", "List the PSUs, or the period, where whole PSUs were canvassed regardless of segment order", "UNIKIN", "16 Nov", "Open"),
  ("8", "Consider extra CAPI date checks (order, same dates, same-age doses) and an end-of-card summary", "UNIKIN (data management)", "16 Nov", "Not yet in Sankuru CAPI 004"),
  ("9", "Record real interview duration while forms stay open", "UNIKIN (data management)", "16 Nov", "Open"),
  ("10", "Add detailed codes for inaccessible segments and share them with Dale", "Bernard", "16 Nov", "Open"),
  ("11", "Run the independent comparison for the Maniema preliminary report", "Bernard", "16 Nov", "Open"),
  ("12", "Review the Sankuru and Sud-Ubangi questionnaires, inception reports and protocols", "Dale", "16 Nov", "Open"),
 ],
 "foot": "Minutes prepared by UNIKIN, 18 November 2026. Internal: not for circulation outside UNIKIN and BGC without agreement.",
}


def minutes(root, logo):
    M = MIN; doc = Document(); base(doc)
    header_block(doc, logo, M["title"], M["sub"], M["meta"])
    doc.add_heading("Attendees", 1)
    for a, b in M["att"]:
        p = doc.add_paragraph(style="List Bullet"); r = p.add_run(a + ": "); r.bold = True; p.add_run(b)
    doc.add_heading("Purpose", 1); doc.add_paragraph(M["purpose"])
    doc.add_heading("Discussion", 1)
    for h, items in M["items"]:
        doc.add_heading(h, 2); bullets(doc, items)
    doc.add_heading(M["dec_h"], 1); bullets(doc, M["dec"])
    doc.add_heading(M["act_h"], 1)
    table(doc, M["act_cols"], M["act"], [0.8, 8, 3.2, 1.6, 3.4])
    footer(doc, M["foot"])
    out = os.path.join(root, "02_Minutes_BGC_meetings", "Minutes_BGC_UNIKIN_13_and_16_Nov_2026.docx"); doc.save(out); print("wrote", out)


if __name__ == "__main__":
    root, logo = sys.argv[1], sys.argv[2]
    guide(guide_text.EN, "en", root, logo)
    guide(guide_text.FR, "fr", root, logo)
    minutes(root, logo)
