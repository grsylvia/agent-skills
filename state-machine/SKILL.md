---
name: state-machine
description: Generate source-grounded ROS and robotics state-machine diagrams as PDFs for reverse engineering, from whole-robot operation through application tasks, motion execution, joint bridges, and motor drives. Also supports managed-node lifecycle views. Use for states, events, guards, and transitions; node/interface maps and procedural control-flow diagrams are outside its scope.
---

# Robotics state-machine visualizer

Create the state-machine view selected by the user as a readable PDF. Explain what state an identifiable component or goal occupies, what changes that state, and which conditions govern the change.

## Select the level and target

Use the user's current selection or an unambiguous selection from the conversation. If neither establishes a level, ask which of the following levels to generate and wait for the answer. For a detail view, clarify the component or task only when it is not already clear. Do not ask these questions when merely editing the skill.

These are diagram abstraction levels, not official ROS levels or a claim that the code implements a nested hierarchy. Preserve this numbering:

| Level | Scope |
| --- | --- |
| 1 — Whole-robot operation | High-level operating modes and coordination boundaries across the requested workspace. If no global supervisor exists, explicitly label the view conceptual and the modes inferred; do not invent a global state owner, readiness gate, stop, or recovery path. |
| 2 — Application / task | One application's behavior, such as target preparation or pick-task progression. Separate independent or concurrent machines. |
| 3 — Motion execution | A motion request or trajectory goal, including relevant acceptance, execution, completion, cancellation, and failure behavior. Distinguish parent and child goals where applicable. |
| 4 — Joint bridge | Software modes for preparing, arming, moving, holding, or recovering an actuator, as implemented by the selected bridge. |
| 5 — Motor drive / protocol | Hardware/protocol states and their command- or feedback-driven transitions, such as a drive's CiA 402 state machine. |

ROS managed-node lifecycle is a separate view, not Level 6. Use it only for components that implement lifecycle behavior. Do not assume every ROS node is managed. ROS action goal status can appear at different levels and is distinct from task steps, bridge modes, drive states, and node lifecycle.

A double-click expands only the selected state, task, or component. Preserve the parent terminology and relevant incoming/outgoing events. Do not require or generate a parent view first. Asking what could be expanded authorizes an explanation, not new diagrams.

## Scope and source grounding

- Follow the current command only. Skill creation or maintenance does not also authorize diagram generation. Do not automatically expand all levels.
- Inspect code and configuration without running robot nodes, sending ROS commands, building packages, or installing dependencies. Do not change robot code or add audits, tests, launch instructions, or unrelated documentation.
- Establish the workspace boundary and configuration. Read relevant manifests, executable entry points, launch/configuration files, and implementations. Treat documentation as leads to verify against code.
- Keep imported copies and alternative controller configurations distinct. Do not merge mutually exclusive paths into one apparent runtime. Use the variant established by context; clarify only when the choice materially changes the requested view.
- Identify each machine's owner and state storage: enum, member variable, action goal, lifecycle object, drive statusword, or inferred behavior. Trace assignments and their callers, guards, event handlers, and result paths. An enum alone does not prove its transitions.
- Keep a temporary transition/evidence inventory when useful. Ground states and arrows in implementation symbols and configuration. Do not publish an extra evidence document unless requested.
- Mark unavailable code and unresolved handoffs. A matching topic or a comment does not prove a functioning connection. Describe static findings as source-derived, not runtime-verified.

## State-machine meaning

- Put states in state boxes. Represent interfaces, dependencies, code context, and unresolved boundaries with visibly different context boxes. Do not turn each package, function, or ROS node into a state.
- Label transitions with an event and, where relevant, a guard or effect: `event [condition] / effect`. Keep labels short at the selected level.
- Distinguish explicit software states from inferred behavioral phases. At Level 1, use only modes supported by the selected scope and mark the conceptual abstraction. If independent nodes can occupy different modes at once, do not imply exclusive whole-robot states.
- Preserve implementation behavior even when names are misleading. Do not equate a motion with a `MOVING` enum unless the path actually sets it. A timeout may return to an armed state, and a task's reported success may not establish physical completion.
- Keep action acceptance, cancellation requests, observed cancellation, terminal status, and result payload distinct. Do not infer immediate motor stopping from accepted cancellation or from a perception safety flag.
- Draw fault propagation, recovery, retries, and reset transitions only when supported. Do not make a local fault into a robot-wide fault. Omit unsupported transitions or identify them as unresolved, rather than supplying an idealized implementation.
- Use initial/final markers only when their meaning is established. A terminal action outcome is not necessarily a terminal node or robot state.
- Summarize omitted detail accurately. A simplified drive-state diagram need not include every protocol transition, but it must not contradict the implemented ones.

## Presentation

- Use one state machine per PDF page. Context boxes and a clearly scoped composite state may remain on that page. Separate independent task, bridge, drive, and lifecycle machines into their own pages when requested.
- For Agrobot, use `state_machine/agrobot-states.pdf` as the style reference when available. Match the approved spacious layout, not an older crowded version. Inspect any user-provided reference before styling.
- Use a left-aligned title, brief scope subtitle, small legend, and page number. Keep Level 1 understandable at a glance; move internal steps and interface detail into requested deeper views.
- Use clear sans-serif type, bold state names, muted navy text (`#23364a`), pale blue states (`#eaf2fa`), gray context boxes (`#f3f6f8`), and restrained green, amber, or rose outcomes. Labels must convey meaning without relying on color.
- Incorporate necessary behavioral qualifications and unresolved connections into concise state details, guards, edge labels, or attached context boxes. Remove generic explanatory prose. Do not add bottom-of-page paragraphs, evidence appendices, or dense source catalogs.
- Keep source references unobtrusive: short owner/symbol labels in detail views or clickable source links where supported. Do not fill an overview with file paths.
- Use solid arrows for evidenced state transitions and dotted connectors for interfaces/context, with a small legend. If a conceptual overview uses inferred arrows, identify that meaning explicitly. Never silently reuse one connector style for conflicting meanings.
- Align states on a consistent grid. Route arrows through dedicated corridors; use separate lanes for return transitions and loops. Place labels beside connectors with clearance from every line, arrowhead, and box. Do not cover a line with a white text background to disguise overlap.
- Use page space efficiently without crowding. Increase the PDF canvas, change orientation, wrap concise labels, or manually route connectors when necessary. Do not shrink text or tightly crop pages at the expense of readability. Prefer a larger spacious page over overlapping edges or labels.

## PDF output and verification

- Save into the user's requested location; otherwise use `state_machine/` in the working project. Use short descriptive names, such as `agrobot-states.pdf`, `pick-states.pdf`, or `drive-states.pdf`. Preserve an existing name during revisions unless asked to rename it.
- Deliver PDFs only unless other artifacts are requested. No Markdown diagram, README, PNG, or source script is a default deliverable. This restriction concerns diagram outputs, not the required `SKILL.md` when creating or editing the skill.
- Keep rendering sources, transition inventories, and previews in a temporary directory. Do not depend on temporary scripts from earlier sessions remaining available.
- Use an available renderer that produces a real PDF: Graphviz, a plotting/PDF library, or another suitable tool. Prefer vector text and shapes where practical. Manual positioning is appropriate when automatic layout crowds labels or crosses connections.
- Verify the PDF opens and has the requested page count. Render temporary previews of every PDF page with an available PDF tool and inspect clipping, text size, spacing, arrow directions, and connector crossings. A source-canvas preview is useful but is not proof that the exported PDF renders correctly. If PDF inspection is unavailable, state the verification limit accurately.
- Check that contextual edges cannot be mistaken for state transitions and that inference labels remain visible after simplification. Return a PDF link and a brief completion statement, then stop.

## Incorporate refinements

- Apply user corrections to the requested work. When feedback changes reusable skill behavior, update this skill directly; keep one-off content or layout edits local to the diagram.
- Preserve the scope of feedback and replace superseded instructions rather than accumulating conflicting rules or a chronological log. Ask only when persistence is genuinely ambiguous and consequential.
- Before reporting completion of a requested refinement batch, consolidate the affected skill sections and check level names, scope, diagram semantics, and PDF requirements for consistency. Do not generate additional examples or change the separate control-flow skill as part of this cleanup unless requested.
- Validate new or edited skill instructions with the skill-creator validator when available. Skill maintenance remains subject to filesystem permissions; do not claim persistence until the write succeeds.
