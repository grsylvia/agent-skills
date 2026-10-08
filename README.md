# Agent skills

Reusable skills for robotics, engineering research, and diagrams, shared between Codex and Claude Code. Each skill has a `SKILL.md` describing its scope and workflow, with supporting scripts, references, or assets where needed.

## Skills

| Skill | Purpose |
| --- | --- |
| [control-flow](control-flow/SKILL.md) | Trace ROS 2 execution through nodes, interfaces, and callbacks at overview or detail level. |
| [robot-urdf-viewer](robot-urdf-viewer/SKILL.md) | Build a standalone offline HTML viewer from URDF or Xacro, with joint controls, frames, and block or STL geometry. |
| [roboticist](roboticist/SKILL.md) | Review a ROS 2 workspace for beginner-level issues with URDF, frames, units, joint limits, and packaging; report cited findings without editing files. |
| [state-machine](state-machine/SKILL.md) | Map robotics states, events, guards, and transitions, including ROS managed-node lifecycles. |

The `control-flow` and `state-machine` skills produce paired PDF diagrams and agent-readable Markdown. Use these skills for ROS execution and state analysis.

## Required writing dependency

The `control-flow` and `state-machine` skills require [ASD-STE100](https://github.com/danyuchn/asd-ste100-skill) for writing and revisions. They use it to clarify diagram text and Markdown companions while preserving technical meaning and exact identifiers. Each skill stops writing if the dependency is unavailable.

This repository does not contain it. [`external-skills.txt`](external-skills.txt) lists it with a pinned commit, and the install script below clones it to `~/.agents/external/asd-ste100` and links it in as a skill.

## Install

Clone this repository, then run the install script:

```bash
git clone https://github.com/grsylvia/agent-skills.git ~/agent-skills
~/agent-skills/scripts/link-skills.sh
```

The script does three things:

- It clones each skill in `external-skills.txt` into `~/.agents/external/`, checks out its pinned commit, and links it into this repository. Git ignores the link through `.git/info/exclude`.
- It links `~/.agents/skills` to this repository for Codex.
- It links each skill into `~/.claude/skills/` for Claude Code. Claude Code keeps synced skills in that directory, so the script links skills one by one instead of replacing it.

It never replaces an existing file, folder, or link that points somewhere else.

To update, pull and run the script again. The script adds links for new skills, removes broken links to deleted ones, and moves external skills to their pinned commits:

```bash
git -C ~/agent-skills pull --ff-only
~/agent-skills/scripts/link-skills.sh
```

Each skill documents its own inputs, dependencies, and output requirements. Scripts and bundled assets are specific to the skill that contains them.

## External skills

To add an external skill, add a line to `external-skills.txt` with its name, repository URL, and full commit hash, then run the script.

To update a pin, list the upstream changes, review them, then change the commit in `external-skills.txt` and commit that change:

```bash
~/agent-skills/scripts/link-skills.sh --check-updates
```

## Sourcing-agent skills

`find-suppliers` and `source-bom` are maintained in the separate [sourcing_agent repository](https://github.com/grsylvia/sourcing_agent), under `skill/`. Their contents are versioned there.

Local links to those skills may be installed in `~/.agents/skills/`; this repository ignores those two entries. Point the links at a persistent sourcing-agent checkout so they continue to work after temporary worktrees are removed.

## License

[MIT](LICENSE). The [robot viewer HTML](robot-urdf-viewer/assets/viewer.html) bundles Three.js under its MIT license, with the notice included in the file.
