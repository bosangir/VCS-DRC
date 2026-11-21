# Field data collection and quality assurance: Sankuru training, November 2026

Training material for coordinators, field supervisors, team chiefs, enumerators, data managers and quality assurance staff of the UNIKIN vaccination coverage surveys in the DRC. The goal is quality data from PSUs that are canvassed completely and in line with the protocol.

The rules come from the Sankuru Study Protocol V1.0 (5 November 2026), SOP-01 Compact Segment Protocol V1.0 (7 November 2026) and the DQA Plan V1.0. Where this material and the Study Protocol differ, the Study Protocol governs.

## Contents

| Folder | What it is | Use it for |
|---|---|---|
| `01_Key_messages_by_role/` | Word guide in French and English: six messages for everyone, then what each role does before, during and after fieldwork; disposition codes; alerts A1–A13; changes after the BGC review; points to confirm; the enumerator daily self-check | Handout and the outline of the training |
| `02_Minutes_BGC_meetings/` | Combined minutes of the BGC and UNIKIN meetings of 13 and 16 November 2026 (internal, not in the public repository) | Briefing the team leads |
| `03_Process_infographic/` | Poster with pictograms: the 10 steps from preparation to independent checks, the red lines, what is new, and who does what (HTML, PNG, PDF; French and English) | Slide, printed poster, WhatsApp image |
| `04_Segment_protocol_demo/` | Interactive scenarios of the segment protocol: eleven situations from the disposition form, each with the right practice and the mistake, on one screen. Target of 6 interviews. Also still figures | Live demonstration during the training |
| `06_Slides/` (PowerPoint in the repository: `docs/assets/`) | Day 2 deck "Canvassing the PSU": web version in French and English (`canvassing_slides.html`, scenario animations play inside the slides) and PowerPoint in English with the scenario videos embedded | Day 2 session on the protocol |
| `07_Videos/` (in the repository: `docs/assets/videos/`) | One MP4 per scenario and version (correct, wrong), French and English, recorded from the animations | WhatsApp, projection without internet |
| `05_Website/` (in the repository: `docs/`) | One-page website (French and English) with everything above plus two live demonstrations of CAPI 006 checks: card dates and active interview duration. Published from the `docs/` folder of the VCS-DRC repository | Showing the material on a projector or phone; sharing one link |
| `_build/` | Python scripts that generate the guide, the poster and the website | Changing the text and rebuilding |

## Running the scenarios

Open `04_Segment_protocol_demo/segment_protocol_demo.html` in any browser; it works offline and fits on one screen. Choose a scenario on the left and its version (Correct or Wrong), then **Play**, **Next step** (one action at a time, good for discussion) or **Jump to end**. The FR / EN buttons switch language. The target is 6 interviews of children aged 12–23 months per PSU.

| # | Scenario | Codes |
|---|---|---|
| 1 | Basic canvassing: target reached in Segment 2, which is finished; two revisits | A, PSU 1 |
| 2 | Target reached inside Segment 1 | A, PSU 1 |
| 3 | Flooded segment: stop, call, supervisor approves the skip | D1, PSU 2 |
| 4 | Uninhabited segment: walked in full, "empty area" record | C1 |
| 5 | Segment across a river, no canoe | E3, PSU 2 |
| 6 | Insecurity during work: withdraw, partial segment | J + F1, PSU 2 |
| 7 | Swamp in part of a segment | J + D2, PSU 2 |
| 8 | Two enumerators in one PSU: separate blocks (the wrong version follows the July 2026 map review) | blocks |
| 9 | Target not reached after every segment | PSU 6 |
| 10 | Entirely empty PSU: replaced by its backup with Coordination approval | C1, PSU 5 |
| 11 | Segment decided from satellite imagery before fieldwork | G1, PSU 2 |

URL options: `?s=<scenario id>&v=correct|wrong&lang=fr|en`, `&final=1` (end state), `&autoplay=1`, `&embed=1` (no scenario list), `&video=1`, `&speed=1..10`. Scenario ids: basic, quota1, flood, empty, river, danger, swamp, two, below, emptypsu, g1.

**Segment order is strict in Sankuru** (decision of 18 November 2026). Whole-PSU canvassing out of order (code B) is not used, even in small PSUs. If the quota is not reached after every segment is exhausted, the PSU is recorded as exhausted below quota.

## Rebuilding

```
python _build/build_infographic.py 03_Process_infographic
python _build/build_docs.py . path/to/logo.png
python _build/record_videos.py . 07_Videos fr
python _build/record_videos.py . 07_Videos en
python _build/build_canvassing_pptx.py . <Day 1 incidents deck as template> "06_Slides/Day 2 - Canvassing the PSU - Sankuru - Bernard.pptx"
python _build/build_site.py . ../docs
```

The PNG and PDF versions of the poster were rendered with Microsoft Edge in headless mode from the HTML files.

## Active interview duration

Decided 18 November 2026: CAPI version 006 records the time the form is open on screen (`duration()`), frozen at consent, at the start and end of each woman's interview, and at the visit result. `dur_interview_min` is the duration to report; `flag_short_interview` marks alerts A4/A5. Enumerators save and close the form when they leave a household.

## To confirm before deployment

- **Inaccessible reasons:** the detailed list.

PSUs, segments and households in the demonstration are simulated.
