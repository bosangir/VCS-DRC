# Field data collection and quality assurance: Sankuru training, November 2026

Training material for coordinators, field supervisors, team chiefs, enumerators, data managers and quality assurance staff of the UNIKIN vaccination coverage surveys in the DRC. The goal is quality data from PSUs that are canvassed completely and in line with the protocol.

The rules come from the Sankuru Study Protocol V1.0 (5 November 2026), SOP-01 Compact Segment Protocol V1.0 (7 November 2026) and the DQA Plan V1.0. Where this material and the Study Protocol differ, the Study Protocol governs.

## Contents

| Folder | What it is | Use it for |
|---|---|---|
| `01_Key_messages_by_role/` | Word guide in French and English: five messages for everyone, then what each role does before, during and after fieldwork; disposition codes; alerts A1–A13; changes after the BGC review; points to confirm; the enumerator daily self-check | Handout and the outline of the training |
| `03_Process_infographic/` | Poster with pictograms: the 10 steps from preparation to independent checks, the red lines, what is new, and who does what (HTML, PNG, PDF; French and English) | Slide, printed poster, WhatsApp image |
| `04_Segment_protocol_demo/` | Interactive demonstration of the segment protocol in a simulated PSU, with three scenarios: correct protocol, common errors, and whole-PSU canvassing (code B). Also still figures of each scenario | Live demonstration during the training |
| `_build/` | Python scripts that generate the guide and the poster | Changing the text and rebuilding |

## Running the segment demonstration

Open `04_Segment_protocol_demo/segment_protocol_demo.html` in any browser; it works offline. Choose a scenario, then **Play**, **Next step** (one structure at a time, good for discussion) or **Jump to end**. The FR / EN buttons switch language.

URL options, for making still images: `?mode=correct|errors|whole`, `?lang=fr|en`, `?final=1`.

What each scenario shows:

1. **Correct protocol.** Arrival at the centroid, Segment 1 first, serpentine sweep, one record for every structure (including vacant, no eligible child, absent and refusal). The quota is reached partway through Segment 2, but the segment is finished. Then the team returns to absent households (at most 2 visits) and gives every segment from 1 to the highest reached a code.
2. **Common errors**, modelled on the BGC map review. The team starts in the wrong segment, leaves Segment 1 half done, replaces a refusal with a neighbour, jumps to Segment 8, and leaves when the quota is reached. Red circles mark households that had no chance of selection, and the declared "A" codes do not match the map.
3. **Whole PSU (code B).** Every segment and every structure is covered, whatever the number order. Codes are B (interviews), C (no interviews) and D (inaccessible: forest). This scenario applies only with the field supervisor's authorisation, and the list of these PSUs goes to BGC.

## Rebuilding

```
python _build/build_infographic.py 03_Process_infographic
python _build/build_docs.py . path/to/logo.png
```

The PNG and PDF versions of the poster were rendered with Microsoft Edge in headless mode from the HTML files.

## To confirm before deployment

- **Whole-PSU canvassing:** the Sankuru SOP-01 V1.0 removed the full-PSU amendment, but BGC accepted code B.
- **Active interview duration:** how it will be recorded.
- **In-form date checks:** whether to add same, reversed and same-age date checks to the CAPI.
- **Inaccessible reasons:** the detailed list.

PSUs, segments and households in the demonstration are simulated.
