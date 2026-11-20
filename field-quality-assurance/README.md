# Field data collection and quality assurance: Sankuru training, November 2026

Training material for coordinators, field supervisors, team chiefs, enumerators, data managers and quality assurance staff of the UNIKIN vaccination coverage surveys in the DRC. The goal is quality data from PSUs that are canvassed completely and in line with the protocol.

The rules come from the Sankuru Study Protocol V1.0 (5 November 2026), SOP-01 Compact Segment Protocol V1.0 (7 November 2026) and the DQA Plan V1.0. Where this material and the Study Protocol differ, the Study Protocol governs.

## Contents

| Folder | What it is | Use it for |
|---|---|---|
| `01_Key_messages_by_role/` | Word guide in French and English: six messages for everyone, then what each role does before, during and after fieldwork; disposition codes; alerts A1–A13; changes after the BGC review; points to confirm; the enumerator daily self-check | Handout and the outline of the training |
| `02_Minutes_BGC_meetings/` | Combined minutes of the BGC and UNIKIN meetings of 13 and 16 November 2026 (internal, not in the public repository) | Briefing the team leads |
| `03_Process_infographic/` | Poster with pictograms: the 10 steps from preparation to independent checks, the red lines, what is new, and who does what (HTML, PNG, PDF; French and English) | Slide, printed poster, WhatsApp image |
| `04_Segment_protocol_demo/` | Interactive demonstration of the segment protocol in a simulated PSU, with two scenarios: correct protocol and common errors. Also still figures of each scenario | Live demonstration during the training |
| `05_Website/` (in the repository: `docs/`) | One-page website (French and English) with everything above plus two live demonstrations of CAPI 006 checks: card dates and active interview duration. Published from the `docs/` folder of the VCS-DRC repository | Showing the material on a projector or phone; sharing one link |
| `_build/` | Python scripts that generate the guide, the poster and the website | Changing the text and rebuilding |

## Running the segment demonstration

Open `04_Segment_protocol_demo/segment_protocol_demo.html` in any browser; it works offline. Choose a scenario, then **Play**, **Next step** (one structure at a time, good for discussion) or **Jump to end**. The FR / EN buttons switch language.

URL options, for making still images: `?mode=correct|errors`, `?lang=fr|en`, `?final=1`.

What each scenario shows:

1. **Correct protocol.** Arrival at the centroid, Segment 1 first, serpentine sweep, one record for every structure (including vacant, no eligible child, absent and refusal). The quota is reached partway through Segment 2, but the segment is finished. Then the team returns to absent households (at most two revisits) and gives every segment from 1 to the highest reached a code.
2. **Common errors**, modelled on the BGC map review. The team starts in the wrong segment, leaves Segment 1 half done, replaces a refusal with a neighbour, jumps to Segment 8, and leaves when the quota is reached. Red circles mark households that had no chance of selection, and the declared "A" codes do not match the map.

**Segment order is strict in Sankuru** (decision of 18 November 2026). Whole-PSU canvassing out of order (code B) is not used, even in small PSUs. If the quota is not reached after every segment is exhausted, the PSU is recorded as exhausted below quota.

## Rebuilding

```
python _build/build_infographic.py 03_Process_infographic
python _build/build_docs.py . path/to/logo.png
python _build/build_site.py . ../docs
```

The PNG and PDF versions of the poster were rendered with Microsoft Edge in headless mode from the HTML files.

## Active interview duration

Decided 18 November 2026: CAPI version 006 records the time the form is open on screen (`duration()`), frozen at consent, at the start and end of each woman's interview, and at the visit result. `dur_interview_min` is the duration to report; `flag_short_interview` marks alerts A4/A5. Enumerators save and close the form when they leave a household.

## To confirm before deployment

- **Inaccessible reasons:** the detailed list.

PSUs, segments and households in the demonstration are simulated.
