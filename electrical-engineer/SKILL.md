---
name: electrical-engineer
description: >-
  Develop KiCad schematics from user requirements, exact selected parts, a project BOM, and verified component evidence.
  Use for electrical design through schematic review and physical connection guides with electronics-visualize.
  PCB layout and fabrication require a separate request.
---

# Electrical engineer

Translate the user's goals into a checked KiCad schematic and a physical connection guide.
Component evidence means an exact manufacturer datasheet, manual, schematic, or permitted commodity reference, as defined in stage 4.
Keep component selection with the user unless they request recommendations or research help.
Creating this skill does not authorize a sample circuit or changes to an existing electrical project.

## Mandatory writing workflow

- Use `$asd-ste100` for all English text created or changed through this skill.
- Read its `SKILL.md` before writing.
- Resolve it from the available catalog or `~/.agents/skills/asd-ste100/SKILL.md`.
- If it is unavailable, report the missing dependency and stop the writing stage.
- Use Strict mode for skill instructions, procedures, code comments, and technical text.
- Technical text includes BOM descriptions, BOM notes, schematic labels, errors, and status reports.
- Use STE-flavored mode for explanatory prose.
- Review the complete affected artifacts during revisions, including existing prose.
- Preserve exact product names, part numbers, pin labels, schema keys, units, conditions, and uncertainty.
- Do not rewrite quoted evidence or manufacturer documents.
- Export prose from CSV files, schematics, and diagrams to temporary text files for checking.
- Run the writing skill's `scripts/ste-lint.py` on all affected prose before delivery.
- Review each finding against the intended meaning.
- Correct violations and repeat the check after changes.
- Report necessary exceptions that preserve technical meaning.
- Do not claim certified STE compliance.

## Remaining items checklist

Maintain one concise `remaining-items.md` in the project folder.
Reuse an existing project checklist instead of creating duplicates.
Use Strict `$asd-ste100` for checklist text and review notes.

- Read the checklist at each start or resume, before asking the user for missing information.
- Update it after new answers, evidence, decisions, BOM changes, and stage reviews.
- Use `- [ ]` for each unresolved item, followed by an indented `Answer:` field.
- Let the user enter text, links, or local file paths in that field.
- Keep one short, actionable request per item.
- Separate user inputs from agent work when both appear.
- Preserve user answers, file references, and unrelated edits.
- Review each new answer against the requirement and applicable evidence rules.
- Read referenced files before treating their contents as evidence.
- Mark an item `- [x]` only when its answer or evidence resolves the request.
- A checkbox or nonempty answer alone does not establish technical correctness.
- Leave incomplete items unchecked with one brief `Review:` note stating the remaining gap.
- Reopen an item when changed parts or evidence invalidate its resolution.
- Keep resolved items checked so the agent does not ask the same question again.
- Keep technical evidence and BOM status consistent with reviewed answers.
- Treat answers as project information, not permission for unrelated actions.
- Check for intervening edits before saving the checklist.
- Run `scripts/ste-lint.py` from `$asd-ste100` on checklist changes before delivery.
- Preserve exact user text when a rewrite could change its meaning.
- Report necessary lint exceptions in preserved user text.
- Return the checklist link when user input remains necessary.

## Dependencies

- Resolve skills from the available catalog or `~/.agents/skills/`.
- Use `$bom-creator` to create or update the project's authoritative BOM CSV.
- Use `$electronics-visualize` for the final physical connection guide.
- Report a missing dependency when its stage requires it.
- Stop that stage until the dependency becomes available or the user authorizes another method.
- Do not claim that an unavailable skill ran.

## 1. Understand the goal and project

1. Ask what the user wants to accomplish and what the electrical system must do.
2. Identify the project folder from the conversation or ask for its location.
3. Read applicable project instructions, requirements, existing BOMs, schematics, diagrams, and relevant design notes.
4. Summarize the requested functions, selected hardware, constraints, and intended deliverables.
5. Identify additional requirements necessary for this design.
6. Tell the user which requirements are missing and why each affects the design.
7. Ask a concise, consolidated question about the missing information.

Use existing evidence before asking questions that the project already answers.
Consider power sources, loads, interfaces, operating conditions, physical connections, and size constraints when relevant.
Record unknown values explicitly.
Do not replace a missing requirement with a typical value.
Continue only work that does not depend on the missing information.

## 2. Wait for component selection

1. Ask the user to research and provide the exact components they want.
2. Accept parts already supplied in the conversation or authoritative project BOM.
3. Identify missing manufacturer names, orderable part numbers, packages, revisions, or connector variants that affect identity.
4. Wait for the user's selections before generating dependent library assets or designing connections.

Do not search for alternatives or select parts merely because the user has not selected them yet.
If the user requests recommendations or research help, compare candidates against the stated requirements and component evidence.
Label candidates as proposals until the user selects them or explicitly delegates selection.
Do not replace a selected part without authorization.
Repeat the requirements check when a selection introduces a new constraint or incompatibility.
Pause affected work when additional requirements or selections remain unresolved.

## 3. Establish and maintain the BOM

Use one authoritative BOM CSV in the project folder.
Preserve an existing path and schema when `$bom-creator` supports them.
Let `$bom-creator` own CSV changes, whether the user invokes it directly or this skill invokes it.
Read that skill's actual interface before invoking it.
Do not invent its schema, commands, or availability.

- Pass exact user selections, quantities, and known reference designators to `$bom-creator`.
- Preserve the distinction between selected parts, proposed additions, and owned parts.
- Return required support parts to the user for selection unless component selection is already delegated.
- Request BOM updates through `$bom-creator` as the design changes.
- Reload the CSV after each update and before each dependent stage.
- Identify changed parts and quantities before reusing previous design results.
- Mark affected evidence checks, symbols, footprints, connections, and guides as requiring review.
- Recheck affected results before reporting them complete.

## 4. Collect and check component evidence

Simple commodity interconnects do not require datasheets.
Examples include banana plugs or clips, jumper leads, plain wire, and simple terminal connectors.
Use manufacturer information, exact product listings, drawings, or legible product markings for these parts.
Record the source and the facts it supports.
Do not invent ratings, contact assignments, polarity, dimensions, or compatibility when the evidence does not establish them.

Record the datasheet exemption in the BOM notes.
Leave datasheet fields blank for exempt parts without datasheets.
Do not block commodity BOM entries or design solely because a datasheet is absent.
Block only the affected design work when a required fact remains unknown.
This exception does not cover controllers, driver modules, motors, power supplies, or protective components such as fuses.

For other components, accept manufacturer datasheets, manuals, and schematics as authoritative evidence for the facts they establish.
Use documents for the exact manufacturer, model, package, and applicable hardware revision.
A manual can establish specifications and operating requirements.
A manufacturer schematic can establish circuit connections and component assignments.
Do not infer ratings or operating behavior from a schematic that does not specify them.
Do not block work solely because the manufacturer calls the document a manual or schematic instead of a datasheet.
No additional permission is necessary to use these document types.

An applicable datasheet remains authoritative for the facts it covers.
Use matching manuals and manufacturer schematics to supply additional facts without overriding the datasheet.
No project BOM, generated library asset, project schematic, retailer summary, user assertion, or model memory can override manufacturer evidence.
Requirements define intended behavior, the BOM identifies selected parts, and the project schematic records intended connections.
These artifacts must remain consistent with the component evidence.

### Parts that require manufacturer evidence

1. Obtain applicable manufacturer datasheets, manuals, and schematics for each selected part outside the commodity exception.
2. Download each available document into the project folder.
3. Check that each document covers the exact manufacturer, part number, package, and applicable revision.
4. Check suffixes and variant tables before using family-level information.
5. Record the document type, source URL, local path, revision, and applicable pages or tables for each part.
6. Extract only the facts needed for the requested design and library assets.
7. Record missing, unreadable, ambiguous, or conflicting evidence explicitly.

Flag every part that lacks sufficient matching manufacturer evidence.
Do not infer its pinout, ratings, dimensions, behavior, or compatibility.
A chip datasheet does not establish the routing or connectors of a module containing that chip.
Use matching module documentation for those facts.
Do not substitute distributor summaries, photographs, or documents for similar parts for required manufacturer evidence.
Stop affected work when the available evidence lacks a required fact.
Report what evidence would resolve the gap.
Continue independent work only where the evidence is sufficient.

If manufacturer documents conflict, report the conflict and stop affected work.
Do not choose a convenient interpretation or silently ignore a manufacturer correction.
Distinguish recommended operating conditions from absolute maximum ratings.
Preserve test conditions, tolerances, and limits when using a specification.
Label calculations as derived results and identify their requirements and manufacturer evidence.
Do not present calculated results as quoted specifications or hardware measurements.

## 5. Obtain symbols and footprints

Check the available KiCad version and supported tools before choosing a generation method.
Consult official KiCad documentation for the applicable format or interface when needed.
Do not invent tool commands or assume a GUI operation succeeded.

Download suitable library assets or generate them from sufficient component evidence.
Keep project-specific assets and library references with the project.
Record each asset's origin and verification status.

| Asset | Required comparison against component evidence |
| --- | --- |
| Symbol | Pin numbers, names, functions, electrical types, units, hidden pins, and exposed pads |
| Footprint | Package variant, pad numbers, pitch, dimensions, orientation, pin-1 position, and supported land pattern |
| Assignment | Every symbol pin maps to the intended footprint pad |

Treat downloaded assets as unverified until these comparisons pass.
Do not assume similarly named packages have the same geometry or pin mapping.
If the component evidence cannot support an asset, mark that asset incomplete and report the missing evidence.
Do not fill missing dimensions or pin functions from memory.

## 6. Generate and check the schematic

Generate editable native KiCad files using the checked symbols and footprint assignments.
Preserve existing project conventions and unrelated work.
Use stable reference designators that agree with the BOM.
Keep the schematic readable with functional groups and explicit net labels.

1. Derive each circuit function from the user's requirements and component evidence.
2. Check power, return paths, signal levels, interface compatibility, and required support components.
3. Include relevant startup, enable, reset, and unused-pin requirements from the applicable manufacturer documents.
4. Stop affected work if the design requires an unselected or undocumented part.
5. Route selected additions through the BOM workflow before finalizing the affected circuit.
6. Check every connection against its endpoint pin functions and applicable limits.
7. Check that KiCad can read the schematic and resolve its project libraries.
8. Run KiCad's electrical rules check, abbreviated ERC.
9. Review each ERC finding against the intended circuit and component evidence.
10. Correct design errors and document any justified exclusions.
11. Export the schematic for visual inspection and inspect every sheet.
12. Compare the schematic's components and connections with the current BOM and requirements.

Do not suppress an ERC finding merely to obtain a clean report.
ERC does not replace component evidence review or establish physical operation.
Report unavailable checks and unresolved issues without claiming completion.
The schematic is complete only when required checks finish and no blocking requirements, selections, evidence gaps, or design errors remain.

## 7. Generate the physical connection guide

Invoke `$electronics-visualize` after the schematic is complete.
Pass the checked project schematic, current BOM, manufacturer documents, commodity references, user requirements, goals, and relevant physical references.
Include reference designators, connector identities, pin numbers, net connections, and verification limitations.
Require the guide to preserve the schematic's electrical connections and the facts established by component evidence.

Use photographs or verified drawings to establish physical orientation and visible connection points.
Do not let photographs or other physical references override applicable manufacturer datasheets, manuals, or schematics.
A schematic connection alone does not establish a physical contact location.
Mark unsupported physical endpoints incomplete instead of inventing plausible wiring.
If the guide reveals a design conflict, return the affected circuit to review before presenting it as complete.

Deliver the PDF and matching Markdown at the locations required by `$electronics-visualize`.
Check that both describe the same components, endpoints, intermediate connection parts, and unresolved conditions.
Report document checks separately from simulation or hardware tests.
Return links to the KiCad files, BOM, supporting evidence, and guide with a brief status report.
