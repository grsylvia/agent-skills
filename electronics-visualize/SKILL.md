---
name: electronics-visualize
description: Create visual electronics connection guides with component photos or accurate drawings, exact pin and terminal locations, and named connection parts. Use when the user wants to see where wires connect on physical hardware. Match visualize's navy and pale blue style. Deliver paired PDF and Markdown files. Use general visualize for abstract system maps.
---

# Electronics connection visualizer

Show the component, show the connection point, and show the parts between the endpoints.
The reader must see where each wire physically attaches without translating an abstract block diagram.

## Scope and writing

- Use this skill for physical connections between boards, modules, connectors, power supplies, sensors, motors, and similar electronics.
- Preserve the user's selected hardware, scope, and output preferences. Label additional connection parts as proposals or requirements, not owned components.
- Creating or editing this skill does not authorize a sample diagram or changes to hardware or firmware.
- Use `$asd-ste100` for English text. Resolve its `SKILL.md` from the available skills catalog or `~/.agents/skills/asd-ste100/SKILL.md`.
- Read that skill before writing. If it is unavailable, report the missing dependency before continuing the writing workflow.
- Use Strict mode for wiring instructions and technical descriptions. Use STE-flavored mode for explanatory prose.
- Preserve exact product names, pin labels, units, and uncertainty. Do not claim certified STE compliance.
- Before rendering, review the text and run `scripts/ste-lint.py` from the writing skill on temporary text exports.
- Review each finding against the intended meaning. Repeat the review after text changes. Report necessary exceptions briefly.

## Establish the physical reference

1. Identify each component's manufacturer, model, revision, and connector variant from the user's information and available evidence.
2. Separate owned parts, planned purchases, and additional proposed parts. Ownership does not prove an installed connection.
3. Prefer a clear user photo for the physical item. Prefer manufacturer pinouts, drawings, and manuals for electrical identity.
4. Check that the image and pinout describe the same hardware revision. A similar product photo is insufficient evidence for pin positions.
5. Inspect each image before using it. Record its source and the visible orientation.
6. Resolve material gaps through existing evidence first. Request a clear photo or exact model when the physical endpoint remains uncertain.

The default result describes proposed wiring unless evidence establishes the installed wiring.
Document-derived pin locations do not prove continuity, polarity, correct assembly, or operation on the user's hardware.

## Component pictures and orientation

- Make recognizable component pictures the main content. Do not replace components with text cards, generic icons, or schematic symbols alone.
- Use exact product photos, manufacturer illustrations, or accurate vector drawings based on verified references.
- Preserve the physical connector arrangement, pin count, keying, polarity marks, and important silkscreen labels.
- Show orientation explicitly: component side, solder side, connector mating face, or wire-entry face, as applicable.
- Include a recognizable landmark near each pin group, such as the USB socket, mounting hole, latch, notch, or pin-1 mark.
- Do not mirror a board or connector image to simplify routing. Rotate only with consistent pin mapping and a visible orientation cue.
- Enlarge small headers and terminals in detail insets. Keep the full component visible for orientation.
- A generated illustration can support a conceptual overview. It cannot establish physical pin locations or replace a verified wiring reference.
- Keep all critical pin labels and wire paths under deterministic layout control. Do not depend on image generation for exact wiring geometry.
- If a source image hides an endpoint, use a verified alternate view or a marked inset. Do not invent the hidden contact.

## Anchor each connection to a physical point

Maintain one connection model for the drawings and the Markdown companion.
Record these fields before routing wires:

| Record | Required information |
| --- | --- |
| Component | Stable ID, exact model/revision, ownership, image source, view orientation, and orientation landmark |
| Endpoint | Component ID, printed label, connector reference, pin or terminal position, and evidence |
| Anchor | Endpoint ID, position on the source image or drawing, and the transform into the page |
| Connection | Stable ID, both endpoint IDs, electrical purpose, wire or cable, intermediate parts, and assembly status |
| Uncertainty | Missing fact, affected endpoint or connection, and what would resolve it |

An anchor is a point on the actual contact or wire-entry location, not the edge of a component card.
Use image coordinates or normalized coordinates consistently. Preserve anchors through scaling, rotation, and placement.

- Terminate each wire at its verified anchor. Show a small marker and a legible pin or terminal label beside that point.
- Keep endpoint labels separate from wire labels. Use the same endpoint IDs in detail insets and the companion text.
- For a plug, show the mating socket and the insertion side. Distinguish male and female contacts.
- For a screw terminal, mark the wire-entry opening. Do not make the wire appear to attach to the screw head.
- For a header, identify the individual hole or pin. Do not terminate the wire at the header group or board outline.
- For a breadboard, show the actual hole positions and the relevant internal connections. Check rail breaks and the center gap.
- For a stepstick or similar module, distinguish module pins from carrier terminals. Check the carrier routing and module orientation.
- If a carrier or connector remains unselected, show the known component and an amber detail labeled `Needs confirmation`.
- Do not draw an uncertain endpoint as a completed connection. Continue the verified portions and identify the unresolved physical connection.

## Show the connection parts

For each connection, show the parts that make the connection possible.
Use a recognizable picture or verified drawing for an intermediate connector, splice, fuse holder, or adapter when its physical use matters.

- Label the cable or wire type, quantity, connector gender, and conductor size where relevant and known.
- Show both ends of a cable. Identify any required plug removal, stripping, crimping, soldering, or adapter.
- Draw both interfaces of an intermediate connector. Do not hide a missing interface behind a generic line.
- Identify each independent conductor when polarity, coil pairing, or signal assignment matters.
- Show the internal relationship between contacts when it affects wiring. For example, all contacts in a common splice share one electrical node.
- Preserve verified wire colors. Mark proposed colors as proposed. Use neutral colors when the installed colors are unknown.
- Keep power and return paths distinct. Show common ground only where the connection model establishes it.
- Check relevant voltage, current, polarity, and wire compatibility against primary documentation before presenting a usable physical connection.
- Do not use ordinary logic jumpers or breadboard contacts for a power path without evidence that their ratings support the proposed load.
- Show essential support parts, such as a required capacitor, when they belong to the requested connection. Label unresolved values or parts explicitly.
- Do not turn a wiring illustration into an unsolicited redesign or an exhaustive safety checklist.

## Visual style

Retain the visual language of `$visualize` while making component pictures dominant.
The following parameters are sufficient to use this skill without loading the general diagram workflow.

| Element | Standard |
| --- | --- |
| Canvas | White, spacious, usually landscape |
| Text | Muted navy `#23364a`, clear sans-serif type |
| Component panels | Pale blue `#eaf2fa`, with prominent component pictures |
| Context panels | Gray `#f3f6f8` |
| Status accents | Muted green for established status, amber for uncertainty, rose for a supported fault |
| Title | One left-aligned title, without an overline or subtitle |
| Wiring | Thin, clear paths with readable endpoint and connection labels |
| Footer | Compact legend and page number |

- Use color with explicit text. Do not tint product images so strongly that connectors or silkscreen marks become unclear.
- Keep physical wire colors distinct from status colors. Explain both meanings when both appear.
- Use lines without arrowheads for electrical connections. Add arrows only when direction is relevant and explicitly defined.
- Use dots only for electrical junctions. Use visible gaps or bridges at unrelated crossings.
- Define line styles in the legend. Distinguish proposed wiring, reported assembly, and unresolved connections without implying hardware verification.
- Route wires through open space. Avoid components, labels, and unrelated contacts.
- Use short numbered connection labels with nearby part callouts. Do not replace the drawing with a connection table.
- Prefer an assembly view with detail insets. Split into additional pages when the contacts or labels would otherwise become too small.
- Preserve component and endpoint IDs across pages. Give a page reference for each continued connection.
- Do not add pages outside the requested scope. A request for exact physical connections includes the detail needed to see those connections.

## Deliverables

- Deliver a real PDF at `pdf_docs/<stem>.pdf` and a matching text companion at `md_docs/<stem>.md`.
- Preserve existing filename stems during revisions unless the user asks for a new name.
- If the user requests PNG output, also export the requested pages as PNG files. A PNG preview does not replace the paired deliverables by default.
- Respect existing ignore rules and explicit requests to keep generated PDFs local. Do not force-add ignored artifacts.
- Keep renderer code, source-image copies, coordinate maps, and review previews temporary unless the user requests them as deliverables.
- Keep source links unobtrusive in the PDF. Include image and pinout provenance in the companion, without a separate reference appendix.

The Markdown must describe the same physical connections as the PDF.
Use `source_pdf`, `scope`, `basis`, and `verification` metadata, followed by `Semantics`, `Nodes`, and `Edges` sections for each view.

- `Nodes`: Record component IDs, model/revision, ownership, image reference, view orientation, and orientation landmarks.
- Under each component, record its endpoint IDs, printed labels, physical locations, and pinout evidence.
- `Edges`: Use `component.endpoint -- component.endpoint` for electrical continuity without a direction claim.
- Give each edge its connection ID, purpose, connection parts, conductor details, assembly status, and unresolved conditions.
- Define wire colors, junctions, crossings, line styles, insets, and continuation labels in words.
- Record unknown endpoints explicitly. Do not invent a physical anchor to satisfy the document structure.
- Keep meaningful labels and qualifications synchronized. A logical netlist alone does not describe a physical connection guide.

## Check before delivery

1. Check the connection model against the exact component references. Check orientation, polarity, and connector face before checking layout.
2. Export the PDF. Check that it opens and contains the intended pages.
3. Render and inspect every exported page. Inspect each endpoint at sufficient magnification to distinguish adjacent contacts.
4. Trace every wire from one physical endpoint to the other, including all intermediate connection parts.
5. Check for false junctions, reversed views, hidden contacts, ambiguous pin labels, and unsupported hardware claims.
6. Check that every depicted component, endpoint, connection, and unresolved detail appears in the Markdown.
7. Correct defects and inspect the affected pages again. State any verification limitation accurately.
8. Return the artifact links and a brief completion message. Do not claim electrical testing from a document review.

A finished physical guide must let the reader recognize the component, orient it, identify the correct contact, and identify the required connection parts.
When evidence cannot support one of these actions, mark that portion incomplete instead of presenting a plausible wiring picture as verified.
