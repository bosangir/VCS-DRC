# -*- coding: utf-8 -*-
"""Day 2 deck: Canvassing the PSU (compact segment protocol), in the style of the Day 1 decks.
Usage: python _build/build_canvassing_pptx.py <training_folder> <template.pptx> <out.pptx>
Scenario slides embed the English MP4s from 07_Videos (if present) with a still of the final state as poster."""
import copy
import os
import pathlib
import subprocess
import sys
import tempfile

from pptx import Presentation
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE, MSO_CONNECTOR
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.oxml.ns import qn
from pptx.util import Inches, Pt

ROOT, TEMPLATE, OUT = sys.argv[1:4]
FONT = 'Century Gothic'
BLUE, GREY, DARK, INK = RGBColor(0x02, 0x88, 0xD1), RGBColor(0x5E, 0x6F, 0x7C), RGBColor(0x01, 0x57, 0x9B), RGBColor(0, 0, 0)
GREEN, RED, AMBER = RGBColor(0x2E, 0x7D, 0x32), RGBColor(0xC6, 0x28, 0x28), RGBColor(0xB2, 0x6A, 0x00)
CARD, OKBG, BADBG, AMBG = RGBColor(0xF2, 0xF4, 0xF6), RGBColor(0xE8, 0xF5, 0xE9), RGBColor(0xFD, 0xEC, 0xEC), RGBColor(0xFF, 0xF4, 0xE0)
FOOT = 'UNIKIN  |  DRC Vaccination Coverage Survey  |  Sankuru Province'
EDGE = r'C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe'
DEMO = pathlib.Path(ROOT, '04_Segment_protocol_demo', 'segment_protocol_demo.html').resolve().as_uri()
VID = os.path.join(ROOT, '07_Videos')
STILL = os.path.abspath(os.path.join(ROOT, '07_Videos', 'stills'))
os.makedirs(STILL, exist_ok=True)

prs = Presentation(TEMPLATE)
ids = prs.slides._sldIdLst
for sid in list(ids)[1:]:          # keep the title slide (team names), drop the rest
    prs.part.drop_rel(sid.get(qn('r:id')))
    ids.remove(sid)
LAYOUT = prs.slides[0].slide_layout


def tb(slide, x, y, w, h, text='', size=20, bold=False, color=INK, align=None, anchor=None):
    box = slide.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h))
    tf = box.text_frame
    tf.word_wrap = True
    if anchor:
        tf.vertical_anchor = anchor
    lines = text if isinstance(text, list) else [text]
    for i, ln in enumerate(lines):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        if align:
            p.alignment = align
        r = p.add_run()
        r.text = ln
        r.font.name, r.font.size, r.font.bold, r.font.color.rgb = FONT, Pt(size), bold, color
    return box


def bullets(slide, x, y, w, h, items, size=20, color=INK, space=8):
    box = slide.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h))
    tf = box.text_frame
    tf.word_wrap = True
    for i, it in enumerate(items):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        pPr = p._p.get_or_add_pPr()
        pPr.set('marL', str(Inches(0.32)))
        pPr.set('indent', str(-Inches(0.26)))
        bu = pPr.makeelement(qn('a:buChar'), {'char': '•'})
        pPr.append(bu)
        p.space_after = Pt(space)
        r = p.add_run()
        r.text = it
        r.font.name, r.font.size, r.font.color.rgb = FONT, Pt(size), color
    return box


def rect(slide, x, y, w, h, fill, line=None):
    s = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(x), Inches(y), Inches(w), Inches(h))
    s.fill.solid()
    s.fill.fore_color.rgb = fill
    if line:
        s.line.color.rgb = line
    else:
        s.line.fill.background()
    s.shadow.inherit = False
    return s


def card(slide, x, y, w, h, title, text, fill=CARD, accent=BLUE, tsize=18, size=15):
    rect(slide, x, y, w, h, fill)
    rect(slide, x, y, 0.08, h, accent)
    tb(slide, x + 0.2, y + 0.1, w - 0.3, 0.5, title, tsize, True, DARK)
    tb(slide, x + 0.2, y + 0.58, w - 0.3, h - 0.65, text, size, False, INK)


def table(slide, x, y, w, rows, widths, size=13, head=True):
    t = slide.shapes.add_table(len(rows), len(rows[0]), Inches(x), Inches(y), Inches(w), Inches(0.36 * len(rows))).table
    for j, cw in enumerate(widths):
        t.columns[j].width = Inches(cw)
    for i, row in enumerate(rows):
        for j, val in enumerate(row):
            c = t.cell(i, j)
            c.text = ''
            p = c.text_frame.paragraphs[0]
            r = p.add_run()
            r.text = str(val)
            hd = head and i == 0
            r.font.name, r.font.size, r.font.bold = FONT, Pt(size), hd or (j == 0)
            r.font.color.rgb = RGBColor(255, 255, 255) if hd else (GREY if row[-1] in ('No', 'No: strict order') else INK)
            c.fill.solid()
            c.fill.fore_color.rgb = BLUE if hd else (CARD if i % 2 else RGBColor(255, 255, 255))
            c.margin_top = c.margin_bottom = Inches(0.03)
    return t


def set_notes(slide, text):
    tf = slide.notes_slide.notes_text_frame
    if tf is not None:
        tf.text = text


def new(title, sub=None, notes=None):
    s = prs.slides.add_slide(LAYOUT)
    for ph in list(s.placeholders):
        ph._element.getparent().remove(ph._element)
    tb(s, 0.5, 0.45, 12.33, 0.75, title, 30, True, BLUE)
    if sub:
        tb(s, 0.5, 1.15, 12.33, 0.45, sub, 18, False, GREY)
    ln = s.shapes.add_connector(MSO_CONNECTOR.STRAIGHT, Inches(0.5), Inches(1.68), Inches(12.83), Inches(1.68))
    ln.line.color.rgb = RGBColor(0xD0, 0xD7, 0xDE)
    tb(s, 0.5, 7.1, 11.5, 0.3, FOOT, 11, False, GREY)
    tb(s, 12.5, 7.1, 0.7, 0.3, str(len(prs.slides)), 11, False, GREY, PP_ALIGN.RIGHT)
    if notes:
        set_notes(s, notes)
    return s


def divider(kicker, title, sub=''):
    s = prs.slides.add_slide(LAYOUT)
    for ph in list(s.placeholders):
        ph._element.getparent().remove(ph._element)
    tb(s, 0.5, 2.7, 12.33, 0.6, kicker, 22, True, GREY, PP_ALIGN.CENTER)
    ln = s.shapes.add_connector(MSO_CONNECTOR.STRAIGHT, Inches(5), Inches(3.45), Inches(8.33), Inches(3.45))
    ln.line.color.rgb = BLUE
    tb(s, 0.5, 3.65, 12.33, 1.4, title, 40, True, BLUE, PP_ALIGN.CENTER)
    if sub:
        tb(s, 1.0, 5.0, 11.33, 0.8, sub, 18, False, GREY, PP_ALIGN.CENTER)
    tb(s, 0.5, 7.1, 11.5, 0.3, FOOT, 11, False, GREY)
    tb(s, 12.5, 7.1, 0.7, 0.3, str(len(prs.slides)), 11, False, GREY, PP_ALIGN.RIGHT)
    return s


def src(s, text, y=6.6):
    tb(s, 0.5, y, 12.33, 0.4, text, 12, False, GREY)


def still(sid, v):
    out = os.path.join(STILL, f'{sid}_{v}_en.png')
    if not os.path.exists(out):
        prof = tempfile.mkdtemp()
        subprocess.run([EDGE, '--headless=new', '--disable-gpu', '--hide-scrollbars', f'--user-data-dir={prof}', '--window-size=1280,720',
                        '--virtual-time-budget=6000', f'--screenshot={out}', f'{DEMO}?video=1&s={sid}&v={v}&lang=en&final=1'],
                       check=True, capture_output=True)
    return out


# ------------------------------------------------------------------ slides
divider('DAY 2  -  SESSION', 'Canvassing the PSU', 'The compact segment protocol, step by step, with the scenarios you will meet in the field')

s = new('What You Will Be Able To Do', 'By the end of this session')
bullets(s, 0.7, 1.9, 11.9, 4.8, [
    'Find Segment 1 and sweep it structure by structure, skipping none.',
    'Know when to stop: the target of 6 interviews and the "finish the segment" rule.',
    'Establish eligibility and the date of birth, even without a vaccination card.',
    'Respond correctly to a flooded, empty or river segment, insecurity, or an empty PSU.',
    'Complete the segment and PSU disposition form with the right code and fields.'], 22)

s = new('Why: Every Household Needs the Same Chance', 'A survey only represents the households that could be selected',
        'Ask the room: which children are most likely to be missed if teams stay near the road?')
bullets(s, 0.7, 1.9, 6.6, 4.6, [
    'If we stay near the road, we miss remote households, often the least vaccinated.',
    'Coverage then looks better than it is. No analysis can correct that afterwards.',
    'The protocol takes every choice away from the team: where to start, which house, when to stop.'], 21)
card(s, 7.7, 1.95, 5.1, 2.1, 'Gridded sample, random segments', 'BGC draws PSUs from gridded population data (GRID3). Each PSU is cut into compact segments numbered at random.', OKBG, GREEN)
card(s, 7.7, 4.25, 5.1, 2.2, 'Design 6 in the GRID3 manual', 'Go to the first cell and interview all households. Target reached? Stop. If not, go to the next cell, until the target is met or cells run out.')
src(s, 'Source: GRID3, Designing and Implementing Gridded Population Surveys (2022), design 6, p. 45.')

s = new('The Numbers to Remember', 'They are the same for every team')
nums = [('6', 'interviews per PSU', 'Children aged 12-23 months. Team decision, 20 Nov 2026.', OKBG, GREEN),
        ('1', 'starting segment', 'Always Segment 1, then ascending numbers.', CARD, BLUE),
        ('1 + 2', 'visit + revisits', 'At most two revisits to an absent household.', AMBG, AMBER),
        ('15 m', 'GPS accuracy', 'At the door. Wait up to 5 minutes if needed.', CARD, BLUE),
        ('1', 'record per structure', 'Even vacant, not eligible, absent or refusing.', CARD, BLUE),
        ('~10', 'interviews per team per day', 'About 2 PSUs a day. Speed never justifies a skip.', CARD, BLUE)]
for i, (n, t, d, f, a) in enumerate(nums):
    x, y = 0.6 + (i % 3) * 4.15, 1.95 + (i // 3) * 2.45
    rect(s, x, y, 3.95, 2.25, f)
    rect(s, x, y, 0.08, 2.25, a)
    tb(s, x + 0.25, y + 0.1, 3.6, 0.8, n, 36, True, DARK)
    tb(s, x + 0.25, y + 0.9, 3.6, 0.45, t, 17, True, INK)
    tb(s, x + 0.25, y + 1.35, 3.6, 0.85, d, 14, False, GREY)

s = new('Before Leaving', 'The team chief checks with each enumerator the evening before')
bullets(s, 0.7, 1.9, 6.0, 4.6, [
    'PSU and segment boundaries visible on the CAPI map, with numbers.',
    'Segment 1 written on the assignment sheet.',
    'Paper PSU map in the bag: the backup if the tablet or app stops.',
    'Current CAPI version, one test submission sent.'], 19)
bullets(s, 6.9, 1.9, 6.0, 4.6, [
    'Phone and power bank charged.',
    'Consent forms in French and Otetela.',
    'Two enumerators in one PSU? Segment blocks written down before leaving.',
    'Calendar of local events prepared during training.'], 19)
src(s, 'SOP-01 pre-deployment list; GRID3 (2022), section 2.1.2.2, p. 24 (paper map as backup).')

s = new('Navigating to the PSU and into Segment 1')
bullets(s, 0.7, 1.9, 6.4, 4.8, [
    'The centroid is for navigation only. Do not interview on the way or at the centroid.',
    'Check that the blue dot is inside the PSU polygon. Courtesy visit to the local authority.',
    'Find Segment 1 on the map and compare it with the assignment sheet. Disagreement? Stop and call the supervisor.',
    'Work starts when the marker is inside the Segment 1 polygon. Start with the structure nearest the entry point.',
    'Fix one sweep direction (serpentine) for the whole segment and tell the team chief.'], 18)
card(s, 7.5, 1.95, 5.3, 2.3, 'Tools', 'Offline navigation app (SW Maps) showing the PSU boundary and your position; a paper map as backup. Paper maps also help explain the survey to residents and leaders.')
card(s, 7.5, 4.45, 5.3, 1.9, 'Next segment', 'The next number, not the nearest neighbour. Navigate to it by its number on the map.', AMBG, AMBER)
src(s, 'SOP-01 Phases 1 and 6; GRID3 (2022), section 2.1.2.2, p. 24.')

s = new('The Sweep: Every Structure, One Record')
bullets(s, 0.7, 1.9, 6.2, 4.8, [
    'Go to the next structure on your line, one by one.',
    'Never skip a structure because it is far, uphill, fenced, looks empty or "has no child".',
    'Every structure produces a record, submitted before walking on, with GPS of 15 m or better at the door.',
    'A structure outside the segment belongs to the segment that contains it: not now.'], 19)
items = [('Interview', 'Child aged 12-23 months: counts toward the target.', OKBG, GREEN), ('Not eligible', 'No child aged 0-23 months: a record anyway.', CARD, BLUE),
         ('Absent', 'Record, then revisit.', AMBG, AMBER), ('Refusal', 'Record, never replaced by a neighbour.', BADBG, RED),
         ('Vacant or non-residential', 'Record with GPS: proof the team passed.', CARD, BLUE), ('Child 0-11 months only', 'Interview, not in the target.', CARD, BLUE)]
for i, (t, d, f, a) in enumerate(items):
    card(s, 7.2 + (i % 2) * 2.85, 1.9 + (i // 2) * 1.6, 2.7, 1.45, t, d, f, a, 15, 13)

s = new('A Structure on a Boundary', 'The main entrance decides')
bullets(s, 0.7, 1.9, 7.0, 4.6, [
    'Boundary between two segments: the structure belongs to the segment that contains its main entrance. Note the reason in the comment.',
    'PSU boundary: same rule. The interview goes ahead and the record carries the "out of boundary" flag for review.',
    'Each structure is counted in one segment only.'], 20)
rect(s, 8.2, 2.1, 2.2, 3.4, RGBColor(0xFF, 0xF3, 0xC4), GREY)
rect(s, 10.4, 2.1, 2.2, 3.4, CARD, GREY)
rect(s, 9.7, 3.3, 1.4, 1.0, RGBColor(255, 255, 255), INK)
rect(s, 9.8, 3.75, 0.25, 0.55, GREEN)
tb(s, 8.2, 2.2, 2.2, 0.4, 'Segment 1', 15, True, DARK, PP_ALIGN.CENTER)
tb(s, 10.4, 2.2, 2.2, 0.4, 'Segment 2', 15, True, DARK, PP_ALIGN.CENTER)
tb(s, 8.2, 4.8, 2.2, 0.5, 'Door: Segment 1', 14, True, GREEN, PP_ALIGN.CENTER)
src(s, 'SOP-01, section 7. The GRID3 manual suggests another rule (north and east edges included); in Sankuru we follow the SOP.')

s = new('At the Door: Who Is Eligible?')
bullets(s, 0.7, 1.9, 7.2, 4.8, [
    'A child aged 0-23 months who usually lives here and slept here last night.',
    'Children aged 12-23 months count toward the target; those aged 0-11 months are interviewed outside it.',
    'The mother or caregiver who decides on vaccination is needed. If she is away, do not interview someone else: come back.',
    'Consent is read in full, every time.'], 20)
card(s, 8.3, 1.95, 4.5, 2.6, 'Why this rule', 'Age decides eligibility. A mistake on age puts a child into or out of the sample.')
src(s, 'WHO (2018), Vaccination coverage cluster surveys: reference manual, section 4.1.2.')

s = new('Finding the Date of Birth', 'In this order', 'Build the calendar of local events with the trainees: feasts, elections, seasons, harvests, village events.')
dob = [('1  Vaccination card', 'The best source. Copy the date as written.', OKBG, GREEN),
       ('2  Birth certificate', 'No card? Ask for the birth certificate or another document.', CARD, BLUE),
       ('3  Calendar of local events', 'Religious feasts, elections, rainy seasons, harvests, village events. Prepared during training.', AMBG, AMBER)]
for i, (t, d, f, a) in enumerate(dob):
    card(s, 0.6 + i * 4.15, 1.95, 3.95, 2.6, t, d, f, a, 19, 16)
rect(s, 0.6, 4.85, 12.2, 0.9, RGBColor(0xFF, 0xFB, 0xEA))
rect(s, 0.6, 4.85, 0.08, 0.9, RGBColor(0xF2, 0xC9, 0x4C))
tb(s, 0.85, 5.0, 11.8, 0.6, '"It might be time consuming but is essential."  (WHO 2018)', 20, False, INK)
src(s, 'WHO (2018), section 4.1.2, p. 50 (p. 73 of the French edition).')

s = new('The Interview, in Order')
bullets(s, 0.7, 1.9, 6.6, 4.8, [
    'Caregiver recall before asking for the card.',
    'Ask for the card: "Were you ever given one? Do you still have it? Can you bring it?"',
    'Give time to find it; offer to come back if it is locked away.',
    'Enter every visible date as written; take a clear photo of the whole card.'], 19)
card(s, 7.6, 1.95, 5.2, 2.8, 'If the CAPI flags a date', 'Recheck it on the card before leaving. If the card shows that date, keep it and write a comment. Data management decides afterwards.')
src(s, 'WHO (2018), sections 4.1.2 and 4.1.4; SOP-01.')

s = new('Absent, Refusal, Postponed', 'One visit and two revisits at most')
bullets(s, 0.7, 1.9, 6.6, 4.8, [
    'Nobody home: record, then revisit the same day or next morning.',
    'At most two revisits; after that it is a documented non-contact.',
    'Every visit is a new form, with the HHI08 ID from the 1st visit.',
    'Refusal: thank, record, do not return, never replace.'], 19)
card(s, 7.6, 1.95, 5.2, 3.0, 'What WHO says', 'Evening or early-morning visits are often needed. A second and third visit should take place before leaving the cluster, and the outcome of each visit is recorded.')
src(s, 'WHO (2018), section 4.1.1, p. 50.')

s = new('Target Reached? Finish the Segment', 'SOP-01 Rule 5.1')
bullets(s, 0.7, 1.9, 12.0, 4.6, [
    'The target counts only once the segment in progress is exhausted.',
    'Leaving halfway leaves households with no chance of selection: alert A11.',
    'Target reached in Segment 1: finish Segment 1 and do not start Segment 2.',
    'Interviews beyond 6 are kept.',
    'Then declare the segment to the team chief: number, records, eligible households, interviews, absent households to revisit.'], 21)

s = new('Who Decides What')
table(s, 0.6, 1.95, 12.1, [
    ['Role', 'Decides', 'Never does'],
    ['Enumerator', 'Order of structures on the line; the result of each visit', 'Skip a segment or a structure on their own'],
    ['Team chief', 'Segment blocks; each segment\'s code; first review of forms', 'Authorise a segment skip'],
    ['Field supervisor', 'Skipping an inaccessible segment (D, E, F, J); edge cases', 'Replace a PSU'],
    ['DQM', 'Told the same day; checks codes against maps', 'Discuss records under verification with back-checkers'],
    ['Coordination and PI', 'Replacing a PSU by its backup (PSU code 5)', 'Let a team choose another village'],
    ['Supervisor and DQM, before fieldwork', 'Code G from satellite imagery', 'Accept a G decided in the field']], [3.0, 4.8, 4.3], 14)

s = new('Segment Disposition Codes', 'Disposition form V2 (20 November 2026)')
table(s, 0.6, 1.85, 12.1, [
    ['Code', 'Meaning', 'In Sankuru'],
    ['A', 'Canvassed in full, in order, with forms completed', 'Yes'],
    ['B', 'Canvassed in full, out of order', 'No: strict order'],
    ['C1 / C2', 'Canvassed in full, no form: C1 no dwelling; C2 dwellings without a form (error to check)', 'Yes'],
    ['D1-D13', 'Inaccessible: flooding, swamp, forest, terrain, road cut, fields, camp, school, market...', 'Yes, supervisor'],
    ['E1-E4', 'Water: river, lake, island with no canoe, unsafe crossing', 'Yes, supervisor'],
    ['F1-F9', 'Other: insecurity, tension, access refused, epidemic, too far', 'Yes, supervisor'],
    ['G1 / G2', 'Decided from satellite imagery', 'Before fieldwork'],
    ['H', 'Enumerator error: segment skipped by mistake', 'Report honestly'],
    ['I', 'Unknown whether the segment was visited', 'Review'],
    ['J', 'Incomplete, in order; reason for the part not done', 'Yes'],
    ['K / L', 'Incomplete out of order; PSU combed without order', 'No']], [1.4, 8.3, 2.4], 13)

s = new('For Every Segment Not Done: a Reason and Six Fields')
table(s, 0.6, 1.95, 7.2, [
    ['Field', 'What to record'], ['MR', 'Main reason: one sub-code'], ['SH', 'Dwellings visible? People seen?'],
    ['NL', 'Estimated dwellings (0, 1-5, 6-20...)'], ['PT', 'Share not done: all, more or less than half'],
    ['DU', 'Temporary or permanent barrier'], ['SRC, PH, VR', 'Source, geotagged photo, supervisor approval']], [1.8, 5.4], 15)
card(s, 8.2, 1.95, 4.6, 3.3, 'Why so much detail?', 'GiveWell wants to know how many children may have been excluded, where and why: empty or inaccessible. The fields answer these questions and let every decision be checked.')

s = new('PSU Codes', 'One code per PSU, at the end')
table(s, 0.6, 1.95, 12.1, [
    ['Code', 'Meaning', 'In Sankuru'],
    ['1', 'According to the protocol: all required segments were accessible', 'Yes'],
    ['2', 'According to the protocol, with segments skipped (each with its sub-code)', 'Yes'],
    ['3', 'Not according to the protocol: higher numbers before lower ones', 'Avoid; report'],
    ['4', 'Whole PSU visited without following segments', 'No'],
    ['5', 'Replaced by a backup PSU: reason + Coordination approval', 'Yes'],
    ['6', 'Exhausted below target: every segment worked or coded', 'Yes']], [1.2, 8.5, 2.4], 15)

# ------------------------------------------------------------------ scenarios
SCN = [('basic', 'Basic canvassing', 'A, PSU 1',
        ['Segment 1 first, then ascending numbers.', 'Target reached in Segment 2: finish it anyway.', 'Absent households: at most two revisits.'],
        ['Starts in Segment 9 near the road.', 'Leaves Segment 1 half done; a refusal "replaced".', 'Jumps to Segment 8, leaves at the target; false A codes.']),
       ('quota1', 'Target Reached in Segment 1', 'A, PSU 1',
        ['Finish Segment 1 completely, even after 6 interviews.', 'Do not start Segment 2.', 'Interviews beyond 6 are kept.'],
        ['Leaves at the 6th interview.', 'Households left with no chance of selection.', 'Alert A11; code A does not match the map.']),
       ('flood', 'Flooded Segment', 'D1, PSU 2',
        ['Stop at the edge and call: never decide alone.', 'Supervisor approves the skip: D1 + photo + source + approval.', 'DQM told the same day; PSU code 2.'],
        ['Sees the water and moves on without calling.', 'Segment 2 has no record and no code.', 'Nobody can tell whether children lived there.']),
       ('empty', 'Uninhabited Segment', 'C1, PSU 1',
        ['Walk the whole segment, even if it looks empty.', '"Empty area" record with GPS and photo.', 'Code C1: no dwelling found.'],
        ['Codes C from the track, without going in.', 'A back-check finds 3 houses hidden by trees.', 'With no GPS point, the code becomes I (unknown).']),
       ('river', 'Segment Across the River', 'E3, PSU 2',
        ['No swimming across, no crossing without life jackets.', 'Call the supervisor; code E3, temporary barrier (DU1).', 'Another attempt is planned if a canoe is found.'],
        ['Interviews near-bank houses in Segment 8 and declares them Segment 2.', 'Alert A2: points outside the declared segment.', 'Segment 2 houses have no record and no code.']),
       ('danger', 'Insecurity During Work', 'J + F1, PSU 2',
        ['Safety overrides every rule: withdraw at once.', 'Code J + F1 for the part not done.', 'Team chief, supervisor and coordination informed.'],
        ['Carries on during the fight to finish the segment.', 'Team and families put at risk.', 'A critical incident not reported.']),
       ('swamp', 'Swamp in Part of a Segment', 'J + D2, PSU 2',
        ['Work all of the accessible part.', 'For the rest: J + D2, SH1, NL1, PT3.', 'Supervisor approves; another attempt if the water goes down.'],
        ['Codes A for an incomplete segment.', 'The 3 houses beyond the swamp vanish from the data.']),
       ('two', 'Two Enumerators in One PSU', 'blocks',
        ['Blocks written before leaving: A = Segment 1, B = Segment 2.', 'Each keeps to their own segments, in ascending order.', 'Target reached: each finishes their current segment.'],
        ['No blocks: both work Segments 1 and 2 at the same time.', 'Then a jump to Segment 11 near the road.', 'Modelled on a PSU from the July 2026 map review.']),
       ('below', 'Target Not Reached After Every Segment', 'PSU 6',
        ['Every segment worked or coded, in order.', 'PSU code 6: exhausted below target; supervisor and DQM told.', 'Never work outside the PSU to make up numbers.'],
        ['Goes to the next village, outside the PSU, for 2 more children.', 'Alert A1: points outside the PSU.', 'Those interviews are rejected.']),
       ('emptypsu', 'Entirely Empty PSU', 'C1, PSU 5',
        ['Check on the ground, with photos and GPS.', 'Supervisor verifies; Coordination approves the backup.', 'PSU code 5 + C1; start the backup PSU at its Segment 1.'],
        ['The team picks the nearest village itself.', 'Unapproved replacement: the data cannot be used.', 'Only Coordination assigns the backup.']),
       ('g1', 'Decision From Satellite Imagery', 'G1, PSU 2',
        ['G is decided before fieldwork, from imagery, by the supervisor and DQM.', 'G1: no building visible; the team does not go there.'],
        ['The enumerator codes a far segment G to avoid the walk.', 'That segment had 10 houses.', 'G is never a field excuse.'])]
divider('DAY 2  -  SCENARIOS', 'Field Scenarios', 'Each situation on the disposition form, played twice: the right practice, then the mistake')
s = new('Eleven Situations You Will Meet', 'Each one is played as a short video: right practice, then mistake')
for i, (sid, t, c, _, _) in enumerate(SCN):
    x, y = 0.6 + (i % 4) * 3.07, 1.9 + (i // 4) * 1.6
    card(s, x, y, 2.92, 1.45, f'{i + 1}. {t}', c, CARD, BLUE, 14, 13)
for i, (sid, t, c, ok, bad) in enumerate(SCN):
    for v, lst in (('correct', ok), ('wrong', bad)):
        label = 'RIGHT PRACTICE' if v == 'correct' else 'WHAT NOT TO DO'
        s = new(f'Scenario {i + 1}: {t}', f'{label}  |  {c}')
        poster = still(sid, v)
        mp4 = os.path.join(VID, f'{sid}_{v}_en.mp4')
        if os.path.exists(mp4):
            s.shapes.add_movie(mp4, Inches(0.5), Inches(1.85), Inches(8.6), Inches(4.84), poster_frame_image=poster, mime_type='video/mp4')
        else:
            s.shapes.add_picture(poster, Inches(0.5), Inches(1.85), Inches(8.6), Inches(4.84))
        rect(s, 9.35, 1.85, 3.5, 4.84, OKBG if v == 'correct' else BADBG)
        rect(s, 9.35, 1.85, 0.08, 4.84, GREEN if v == 'correct' else RED)
        tb(s, 9.6, 1.95, 3.15, 0.5, label, 15, True, GREEN if v == 'correct' else RED)
        bullets(s, 9.5, 2.5, 3.3, 4.1, lst, 15, INK, 10)
        set_notes(s, 'Click the video to play. Pause to ask: what should the enumerator do now, and which code goes on the disposition form?')

# ------------------------------------------------------------------ closing
s = new('What the Protocol Is Not: A Real Case', 'Redrawn from BGC\'s map review (Kongo Central, July 2026); names removed, times approximate')
img = os.path.join(STILL, 'real_case_en.png')
if not os.path.exists(img):
    prof = tempfile.mkdtemp()
    sl = pathlib.Path(ROOT, '06_Slides', 'canvassing_slides.html').resolve().as_uri()
    subprocess.run([EDGE, '--headless=new', '--disable-gpu', '--hide-scrollbars', f'--user-data-dir={prof}', '--window-size=1280,720',
                    '--virtual-time-budget=4000', f'--screenshot={img}', f'{sl}?lang=en#45'], check=True, capture_output=True)
    from PIL import Image
    Image.open(img).crop((50, 135, 1240, 650)).save(img)
s.shapes.add_picture(img, Inches(0.6), Inches(1.85), Inches(12.1), Inches(5.2))

s = new('Prohibited Practices', 'Each one is detected by a monitoring indicator')
bullets(s, 0.7, 1.85, 6.0, 5.1, [
    'Choosing or changing the starting segment.', 'Starting N+1 before declaring N complete.',
    'Leaving a segment at the target before it is exhausted.', 'Skipping a structure (distance, terrain, appearance).',
    'Replacing a refusing or absent household by a neighbour.', 'No record for a non-eligible, absent, refusing or vacant structure.',
    'GPS recorded away from the structure or worse than 15 m.'], 16, INK, 6)
bullets(s, 6.9, 1.85, 6.0, 5.1, [
    'Completing forms away from the structure, or several at once.', 'Interviewing outside the declared segment or the PSU.',
    'Asking for the card before the recall questions.', 'Suggesting answers or shortening the consent.',
    'Sharing a phone or a PIN.', 'Contacting an independent back-checker about records under verification.'], 16, INK, 6)

s = new('Your Turn: Which Code?', 'Answer without looking back', 'Answers: 1. finish Segment 1 (A, PSU 1). 2. C1. 3. D1 (PSU 2). 4. PSU 6, never outside the PSU.')
qs = ['The 6th interview comes at house 5 of Segment 1, which has 12 houses.', 'Segment 3 is a market with no dwelling; the team walks all of it.',
      'The track to Segment 2 is under water; the supervisor has approved the skip.', 'All 5 segments are done; only 4 interviews.']
for i, q in enumerate(qs):
    card(s, 0.6 + (i % 2) * 6.15, 1.95 + (i // 2) * 2.3, 5.95, 2.1, f'Question {i + 1}', q, CARD, BLUE, 17, 16)

s = new('Key Points')
bullets(s, 0.7, 1.9, 12.0, 4.4, [
    'Segment 1, then ascending numbers. Nobody chooses.',
    'Every structure, one record, submitted at the door with GPS.',
    '6 interviews, but always finish the segment in progress.',
    'One visit and two revisits; a refusal is never replaced.',
    'A segment is skipped only with the supervisor, with a sub-code, a photo and an approval.',
    'The code written must match the map of GPS points.'], 21)
src(s, 'Sources: Sankuru Study Protocol V1.0; SOP-01 V1.0; disposition form V2; WHO vaccination coverage cluster surveys reference manual (2018); GRID3, Designing and Implementing Gridded Population Surveys (2022). Animations: bosangir.github.io/VCS-DRC', 6.35)

prs.save(OUT)
print('saved', OUT, len(prs.slides), 'slides')
