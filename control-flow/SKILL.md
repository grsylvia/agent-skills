---
name: control-flow
description: Generate source-grounded ROS 2 control-flow diagrams as PDFs for reverse engineering at system overview, package/node, or callback/operation level. Use to trace execution through nodes, topics, services, actions, and callbacks. State-machine diagrams are outside its scope.
---

# ROS 2 control-flow diagrams

Generate the control-flow view selected by the user as a readable PDF. Explain how commands and events trigger execution and which responses or results allow work to continue.

## Select the level

Before generating a diagram, prompt the user: "Which control-flow level would you like: system overview, package / node detail, or callback / operation detail?" Present these three choices and wait for the selection. If the current command already specifies a level, use that selection without asking again. This prompt applies to diagram generation, not requests to edit the skill.

| Level | Scope and content |
| --- | --- |
| System overview | A very high-level visual map of the main nodes/subsystems and command paths. Use short role/node labels and a few essential ROS connections. Reserve interface catalogs, implementation detail and extensive references for double-click views. |
| Package / node detail | Nodes within the selected package or the internals of one node; publishers, subscriptions, service/action clients and servers, timers, callbacks, and how inputs lead to outputs. Keep external peers as context. |
| Callback / operation detail | One selected callback or operation; function calls, decisions, loops, asynchronous waits, result handling, cancellation, and failure branches. Include executor and callback-group constraints where they affect execution and are established by the code. |

For a detail view, ask which package/node or callback/operation to expand if the target is not already specified or clear from context. Generate only the selected view. Preserve the parent view's node names and incoming/outgoing interfaces when expanding an existing diagram; do not require or generate a parent diagram first.

## Level 1 visual standard

- Make the overview understandable at a glance. Show the main control path and only supporting paths needed to understand it; do not inventory every node, endpoint, utility or optional component.
- Keep boxes to a short role and node name, or a clearly labeled subsystem when several nodes are collapsed. Keep edges to a ROS kind (`TOPIC`, `SERVICE`, `ACTION`) and a short purpose. Use exact interface names only when they materially improve understanding.
- Leave message/service/action types, executable names, callback behavior, timing, detailed cancellation/failure handling, and configuration explanations to the requested double-click view.
- Preserve important gaps with brief labels such as `external` or `handoff unresolved`. Simplification must not invent a working connection.
- Use generous spacing, large readable text and a larger PDF canvas when useful. Do not shrink labels or pack explanatory paragraphs into the diagram. Choose orientation to suit the flow.
- Limit prose to a brief scope/configuration subtitle and a small legend. Do not add a dense evidence appendix to Level 1. Keep source grounding through inspection and unobtrusive source links on diagram elements where supported; show detailed source references in double-click views.

## Visual style

- For Agrobot, match the established state-machine diagrams, using `state_machine/agrobot-states.pdf` as a visual reference when available. Inspect a user-specified reference before styling; match presentation without importing state-machine semantics into control flow.
- Use a clean landscape page, a left-aligned title block, clear sans-serif typography, bold role labels, and smaller node names. Align boxes on a consistent grid with generous margins and whitespace.
- Use muted navy text (`#23364a`), pale blue node boxes (`#eaf2fa`), gray context/hardware boxes (`#f3f6f8`), and restrained amber or rose highlights for unresolved boundaries. Explain meaning with labels, not color alone.
- Route thin, consistent arrows through dedicated corridors. Keep labels away from lines and boxes; avoid crossings. Use a small legend and page number, with no decorative clutter or extra explanatory text.

## Scope

- Follow only the user's current command. An overview request authorizes one overview, not automatic package or callback expansions.
- Inspect the requested code and configuration without running robot nodes, building packages, installing software, or sending ROS commands.
- Do not add state machines, detailed motion sequences, audits, tests, launch instructions, recommendations, or extra documentation unless requested.
- If asked to modify this skill, modify it without also generating an example diagram unless requested.
- Generate deeper views only when selected by the user. Keep stable node and interface names across views.

## Skill refinement feedback loop

- Incorporate user tweaks and corrections as they arrive during skill use. Apply them to the current requested work and update this `SKILL.md` directly when they refine reusable skill behavior; do not defer all learning until the diagram is finished.
- Preserve the intended scope of feedback. Keep one-off diagram edits local to that diagram. Record reusable preferences or workflow corrections in the relevant skill section, qualified by level or context when appropriate. Ask only if it is unclear whether a change should persist and that distinction matters.
- Treat the user's latest explicit correction as superseding conflicting earlier guidance. Replace the affected instruction instead of accumulating contradictory rules or a chronological feedback log. Do not infer unrelated requirements from a single example.
- At the end of each series of changes—when the user signals completion, or before reporting completion of the currently requested batch—refactor and organize `SKILL.md`. Integrate refinements into the appropriate sections, consolidate duplicates, remove superseded wording, and check that scope, terminology, and PDF requirements remain consistent. Do not wait for or assume additional requests.
- Keep this cleanup limited to the skill and preserve all still-applicable user requirements. Do not create changelogs, extra documentation, example diagrams, or other artifacts as part of refinement unless requested.
- Validate the edited skill with the skill-creator validator when available and review it for conflicting instructions. Briefly report persisted refinements and completion, then stop. Skill maintenance does not authorize generating additional views or changing robot code.

## Establish the system boundary

1. Identify the requested workspace, subsystem, and launch/configuration variant. Read package manifests, executable entry points, launch files, parameters, and relevant node implementations.
2. Resolve node names, namespaces, interface names, remappings, and parameter overrides where the source permits. Record the selected configuration in the PDF. If no variant is specified, choose one supported by the source and state that assumption; ask only when alternatives would materially change the requested overview.
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

## PDF deliverable

- Write the PDF to the user's requested location; otherwise use `control-flow/system-overview.pdf`, `control-flow/<target>-detail.pdf`, or `control-flow/<target>-operation.pdf` in the working project, matching the selected level. Use a filesystem-safe target name.
- Use Graphviz DOT with clusters and labeled edges, rendered with `dot -Tpdf`, or another available renderer that produces a real PDF. A Markdown diagram or screenshot alone does not satisfy the request.
- Keep intermediate diagram source and preview images in a temporary directory unless the user requests those artifacts too.
- Choose page size and orientation for a spacious diagram with readable text. Level 1 follows the visual standard above; detail views may include concise source references, configuration assumptions and unresolved boundaries, with an additional reference page only when needed.
- In detail views, map diagram elements to repository-relative file paths, symbols and line numbers. Cite the implementation/configuration supporting connections, not just package documentation. At Level 1, keep this evidence out of the visible diagram except for unobtrusive links.
- Verify the PDF exists and opens successfully. Render a temporary page preview with an available PDF tool and inspect it for clipped labels, overlapping edges, and unreadable text. If rendering or inspection is unavailable, report the limitation without claiming verification.
- Return a link to the PDF and a brief completion statement. Stop after the requested deliverable; do not propose or generate additional views.
