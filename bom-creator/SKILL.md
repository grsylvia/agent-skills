---
name: bom-creator
description: >-
  Create and maintain a project BOM CSV for any engineering project, with optional electrical metadata.
  Use for recording selected parts, quantities, specifications, and component changes, directly or through electrical-engineer.
  Follow source-bom's input format without invoking sourcing, estimating costs, or choosing suppliers.
---

# Create and maintain a BOM

Maintain one authoritative bill of materials, abbreviated BOM, in the project folder.
Support direct user requests and updates requested through `$electrical-engineer`.
Use `$source-bom` as a format reference only.
Future sourcing coordination belongs to the calling skill or user.

## Scope

- Create or update BOM data only within the requested project and scope.
- Do not invoke `$source-bom`, run sourcing commands, estimate costs, or request sourcing approval.
- Do not choose suppliers, obtain quotes, purchase parts, or edit a costed BOM.
- Do not change sourcing preferences, supplier configuration, or the sourcing agent.
- Do not generate schematics or connection guides as part of BOM maintenance.

## Mandatory writing workflow

- Use `$asd-ste100` for all English text created or changed through this skill.
- Read its `SKILL.md` before writing.
- Resolve it from the available catalog or `~/.agents/skills/asd-ste100/SKILL.md`.
- If it is unavailable, report the missing dependency and stop the writing stage.
- Use Strict mode for skill instructions, procedures, code comments, and technical text.
- Technical text includes BOM descriptions, specifications, notes, errors, and status reports.
- Use STE-flavored mode for explanatory prose.
- Review the complete affected artifacts during revisions, including existing prose.
- Preserve exact manufacturer names, part numbers, reference designators, schema keys, units, conditions, and uncertainty.
- Do not rewrite quoted evidence or manufacturer documents.
- Export prose from CSV fields to a temporary text file for checking.
- Run the writing skill's `scripts/ste-lint.py` on all affected prose before delivery.
- Review each finding against the intended meaning.
- Correct violations and repeat the check after changes.
- Report necessary exceptions that preserve technical meaning.
- Do not claim certified STE compliance.

## Establish project context

1. Identify the project folder and requested BOM operation.
2. Read applicable project instructions, requirements, existing BOM data, and relevant component records.
3. Use the existing authoritative CSV when its identity is clear.
4. Ask which file is authoritative if multiple candidates remain ambiguous.
5. Use `bom.csv` in the project folder for a new BOM unless the user specifies another path.
6. Identify missing requirements that affect part identity, specifications, or quantities.
7. Explain why those requirements matter and ask a concise question about the missing information.

Do not overwrite an imported workbook or unrelated CSV during conversion.
Preserve the source file and identify the resulting project CSV explicitly.
If an existing schema requires conversion, explain the mapping before changing it.
Do not discard information that the target columns cannot represent.

## Component selection and evidence

Accept exact selections from the user, existing project records, or the calling skill's authorized request.
Do not treat an example as evidence of selection or ownership.
Wait for the user to research unresolved components unless they request research help or delegate selection.
Label recommendations as proposals until the user selects them or explicitly delegates selection.
Do not silently substitute another manufacturer, part number, package, or revision.

Use supplied evidence to record component facts.
For electrical components, accept exact manufacturer datasheets, manuals, and schematics under `$electrical-engineer`'s evidence rules.
Use each document only for facts it establishes about the selected model and applicable revision.
An applicable datasheet remains authoritative for the facts it covers.
Report conflicts between manufacturer documents before dependent design.
Do not block a part solely because its evidence is a manufacturer manual or schematic.
Preserve the following exception for simple commodity interconnects.
Examples include banana plugs or clips, jumper leads, plain wire, and simple terminal connectors.
These commodity parts do not require datasheets.
Use manufacturer information, exact product listings, drawings, or legible markings to support the recorded facts.

Record the source and datasheet exemption in `notes`.
Leave datasheet fields blank for exempt parts without datasheets.
Do not infer missing ratings or contact assignments.
The exception does not cover controllers, driver modules, motors, power supplies, or protective components such as fuses.
Do not infer component facts when matching manufacturer evidence does not establish them.

Record proposed requirements as requirements, not verified component specifications.
Keep unresolved information explicit while continuing independent BOM work.

## CSV format

Find `$source-bom` through the available skill catalog or `~/.agents/skills/source-bom/SKILL.md`.
Resolve symbolic links before locating its repository and referenced format documentation.
Read its `docs/FORMATS.md` and the active `suppliers.toml` as format references.
Do not execute its setup or sourcing workflow.
If these references are unavailable, use the columns below for a draft and report that current compatibility remains unchecked.
If the documented format changes, report the difference before converting existing data.

Keep the seven core columns first, in this order:

| Column | Meaning and constraints |
| --- | --- |
| `part_id` | Stable, unique, nonempty identifier for the BOM row |
| `description` | Clear part name and manufacturer when known |
| `category` | Exact category from the active `suppliers.toml` |
| `quantity` | Total required quantity, expressed as a positive integer |
| `spec` | Purchasing requirements, including manufacturer, package, revision, units, and substitution restrictions where applicable |
| `mfr_part_number` | Exact manufacturer part number, including suffixes |
| `notes` | Supporting context that does not change purchasing eligibility |

The format requires `part_id`, `description`, `category`, and `quantity` for every complete row.
Keep unknown required values blank in a draft and report the affected identifiers.
Never invent a quantity or select a category merely to pass an input check.

Leave `mfr_part_number` blank for unresolved parts or parts defined by an approved specification.
An exact electrical component selection requires its full identity before dependent electrical design can proceed.

Define the counted unit in `spec` when a row does not count individual pieces.
For bulk materials, preserve the required length, mass, or volume with explicit units.
Agree on a purchasing unit before converting a fractional requirement into an integer quantity.
Do not round silently or confuse required quantity with supplier pack size.
Do not automatically subtract owned parts from the total requirement.

Append these engineering columns when needed:

| Column | Meaning and permitted values |
| --- | --- |
| `selection_status` | `proposed`, `selected`, or `unresolved` |
| `ownership_status` | `owned`, `planned`, or `unknown` |
| `reference_designators` | Space-separated component references, such as `R1 R2` |
| `datasheet_url` | Source URL for the exact datasheet |
| `datasheet_path` | Project-relative path to the local datasheet |
| `evidence_status` | `verified`, `missing`, `conflicting`, or `not_applicable` |

Use `selection_status` whenever rows include proposals or unresolved selections.
If this column is absent, do not infer selection solely from a row's presence.
Use existing project decisions or ask the user when selection affects the requested operation.
Use `ownership_status` when ownership information is relevant.
Do not infer ownership from a selection, quotation, or schematic reference.

`verified` means the evidence matches the component and supports the recorded facts.
It does not mean the circuit or physical assembly passed a test.
For parts that require manufacturer evidence, use `missing` when matching documents are unavailable or insufficient.
A matching manual or manufacturer schematic can support `verified` status for the facts it establishes.
For exempt commodity parts, use `verified` when the permitted evidence supports the recorded facts.
Use `missing` when a required commodity fact lacks evidence, rather than merely because no datasheet exists.

Use `not_applicable` only when the evidence requirement does not apply, with the reason in `notes`.
Keep `datasheet_url` and `datasheet_path` specific to actual datasheets.
Record manual and schematic types, source URLs, local paths, revisions, and relevant pages in `notes` or a linked evidence index.
Leave datasheet fields blank when only manuals or manufacturer schematics are available.
Check every cited local evidence path before delivery.
Keep package and revision requirements in `spec` instead of adding conflicting duplicate fields.
Preserve existing additional columns and their documented meanings.

## Create or update the BOM

1. Read the current CSV before preparing changes.
2. Match requested updates to stable `part_id` values and exact part identities.
3. Ask for clarification when a requested update could affect multiple different parts.
4. Add, change, or remove only the requested rows and fields.
5. Preserve identifiers for existing rows and never reuse a removed identifier for an unrelated part.
6. Preserve distinct packages, revisions, specifications, and selection states when considering duplicate rows.
7. Record reference designators without assigning the same component instance to multiple parts.
8. Explain quantity differences caused by spares or other requirements when reference counts differ.
9. Check the proposed content before replacing the authoritative CSV.
10. Check that the source file did not change during preparation.
11. Reconcile intervening edits before saving.
12. Use a CSV writer that preserves quoting, text identifiers, and embedded punctuation.
13. Write the complete replacement to a temporary file before replacing the destination.
14. Reopen the saved CSV and check the resulting rows.

Report an identity change even when the row identifier stays the same.
Do not merge rows merely because their descriptions resemble each other.
For new rows, follow the existing identifier convention or use `P-001`, `P-002`, and subsequent unused identifiers.
Preserve leading zeros, capitalization, and suffixes in part numbers.

## Check and return the result

- Check column names, row structure, unique identifiers, and required values.
- Check that complete quantities are positive integers with defined units where needed.
- Check categories against the active format reference.
- Check engineering status values and references when those columns exist.
- Check that cited local datasheet paths exist before reporting those files as available.
- Preserve unresolved and conflicting evidence in the completion report.
- Distinguish a saved draft from a BOM whose core fields pass the format checks.

Return the authoritative CSV path and a short summary of added, changed, and removed rows.
Include affected `part_id` values, changed fields, unresolved requirements, and compatibility limitations.
When `$electrical-engineer` calls this skill, identify changes that require dependent design results to be checked again.
Return control to the caller after BOM maintenance.
Do not start sourcing or the caller's next design stage.

## Compatibility boundary for future sourcing

The current sourcing importer retains only the seven core columns in its working data.
Preserve engineering metadata in the authoritative CSV.
Never replace that CSV with a sourcing export or costed BOM.

The current quote cache excludes `notes` and additional engineering columns from part identity.
Keep purchasing constraints in `spec`, `description`, or `mfr_part_number` so future sourcing receives them.
The importer does not filter selection or ownership status.
Report this limitation to the caller when the BOM contains mixed states.
The future sourcing coordinator must choose eligible rows and resolve total-cost versus remaining-purchase scope.
Any later export must preserve identifiers and remain derived from the authoritative CSV.
Creating this skill does not implement or authorize that future sourcing workflow.
