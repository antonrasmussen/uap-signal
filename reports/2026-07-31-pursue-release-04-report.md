# PURSUE Release 04 — UAP Signal Intelligence Report

**Report date:** July 31, 2026  
**Prepared by:** uap-signal automated analysis  
**Subject:** Pentagon PURSUE Release 04 (July 10, 2026) and surrounding news cycle

---

## Executive Summary

On **July 10, 2026**, the Department of War published **PURSUE Release 04** — the fourth batch of declassified UAP materials under the Presidential Unsealing and Reporting System for UAP Encounters. This release adds **40 files**, bringing the cumulative PURSUE archive to **334 files** spanning **82 years**.

Release 04 shifts emphasis toward **officially unresolved military sensor data** and a **nuclear-facility thread**:

| Dimension | Release 01 (May 8) | Release 02 (May 22) | Release 03 (Jun 12) | Release 04 (Jul 10) |
|-----------|-------------------|---------------------|---------------------|---------------------|
| **Focus** | Broad historical sweep | Military engagement footage | FBI/domestic eyewitness | AARO "unresolved" IR + nuclear sites |
| **Standout** | 158–162 files, Apollo | Lake Huron shootdown, transmedium | Mother-orb, Colorado Springs, Hoover | 19 unresolved IR videos, Pantex 2015, Los Alamos 1949 |
| **Avg novelty (primary)** | ~5.1/10 | High (top 8) | ~5.3/10 | ~5.4/10 |
| **Agency emphasis** | Multi-agency | DoW / ODNI | **FBI** | **DoW** (28) + NASA (7) + DOE (2) |

**Three findings dominate this release:**

1. **19 AARO "unresolved" infrared videos (2015–2025)** — Officially unexplained military sensor clips from INDOPACOM (Yellow Sea / East China Sea / South China Sea, including **2025** cases), USNORTHCOM (CONUS/Atlantic), and CENTCOM (Middle East). Largest admitted-unexplained sensor tranche yet.

2. **Nuclear-facility continuity: Los Alamos 1949 → Pantex 2015** — DOE-UAP-D004 (Los Alamos "green fireballs" conference transcript) and DOE-UAP-D005 (Pantex unidentified object, Sept 1, 2015) both scored **8/10** — the highest novelty in this run.

3. **Foundational Cold War studies** — Project Sign progress report (1948), Air Intelligence "Analysis of Flying Object Incidents" (1948/1949), Blue Book SAB review (1966–67), and joint U.S.–Canadian VTOL/UFO files that lean toward prosaic/foreign-tech explanations even as modern IR cases stay unresolved.

News since June 15 is mostly coverage of this drop plus continued reporting on the **UAP Science Advisory Council** (Avi Loeb / White House). No Release 05 yet.

---

## Methodology

| Run | Command / approach | Items analyzed |
|-----|-------------------|----------------|
| News/media sweep | `uap-signal check --date 2026-07-31 --source news_rss --new-only` | 18 new CONTEXT items |
| Primary documents | Custom warufo filter `data-release="04"` + LLM analysis | **40/40** Release 04 items |
| Last prior run | June 15, 2026 (Release 03 report) | — |

Classification: rule-based (`classifier.py`) + LLM summarization/novelty (`analyzer.py`). Scores ≥6 flagged as high-signal.

---

## Release 04: Primary Document Analysis

**Composition (per warufo):** 28 DoW, 7 NASA, 2 CIA, 2 DOE, 1 FBI — by type: 19 videos, 14 PDFs, 4 audio, 3 images. ~48% partially redacted.

### Top signal (novelty 8/10)

#### DOE-UAP-D004 — Los Alamos Conference on Aerial Phenomena, 1949
- **Content:** Transcript of a March 22, 1949 conference at Los Alamos Scientific Laboratory on aerial phenomena ("green fireballs" era).
- **Significance:** Formal scientific convening at the nuclear weapons birthplace; anchors the nuclear-site UAP pattern at the start of the modern era.
- [PDF](https://www.war.gov/medialink/ufo/071026/release_04/documents/DOE-UAP-D004_Los-Alamos-Conference-on-Aerial-Phenomena_1949.pdf)

#### DOE-UAP-D005 — Pantex Unidentified Object Incident Report, 2015
- **Content:** Imagery + incident report for a Sept 1, 2015 unidentified object at/near the Pantex nuclear weapons plant (Texas).
- **Significance:** Closes a 66-year nuclear-facility thread from Los Alamos 1949 to a contemporary DOE site; high national-security relevance.
- [PDF](https://www.war.gov/medialink/ufo/071026/release_04/documents/DOE-UAP-D005_Pantex-Unidentified-Object-Incident-Report_2015.pdf)

### High signal (novelty 6/10)

#### Range Fouler Debriefs — DOW-UAP-D089 / D090 / D091 (2019–2020)
- Navy standardized forms documenting unauthorized objects in Eastern U.S. / Atlantic training ranges.
- [D089](https://www.war.gov/medialink/ufo/071026/release_04/documents/DOW-UAP-D089_Range-Fouler-Debrief_Eastern-US_2020.pdf) | [D090](https://www.war.gov/medialink/ufo/071026/release_04/documents/DOW-UAP-D090_Range-Fouler-Debrief_Eastern-US_2019.pdf) | [D091](https://www.war.gov/medialink/ufo/071026/release_04/documents/DOW-UAP-D091_Range-Fouler-Debrief_Atlantic-Ocean_2020.pdf)

#### Foundational studies
| ID | Topic | Link |
|----|-------|------|
| DOW-UAP-D097 | Project Sign Progress Report, 1948 | [PDF](https://www.war.gov/medialink/ufo/071026/release_04/documents/DOW-UAP-D097_Project-Sign-Progress-Report_1948.pdf) |
| DOW-UAP-D093 / D094 | Air Intel "Analysis of Flying Object Incidents," 1948–49 | [1948](https://www.war.gov/medialink/ufo/071026/release_04/documents/DOW-UAP-D093_Analysis-of-Flying-Object-Incidents-in-the-US_1948.pdf) · [1949](https://www.war.gov/medialink/ufo/071026/release_04/documents/DOW-UAP-D094_Analysis-of-Flying-Object-Incidents-in-the-US_1949.pdf) |
| DOW-UAP-D092 | SAB Ad Hoc Committee reviewing Blue Book, 1966–67 | [PDF](https://www.war.gov/medialink/ufo/071026/release_04/documents/DOW-UAP-D092_DAF-Committee-to-Review-Project-Bluebook_1966-1967.pdf) |
| DOW-UAP-D095 | Joint U.S.–Canadian VTOL projects + UFO reports, 1954–55 | [PDF](https://www.war.gov/medialink/ufo/071026/release_04/documents/DOW-UAP-D095_Joint-US-Canadian-Aviation-Projects-and-UFO-Sighting-Reports_1954-1955.pdf) |

#### NASA STS-80 Unidentified Object Images (1996) — D030 / D031 / D032
- Three stills from Shuttle Columbia astronauts of an unidentified orbital object.
- [D030](https://www.war.gov/medialink/ufo/071026/release_04/documents/NASA-UAP-D030_STS-80-Unidentified-Object-Image1_1996.jpg) | [D031](https://www.war.gov/medialink/ufo/071026/release_04/documents/NASA-UAP-D031_STS-80-Unidentified-Object-Image2_1996.jpg) | [D032](https://www.war.gov/medialink/ufo/071026/release_04/documents/NASA-UAP-D032_STS-80-Unidentified-Object-Image3_1996.jpg)

#### Indo-Pacific unresolved IR videos (2023–2025)
| ID | Location / year | Video |
|----|-----------------|-------|
| DOW-UAP-PR100 | Yellow Sea, 2023 | [DVIDS](https://www.dvidshub.net/video/1014096) |
| DOW-UAP-PR101 | South China Sea, 2024 | [DVIDS](https://www.dvidshub.net/video/1014097) |
| DOW-UAP-PR102 / PR103 | East China Sea, 2024 | [1014098](https://www.dvidshub.net/video/1014098) · [1014099](https://www.dvidshub.net/video/1014099) |
| DOW-UAP-PR104 | Yellow Sea, **2025** | [DVIDS](https://www.dvidshub.net/video/1014101) |
| DOW-UAP-PR105 | East China Sea, **2025** | [DVIDS](https://www.dvidshub.net/video/1014103) |

### Mid signal (novelty 4–5/10)

- **CIA-UAP-D020 / D021** — 1955 unconventional aircraft debrief + analysis (Azerbaijan / Cold War context).
- **CONUS / Atlantic / Gulf unresolved videos** — PR106–PR116, PR113 (1996 Western U.S.), PR115 (Gulf of America 2019); mostly USNORTHCOM/Navy.
- **CENTCOM Middle East** — PR024 / PR030 (2023), novelty 4 (thin extracted detail).
- **Apollo 14/17 debrief audio** — NASA-UAP-D026–D029 (historical; limited UAP-specific detail in extracts).
- **DOW-UAP-D096** — Blue Book correspondence, 1955.
- **FBI-UAP-D014** — Civilian UFO correspondence 1967/1974 (novelty 3).

---

## News Cycle (since June 15)

18 new RSS items analyzed; nearly all **CONTEXT**, novelty 1–3. Themes:

- Coverage of Release 04 (LAmag, People, WAVY Virginia Beach, NewsNation "jellyfish," CBS/NBC earlier batches).
- **UAP Science Advisory Council** — DefenseScoop / PBS on White House pick of Avi Loeb to lead council (continues June storyline).
- NY Post (July 18): Trump UFO advisors claim explanations for most glowing orbs except one recent encounter.

No evidence in feeds of a fifth PURSUE drop.

---

## Cross-Release Comparison

| Release | Date | Files added | Cumulative | Character |
|---------|------|-------------|------------|-----------|
| 01 | May 8, 2026 | ~158 | ~158 | Broad multi-agency opener |
| 02 | May 22, 2026 | ~64 | ~222 | Engagement / transmedium / intel testimony |
| 03 | June 12, 2026 | ~72 | ~294 | FBI domestic + CIA Cold War |
| 04 | July 10, 2026 | **40** | **334** | Unresolved IR mass + nuclear thread |

Release 04 does **not** match Release 02's engagement footage peak, but it is the largest set of **explicitly AARO-unresolved** military IR clips, and the DOE nuclear pair is the clearest continuity narrative across decades.

---

## Suggested Next Steps

1. Spot-check the highest-signal PDFs (Los Alamos conference, Pantex 2015, Project Sign, range foulers) for details the RSS/extractor truncated.
2. Watch a sample of Indo-Pacific 2024–2025 IR clips (PR101–PR105) vs CONUS range-fouler videos.
3. Re-run `uap-signal check` after the next expected PURSUE cadence (~2–4 weeks) or when warufo indexes Release 05.
