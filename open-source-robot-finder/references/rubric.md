# Rubric

Gate, then score survivors. Every gate result and score cites a URL or a `gh_repo_facts.sh` output line; no evidence → the gate fails or the score is 0.

## Where evidence lives

Look in all of these before failing a gate. Good projects often split code, CAD, and BOM across places.

| Place | Example |
| --- | --- |
| The repo | `BOM/BOM.md`, `STL/` |
| Sibling repos in the same org | OpenArm: CAD via `enactic/openarm_hardware` |
| Links in the README or `homepage` (website, docs, Google Drive, Onshape) | Thor: BOM on thor.angel-lm.com |
| Off-GitHub project page | AR4: downloads on anninrobotics.com |

## Gates (any fail → reject)

**Buildable** (the project itself)

| ID | Gate | Pass when |
| --- | --- | --- |
| G1 | Hardware | Print or CAD files exist. Software-only repos fail. |
| G2 | Free files | Build files download without payment (a free account is fine). Paid STLs or kit-only frames fail. |
| G3 | License | A license or written terms allow a personal build: OSI, Creative Commons, CERN-OHL, TAPR. Non-commercial (NC) passes with a flag. None found → "no license stated". |
| G4 | Parts list | A BOM exists: file, README table, docs page, or build manual. |

**Fit** (this user's intake)

| ID | Gate | Pass when |
| --- | --- | --- |
| G5 | Budget | Stated cost ≤ 1.5 × budget. Unstated cost passes with a flag. |
| G6 | Timeline | Weekend: no machining, no custom PCB order. A month: custom PCBs OK. No rush: machining OK. |
| G7 | ROS 2 | Only if "Required": a URDF, Xacro, or ROS 2 package exists. |

## Scores (0–5 each)

Total = Σ weight × score ÷ 5, out of 100. 2 and 4 fall between anchors. Ties: higher S1, then S2.

| ID | Criterion | Weight | 5 | 3 | 1 |
| --- | --- | --- | --- | --- | --- |
| S1 | Print effort | 25 | ≤ 20 printed parts or ≤ 20 h; no machining | 21–60 parts or 21–60 h; or minor machining | > 60 parts or > 60 h; or major machining |
| S2 | BOM and parts | 20 | Part numbers + vendor links; all off-the-shelf | Part names, some links; 1–2 hard-to-find parts | Vague list; custom or discontinued parts |
| S3 | Docs | 20 | Step-by-step assembly (photos or video), wiring, first-power setup | Assembly guide, missing wiring or setup | README or CAD only |
| S4 | Software | 15 | Working control software with install steps + URDF or ROS 2 package | Working control software, no URDF/ROS 2 | Partial, abandoned, or DIY |
| S5 | Openness | 10 | Open license (not NC) + editable CAD (STEP, Onshape, FreeCAD, Fusion, SolidWorks) | NC license, or STL only | NC license and STL only |
| S6 | Activity | 10 | Updated ≤ 6 months ago + others' builds (forks > 100, makes, forum, Discord) | Updated ≤ 2 years ago, or some builds | Older than 2 years, few builds |

Stars and forks count only toward S6; popularity is not build quality.

## Flags

Report these; they don't reject.

| Flag | When |
| --- | --- |
| NC license | Non-commercial license |
| STL only | No editable CAD |
| Cost not stated | No total or priced BOM |
| Stale | No update in > 2 years |
| Big bed | Docs require a bed > 256 mm (the user's P1S) |
| Partial counts | `tree_truncated: true` |

## `gh_repo_facts.sh` output → rubric

| Line | Feeds |
| --- | --- |
| `homepage` | Where evidence lives |
| `license` | G3, S5 (`NOASSERTION` or `NONE` → read the LICENSE file and README) |
| `print_files`, `source_cad` | G1, S1 (STL count ≈ printed parts), S5 |
| `bom_files`, `readme … bom_mentions vendor_links` | G4, S2 |
| `robot_model`, `software` | G7, S4 |
| `docs`, `readme lines` | S3 hint only; open the docs to score |
| `last_commit`, `latest_release`, `stars forks` | S6 |
| `tree_truncated` | Partial-counts flag |
