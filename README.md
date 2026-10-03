# Agent skills

Reusable skills for robotics, engineering research, and diagrams, shared between Codex and Claude Code. Each skill has a `SKILL.md` describing its scope and workflow, with supporting scripts, references, or assets where needed.

## Skills

| Skill | Purpose |
| --- | --- |
| [bearing-specialist](bearing-specialist/SKILL.md) | Clarify bearing requirements and research manufacturer guidance and engineering references. Covers requirements and research, without selecting or validating a bearing. |
| [control-flow](control-flow/SKILL.md) | Trace ROS 2 execution through nodes, interfaces, and callbacks at overview or detail level. |
| [diagram-code-walkthrough](diagram-code-walkthrough/SKILL.md) | Walk through an existing control-flow or state-machine diagram step by step, tied to small code examples. |
| [open-source-robot-finder](open-source-robot-finder/SKILL.md) | Find and compare buildable open-source robots, checking licenses, build files, and bills of materials. |
| [robot-urdf-viewer](robot-urdf-viewer/SKILL.md) | Build a standalone offline HTML viewer from URDF or Xacro, with joint controls, frames, and block or STL geometry. |
| [roboticist](roboticist/SKILL.md) | Review a ROS 2 workspace for beginner-level issues with URDF, frames, units, joint limits, and packaging; report cited findings without editing files. |
| [state-machine](state-machine/SKILL.md) | Map robotics states, events, guards, and transitions, including ROS managed-node lifecycles. |
| [visualize](visualize/SKILL.md) | Create general-purpose diagrams of systems, workflows, and relationships. |

The `control-flow`, `state-machine`, and `visualize` skills produce paired PDF diagrams and agent-readable Markdown. Use the specialized ROS skills for execution and state analysis, and `visualize` for general diagrams. Use `diagram-code-walkthrough` to study an existing diagram alongside its implementation.

## Install

Clone this repository into Codex's user skills directory:

```bash
mkdir -p ~/.agents
git clone https://github.com/grsylvia/agent-skills.git ~/.agents/skills
```

If that location already contains this checkout, update it instead:

```bash
git -C ~/.agents/skills pull --ff-only
```

To share these skills with Claude Code, create a link for each skill in `~/.claude/skills/`. This Bash snippet preserves existing entries:

```bash
mkdir -p ~/.claude/skills
for skill in ~/.agents/skills/*/; do
    [ -f "${skill}SKILL.md" ] || continue
    name=$(basename "$skill")
    target="$HOME/.claude/skills/$name"
    if [ ! -e "$target" ] && [ ! -L "$target" ]; then
        ln -s "${skill%/}" "$target"
    fi
done
```

Each skill documents its own inputs, dependencies, and output requirements. Scripts and bundled assets are specific to the skill that contains them.

## Sourcing-agent skills

`find-suppliers` and `source-bom` are maintained in the separate [sourcing_agent repository](https://github.com/grsylvia/sourcing_agent), under `skill/`. Their contents are versioned there.

Local links to those skills may be installed in `~/.agents/skills/`; this repository ignores those two entries. Point the links at a persistent sourcing-agent checkout so they continue to work after temporary worktrees are removed.

## License

[MIT](LICENSE). The [robot viewer HTML](robot-urdf-viewer/assets/viewer.html) bundles Three.js under its MIT license, with the notice included in the file.
