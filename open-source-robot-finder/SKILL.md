---
name: open-source-robot-finder
description: Find open-source robot projects (arms, mobile bases, legged robots, grippers) that can be 3D printed and running fast, with machined or off-the-shelf parts where needed. Searches GitHub, Hugging Face LeRobot, Hackaday.io, Printables, and OSHWA; checks each project's license, build files, and BOM; returns a ranked, cited scorecard. Use whenever the user wants to find, scout, compare, or pick a DIY, printable, or open-source robot to build, even if they don't say "open source" (e.g., "what robot arm could I print this weekend?").
---

# Open-Source Robot Finder (v0.2)

Find open-source robots the user can print and have moving fast. Searching is easy; the value is the verdict. Most "open-source robot" hits fail on license, missing files, or a vague BOM, so every verdict rests on evidence fetched this session.

## Ground rules

| Rule | Why |
| --- | --- |
| Evidence or zero | Project facts go stale. Cite a URL or script line fetched this run; with no evidence, write "not stated" and score 0. |
| Show rejects | Each reject gets a gate ID and a reason, so the user can override (e.g., free files but no license). |
| Link, don't download | Point to build files; never download, re-upload, or commit them. |
| Plain writing | Short table cells; define unavoidable jargon in a few words. |

## Workflow

| Step | Who | Output |
| --- | --- | --- |
| 1 · Intake | You | Criteria |
| 2 · Scout | One `general-purpose` subagent | Scored and rejected projects |
| 3 · Check | You | Verified top 3 |
| 4 · Report | You | Ranked scorecard in chat |

### 1 · Intake

Ask in one AskUserQuestion call; skip what the user already said.

| Question | Options (first is default) | Feeds |
| --- | --- | --- |
| Robot type? | Arm · Mobile base · Legged · Gripper or hand | Search |
| Budget for bought parts? | Under $250 · $250–$1,000 · Over $1,000 · Any | G5 |
| How soon moving? | Weekend · A month · No rush | G6 |
| ROS 2 / URDF? | Nice to have · Required · Not needed | G7, S4 |

Unless told otherwise: any number of joints, top 5 results.

### 2 · Scout

Search output and page dumps are long, so a subagent does the legwork and returns only results. Spawn it with this brief:

```text
Scout open-source robot projects for: <intake answers>.
Skill folder: ~/.agents/skills/open-source-robot-finder. Read references/sources.md and references/rubric.md.
1. Find 15–30 candidates from every source in sources.md. Merge duplicate listings.
2. Gather evidence for each: GitHub repos → scripts/gh_repo_facts.sh <owner/repo>;
   other pages → WebFetch. Check every place in rubric.md "Where evidence lives" before failing a gate.
3. Apply the gates, then score survivors. Cite a URL or script line for every result.
Return markdown only, no prose:
- One block per scored project, best first:
  ### <project> · <total>/100
  <url> · <license> · <cost> · <print parts or hours> · <motors + controller> · <ROS 2/URDF> · <last update> · flags: <…>
  | ID | Score | Evidence |   (S1–S6)
- Rejected: | Project | URL | Gate | Reason |
```

### 3 · Check

The subagent can be wrong. For the top 3, re-run `scripts/gh_repo_facts.sh` or WebFetch the cited page and confirm the license (G3) and parts list (G4). Correct any score whose evidence doesn't hold, and note the correction in the report.

### 4 · Report

````markdown
## Open-source robot finder · <type, budget, timeline> · <date>

**Top pick:** <project> — <one line on why it's fastest to get moving>

| # | Project | Score | Cost | Print | Motors | Updated |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | [<name>](<url>) | <n>/100 | <$ or not stated> | <parts or hours> | <count × model> | <yyyy-mm> |

**Top 3**
- **<project>** · Why fast: <…> · Watch out: <flags, gaps> · Evidence: <links>

**Rejected**

| Project | Gate | Reason |
| --- | --- | --- |

**Not checked:** part fit on the bed and print hours, unless the project states them.

**Next:** price the BOM with `source-bom`; open a shipped URDF with `robot-urdf-viewer`.
````

## Files

| Path | Use |
| --- | --- |
| [references/sources.md](references/sources.md) | Where and how to search |
| [references/rubric.md](references/rubric.md) | Where evidence lives, gates, scores, flags |
| [scripts/gh_repo_facts.sh](scripts/gh_repo_facts.sh) | GitHub facts for one repo |
| [evals/](evals/) | Test prompts and a calibration set; not for runtime use |
