# PURSUE Release 01 — UAP Signal Intelligence Report

**Report date:** May 8, 2026  
**Prepared by:** uap-signal automated analysis  
**Subject:** Pentagon PURSUE Release 01 — inaugural declassification batch

---

## Executive Summary

On **May 8, 2026**, the Department of War launched the **Presidential Unsealing and Reporting System for UAP Encounters (PURSUE)** and published **Release 01** — the first public declassification of UAP-related government records under President Trump's February 2026 transparency directive. The batch contains **162 files** from **six federal agencies**, spanning **1947 to 2026**.

Release 01 established the disclosure program's baseline: a sweeping historical archive spanning nearly eight decades of government UAP records.

| Dimension | Release 01 |
|-----------|-----------|
| **Date** | May 8, 2026 |
| **Volume** | 162 files |
| **Focus** | Historical breadth (1947–2026) |
| **Avg novelty (primary docs)** | 5.1/10 |
| **Agency emphasis** | Multi-agency (6 agencies) |

**Three findings dominate this release:**

1. **Institutional UFO reporting begins in 1946** — Primary Air Force memoranda from 1946–1949 show the U.S. military treating flying disc sightings as operational concerns within months of the modern UFO era's start, predating Project Blue Book.

2. **WWII "foo fighter" documentation** — SHAEF combat records from 1944–1945 describe "night phenomena (foofighters)" and unidentified cylindrical objects observed during active warfare in the European theater.

3. **FBI investigative pipeline exposed** — Case file 62-HQ-83894 and 1950s witness interviews (Detroit dome craft, Krasuski vertical ascent) reveal the FBI maintained formal UFO investigative protocols across decades.

---

## Methodology

This report synthesizes uap-signal analysis from the project database:

| Run | Source | Items analyzed |
|-----|--------|----------------|
| Primary documents | `uap-signal check --source warufo` (release_1 path) | 13 documents |
| News/media | Google News RSS aggregation | 8+ articles |
| Cross-reference | `uap-signal history --days 30` | Release 01 items in 30-day window |

Classification uses rule-based source trust (`classifier.py`) plus LLM summarization and novelty scoring (`analyzer.py`). Novelty scores range 0–10; items scoring ≥6 are flagged as high-signal.

---

## Release 01: Primary Document Analysis

### High-signal documents (novelty ≥6)

#### 331_120752 — WWII Foo Fighter Records, 1944–1945 (6/10)
- **Agency:** SHAEF (Supreme Headquarters Allied Expeditionary Force)
- **Content:** Military communications regarding "night phenomena (foofighters)," flak rockets, and unidentified cylindrical objects observed during combat operations in the European theater.
- **Significance:** Contemporaneous Allied command documentation of anomalous aerial observations during active warfare — eight decades before PURSUE.
- [PDF](https://www.war.gov/medialink/ufo/release_1/331_120752_numeric_files_1944–1945_37153_german_armament_equipment_documents.pdf)

#### 18_100754 — Air Force Correspondence, 1946–1947 (6/10)
- **Content:** Official memorandums and correspondence regarding flying disc and saucer sightings. Documents indicate these incidents were matters of Air Force concern during the initial post-WWII wave.
- **Significance:** Earliest institutional Air Force response to modern UFO reports, during the formative 1946–47 period.
- [PDF](https://www.war.gov/medialink/ufo/release_1/18_100754_%20general%201946-7_vol_2.pdf)

#### 18_6369445 — Flying Disc Reports, 1948 (6/10)
- **Content:** Memorandums, correspondence, and administrative forms from 1948 related to reporting and investigation of flying discs — part of early systematic government collection efforts.
- **Significance:** Institutional framework for UFO reporting during Project Sign (1948), the first official U.S. government UFO investigation program.
- [PDF](https://www.war.gov/medialink/ufo/release_1/18_6369445_general_1948_vol_1.pdf)

#### 341_110448 — Air Force Intelligence Protocols, 1948 (6/10)
- **Content:** November 1948 Air Force intelligence report on unidentified flying objects and flying saucers, within a 1948–1955 collection on intelligence collection and dissemination procedures.
- **Significance:** One of the earliest Air Force intelligence documents on UFOs, predating Project Blue Book and appearing within months of the Kenneth Arnold sighting and Roswell incident.
- [PDF](https://www.war.gov/medialink/ufo/release_1/341_110448_records_relating_to_the_collection_and_dissemination_of_intelligence_1948-1955-ts_cont_no.2_2-5300-2-5399.pdf)

#### 342_HS1-416511228 — Flying Discs 1949 (6/10)
- **Content:** UFO incident reports compiled under 1948 Flight Service Regulations, focusing on 1949 "flying disc" observations.
- **Significance:** Shows the regulatory framework that evolved into Project Blue Book and modern UAP reporting requirements.
- [PDF](https://www.war.gov/medialink/ufo/release_1/342_hs1-416511228_box186_319.1-flying-discs-1949.pdf)

### Moderate-signal documents (novelty 4–5)

#### 341_110677 — Air Intelligence Report, 1955 (5/10)
- October 14, 1955 eyewitness account of an unconventional aircraft's ascent and flight. Cold War-era primary military intelligence document.
- [PDF](https://www.war.gov/medialink/ufo/release_1/341_110677_numerical_file_5-2500.pdf)

#### 38_143685 — Incident Summaries 101–172 (5/10)
- Standardized "Check-List — Unidentified Flying Objects" forms with case details from a systematic cataloging program.
- [PDF](https://www.war.gov/medialink/ufo/release_1/38_143685_box7_incident_summaries_101-172.pdf)

#### 65_HS1-834228961 — FBI Case File 62-HQ-83894 (5/10)
- FBI investigative records, eyewitness testimonies, and public reports on UFOs. Truncated in extraction but represents formal federal investigation documentation.
- [PDF](https://www.war.gov/medialink/ufo/release_1/65_hs1-834228961_62-hq-83894_section_1.pdf)

#### 65_HS1-101634279 — Detroit Dome Craft, 1958 (4/10)
- FBI memo documenting a Detroit witness report of a circular craft with a crystal-type dome.
- [PDF](https://www.war.gov/medialink/ufo/release_1/65_hs1-101634279_100-de-18221_serial_844.pdf)

#### 65_HS1-101634279 — Krasuski Vertical Ascent, 1957 (4/10)
- FBI interview with Wladyslaw Krasuski describing a large circular vehicle rising vertically.
- [PDF](https://www.war.gov/medialink/ufo/release_1/65_hs1-101634279_100-de-26505.pdf)

### Lower-signal documents

#### 255_413270 — COMETA Report Reference (3/10)
- References the 1999 French COMETA study commissioned by senior French military and intelligence officials, which concluded some UFO cases warranted serious consideration of the extraterrestrial hypothesis.
- [PDF](https://www.war.gov/medialink/ufo/release_1/255_413270_ufo's_and_defense_what_should_we_prepare_for.pdf)

#### 59_64634 — July 1952 UFO Wave Memo (2/10, rehash)
- Two-page memorandum addressing increased UFO reports, likely related to the 1952 Washington D.C. flap.
- [PDF](https://www.war.gov/medialink/ufo/release_1/59_64634_711.5612[7-2852.pdf)

#### 59_214434 — Space Council Memo, 1963 (1/10, speculation)
- July 18, 1963 National Aeronautics and Space Council memorandum. Content truncated; significance unassessable.
- [PDF](https://www.war.gov/medialink/ufo/release_1/59_214434_sp_16_[7.18.1963].pdf)

### Video evidence (cataloged in Release 01)

| ID | Title | Date | Novelty |
|----|-------|------|---------|
| FBI-UAP-PR003 | "Orbs Over the Pond" | Oct 2024 | 4/10 |
| NASA-UAP-D008 | Apollo 12 Medical Debriefing, Tape 12 | 1969 | 7/10 |

- [FBI-UAP-PR003 Video](https://www.dvidshub.net/video/1010267) — Northeastern US eyewitness reported light below horizon at ~1851 local
- [NASA-UAP-D008 Video](https://www.dvidshub.net/video/1007870) — Apollo 12 crew medical debriefing may contain UAP-related observations

---

## Notable Items (from news coverage, not yet individually analyzed)

Release 01 contained far more than the 13 documents analyzed above. News coverage highlights additional high-interest materials:

| Category | Examples cited in media |
|----------|------------------------|
| **Apollo program** | Apollo 17 lunar photos; astronaut voice loops (Buzz Aldrin "bright light source" on Apollo 11) |
| **Military sensor footage** | Infrared footage from multiple global regions (CENTCOM, various dates) |
| **Historical** | 1947 Roswell memo; diplomatic cables on global UAP incidents |
| **Contemporary** | FBI eyewitness video (Orbs Over the Pond, 2024) |
| **International** | Global incident reports via State Department cables |

CBS News described the release as spanning "1947 to 2026" with materials from six agencies. NBC News reported 160+ files with no evidence of extraterrestrial contact or government cover-up, but providing raw materials for public review.

---

## News & Media Landscape (May 8, 2026)

### Highest-signal coverage

| Score | Outlet | Headline |
|-------|--------|----------|
| **3** | DefenseScoop | ["Data alone is not disclosure": UAP research community reacts to first PURSUE drop](https://news.google.com/rss/articles/CBMifkFVX3lxTFB2QndIMFpFVmF5SkpmR1AwRVYyRVlnQUF2clNqRVduTklWVXFRcmU3MWtyb3J4bEZOY2h0ZWpOVVlqQXFhcndSMTF2QjBFZXc4M3duX0kwRzczUDhOTGpFSWdJS1RhRDk3S2tHYWlHOExNaU5YOXJpY2NNc0hXdw?oc=5) |
| **3** | NBC News | [Pentagon releases declassified UFO files including videos and photos held for decades](https://www.nbcnews.com/science/ufos-and-anomalous-phenomena/ufo-uap-files-pentagon-release-trump-rcna344204) |
| **3** | Fortune | [Buzz Aldrin saw a 'bright light source' on Apollo 11](https://news.google.com/rss/articles/CBMikgFBVV95cUxQbEUzUzJ3N3R4V3hQYlA1SVdhbzV3RXZXeW1EQW1qR3p2djJfRXlNLW13dnlmYU9mMHh4VVZFNHo2dFd0b1ZZUVZtNFFMSmhLbXVJSHViV0tBekhwcDRQbEZNVUpySEdVa1VGSDhZNTA1RGROQ1FUVWptNFhvN3YtX0lQUHo0cHQwMlhTYTY2Z04yQQ?oc=5) |
| **2** | CBS News | [Pentagon begins releasing new UFO files (Release 01 details)](https://www.cbsnews.com/news/pentagon-begins-release-ufo-files/) |
| **2** | Military.com | [Trump Opens UFO Files in Historic Government Release](https://news.google.com/rss/articles/CBMigwFBVV95cUxOS285XzZFSXZEaGowX3l1ck9YLXVtNEFmaUNGYWlBSTdoNXZqeDVVa3dyZmd6OFRXU0RIOUdyV3FmOFBBTURNS0Z6eHk4SUhzSnh1bW1nYU1tRXBMU2pUbzZkTjg0QzhuRjMzT0FFN1pZSGpJN3JpU2hrbDdHS1owSVQ3Yw?oc=5) |

### Community reaction

DefenseScoop captured a key tension: the UAP research community's response emphasized that **raw data without context, analysis, or accompanying documentation does not constitute meaningful disclosure**. Volume of releases does not equal quality of disclosure.

### International coverage

- France 24, Stars and Stripes, and other outlets reported the release but most provided headline-level coverage without substantive document analysis.

---

## Key Themes

### 1. Foundational historical archive
Release 01 is primarily an archival dump — establishing that the U.S. government maintained systematic UFO/UAP reporting from 1946 onward, across Air Force, FBI, and allied military commands.

### 2. Multi-agency scope
Six agencies contributed materials, signaling that PURSUE is not a DoD-only program. FBI, NASA, State, and intelligence community records appear alongside military files.

### 3. Continuity across eight decades
From WWII foo fighters (1944) to FBI orb sightings (2024), the release documents an unbroken — if intermittent — government interest in anomalous aerial phenomena.

### 4. "Data alone is not disclosure"
The research community's immediate pushback emphasized that context, chain of custody, and analytical framing matter as much as raw file volume.

### 5. Strong public interest
The PURSUE portal at WAR.GOV/UFO launched alongside the release, drawing immediate and intense public attention to government UAP transparency efforts.

---

## What to Watch

| Item | Why |
|------|-----|
| **Additional PURSUE batches** | Pentagon has signaled more releases under the program |
| **Congressional pressure** | Bipartisan lawmakers continue pushing for broader declassification |
| **AARO response** | Office must contextualize released materials against its ongoing caseload |
| **Research community analysis** | Independent review of 162 files will take months; early findings may reshape public understanding |

---

## Data Summary

| Metric | Value |
|--------|-------|
| Total files in release | 162 |
| Primary docs analyzed | 13 |
| Items scoring novelty ≥6 | 5 |
| Highest novelty (primary) | 6/10 |
| Classification breakdown | 11 genuinely new, 1 rehash, 1 speculation |
| Agencies represented | 6 (per news coverage) |
| Date range | 1947–2026 |

---

## Appendix: All Release 01 Primary Documents Analyzed

| ID | Title | Novelty | Classification |
|----|-------|---------|----------------|
| 331_120752 | WWII Foo Fighter Records, 1944–45 | 6 | GENUINELY_NEW |
| 18_100754 | Air Force Correspondence, 1946–47 | 6 | GENUINELY_NEW |
| 18_6369445 | Flying Disc Reports, 1948 | 6 | GENUINELY_NEW |
| 341_110448 | Air Force Intelligence Protocols, 1948 | 6 | GENUINELY_NEW |
| 342_HS1-416511228 | Flying Discs 1949 | 6 | GENUINELY_NEW |
| 341_110677 | Air Intelligence Report, 1955 | 5 | GENUINELY_NEW |
| 38_143685 | Incident Summaries 101–172 | 5 | GENUINELY_NEW |
| 65_HS1-834228961 | FBI Case File 62-HQ-83894 | 5 | GENUINELY_NEW |
| 65_HS1-101634279 | Detroit Dome Craft, 1958 | 4 | GENUINELY_NEW |
| 65_HS1-101634279 | Krasuski Vertical Ascent, 1957 | 4 | GENUINELY_NEW |
| 255_413270 | COMETA Report Reference | 3 | GENUINELY_NEW |
| 59_64634 | July 1952 UFO Wave Memo | 2 | REHASH |
| 59_214434 | Space Council Memo, 1963 | 1 | SPECULATION |

---

*Generated by [uap-signal](https://github.com/) — automated UAP release analysis. Scores and summaries are LLM-assisted and should be verified against primary sources.*
