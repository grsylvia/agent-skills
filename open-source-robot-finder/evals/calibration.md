# Calibration set

Test data, not runtime reference: known projects with facts checked on 2026-09-26 (`gh_repo_facts.sh`, WebFetch). A test run covering their type should reach these verdicts. Re-check the facts before each test round; they go stale.

| Project | Type | Primary source | Facts (2026-09-26) | Expected verdict |
| --- | --- | --- | --- | --- |
| SO-101 | Arm | `TheRobotStudio/SO-ARM100` | Apache-2.0 · 114 STL, 36 STEP, 5 URDF · BOM table in README (18 vendor-link lines) · 6× Feetech STS3215 · LeRobot software · commit 2026-09 | Passes all gates; top pick for a fast, cheap arm |
| Koch v1.1 | Arm | `jess-moss/koch-v1-1` | Apache-2.0 · 17 STL, 24 STEP · BOM in README (26 vendor-link lines) · commit 2024-09 | Passes; strong S1–S2, weaker S6 |
| PAROL6 | Arm | `Source-Robotics/PAROL6-Desktop-robot-arm` | GPL-3.0 · 52 STL, 2 STEP · `BOM/BOM.md` · URDF + ROS package · firmware · commit 2026-09 | Passes; strong S3–S4; costlier and slower to build than SO-101 |
| Thor | Arm | `AngelLM/Thor` | CC-BY-SA-4.0 · 72 STL, 72 STEP, 79 FreeCAD · BOM on thor.angel-lm.com, not in repo · last release 2021 | Passes only if README links are followed (tests G4 lookup) |
| BCN3D Moveo | Arm | `BCN3D/BCN3D-Moveo` | MIT · 32 STL, SolidWorks · BOM PDF · commit 2016-10 | Passes gates; low S6 (stale) |
| OpenArm | Arm | `enactic/openarm` + `enactic/openarm_hardware` | Apache-2.0 / CERN-OHL-S · no CAD in repo; STEP, STL, BOM on Google Drive and docs.openarm.dev | Passes G1 only via sibling repo (tests multi-repo rule); likely fails "weekend" |
| AR4 | Arm | anninrobotics.com/downloads | Free STL, manuals with BOM, software · no license stated · printed or machined | Rejected G3 "no license stated"; must appear in Rejected |
| LeKiwi | Mobile base | `SIGRobotics-UIUC/LeKiwi` | Apache-2.0 · 76 STL · `BOM.md` · URDF · commit 2026-08 | Passes; top pick for a mobile base |
| ruckig | — | `pantor/ruckig` | MIT · no STL or CAD (motion library) | Rejected G1 (software only) if it surfaces |
