---
name: control-flow
description: Generate source-grounded ROS 2 control-flow diagrams as paired PDFs and agent-readable Markdown for reverse engineering at system overview, package/node, or callback/operation level. Use to trace execution through nodes, topics, services, actions, and callbacks. State-machine diagrams are outside its scope.
---

# ROS 2 control-flow diagrams

Generate the control-flow view selected by the user as a readable PDF with an agent-readable Markdown companion. Explain how commands and events trigger execution and which responses or results allow work to continue.

## Required writing skill

- You must use `$asd-ste100` for all English text you write or revise while using or maintaining this skill. Read its `SKILL.md` before writing. Resolve it from the available skills or [the sibling installation](../asd-ste100/SKILL.md). If it is unavailable, report the missing dependency and stop writing until it is available.
- Apply it to diagram titles, labels, legends, Markdown companions, user messages, and skill edits. Use Strict mode for technical descriptions, conditions, instructions, and text for agents. Use STE-flavored mode for explanatory prose.
- Preserve exact identifiers, paths, code, formulas, units, and required notation. Keep named states and interfaces unchanged. Short names and structured labels need not become full sentences. Write complete sentences for behavioral claims when a fragment could hide the actor or condition.
- Preserve every fact, condition, scope limit, uncertainty, and distinction between requests and outcomes. Keep precise wording when a shorter version would change the meaning. Do not claim certified STE compliance.
- Before rendering, apply the skill's review process to the diagram text and Markdown companion. Run its `scripts/ste-lint.py` on temporary text exports. Review findings against the source meaning. Correct applicable findings and record necessary exceptions in the brief completion message. Repeat the review after text changes.
- Use `$asd-ste100` as the writing process within this workflow. Keep this skill's PDF and Markdown structure, notation, and delivery rules. Return the artifact links and brief completion message instead of replacing them with the writing skill's text-only response.


## Select the level

Before generating a diagram, prompt the user: "Which control-flow level would you like: system overview, package / node detail, or callback / operation detail?" Present these three choices and wait for the selection. If the current command already specifies a level, use that selection without asking again. This prompt applies to diagram generation, not requests to edit the skill.

| Level | Scope and content |
| --- | --- |
| System overview | A very high-level visual map of the main nodes/subsystems and command paths. Use short role/node labels and a few essential ROS connections. Reserve essential interface and implementation detail for double-click views. |
| Package / node detail | Nodes within the selected package or the internals of one node; publishers, subscriptions, service/action clients and servers, timers, callbacks, and how inputs lead to outputs. Keep external peers as context. |
| Callback / operation detail | One selected callback or operation; function calls, decisions, loops, asynchronous waits, result handling, cancellation, and failure branches. Include executor and callback-group constraints where they affect execution and are established by the code. |

For a detail view, ask which package/node or callback/operation to expand if the target is not already specified or clear from context. Generate only the selected view. Preserve the parent view's node names and incoming/outgoing interfaces when expanding an existing diagram; do not require or generate a parent diagram first.

## Level 1 visual standard

- Show the main control path and only supporting paths needed to understand it; do not inventory every node, endpoint, utility or optional component.
- Keep boxes to a short role and node name, or a clearly labeled subsystem when several nodes are collapsed. Keep edges to a ROS kind (`TOPIC`, `SERVICE`, `ACTION`) and a short purpose. Use exact interface names only when they materially improve understanding.
- Leave message/service/action types, executable names, callback behavior, timing, detailed cancellation/failure handling, and configuration explanations to the requested double-click view.
- Preserve important gaps with brief labels such as `external` or `handoff unresolved`. Simplification must not invent a working connection.

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

## Control-flow presentation

- Use bold role or callback labels with smaller node names. Keep exact node/interface names when needed to trace execution. Label shared ROS types once; omit repeated types and redundant identifiers.
- Use solid arrows for evidenced command/event and completion paths, and dotted connectors for context. Label ROS communication and local calls distinctly; connector style alone does not establish execution order.
- Keep only conditions, timings, and limitations that affect the selected flow. Concision must preserve verified routing, important failure/cancel distinctions, and unresolved boundaries.
- Keep file paths, symbols, and line references in working research or unobtrusive PDF links, outside the visible diagram.

## Scope

- Follow only the user's current command. An overview request authorizes one overview, not automatic package or callback expansions.
- Inspect the requested code and configuration without running robot nodes, building packages, installing software, or sending ROS commands.
- Do not add state machines, detailed motion sequences, audits, tests, launch instructions, recommendations, or documentation beyond the paired PDF and Markdown unless requested.
- If asked to modify this skill, modify it without also generating an example diagram unless requested.
- Generate deeper views only when selected by the user. Keep stable node and interface names across views.

## Skill refinement feedback loop

- Incorporate user tweaks and corrections as they arrive during skill use. Apply them to the current requested work and update this `SKILL.md` directly when they refine reusable skill behavior; do not defer all learning until the diagram is finished.
- Preserve the intended scope of feedback. Keep one-off diagram edits local to that diagram. Record reusable preferences or workflow corrections in the relevant skill section, qualified by level or context when appropriate. Ask only if it is unclear whether a change should persist and that distinction matters.
- Treat the user's latest explicit correction as superseding conflicting earlier guidance. Replace the affected instruction instead of accumulating contradictory rules or a chronological feedback log. Do not infer unrelated requirements from a single example.
- At the end of each series of changes—when the user signals completion, or before reporting completion of the currently requested batch—refactor and organize `SKILL.md`. Integrate refinements into the appropriate sections, consolidate duplicates, remove superseded wording, and check that scope, terminology, and paired output requirements remain consistent. Do not wait for or assume additional requests.
- Keep this cleanup limited to the skill and preserve all still-applicable user requirements. Do not create changelogs, extra documentation, example diagrams, or other artifacts as part of refinement unless requested.
- Validate the edited skill with the skill-creator validator when available and review it for conflicting instructions. Briefly report persisted refinements and completion, then stop. Skill maintenance does not authorize generating additional views or changing robot code.

## Establish the system boundary

1. Identify the requested workspace, subsystem, and launch/configuration variant. Read package manifests, executable entry points, launch files, parameters, and relevant node implementations.
2. Resolve node names, namespaces, interface names, remappings, and parameter overrides where the source permits. Record the selected configuration in both the PDF and Markdown. If no variant is specified, choose one supported by the source and state that assumption; ask only when alternatives would materially change the requested overview.
3. Keep separate source copies and alternative controller implementations distinct. Do not combine mutually exclusive launch paths into one apparent running system.
4. Treat README descriptions as leads to verify against code. Mark unavailable implementations and unresolved endpoints explicitly. Describe the diagram as source-derived unless runtime evidence was provided.

## ROS notation

Use nodes as the main boxes, with clearly labeled subsystem grouping where useful. In detail views, expand the selected node into its endpoints, callbacks, or operations while retaining its node boundary; include package/executable identity where helpful. A package is a source/build unit, not a runtime participant. Show process or component-container boundaries only when established and relevant to a detail view.

The table below defines ROS meaning and detail-view labels. At Level 1, abbreviate labels according to the visual standard above while preserving their meaning.

| Element | Representation |
| --- | --- |
| Topic | Publisher to named topic to subscription; label `TOPIC`, the resolved name, and `package/msg/Type`. Distinguish command/event triggers from state or sensor updates. |
| Service | Identify client and server; distinguish request and response. Label `SERVICE`, name, and `package/srv/Type`. Show a blocking wait only when implemented. |
| Action | Identify action client and action server. Label `ACTION`, name, and `package/action/Type`. Summarize goal/acceptance, feedback/result, and cancellation only where relevant and supported. |
| Timer | Show a periodic trigger when relevant to the selected view; include the configured period when known. |
| Local call | In detail views, show function or method invocation within a node, visually distinct from ROS communication. |
| Hardware or external system | Use a distinct boundary and label the actual transport, such as CAN. Do not depict hardware as a ROS node unless it is one. |

Use explicit edge labels and a small legend; color alone must not convey meaning. At system level, keep an action as one logical interface rather than expanding its underlying protocol topics and services. Exclude unrelated standard parameter services and diagnostic endpoints.

## Control-flow meaning

- Follow the relevant command/event paths and their completion paths. Show high-level fanout and result aggregation where implemented.
- A topic connection does not establish callback execution order. Distinguish receiving an event that starts work from receiving data that is stored for later use.
- Do not imply immediate execution, deterministic scheduling, or simultaneous motion from asynchronous calls or shared timestamps. Include executor and callback-group internals only in a selected detail view where relevant.
- Distinguish action acceptance from completion, cancellation requests from confirmed cancellation, and an action's terminal status from its result payload.
- Include failure or cancellation connections only when relevant to the selected view and evidenced. Do not invent feedback forwarding, recovery, or hardware-stop behavior.
- Keep conditions that change routing visible as short labels. Leave internal functions, loops, and drive state transitions out of the overview.

## Agent-readable Markdown

- Describe the same selected view as the PDF in plain text, so an agent can trace it without opening the PDF. Use concise bullets rather than narrative paragraphs; images, Mermaid, or renderer source alone are insufficient.
- Start with a title naming the view and level, then metadata bullets such as `source_pdf`, `workspace`, `configuration`, and `verification`. Give `source_pdf` as the project-relative PDF path. Distinguish source-derived findings from runtime verification.
- Use `## Semantics`, `## Nodes`, and `## Edges` sections. For a multi-page PDF, repeat these sections under a heading identifying each page/view. Define edge kinds, direction, grouping, and context or inference markers in words; do not rely on color, position, or line style.
- List each node as ``- `stable_id` | label | key: value | short fact``. Preserve IDs during revisions and exact ROS names where relevant. Include context boxes and group boundaries; use short indented bullets for necessary detail, units, timing, or unresolved behavior at the selected level.
- List each directed connection as ``- `source_id -> target_id` | kind | interface or purpose | condition or outcome``. Use one entry per connection, with optional fields only where relevant. Define undirected context links separately. Distinguish ACTION, SERVICE, TOPIC, LOCAL, and DATA where used; DATA denotes stored data or context, not a call. A list's order does not imply execution order.
- Preserve all meaningful PDF labels, conditions, failure/cancellation distinctions, and uncertainty. Mark missing or unknown facts explicitly without inventing connections or expanding the view. Keep both artifacts synchronized; Markdown is the text representation of the diagram, not an extra audit or evidence catalog.

## PDF and Markdown output and verification

1. Complete the required writing review before rendering. Use an available renderer that produces a real PDF, preferably with vector text and shapes. Graphviz DOT rendered with `dot -Tpdf` suits many graphs; a plotting/PDF library or manual placement may better handle complex routing. Do not assume automatic layout satisfies the visual rules.
2. Export PDFs to `./pdf_docs/` and Markdown companions to `./md_docs/`, relative to the working project root. Create these directories if needed. Use matching filename stems, such as `pdf_docs/system-overview.pdf` and `md_docs/system-overview.md`, or `<target>-detail` and `<target>-operation` for the selected detail level. Use filesystem-safe names and preserve existing filename stems during revisions unless asked to rename them.
3. Deliver both the PDF and its Markdown companion for every requested view, and update both during revisions. Neither a Markdown-only diagram nor a screenshot replaces the PDF. Keep renderer sources, working evidence inventories, and preview images in a temporary directory unless requested as deliverables; do not depend on temporary scripts from earlier sessions remaining available. This output rule does not restrict editing `SKILL.md` during skill maintenance.
4. Verify the exported PDF opens and has the intended page count. Render temporary previews of every exported page and inspect clipping, typography, spacing, label collisions, arrow direction, crossings, and distinctions between context, inference, and primary connections.
5. Correct layout defects and inspect the affected exported pages again. If PDF rendering or visual inspection is unavailable, state that limitation accurately; do not claim verification from the source canvas alone.
6. Check PDF–Markdown agreement: every diagram node and connector has a corresponding text entry, all edge endpoints resolve to declared IDs, and labels, direction, conditions, grouping, and uncertainty agree. Confirm the Markdown points to the matching PDF and retains the selected scope.
7. Return links to both the PDF and Markdown with a brief completion statement, then stop. Do not propose or generate additional views.
