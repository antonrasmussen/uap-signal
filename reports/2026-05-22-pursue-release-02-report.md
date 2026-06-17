# PURSUE Release 02 — UAP Signal Intelligence Report

**Report date:** May 22, 2026  
**Prepared by:** uap-signal automated analysis  
**Subject:** Pentagon PURSUE Release 02 — military sensor data and contemporary testimony

---

## Executive Summary

On **May 22, 2026**, the Department of War published **PURSUE Release 02** — the second batch of declassified UAP materials. The release contains **64 files**: approximately **51 military sensor videos**, **6 documents**, and **7 NASA audio files**, spanning decades of observations from CENTCOM, Coast Guard, and intelligence community sources.

Release 02 marked a sharp pivot from Release 01's historical archive toward **contemporary military sensor data and first-hand testimony** from serving officials.

| Dimension | Release 01 (May 8) | Release 02 (May 22) |
|-----------|-------------------|---------------------|
| **Volume** | 162 files | 64 files |
| **Focus** | Historical breadth (1947–2026) | Military sensor footage & intel testimony |
| **Standout** | Apollo footage, Roswell memo, foo fighters | Sandia Base (116 pp), Lake Huron, Iran formation |
| **Avg novelty (primary docs)** | 5.1/10 | **8.0/10** (top item) |
| **Agency emphasis** | Multi-agency (6 agencies) | DoD, CIA, DOE, ODNI |

**Three findings dominate this release:**

1. **Sandia Base nuclear facility UAP reports (1948–1950)** — A 116-page AFSWP document covering **209 sightings** at the Armed Forces Special Weapons Program's Sandia Base, the highest-scoring primary document in the PURSUE program to date (novelty 8/10).

2. **Senior intelligence officer testimony (2025)** — A serving senior U.S. intelligence community official describes **hour-long encounters with orange orbs** near a military helicopter, with orbs that appeared to **chase scrambled fighter jets**.

3. **Military sensor footage catalog** — 51 videos including Lake Huron shootdown (2023), 4-UAP formation over Iran (2022), instant acceleration over Syria (2021), CENTCOM sphere over population center (2020), and Coast Guard infrared near aircraft (2024).

---

## Methodology

This report synthesizes uap-signal analysis from the project database and news coverage:

| Run | Source | Items analyzed |
|-----|--------|----------------|
| Primary documents | `uap-signal check --source warufo` (release_02 path) | 4 PDFs + 3 videos |
| News/media | Google News RSS aggregation | 12+ articles |
| Cross-reference | `uap-signal history --days 30` | Release 02 items in 30-day window |

Classification uses rule-based source trust (`classifier.py`) plus LLM summarization and novelty scoring (`analyzer.py`). Novelty scores range 0–10; items scoring ≥6 are flagged as high-signal.

---

## Release 02: Primary Document Analysis

### Highest-signal document

#### DOW-UAP-D017 — Sandia Base UAP Reports, 1948–1950 (8/10)
- **Agency:** Armed Forces Special Weapons Program (AFSWP)
- **Pages:** 116
- **Sightings:** 209 documented UAP reports
- **Content:** General correspondence covering UAP reports at Sandia Base during 1948–1950. Sandia was a critical nuclear weapons facility during the early Cold War; AFSWP managed nuclear weapons operations immediately post-WWII.
- **Significance:** UAP activity at a top-tier nuclear weapons facility during the formative years of the U.S. nuclear program. **Highest novelty score of any primary document analyzed in the PURSUE program to date.**
- [PDF](https://www.war.gov/medialink/ufo/052226/release_02/documents/DOW-UAP-D017_General_Correspondence_Of_Sandia.pdf)

### Moderate-signal documents

#### CIA-UAP-D001 — USSR Intelligence Report, 1973 (4/10, rehash)
- CIA Intelligence Information Report concerning UAP-related activities in the USSR. Demonstrates Cold War-era HUMINT interest in Soviet UAP incidents.
- [PDF](https://www.war.gov/medialink/ufo/052226/release_02/documents/CIA-UAP-D001_Intelligence_Information_Report_USSR_1973.pdf)

#### DOE-UAP-D001 — Pantex Radar Imagery (3/10, rehash)
- Incident report from Pantex nuclear weapons assembly/disassembly plant documenting an unidentified object on ground surveillance radar, with enhanced imagery.
- **Significance:** Continues the nuclear-facility UAP pattern seen in Sandia Base documents.
- [PDF](https://www.war.gov/medialink/ufo/052226/release_02/documents/DOE-UAP-D001_PANTEX_Image.pdf)

#### ODNI-UAP-D001 — Senior USIC Official Narrative (2/10, rehash)
- First-hand account from a senior U.S. intelligence official serving as of May 2026 regarding UAP experiences. Content truncated in extraction.
- [PDF](https://www.war.gov/medialink/ufo/052226/release_02/documents/ODNI-UAP-D001_USPER_Narrative_Senior_USIC.pdf)

### Video evidence

| ID | Title | Date | Novelty | Description |
|----|-------|------|---------|-------------|
| DOW-UAP-PR050 | 4 UAP Formation, Iran | Aug 26, 2022 | **7/10** | Military aircraft witnessed 4 UAPs in formation over water near Iran. Eight House Reps requested access March 6, 2026. |
| NASA-UAP-D008 | Apollo 12 Medical Debriefing, Tape 12 | 1969 | **7/10** | Medical debriefing of Conrad, Gordon, Bean — may contain UAP-related mission observations. |
| FBI-UAP-PR004 | "Northeastern Orb Sighting" | Jul 2025 | 4/10 | Eyewitness reported intense bright light in backyard ~9 PM. Most recent catalog entry at time of release. |

- [DOW-UAP-PR050 Video](https://www.dvidshub.net/video/1007706)
- [NASA-UAP-D008 Video](https://www.dvidshub.net/video/1007870)
- [FBI-UAP-PR004 Video](https://www.dvidshub.net/video/1010269)

---

## Military Sensor Footage — Deep Dive

Synthesized from news coverage of the 51 videos in Release 02:

### Lake Huron Shootdown — February 2023
- Video appears to show the February 2023 Lake Huron shootdown incident
- Context: Post-Chinese spy balloon heightened airspace alert; F-16 engagement during a period of elevated NORAD activity
- **Significance:** Places a high-profile airspace incident in the PURSUE catalog; identity of the object remains contested in public reporting.

### Persian Gulf / Iran Formation — 2019–2022
- Military infrared footage showing UAP formations over the Persian Gulf and Iran (2019–2022)
- **DOW-UAP-PR050** specifically documents 4 UAPs in formation over water near Iran, August 26, 2022
- Congressional oversight: 8 House Representatives requested access to 51 UAP records including this video (March 6, 2026)

### Syria Instant Acceleration — 2021
- Footage showing object exhibiting rapid/instant acceleration over Syria
- Reported by CENTCOM to AARO

### CENTCOM Sphere — 2020
- Video of a sphere over a population center in CENTCOM area of operations

### Coast Guard Infrared — 2024
- Coast Guard infrared footage of an object near a plane over the southeastern United States

### Submarine Interaction — 2022
- Video from 2022 showing spherical objects entering and exiting water near a submarine

### Eight-Pointed Star — 2013
- 1:46 infrared military video showing eight-pointed star-shaped object moving in and out of frame
- Reported by CENTCOM to AARO; gained significant media attention (KTTC, White House sharing)

---

## Senior Intelligence Officer Testimony — Deep Dive

The most politically significant new material in Release 02:

### Account details (from news synthesis)
- **Source:** Serving senior U.S. intelligence community official (USIC), as of May 2026
- **Date:** Late 2025 helicopter mission
- **Duration:** Hour-long encounters
- **Objects:** Oval-shaped orange UAPs with bright white/yellow centers
- **Behavior:** Orbs appeared to **chase fighter jets** scrambled to investigate
- **Document:** ODNI-UAP-D001 (written narrative); content truncated in uap-signal extraction

### Why it matters
- First contemporary first-hand testimony from a **currently serving** senior intelligence official
- Describes pursuit/evasion behavior not attributed to known technology
- Released alongside 51 sensor videos, giving the testimony visual corroboration context
- AARO maintains no evidence of extraterrestrial origin despite unresolved cases

---

## NASA Audio Files

Release 02 included **7 NASA audio files** — astronaut voice recordings from Mercury and Apollo missions:

| Item | Description |
|------|-------------|
| NASA-UAP-D008 | Apollo 12 medical debriefing, Tape 12 (1969) — novelty 7/10 |
| Apollo 11 references | Buzz Aldrin "bright light source" observation (covered in Fortune, Release 01/02 news cycle) |
| Mercury missions | Voice loops from early space program |

The Guardian noted Neil deGrasse Tyson's caution against conflating declassified military sensor data with non-classified NASA recordings.

---

## News & Media Landscape (May 22, 2026)

### Highest-signal coverage

| Score | Outlet | Headline |
|-------|--------|----------|
| **4** | KTTC | [Star-shaped UFO spotted in newly released video](https://www.kttc.com/2026/05/20/star-shaped-ufo-spotted-newly-released-video/) |
| **3** | CBS News | [Pentagon releases more UFO files: "Speechless after these observations"](https://www.cbsnews.com/news/ufo-files-pentagon-videos-documents/) |
| **3** | ABC News | [Intelligence officer's account of seeing 'orbs'](https://abcnews.com/US/pentagon-releases-declassified-ufo-files-including-intelligence-officers/story?id=133209645) |
| **3** | The Guardian | [Second batch of UFO videos and first-hand testimony](https://www.theguardian.com/world/2026/may/22/pentagon-ufo-videos-testimony-documents) |
| **3** | Good Morning America | [Declassified UFO files including intelligence officer's orbs account](https://www.goodmorningamerica.com/news/story/pentagon-releases-declassified-ufo-files-including-intelligence-officers-133209645) |
| **3** | MeriTalk | [Pentagon Releases Second Batch of UAP Files](https://www.meritalk.com/articles/pentagon-releases-second-batch-of-uap-files/) |
| **3** | IBTimes | [Newly Declassified Pentagon UFO Records](https://www.ibtimes.com/newly-declassified-pentagon-ufo-records-reveal-videos-pilot-reports-unexplained-sightings-3803214) |

### Public interest metrics

- WAR.GOV/UFO exceeded **1 billion hits** since launching May 8, 2026 (per MeriTalk)
- Pentagon signaled a **third release** was planned
- Mainstream morning television (GMA) coverage reached mass audiences with firsthand military testimony

### Official framing

- Pentagon: no evidence of extraterrestrial origin
- Many materials acknowledged to lack substantiated chain of custody
- AARO: many cases remain unresolved despite investigations

---

## Cross-Release Comparison

### How Release 02 changed the narrative

```
Release 01 (May 8)              Release 02 (May 22)
─────────────────               ───────────────────
"Here's our archive"            "Here's what our sensors saw"
Historical documents            Military IR/FLIR video
1940s–2020s breadth             2013–2025 sensor focus
Archival research value         Operational national security value
```

Release 02 shifted PURSUE from an archival exercise to a **national security transparency** program. The senior IC officer testimony and CENTCOM sensor footage framed UAP as a live operational concern, not just a historical curiosity.

### Nuclear facility pattern

Release 02 reinforced a pattern first visible in Release 01:
- **Sandia Base** (1948–1950): 209 sightings, 116 pages — novelty 8/10
- **Pantex** (undated): Radar detection at nuclear assembly plant — novelty 3/10

---

## Key Themes

### 1. Sensor data goes public
51 military videos represent the largest release of U.S. military UAP sensor footage in history. CENTCOM, Coast Guard, and submarine-mounted systems are represented.

### 2. Contemporary testimony breaks new ground
The senior USIC official narrative is the first released account from a currently serving intelligence community leader describing personal UAP encounters during active duty.

### 3. Nuclear sites as UAP hotspots
Sandia Base (209 sightings) and Pantex radar detection add to a growing body of evidence that anomalous aerial activity clusters around nuclear weapons infrastructure.

### 4. Congressional oversight intensifies
Eight House Representatives formally requested access to 51 UAP records (including the Iran formation video) on March 6, 2026, signaling legislative interest beyond executive-branch disclosure.

---

## What to Watch

| Item | Why |
|------|-----|
| **Third PURSUE release** | Pentagon has signaled another batch is planned (per MeriTalk) |
| **Senior IC officer testimony** | Full ODNI-UAP-D001 narrative may draw further congressional scrutiny |
| **Iran formation video** | Congressional request for access to 51 records may force additional declassification |
| **Chain of custody gaps** | Pentagon acknowledged many materials lack substantiated provenance — independent verification ongoing |

---

## Data Summary

| Metric | Value |
|--------|-------|
| Total files in release | 64 (51 videos, 6 docs, 7 audio) |
| Primary docs analyzed | 4 PDFs + 3 videos |
| Items scoring novelty ≥6 | 1 (Sandia Base, 8/10) |
| Items scoring novelty ≥7 | 3 (Sandia, Iran formation, Apollo 12) |
| Highest novelty (primary) | **8/10** (highest in PURSUE program to date) |
| Classification breakdown | 1 genuinely new (8/10), 3 rehash |
| WAR.GOV/UFO traffic | >1 billion hits (cumulative with Release 01) |

---

## Appendix: All Release 02 Primary Documents Analyzed

| ID | Title | Novelty | Classification |
|----|-------|---------|----------------|
| DOW-UAP-D017 | Sandia Base UAP Reports, 1948–1950 | **8** | GENUINELY_NEW |
| DOW-UAP-PR050 | 4 UAP Formation, Iran, Aug 2022 | **7** | GENUINELY_NEW |
| NASA-UAP-D008 | Apollo 12 Medical Debriefing, 1969 | **7** | GENUINELY_NEW |
| FBI-UAP-PR004 | Northeastern Orb Sighting, 2025 | 4 | GENUINELY_NEW |
| CIA-UAP-D001 | USSR Intelligence Report, 1973 | 4 | REHASH |
| DOE-UAP-D001 | Pantex Radar Imagery | 3 | REHASH |
| ODNI-UAP-D001 | Senior USIC Official Narrative | 2 | REHASH |

---

*Generated by [uap-signal](https://github.com/) — automated UAP release analysis. Scores and summaries are LLM-assisted and should be verified against primary sources.*
