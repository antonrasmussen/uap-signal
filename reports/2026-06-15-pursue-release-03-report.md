# PURSUE Release 03 — UAP Signal Intelligence Report

**Report date:** June 15, 2026  
**Prepared by:** uap-signal automated analysis  
**Subject:** Pentagon PURSUE Release 03 (June 12, 2026) and surrounding news cycle

---

## Executive Summary

On **June 12, 2026**, the Department of War published **PURSUE Release 03** — the third batch of declassified UAP materials under the Presidential Unsealing and Reporting System for UAP Encounters. This release contains **72 items** spanning **1949–2025**: 53 documents, 10 images, 6 videos, and 3 audio recordings from multiple agencies (FBI, CIA, DoD, ICA).

Release 03 marks a **strategic shift** in the disclosure program:

| Dimension | Release 01 (May 8) | Release 02 (May 22) | Release 03 (Jun 12) |
|-----------|-------------------|---------------------|---------------------|
| **Focus** | Broad historical sweep (1947–2026) | Military sensor footage & intel testimony | FBI/law-enforcement eyewitness accounts |
| **Standout** | 162 files, Apollo footage, global incidents | Sandia Base (116 pp), Lake Huron shootdown, Iran formation | Mother-orb incident, Colorado Springs cluster, Hoover FBI correspondence |
| **Avg novelty (primary docs)** | 5.1/10 | 8.0/10 (top item) | 5.3/10 |
| **Agency emphasis** | Multi-agency (6 agencies) | DoD, CIA, DOE, ODNI | **FBI** (contemporary domestic cases) |

**Three findings dominate this release:**

1. **The "mother orb" incident (Oct 2023)** — Federal law enforcement near Cheyenne Mountain, Colorado observed orange "mother orbs" releasing smaller red orbs over two days. AARO's June 2025 summary describes anomalous coordinated motion; one orb hovered silently for hours. **No video or sensor data was collected.** AARO states ~40% of UAP cases remain unexplained.

2. **FBI enters the disclosure pipeline** — Release 03 is the first batch to prominently feature FBI investigative forms (FD-1057, FD-302) for **contemporary domestic UAP cases**, including unresolved 2022 Colorado Springs reports and **2026 northeastern orb sightings** filed this year.

3. **UAP Science Advisory Council announced** — Avi Loeb reports being tasked by the White House, AARO, ODNI, FBI, and the Intelligence Community to lead an **11-person scientific advisory body** — the first formal integration of academic science into the federal UAP investigation apparatus.

---

## Methodology

This report synthesizes two uap-signal analysis runs:

| Run | Command | Items analyzed |
|-----|---------|----------------|
| News/media sweep | `uap-signal check --date 2026-06-15` | 25 items (23 new, 2 cached) |
| Primary documents | `uap-signal check --source warufo --date 2026-06-15 --new-only` | 22 new primary docs |
| Historical context | `uap-signal history --days 30` | 83 total items in 30-day window |

Classification uses rule-based source trust (`classifier.py`) plus LLM summarization and novelty scoring (`analyzer.py`). Novelty scores range 0–10; items scoring ≥6 are flagged as high-signal.

---

## Release 03: Primary Document Analysis

### New in Release 03 (genuinely new, novelty ≥4)

#### CIA-UAP-017 — Harare Airport Alert (6/10)
- **Date:** July 2008
- **Content:** CIA report documenting a UFO sighting at Harare International Airport, Zimbabwe. Officials debated whether the sighting represented aggressive foreign posturing, triggering heightened alert status.
- **Significance:** Demonstrates UAP encounters triggering real-time operational security responses at international airports.
- [PDF](https://www.war.gov/medialink/ufo/061226/release_03/documents/CIA-UAP-017_Placement_on_High_Alert_Due_to_Perceived_Aggressive_Foreign_Posturing.pdf)

#### DOW-UAP-D084 — US Army Flying Saucer Study, 1949 (6/10)
- **Content:** Formal Army evaluation study of flying saucers prepared for Plans & Operations Division during the initial post-WWII sighting wave.
- **Significance:** Institutional-level military analytical engagement within two years of the modern UFO era's beginning.
- [PDF](https://www.war.gov/medialink/ufo/061226/release_03/documents/DOW-UAP-D084_USArmy-Flying-Saucer-Study_1949.pdf)

#### FBI-UAP-D002 — Colorado Springs UAP Report, 2022 (6/10)
- **Content:** FBI FD-1057 investigative activity form documenting an **unresolved** UAP incident in Colorado Springs, 2022.
- **Significance:** FBI treats UAP as legitimate investigative matters requiring standardized protocols. Colorado Springs hosts NORAD, Space Command, and Schriever SFB.
- [PDF](https://www.war.gov/medialink/ufo/061226/release_03/documents/FBI-UAP-D002_FD-1057_Unresolved-UAP-Report_ColoradoSprings_2022.pdf)

#### FBI-UAP-D011 — Hoover Correspondence, 1949 (6/10)
- **Content:** 1949 correspondence between FBI Director J. Edgar Hoover and other officials regarding UAP matters.
- **Significance:** Primary source showing highest-level law enforcement interagency coordination during peak early Cold War UFO activity.
- [PDF](https://www.war.gov/medialink/ufo/061226/release_03/documents/FBI-UAP-D011_DFBI-Correspondence-Referral_1949.pdf)

#### FBI-UAP-D009 / D010 — Northeastern Orb Sightings, 2026 (4–5/10)
- **Content:** FBI FD-302 witness interview forms documenting **February 2026** orb sightings in the northeastern United States.
- **Significance:** Contemporary UAP reports filed and investigated by the FBI **this year**, declassified within months under PURSUE.
- [D009 PDF](https://www.war.gov/medialink/ufo/061226/release_03/documents/FBI-UAP-D009_FD-302-67_Northeastern-Orb-Sighting_2026.pdf) | [D010 PDF](https://www.war.gov/medialink/ufo/061226/release_03/documents/FBI-UAP-D010_FD-302-71_Northeastern-Orb-Sighting_2026.pdf)

#### FBI-UAP-D003 — Colorado Springs Digital Rendering, 2022 (4/10)
- **Content:** Artistic rendering of the unresolved 2022 Colorado Springs UAP incident.
- [PDF](https://www.war.gov/medialink/ufo/061226/release_03/documents/FBI-UAP-D003_Digital-Rendering_Unresolved-UAP-Report_ColoradoSprings_2022.pdf)

#### ICA-UAP-D001 — Colorado Springs Analysis, 2022 (3/10, rehash)
- **Content:** Intelligence Community partner analysis of the 2022 Colorado Springs incident provided to AARO. Content truncated in extraction.
- [PDF](https://www.war.gov/medialink/ufo/061226/release_03/documents/ICA-UAP-D001_Analysis_Colorado-Springs-UAP-Incident.pdf)

### FBI Video Evidence (from earlier releases, re-indexed)

| ID | Title | Date | Description |
|----|-------|------|-------------|
| FBI-UAP-PR003 | "Orbs Over the Pond" | Oct 2024 | Eyewitness in northeastern US reported light below horizon at ~1851 local |
| FBI-UAP-PR004 | "Northeastern Orb Sighting" | Jul 2025 | Intense bright light in backyard ~9 PM local — one of the most recent items in the catalog |

- [PR003 Video](https://www.dvidshub.net/video/1010267)
- [PR004 Video](https://www.dvidshub.net/video/1010269)

---

## The Mother Orb Incident — Deep Dive

The single most-covered story from Release 03. Synthesized from multiple news sources and AARO reporting:

### Timeline
- **October 2023:** Federal law enforcement officials near **Cheyenne Mountain**, Colorado (home to NORAD) observe luminous orange "mother orbs"
- Over **two days**, the larger orbs appear to release smaller red orbs
- One red orb hovers silently for **multiple hours**
- Red orbs exhibit **anomalous coordinated horizontal motion** and altitude changes per AARO's June 2025 summary
- **No video, photographic, or technical sensor data** was collected

### Related: Fort Carson / Cheyenne Mountain, 2022
- Five soldiers reported a white **potato-shaped object** with articulating panels that appeared to "cloak" near Cheyenne Mountain
- Case remains **unresolved** despite a low-confidence conventional explanation

### AARO Position (June 5, 2026 report, Dr. Jon Kosloski)
- **~40% of reported UAP phenomena remain unexplained**
- No single known U.S. system fully explains the reported phenomena
- Describes the orange "mother orb" launching smaller red orbs

### Colorado Springs Cluster
Release 03 groups multiple documents around the Colorado Springs area (NORAD/Space Command):
- FBI FD-1057 unresolved report (2022)
- Digital rendering (2022)
- ICA partner analysis (2022)
- Fort Carson soldier testimony (2022)

This geographic clustering around critical command infrastructure is a recurring pattern across all three PURSUE releases.

---

## News & Media Landscape (June 15, 2026)

### Highest-signal coverage (novelty ≥6)

| Score | Outlet | Headline |
|-------|--------|----------|
| **8** | Avi Loeb / Medium | [UAP Science Advisory Council announced](https://avi-loeb.medium.com/a-uap-science-advisory-council-to-the-u-s-f7262e57b0df) |
| **6** | NY Post | [Feds baffled by orbs launching other orbs near Cheyenne Mountain](https://nypost.com/2026/06/12/us-news/feds-baffled-by-sighting-of-orbs-launching-other-orbs-in-western-us-ufo-files/) |
| **6** | Yahoo/Fox | [Mother orb releasing smaller objects, remains unexplained](https://www.yahoo.com/news/science/articles/pentagon-ufo-files-describe-mother-154015880.html) |
| **6** | SOFX | [Third release exposes gap between debunking and disclosure](https://www.sofx.com/pentagons-third-uap-release-exposes-gap-between-debunking-and-disclosure/) |
| **6** | Avi Loeb / Medium | [UAP Disclosure #3 is the most intriguing release thus far](https://avi-loeb.medium.com/uap-disclosure-3-is-most-intriguing-release-thus-far-e4643013245b) |
| **4** | CBS News | [Pentagon releases 3rd batch: 53 docs, 10 images, 6 videos, 3 audio](https://www.cbsnews.com/news/ufo-files-pentagon-3rd-release-documents-videos/) |

### Moderate coverage (novelty 3–4)

- **David Grusch** returning to Capitol Hill Tuesday for bipartisan press conference demanding further disclosure ([LAmag](https://lamag.com/politics/ufo-whistleblower-david-grusch-returns-to-capitol-hill-tuesday/))
- **Release 02 recap** articles still circulating (MeriTalk, GMA, IBTimes)
- **Fact-check framing:** "unidentified ≠ alien" ([The National News Desk](https://thenationaldesk.com/news/fact-check-team/fact-check-team-pentagon-releases-new-ufo-files-but-no-evidence-of-aliens-found-extraterrestrial-military-space-nasa-particles-declassified-mars))
- **Hegseth/AARO caseload** exceeds 2,000 ([DefenseScoop](https://defensescoop.com/2026/02/25/hegseth-ufo-disclosure-trump-aaro-uap-caseload/))

### Low-signal / noise (novelty ≤2)

- ABC News redirect page with no extractable content
- PBS anticipatory piece about future releases (pre-Release 03)
- Viral unverified claims (CIA searching DNA databases for alien hybrids)

---

## Cross-Release Comparison

### Release 01 — May 8, 2026 (162 files)
**Theme:** Foundational historical disclosure

Top items analyzed:
- WWII "foo fighter" documents (SHAEF, 1944–45) — novelty 6
- Early Air Force intelligence protocols (1948–49) — novelty 6
- Apollo 17 lunar photos, military infrared footage globally
- 1947 Roswell memo, diplomatic cables on global UAP incidents
- FBI-UAP-PR003 "Orbs Over the Pond" (2024 video)

### Release 02 — May 22, 2026 (51 videos, 13 documents)
**Theme:** Military sensor data and contemporary testimony

Top items analyzed:
- **DOW-UAP-D017, Sandia Base (1948–1950)** — 116 pages, 209 sightings at nuclear weapons facility — **novelty 8/10** (highest primary doc score across all releases)
- **DOW-UAP-PR050, 4 UAP formation over Iran** (Aug 2022) — novelty 7
- **NASA-UAP-D008, Apollo 12 medical debriefing** — novelty 7
- **ODNI-UAP-D001, Senior USIC official narrative** (May 2026) — novelty 2 (rehash)
- Lake Huron shootdown footage (2023)
- DOE Pantex radar imagery — novelty 3

### Release 03 — June 12, 2026 (72 items)
**Theme:** FBI domestic investigations + historical policy documents

Top items analyzed:
- CIA Harare airport alert (2008) — novelty 6
- Army flying saucer study (1949) — novelty 6
- FBI Colorado Springs cluster (2022, unresolved) — novelty 6
- Hoover FBI correspondence (1949) — novelty 6
- FBI 2026 northeastern orb FD-302s — novelty 4–5
- 1953 CIA panel recommending formal UAP "debunking" (referenced in SOFX coverage)

### Evolution across releases

```
Release 01          Release 02              Release 03
──────────          ──────────              ──────────
Historical          Military sensors        FBI domestic
breadth             + intel testimony       eyewitness cases
(1947–2026)         + nuclear sites         + policy history
                    + shootdown footage     + 2026 live cases
```

**Pattern:** Each release adds a new agency perspective. Release 01 was multi-agency historical; Release 02 emphasized DoD/IC sensor data; Release 03 brings the **FBI's domestic investigative pipeline** into public view for the first time.

---

## Top 10 Items by Novelty (All Sources, 30-Day Window)

| Rank | Score | Type | Item |
|------|-------|------|------|
| 1 | **8** | News | UAP Science Advisory Council (Avi Loeb) |
| 2 | **8** | Primary | DOW-UAP-D017, Sandia Base 1948–1950 (Release 02) |
| 3 | **7** | Primary | DOW-UAP-PR050, 4 UAP formation Iran (Release 02) |
| 4 | **7** | Primary | NASA-UAP-D008, Apollo 12 debriefing (Release 02) |
| 5 | **6** | News | Mother orb / Cheyenne Mountain (NY Post, Yahoo, SOFX) |
| 6 | **6** | Primary | CIA-UAP-017, Harare airport alert (Release 03) |
| 7 | **6** | Primary | FBI Colorado Springs unresolved report (Release 03) |
| 8 | **6** | Primary | Hoover FBI correspondence 1949 (Release 03) |
| 9 | **6** | Primary | Army flying saucer study 1949 (Release 03) |
| 10 | **6** | Primary | WWII foo fighter documents (Release 01) |

---

## Key Themes

### 1. Domestic FBI pipeline now visible
Release 03 is the first to show the FBI's contemporary UAP investigative workflow: FD-1057 activity forms, FD-302 witness interviews, and video evidence from civilian sightings — with cases as recent as **February 2026** being declassified within months.

### 2. Colorado Springs / Cheyenne Mountain as a hotspot
Three releases now document UAP activity clustered around NORAD, Space Command, and Cheyenne Mountain — spanning 2022 soldier sightings, 2023 mother-orb incidents, and unresolved FBI investigations.

### 3. Historical suppression doctrine surfacing
The 1953 CIA panel recommendation to formally "debunk" UAPs to prevent public panic, juxtaposed with current unexplained cases, creates a narrative tension between Cold War information control and the transparency mandate driving PURSUE.

### 4. Science enters the apparatus
The announced UAP Science Advisory Council (11 scientists, led by Loeb, chartered by White House/AARO/ODNI/FBI/IC) represents the first formal bridge between academic science and the intelligence/defense UAP investigation structure.

### 5. "Unexplained" is the official framing
AARO's 40% unexplained rate, combined with fact-check articles emphasizing "unidentified ≠ alien," suggests the government is comfortable releasing genuinely anomalous cases while maintaining agnosticism on origin.

---

## What to Watch

| Item | Why |
|------|-----|
| **David Grusch Capitol Hill event** (Tuesday) | Bipartisan pressure for further disclosure beyond PURSUE |
| **UAP Science Advisory Council** formation | First scientific body with IC/DoD charter — watch for membership and mandate |
| **FBI 2026 northeastern orb cases** | Most recent domestic reports; follow for additional FD-302 releases |
| **Colorado Springs cluster resolution** | Multiple unresolved docs (2022) near critical command infrastructure |
| **Release 04** | Pentagon has signaled additional batches; WAR.GOV/UFO exceeded 1B hits |
| **AARO 2025 annual report** | Overdue; caseload now exceeds 2,000 with ~1,000 lacking sufficient data |
| **Executive order on disclosure** | Hegseth hinted at possible EO to compel transparency surge |

---

## Data Summary

| Metric | Value |
|--------|-------|
| Total items analyzed (30-day window) | 83 |
| Release 03 primary docs analyzed | 8 |
| News/media items analyzed | 44 |
| Items scoring novelty ≥6 | 16 |
| Highest novelty (any source) | 8/10 |
| Classification breakdown | 22 genuinely new, 3 rehash, 1 speculation, 44 context, 3 meta |

---

## Appendix: All Release 03 Primary Documents

| ID | Title | Novelty | Classification |
|----|-------|---------|----------------|
| CIA-UAP-017 | Placement on High Alert, Harare 2008 | 6 | GENUINELY_NEW |
| DOW-UAP-D084 | US Army Flying Saucer Study, 1949 | 6 | GENUINELY_NEW |
| FBI-UAP-D002 | FD-1057, Colorado Springs 2022 | 6 | GENUINELY_NEW |
| FBI-UAP-D011 | Hoover Correspondence, 1949 | 6 | GENUINELY_NEW |
| FBI-UAP-D010 | FD-302-71, Northeastern Orb 2026 | 5 | GENUINELY_NEW |
| FBI-UAP-D009 | FD-302-67, Northeastern Orb 2026 | 4 | GENUINELY_NEW |
| FBI-UAP-D003 | Digital Rendering, Colorado Springs 2022 | 4 | GENUINELY_NEW |
| ICA-UAP-D001 | Analysis, Colorado Springs 2022 | 3 | REHASH |

---

*Generated by [uap-signal](https://github.com/) — automated UAP release analysis. Scores and summaries are LLM-assisted and should be verified against primary sources.*
