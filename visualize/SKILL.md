---
name: visualize
description: Create paired PDF diagrams and agent-readable Markdown for systems, workflows, relationships, and state machines in any domain, using spacious layouts and a consistent navy and pale blue visual style. Use for general diagram visualization; use specialized ROS control-flow or state-machine skills for their domain-specific source analysis. Not for dashboards, UI implementation, or quantitative charts.
---

# General-purpose diagram visualizer

Turn the requested source material or concept into a readable PDF diagram with an agent-readable Markdown companion. Reuse the visual language of the control-flow and state-machine skills without imposing robotics concepts on other domains.

## Required writing skill

- You must use `$asd-ste100` for all English text you write or revise while using or maintaining this skill. Read its `SKILL.md` before writing. Resolve it from the available skills or [the sibling installation](../asd-ste100/SKILL.md). If it is unavailable, report the missing dependency and stop writing until it is available.
- Apply it to diagram titles, labels, legends, Markdown companions, user messages, and skill edits. Use Strict mode for technical descriptions, conditions, instructions, and text for agents. Use STE-flavored mode for explanatory prose.
- Preserve exact identifiers, paths, code, formulas, units, and required notation. Keep named states and interfaces unchanged. Short names and structured labels need not become full sentences. Write complete sentences for behavioral claims when a fragment could hide the actor or condition.
- Preserve every fact, condition, scope limit, uncertainty, and distinction between requests and outcomes. Keep precise wording when a shorter version would change the meaning. Do not claim certified STE compliance.
- Before rendering, apply the skill's review process to the diagram text and Markdown companion. Run its `scripts/ste-lint.py` on temporary text exports. Review findings against the source meaning. Correct applicable findings and record necessary exceptions in the brief completion message. Repeat the review after text changes.
- Use `$asd-ste100` as the writing process within this workflow. Keep this skill's PDF and Markdown structure, notation, and delivery rules. Return the artifact links and brief completion message instead of replacing them with the writing skill's text-only response.


## Choose the view

- Use the requested diagram kind, target, and detail level when established. Otherwise clarify only the missing choices that materially affect the result: relationships, procedural flow, or states; overview or a selected detail. Wait for required selections before generating.
- Accept prose, structured nodes and connections, code, configuration, or a supplied reference.
- A request to expand or “double-click” means generate only the selected detail, preserving parent names and relevant incoming/outgoing connections. It does not require interactive PDF behavior or generating a parent view first.
- Generate only the requested views. Creating or editing this skill does not also authorize sample diagrams.

## Preserve meaning

Choose semantics before layout. Shared styling must not make distinct relationships appear equivalent.

| View | Boxes represent | Connections represent |
| --- | --- | --- |
| System or relationship map | Entities, components, or explicitly labeled groups | Named relationships, dependencies, or exchanges; arrows only when direction has meaning |
| Workflow or control flow | Operations, decisions, and clearly differentiated participants or context | Execution or event progression, with branch conditions and waits where supported |
| State machine | States of an identifiable owner | Transitions labeled `event [condition] / effect` where relevant |

- For state machines, separate independent machines onto their own requested pages. Identify the owner and distinguish explicit states from inferred phases. Keep interfaces and dependencies in context boxes; do not turn every component or operation into a state. Use initial/final markers only when justified.
- For workflows, distinguish data exchange from execution order and requests from completion. Do not imply synchronous execution or deterministic scheduling from an asynchronous connection.
- For relationship maps, grouping does not establish execution order or exclusive states. Label containment or dependency meaning explicitly where ambiguous.
- Use solid arrows for primary evidenced flow or transitions and dotted connectors for context. In relationship maps, define the applicable relationship styles in the legend.
- Use the specialized control-flow or state-machine skill when the task requires its ROS-specific semantics and source inspection; retain its level selection and scope rules. General diagrams must work without those skills installed.

## Ground the content

- For an existing system, inspect relevant implementation and configuration within the requested boundary. Treat descriptive documentation as leads to verify, keep alternative configurations distinct, and call static findings source-derived rather than runtime-verified.
- For a user-described concept or proposed process, use that description as the basis and label proposals or assumptions appropriately. Do not invent source evidence.
- Preserve missing implementations, uncertain relationships, and unresolved handoffs with concise labels. Do not fill gaps with idealized recovery, readiness, or completion behavior.
- Detail views may use short owner/symbol references and repository-relative paths with line numbers.
- Source inspection does not authorize running the depicted system, building it, installing dependencies, or changing its code.

## Shared visual parameters

| Parameter | Standard |
| --- | --- |
| Page | Clean white canvas; landscape by default, with orientation and size adapted to the flow |
| Text | Muted navy `#23364a`; clear sans-serif type |
| Primary boxes | Pale blue `#eaf2fa` by default; use semantic severity colors for issues; bold primary labels |
| Context boxes | Gray `#f3f6f8`; explicitly labeled context or external boundary |
| Secondary text | Smaller concise identifiers or details, still comfortably readable |
| Highlights | Restrained green for supported successful outcomes, amber for uncertainty, rose for faults; always include textual meaning |
| Title block | Left-aligned main title only; no eyebrow/overline above it and no subtitle below it |
| Layout | Consistent alignment grid, generous margins, whitespace between groups |
| Connectors | Thin, consistent strokes; explicit direction and concise labels where needed |
| Footer | Small legend and page number; no explanatory paragraphs |

Green, amber, and rose are semantic accent families, not fixed hex values. Use restrained, low-saturation colors: pale tinted fills with darker matching labels or borders and readable text contrast. Avoid vivid alarm red and other highly saturated fills, including for severe issues. Do not impose a mandatory font size or page size; preserve legibility at the intended viewing scale.

## Issue and severity views

- Make findings read as issues: use an explicit issue heading, a concise problem statement, and a subordinate consequence. Include proposed fixes only when they belong to the requested source or scope; distinguish them from completed changes.
- Give high, medium, and low severity distinct, tasteful colors and explicit text labels. Prefer muted rose, soft ochre, and muted lavender; reserve green for supported success or resolution. Preserve source severity and uncertainty without inventing a ranking.
- Organize the view around a meaningful hierarchy such as subject → severity → issue, or affected component → issue when that better fits the source. Use group headings, indentation, aligned rows, bands, or labeled branches to make membership and priority visible; avoid an undifferentiated grid of equal cards.
- Use position, spacing, and typography as well as color to convey priority. Keep evidence, consequences, and proposed fixes subordinate to the issue label; keep reference data and uncertainty notes visually distinct. Define grouping connectors without implying sequence or causation, and keep uncertainty distinct from severity.

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

## Agent-readable Markdown

- Describe the same selected view as the PDF in plain text, so an agent can trace it without opening the PDF. Use concise bullets rather than narrative paragraphs; images, Mermaid, or renderer source alone are insufficient.
- Start with a title naming the view and detail level, then metadata bullets such as `source_pdf`, `scope`, `basis`, and `verification`. Give `source_pdf` as the project-relative PDF path. Include configuration or state owner when relevant. Distinguish source-derived findings, user-described concepts, proposals, and assumptions; do not invent runtime verification.
- Use `## Semantics`, `## Nodes`, and `## Edges` sections. For a multi-page PDF, repeat these sections under a heading identifying each page/view. Define connection kinds, direction, grouping, and context or inference markers in words; do not rely on color, position, or line style.
- List each node as ``- `stable_id` | kind: entity | label | short fact``, choosing kinds appropriate to the view, such as operation, decision, state, context, group, or issue. Preserve IDs during revisions. Use short indented bullets for necessary details, units, timing, or unresolved behavior at the selected level. Record group membership and severity explicitly where shown; keep severity distinct from uncertainty.
- List each directed connection as ``- `source_id -> target_id` | kind | relationship or event | condition or effect``. Use one entry per connection, with optional fields only where relevant. Use `--` for undirected relationships and define its meaning. For transitions, retain `event [guard] / effect`; for workflows, distinguish data exchange, execution, requests, and completion. Grouping and list order do not establish execution order or causation. If the view has no connections, state that under `Edges` without inventing any.
- Preserve all meaningful PDF labels, conditions, outcomes, hierarchy, and uncertainty. Mark missing or unknown facts explicitly without inventing connections or expanding the view. Keep both artifacts synchronized; Markdown is the text representation of the diagram, not an extra audit or evidence catalog.

## PDF and Markdown output and verification

1. Complete the required writing review before rendering. Use an available renderer that produces a real PDF, preferably with vector text and shapes. Graphviz DOT rendered with `dot -Tpdf` suits many graphs; a plotting/PDF library or manual placement may better handle complex routing. Do not assume automatic layout satisfies the visual rules.
2. Export PDFs to `./pdf_docs/` and Markdown companions to `./md_docs/`, relative to the working project root. Create these directories if needed. Use matching filename stems, such as `pdf_docs/<short-descriptive-name>.pdf` and `md_docs/<short-descriptive-name>.md`. Use filesystem-safe names and preserve existing filename stems during revisions unless asked to rename them.
3. Deliver both the PDF and its Markdown companion for every requested view, and update both during revisions. Neither a Markdown-only diagram nor a screenshot replaces the PDF. Keep renderer sources, working evidence inventories, and preview images in a temporary directory unless requested as deliverables; do not depend on temporary scripts from earlier sessions remaining available. This output rule does not restrict editing `SKILL.md` during skill maintenance.
4. Verify the exported PDF opens and has the intended page count. Render temporary previews of every exported page and inspect clipping, typography, spacing, label collisions, arrow direction, crossings, and distinctions between context, inference, and primary connections.
5. Correct layout defects and inspect the affected exported pages again. If PDF rendering or visual inspection is unavailable, state that limitation accurately; do not claim verification from the source canvas alone.
6. Check PDF–Markdown agreement: every diagram node and connector has a corresponding text entry, all edge endpoints resolve to declared IDs, and labels, relationship kinds, direction, conditions, outcomes, grouping, severity where applicable, and uncertainty agree. Confirm the Markdown points to the matching PDF and retains the selected scope.
7. Return links to both the PDF and Markdown with a brief completion statement, then stop. Do not propose or generate additional views.

## Refine the skill

Apply one-off content or layout edits only to the current diagram. When user feedback establishes a reusable preference, integrate it into the relevant section of this skill, replacing superseded guidance. Keep refinements scoped to this skill unless the user requests changes elsewhere. Consolidate duplicates, check semantics and paired output requirements for consistency, and run the skill-creator validator when available before reporting a skill update complete. Respect filesystem permissions and claim persistence only after a successful write.
