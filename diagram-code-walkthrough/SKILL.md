---
name: diagram-code-walkthrough
description: Teach control-flow and state-machine diagrams through a user-paced, step-by-step walkthrough tied to small code examples, starting at the implementation's entry point. Use for guided learning from existing diagrams, including control-flow and state-machine skill outputs. Does not generate diagrams or modify the implementation.
---

# Diagram code walkthrough

Help the user understand how a diagram becomes running code, one small step per
turn. Assume a beginner unless context establishes otherwise. Explain necessary
programming and ROS terms when they first appear.

## Establish the starting point

- Use the diagram, source tree, and target already selected in the conversation.
  If the target is unclear, inspect available filenames and ask one focused
  question to select it. Accept either diagram kind; do not require both.
- Inspect the relevant PDF pages visually as well as extracting text when tools
  permit. Follow arrowheads and the legend, not PDF text order. If visual access
  fails, disclose the limitation and do not guess connections from label order.
- Locate the implementation using diagram links, labels, and symbols. Establish
  its source version and launch/configuration variant. Keep historical copies,
  backups, and alternative implementations separate. Read project instructions
  and required evidence before explaining that project's implementation.
- Begin at the earliest evidenced entry point within the selected scope. For a
  system this may be launch, process entry, or node construction; for a selected
  callback it is the triggering event and callback entry. For a state machine,
  locate its owner, state storage, and initialization before its first transition.
  Explain startup even when it sits outside the diagram, labeling that context.
- Briefly orient the user to the selected view, then teach only the first step.
  Avoid a complete tour or a long prerequisite lecture before starting.

## Teach one step

A step covers one small implementation idea, such as creating a subscription,
handling one callback, testing one guard, or assigning one state. Split large
diagram boxes across turns when needed. Use this compact shape flexibly:

1. **Where we are:** Give the step number, diagram filename/page, and exact box
   or arrow label. Name the responsible component and the current state if known.
2. **What happens:** Explain the trigger, immediate operation, and purpose in
   plain language. Introduce only concepts needed for this step.
3. **Code:** Show a small, focused snippet in the implementation's language,
   usually around 5–15 lines. Link actual excerpts to their file and line. Explain
   each meaningful line or short block, connecting it to the diagram.
4. **What changed:** State the before/after values or state, any output, and what
   event or condition allows execution to continue. Say when no state changes.
5. **Pause:** End with a short prompt such as “Say `next` to continue, or ask
   about this step.” End the turn and wait for the user.

Keep an actual excerpt faithful to the source. Mark omissions; label adaptations
as “simplified from source” and explain any behavior omitted. Label invented
snippets “illustrative example—not verified project code.” Never invent file
paths, line references, functions, or transitions and present them as evidence.
Use short comments above logical steps in authored examples; explain unchanged
source excerpts in prose. Do not translate the project to another language unless
the user asks.

If source is unavailable, say so. Teach the diagram's supported meaning with
clearly labeled illustrative code and keep implementation claims unresolved.
If the diagram conflicts with code, cite the mismatch and explain the inspected
code's behavior without silently correcting or rewriting the diagram.

## Let the user control progress

- Advance one step only after an explicit command such as `next`, `continue`,
  or an unambiguous request to proceed. Silence, a question, a quiz answer, or a
  general acknowledgement does not authorize advancement.
- Answer questions about the current step without moving the walkthrough cursor.
  Explain more simply, line by line, or with another small example when asked,
  then pause again. Do not require quizzes or correct answers to proceed.
- Honor `back`, `repeat`, `restart`, `skip to …`, and `stop` as navigation requests.
  Identify the new position after a jump and mention essential skipped context.
  A request to explain a later element is a detour unless the user asks to move
  there; retain the original position for resuming.
- At branches, state the condition being followed. Use a supported normal path
  initially when reasonable; introduce alternatives only as needed at that
  decision or when selected. Never imply the chosen example covers all outcomes.
- Keep the selected artifacts/version, current step, current state, chosen
  branch, and next topic in conversation context. On resume, give a brief
  position reminder. If context is missing, ask rather than inventing progress.
- At the end of the selected path, give a short recap and identify any unresolved
  handoff. Stop without automatically expanding into another path or diagram.

## Preserve diagram and code semantics

- Control flow explains which event invokes which operation. Distinguish a local
  call from a ROS message, callback registration from callback execution, and
  stored data from a trigger. Do not turn asynchronous connections into a proven
  sequential schedule; explain the wait or handoff at the current step.
- State machines explain an owner's state and its transitions. Ground each
  change in its event, guard (condition), assignment, and effect. An enum alone
  does not establish transitions. Label conceptual modes and inferred phases;
  do not invent a state variable or treat every function as a state.
- Keep task state, action goal status, bridge modes, drive states, and managed
  node lifecycle distinct. Keep independent machines separate. When both diagram
  kinds exist, connect them at a verified event or operation; not every control
  step changes state, and a state can contain several operations.
- Distinguish request, acceptance, completion, result payload, cancellation, and
  confirmed physical stopping. Describe code inspection as source-derived;
  claim runtime or hardware behavior only when supported by provided evidence.

## Scope

Teach in chat through read-only inspection. Do not run robot nodes, send ROS or
hardware commands, build packages, install dependencies, edit code, or create
lesson documents as part of a walkthrough. Discuss examples without executing
them unless separately requested and authorized.

Existing diagrams from `$control-flow` and `$state-machine` are inputs to this
skill. Their diagram-generation prompts and PDF delivery rules do not govern
this chat lesson. Use those skills only if the user separately requests a new or
revised diagram; this skill remains usable without them being installed.
