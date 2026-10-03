---
name: state-machine
description: Generate source-grounded ROS and robotics state-machine diagrams as paired PDFs and agent-readable Markdown for reverse engineering, from whole-robot operation through application tasks, motion execution, joint bridges, and motor drives. Also supports managed-node lifecycle views. Use for states, events, guards, and transitions; node/interface maps and procedural control-flow diagrams are outside its scope.
---

# Robotics state-machine visualizer

Create the state-machine view selected by the user as a readable PDF with an agent-readable Markdown companion. Explain what state an identifiable component or goal occupies, what changes that state, and which conditions govern the change.

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

## Shared visual parameters

| Parameter | Standard |
| --- | --- |
| Page | Clean white canvas; landscape by default, with orientation and size adapted to the flow |
| Text | Muted navy `#23364a`; clear sans-serif type |
| Primary boxes | Pale blue `#eaf2fa`; bold role, entity, operation, or state name |
| Context boxes | Gray `#f3f6f8`; explicitly labeled context or external boundary |
| Secondary text | Smaller concise identifiers or details, still comfortably readable |
| Highlights | Restrained green for supported successful outcomes, amber for uncertainty, rose for faults; always include textual meaning |
| Title block | Left-aligned main title only; no eyebrow/overline above it and no subtitle below it |
| Layout | Consistent alignment grid, generous margins, whitespace between groups |
| Connectors | Thin, consistent strokes; explicit direction and concise labels where needed |
| Footer | Small legend and page number; no explanatory paragraphs |

Green, amber, and rose are semantic accent families, not fixed hex values. Choose muted shades with readable contrast. Do not impose a mandatory font size or page size; preserve legibility at the intended viewing scale.

## Layout and concise text

- Keep overviews understandable at a glance: essential entities and paths, short primary labels, and smaller identifiers when helpful. Reserve internal steps and implementation detail for separately requested detail views.
- In detail views, prefer a primary label plus one to three short lines per box; use more only for an essential mapping or interface list. Remove repeated facts, narrative paragraphs, and notes that restate arrows.
- Route connectors through dedicated corridors. Use separate lanes for return paths and loops; avoid crossings and unrelated boxes.
- Position labels beside connectors with clearance from every line, arrowhead, and box. Do not conceal collisions with white text backgrounds.
- Simplify wording, enlarge the canvas, adjust orientation, wrap concise labels, or manually position elements when layout crowds the diagram. Do not shrink text or tightly crop pages to force a fit.
- Put necessary qualifications and unresolved boundaries into short box details, guards, edge labels, or attached context boxes. Keep the title and legend brief. Put essential scope/configuration in the diagram content or PDF metadata, not in title-adjacent text; omit decorative clutter.
- Define connector meanings in the legend and mark inference explicitly. Distinguish primary connections from context; never silently reuse a style for conflicting meanings. Shared styling must preserve the selected diagram's semantics.
- Use one coherent view per page. Split into multiple pages only when the requested scope needs them; do not add unrequested detail views.
- Keep source links unobtrusive where supported. Do not include visible source-evidence sections, dense source catalogs, or reference appendices.
- Inspect supplied visual references before styling. For Agrobot, use the approved spacious layout in `pdf_docs/agrobot-states.pdf` when available; other projects do not depend on that file. Match presentation while preserving the selected diagram's meaning.

## State-machine presentation

- Use one state machine per PDF page. Context boxes and a clearly scoped composite state may remain on that page. Separate independent task, bridge, drive, and lifecycle machines into their own pages when requested.
- Use bold state names. Keep source references to short owner/symbol labels in detail views or unobtrusive clickable links; do not fill an overview with file paths.
- Use solid arrows for evidenced state transitions and dotted connectors for interfaces/context. If a conceptual overview uses inferred arrows, identify that meaning explicitly. Context connectors must remain distinguishable from transitions, and inference labels must remain visible after simplification.

## Agent-readable Markdown

- Describe the same selected view as the PDF in plain text, so an agent can trace it without opening the PDF. Use concise bullets rather than narrative paragraphs; images, Mermaid, or renderer source alone are insufficient.
- Start with a title naming the view and level, then metadata bullets such as `source_pdf`, `workspace`, `configuration`, `verification`, and `state_owner`. Give `source_pdf` as the project-relative PDF path. Record whether the view is conceptual, explicit, or inferred, and distinguish source-derived findings from runtime verification. State when no owner, transitions, or initial/final markers are established.
- Use `## Semantics`, `## Nodes`, and `## Edges` sections. For a multi-page PDF, repeat these sections under a heading identifying each page/machine and its owner. Define transition direction, context links, grouping, and inference markers in words; do not rely on color, position, or line style.
- List each node as ``- `stable_id` | kind: state | label | short fact``. Use distinct kinds for explicit states, inferred modes, context, missing capabilities, and initial/final markers where present. Preserve IDs during revisions and exact state names where relevant. Use short indented bullets for necessary details, state storage, units, timing, or unresolved behavior at the selected level.
- List each transition as ``- `source_id -> target_id` | transition | event [guard] / effect``, omitting guard or effect only when not applicable. Use one entry per connection and mark inferred transitions explicitly. List context connections separately with `kind: context`, using `--` only for undirected links. Context links are not transitions, and list order does not imply a transition sequence.
- Preserve all meaningful PDF labels, conditions, failure/cancellation distinctions, and uncertainty. Mark missing or unknown facts explicitly without inventing states or transitions or expanding the view. Keep both artifacts synchronized; Markdown is the text representation of the diagram, not an extra audit or evidence catalog.

## PDF and Markdown output and verification

1. Use an available renderer that produces a real PDF, preferably with vector text and shapes. Graphviz DOT rendered with `dot -Tpdf` suits many graphs; a plotting/PDF library or manual placement may better handle complex routing. Do not assume automatic layout satisfies the visual rules.
2. Export PDFs to `./pdf_docs/` and Markdown companions to `./md_docs/`, relative to the working project root. Create these directories if needed. Use matching filename stems, such as `pdf_docs/agrobot-states.pdf` and `md_docs/agrobot-states.md`, or `pick-states` and `drive-states` for the selected target. Use filesystem-safe names and preserve existing filename stems during revisions unless asked to rename them.
3. Deliver both the PDF and its Markdown companion for every requested view, and update both during revisions. Neither a Markdown-only diagram nor a screenshot replaces the PDF. Keep renderer sources, working evidence inventories, and preview images in a temporary directory unless requested as deliverables; do not depend on temporary scripts from earlier sessions remaining available. This output rule does not restrict editing `SKILL.md` during skill maintenance.
4. Verify the exported PDF opens and has the intended page count. Render temporary previews of every exported page and inspect clipping, typography, spacing, label collisions, arrow direction, crossings, and distinctions between context, inference, and primary connections.
5. Correct layout defects and inspect the affected exported pages again. If PDF rendering or visual inspection is unavailable, state that limitation accurately; do not claim verification from the source canvas alone.
6. Check PDF–Markdown agreement: every diagram node and connector has a corresponding text entry, all edge endpoints resolve to declared IDs, and labels, owners, state kinds, transition direction, events, guards, effects, grouping, and uncertainty agree. Confirm the Markdown points to the matching PDF and retains the selected scope.
7. Return links to both the PDF and Markdown with a brief completion statement, then stop. Do not propose or generate additional views.

## Incorporate refinements

- Apply user corrections to the requested work. When feedback changes reusable skill behavior, update this skill directly; keep one-off content or layout edits local to the diagram.
- Preserve the scope of feedback and replace superseded instructions rather than accumulating conflicting rules or a chronological log. Ask only when persistence is genuinely ambiguous and consequential.
- Before reporting completion of a requested refinement batch, consolidate the affected skill sections and check level names, scope, diagram semantics, and paired output requirements for consistency. Do not generate additional examples or change the separate control-flow skill as part of this cleanup unless requested.
- Validate new or edited skill instructions with the skill-creator validator when available. Skill maintenance remains subject to filesystem permissions; do not claim persistence until the write succeeds.
