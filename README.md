# Agent skills

Shared skills for Codex and Claude Code (`SKILL.md` format).

| Skill | Purpose |
| --- | --- |
| [control-flow](control-flow/SKILL.md) | ROS 2 control-flow diagrams as PDFs |
| [robot-urdf-viewer](robot-urdf-viewer/SKILL.md) | Offline HTML robot viewer from URDF/Xacro |
| [roboticist](roboticist/SKILL.md) | Beginner audit of a ROS 2 workspace |
| [state-machine](state-machine/SKILL.md) | Robotics state-machine diagrams as PDFs |

## Install

| Tool | Reads |
| --- | --- |
| Codex | `~/.agents/skills/` directly |
| Claude Code | `~/.claude/skills/` (link each skill) |

```bash
git clone https://github.com/grsylvia/agent-skills ~/.agents/skills
for s in ~/.agents/skills/*/; do ln -s "${s%/}" ~/.claude/skills/$(basename "$s"); done
```

## License

[MIT](LICENSE). `robot-urdf-viewer/assets/viewer.html` bundles Three.js (MIT, notice included).
