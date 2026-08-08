# PURSUE Release 05 — UAP Signal Intelligence Report

**Report date:** August 7, 2026  
**Prepared by:** uap-signal automated analysis  
**Subject:** Pentagon PURSUE Release 05 (August 7, 2026) and surrounding news cycle

---

## Executive Summary

On **August 7, 2026**, the Department of War published **PURSUE Release 05** — the fifth batch of declassified UAP materials under the Presidential Unsealing and Reporting System for UAP Encounters. This release adds **41 files**, bringing the cumulative PURSUE archive to **375 files**.

Release 05 pairs **another tranche of AARO-unresolved military sensor videos** with a heavy **FBI domestic / triangle / 2026 eyewitness** package:

| Dimension | Release 01 (May 8) | Release 02 (May 22) | Release 03 (Jun 12) | Release 04 (Jul 10) | Release 05 (Aug 7) |
|-----------|-------------------|---------------------|---------------------|---------------------|---------------------|
| **Focus** | Broad historical sweep | Military engagement footage | FBI/domestic eyewitness | AARO unresolved IR + nuclear sites | Unresolved sensor + FBI triangles / 2026 cases |
| **Standout** | 158–162 files, Apollo | Lake Huron shootdown, transmedium | Mother-orb, Colorado Springs, Hoover | 19 unresolved IR, Pantex, Los Alamos | Gulf of Oman AC-130 cluster, FBI 2026 thermal + FD-302s, Brazil 1963 cables |
| **Avg novelty (primary)** | ~5.1/10 | High (top 8) | ~5.3/10 | ~5.4/10 | **~6.9/10** |
| **Agency emphasis** | Multi-agency | DoW / ODNI | **FBI** | DoW (28) + NASA + DOE | **DoW (19)** + **FBI (17)** + CIA/DoS/EOP |

**Three findings dominate this release:**

1. **Gulf of Oman 2021 unresolved cluster (CENTCOM)** — IIR DOW-UAP-D101 plus six sensor videos (PR117–PR122). CBS coverage highlights an AC-130J gunship multi-UAP encounter; the catalog marks the set as AARO-unresolved.

2. **FBI 2026 western U.S. package** — Multiple FD-302s (slow-moving objects, thermally elevated aerial object, multiple red lights) plus Special Agent thermal video `FBI-UAP-PR007` and accompanying digital renderings. Highest novelty scores in this run (**8/10** on several FD-302s). Continues the Colorado Springs / western triangle thread from Release 03.

3. **Cold War diplomacy + early investigations** — First **DoS** PURSUE cables (Brazil, Nov 1963), EOP/NASC Bahia inquiry, CIA Puerto Rico 1965 memo, Walter Elder briefing notes (**8/10**), 1947 ghost-rocket intelligence review, and Project Sign-era Air Materiel Command file.

News today centers on this drop plus a separate **UAP whistleblower reporting path** (July 31 ODNI memo) covered by NewsNation.

---

## Methodology

| Run | Command / approach | Items analyzed |
|-----|-------------------|----------------|
| News/media sweep | `uap-signal check --date 2026-08-07 --source news_rss --max-items 12 --provider openai --model gpt-4.1-mini` | 12 CONTEXT items |
| Primary documents | warufo `data-release="05"` filter + LLM analysis (archive catalog text; war.gov media URLs returned HTTP 403 to the scraper) | **41/41** Release 05 items |
| Last prior run | July 31, 2026 (Release 04 report) | — |

Classification: rule-based (`classifier.py`) + LLM summarization/novelty (`analyzer.py`). Scores ≥6 flagged as high-signal. Primary analysis used catalog descriptions because direct PDF fetches from `war.gov/medialink` were blocked (403).

---

## Release 05: Primary Document Analysis

**Composition (per warufo):** 19 DoW, 17 FBI, 2 CIA, 2 DoS, 1 Executive Office of the President — by type: **22 PDFs**, **16 videos**, **3 images**. Avg novelty **6.85/10** (range 5–8).

### Top signal (novelty 8/10)

#### CIA-UAP-D023 — Briefing Notes for Mr. Walter Elder
- **Content:** CIA briefing material prepared for Walter N. Elder, Executive Assistant to the DCI (undated in catalog).
- **Significance:** Senior-leadership briefing product — rare window into how UAP material was packaged for CIA executive attention.
- [PDF](https://www.war.gov/medialink/ufo/release_05/Aug_07/documents/CIA-UAP-D023_Briefing-Notes-for-Mr-Walter-Elder.pdf)

#### FBI-UAP-D032 / D033 / D037 — 2026 FD-302s (western U.S.)
| ID | Topic | Link |
|----|-------|------|
| FBI-UAP-D032 | FD-302, “Slow-moving Objects,” 2026 | [PDF](https://www.war.gov/medialink/ufo/release_05/Aug_07/documents/FBI-UAP-D032_FD-302_Slow-moving-Objects_2026.pdf) |
| FBI-UAP-D033 | FD-302, “Thermally Elevated Aerial Object,” 2026 | [PDF](https://www.war.gov/medialink/ufo/release_05/Aug_07/documents/FBI-UAP-D033_FD-302_Thermally-Elevated-Aerial-Object_2026.pdf) |
| FBI-UAP-D037 | FD-302, “Multiple Red Lights,” 2026 | [PDF](https://www.war.gov/medialink/ufo/release_05/Aug_07/documents/FBI-UAP-D037_FD-302_Multiple-Red-Lights_2026.pdf) |

- **Significance:** Same-year FBI interview records of western U.S. incidents, including thermal/optical characterization — strongest contemporaneous domestic package since Release 03’s Colorado Springs materials.

### High signal (novelty 7/10)

#### Gulf of Oman 2021 — IIR + unresolved videos
- **DOW-UAP-D101** — Intelligence Information Report on unresolved UAP, Gulf of Oman, Sept 8, 2021. [PDF](https://www.war.gov/medialink/ufo/release_05/Aug_07/documents/DOW-UAP-D101_IIR_Unresolved-UAP-Report-Gulf-of-Oman_2021.pdf)
- Sensor videos (CENTCOM → AARO):

| ID | DVIDS |
|----|-------|
| DOW-UAP-PR117 | [1017793](https://www.dvidshub.net/video/1017793) |
| DOW-UAP-PR118 | [1017795](https://www.dvidshub.net/video/1017795) |
| DOW-UAP-PR119 | [1017798](https://www.dvidshub.net/video/1017798) |
| DOW-UAP-PR120 | [1017800](https://www.dvidshub.net/video/1017800) |
| DOW-UAP-PR121 | [1017802](https://www.dvidshub.net/video/1017802) |
| DOW-UAP-PR122 | [1017803](https://www.dvidshub.net/video/1017803) |

#### Pacific Ocean 2019 unresolved videos (Navy UAPTF → AARO)
| ID | DVIDS |
|----|-------|
| DOW-UAP-PR123 | [1017805](https://www.dvidshub.net/video/1017805) |
| DOW-UAP-PR124 | [1017806](https://www.dvidshub.net/video/1017806) |
| DOW-UAP-PR125 | [1017788](https://www.dvidshub.net/video/1017788) |
| DOW-UAP-PR126 | [1017790](https://www.dvidshub.net/video/1017790) |
| DOW-UAP-PR127 | [1017791](https://www.dvidshub.net/video/1017791) |

#### Middle East unresolved videos (2023 / 2025)
| ID | Year | DVIDS |
|----|------|-------|
| DOW-UAP-PR134 | 2025 | [1017792](https://www.dvidshub.net/video/1017792) |
| DOW-UAP-PR136 | 2023 | [1017796](https://www.dvidshub.net/video/1017796) |
| DOW-UAP-PR142 | 2025 | [1017797](https://www.dvidshub.net/video/1017797) |
| DOW-UAP-PR149 | 2023 | [1017799](https://www.dvidshub.net/video/1017799) |

#### FBI triangle / red-light case files + thermal video
| ID | Topic | Link |
|----|-------|------|
| FBI-UAP-D024 | FD-302, Airborne Lights and Triangle (2002 / interviewed 2023–24) | [PDF](https://www.war.gov/medialink/ufo/release_05/Aug_07/documents/FBI-UAP-D024_FD-302_Airborne-Lights-and-Triangle_2002_2023-2024.pdf) |
| FBI-UAP-D025 | Digital rendering, Airborne Triangle over Bagram, 2002 | [JPG](https://www.war.gov/medialink/ufo/release_05/Aug_07/documents/FBI-UAP-D025_Digital-Rendering_Airborne-Triangle_2002.jpg) |
| FBI-UAP-D026 / D027 | Dark Translucent Triangle, Colorado Springs 2023 (FD-302 + rendering) | [D026](https://www.war.gov/medialink/ufo/release_05/Aug_07/documents/FBI-UAP-D026_FD-302_Dark-Translucent-Triangle_2023.pdf) · [D027](https://www.war.gov/medialink/ufo/release_05/Aug_07/documents/FBI-UAP-D027_Digital-Rendering_Dark-Translucent-Triangle_2023.pdf) |
| FBI-UAP-D028 | FD-302, Dark Triangle with Lights, 2011 | [PDF](https://www.war.gov/medialink/ufo/release_05/Aug_07/documents/FBI-UAP-D028_FD-302_Dark-Triangle-with-Lights_2011.pdf) |
| FBI-UAP-D030 | FD-302, Large Triangle with Red Lights, Colorado Springs 2023 | [PDF](https://www.war.gov/medialink/ufo/release_05/Aug_07/documents/FBI-UAP-D030_FD-302_Large-Triangle-with-Red-Lights_2023.pdf) |
| FBI-UAP-D040 | FD-302, Multiple Red Lights, 2026 | [PDF](https://www.war.gov/medialink/ufo/release_05/Aug_07/documents/FBI-UAP-D040_FD-302_Multiple-Red-Lights_2026.pdf) |
| FBI-UAP-PR007 | Special Agent handheld thermal video, “Slow-moving Objects,” 2026 | [DVIDS](https://www.dvidshub.net/video/1017801) |

#### Historical / diplomatic
| ID | Topic | Link |
|----|-------|------|
| CIA-UAP-D022 | UFO reported near Puerto Rico, 1965 (AD/SA correspondence) | [PDF](https://www.war.gov/medialink/ufo/release_05/Aug_07/documents/CIA-UAP-D022_Unidentified-Flying-Object-Reported-near-Puerto-Rico_1965.pdf) |
| DOS-UAP-D001 / D002 | Diplomatic cables, Brazil, Nov 14 & 20, 1963 | [D001](https://www.war.gov/medialink/ufo/release_05/Aug_07/documents/DOS-UAP-D001_Diplomatic-Cable_Brazil_November-14-1963.pdf) · [D002](https://www.war.gov/medialink/ufo/release_05/Aug_07/documents/DOS-UAP-D002_Diplomatic-Cable_Brazil_November-20-1963.pdf) |
| EOP-UAP-D001 | NASC inquiry into Bahia, Brazil incident, Nov 13, 1963 | [PDF](https://www.war.gov/medialink/ufo/release_05/Aug_07/documents/EOP-UAP-D001_NASC-Inquiry-into-Bahia-Brazil-Incident_November-13-1963.pdf) |
| DOW-UAP-D099 | Intelligence review of “Ghost Rocket” incidents, 1947 | [PDF](https://www.war.gov/medialink/ufo/release_05/Aug_07/documents/DOW-UAP-D099_Intelligence-Review-of-Ghost-Rocket-Incidents_1947.pdf) |
| DOW-UAP-D100 | Air Materiel Command / Project Sign materials, 1947–1948 | [PDF](https://www.war.gov/medialink/ufo/release_05/Aug_07/documents/DOW-UAP-D100_Air-Materiel-Command-Report-on-UFOs_1947-1948.pdf) |

### Mid signal (novelty 5–6/10)

- **DOW-UAP-D098** — Naval Photographic Interpretation Center film analysis, 1953 (Montana/Utah films, 1950/1952) — novelty 6.
- **FBI digital renderings** of triangles / red lights (D029, D031, D038–D042) — artistic interpretations paired with the FD-302s above; useful context, lower novelty than the interview records and thermal video.

---

## News Cycle (since July 31)

12 RSS items analyzed on Aug 7; all classified **CONTEXT**. Themes:

- **Release 05 coverage** — CBS (“Did you see that?”, 41 files; novelty 7) highlights Gulf of Oman / Afghanistan triangle; Gadget Review and others amplify the drop.
- **Whistleblower channel** — NewsNation (novelty 7): July 31 principal deputy DNI memo outlining how UAP whistleblowers can report to AARO / Presidential UAP Task Force without breaching NDAs.
- **Rehashes** — May 8 Release 01 retrospectives (LawStreet novelty 8 on framing; NBC/DoW historic releases), Virginia Beach AARO annual stats (WAVY), Greece IR clip PR34 (DVIDS).
- **Advisory council / prosaic takes** — DefenseScoop / NY Post on Avi Loeb council; Loeb Medium piece arguing DOW-UAP-PR043 is likely a missile (novelty 4).

---

## Cross-Release Comparison

| Release | Date | Files added | Cumulative | Character |
|---------|------|-------------|------------|-----------|
| 01 | May 8, 2026 | ~158 | ~158 | Broad multi-agency opener |
| 02 | May 22, 2026 | ~64 | ~222 | Engagement / transmedium / intel testimony |
| 03 | June 12, 2026 | ~72 | ~294 | FBI domestic + CIA Cold War |
| 04 | July 10, 2026 | 40 | ~334 | Unresolved IR mass + nuclear thread |
| 05 | **Aug 7, 2026** | **41** | **375** | Unresolved CENTCOM/Pacific/ME videos + FBI 2026 triangles/thermal + DoS Brazil |

Release 05 looks like a **hybrid of Release 03 and 04**: another official-unresolved sensor tranche, plus the strongest same-year **FBI eyewitness + thermal** package yet. First appearance of dedicated **DoS** PURSUE document IDs. No new DOE nuclear-site files in this batch.

---

## Suggested Next Steps

1. Manually open the highest-signal PDFs in a browser (war.gov 403’d the headless fetcher): Elder briefing, D032/D033/D037 FD-302s, D101 IIR, Brazil cables.
2. Watch PR117–PR122 (Gulf of Oman) against PR123–PR127 (Pacific 2019) and FBI-UAP-PR007 (2026 thermal).
3. Track whether the July 31 whistleblower memo produces named referrals in later releases.
4. Re-run `uap-signal check` on the next PURSUE cadence (~2–4 weeks) or when warufo indexes Release 06.
