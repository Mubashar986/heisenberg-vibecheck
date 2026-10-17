# AGENTS.md — Master Engineering Contract

> **STATUS: SUPREME REPOSITORY CONSTITUTION**  
> This is the single governing contract for every AI coding agent working in this repository (Cursor, Claude Code, Antigravity, Copilot, Windsurf, Aider). There is no second rulebook. If something in a conversation, prompt, or skill conflicts with this document, **this file wins**.

Read this file fully before your first edit. Then read only the skills your task manifest selects — never the whole skill library.

---

## 0. Project Charter & Architectural Invariants

*This project is governed by Heisenberg Vibe-Check to maintain laboratory-grade code quality and prevent AI hallucination drift.*

| Authority | Source | What It Governs |
|---|---|---|
| **Highest** | `AGENTS.md` | Core engineering contract & stage-gate workflow |
| **High** | `.agents/rules/*.md` | Operational laws (WBS lifecycle, ADRs, error protocol, git hygiene) |
| **Config** | `.agents/policy.json` | Gate strictness and directory paths |
| **Registry** | `.agents/skills.json` | Available skill definitions and required artifact pairings |

**Rule Zero: A closed architectural decision is not re-openable by an agent.** Spontaneous library changes, silent dependency injections, or modifying files outside your approved scope are strictly prohibited.

---

## 1. Bootstrap Protocol

Every AI agent must follow this exact sequence upon starting work:

1. Read `.agents/policy.json` to verify active gates and enforcement modes.
2. Locate the active task manifest in `.agents/tasks/TASK-*.json`.
   - If none exists and you are about to touch product code, **STOP** — create one first (§2).
3. Load **only** the skills your manifest declares in `selected_skills`, resolving paths via `.agents/skills.json`.
4. **Skill Attestation Mandate:** To prove the skill was read completely and prevent shortcut hallucinations, your `understanding.md` artifact **MUST** include a `Skill Attestation` header quoting the active skill's exact Prime Directive and 3 invariant laws.

Run the validator whenever you have terminal access:
```bash
python .agents/guard.py validate --workspace .
# or:
npx heisenberg-vibecheck validate
```

---

## 2. The Task Gate (The Core Law)

> ⛔ **NO PRODUCT CODE EDITS WITHOUT AN ACTIVE TASK MANIFEST AND PRE-EDIT ARTIFACTS.**

- Manifests live in `.agents/tasks/<TASK-ID>.json`.
- The manifest declares: `task_id`, `task_type`, `selected_skills`, `required_before_edit`, `required_artifacts`, and exact `files_in_scope`.
- Artifacts live in `.agents/artifacts/<TASK-ID>/`.
- Complete tasks require a certified receipt at `.agents/receipts/<TASK-ID>.json`.
- **Anti-Drift Lock:** You are only permitted to edit files explicitly listed in `files_in_scope`. Any file outside that list is a scope violation — the guard hook will terminate your edit.
- Control files (`.agents/`, `AGENTS.md`, `.git/`, `.cursor/`, `.claude/`) are policy infrastructure and exempt from product scope locks.

**Valid Task Statuses:** `planned` ➔ `approved` ➔ `implementing` ➔ `verifying` ➔ `complete` (or `blocked`).

---

## 3. The 4-Stage Planning Sequence

Do not skip any stage. Precision over velocity:

```mermaid
flowchart LR
    S0["Stage 0: WBS Genesis<br/>roadmap-wbs-planner"] --> S1["Stage 1: Understanding<br/>concept-to-code-bridge"]
    S1 --> S2["Stage 2: Design<br/>codebase-design + Mermaid"]
    S2 --> Pause["<b>THE DESIGN PAUSE</b><br/>Human explicit sign-off"]
    Pause --> S3["Stage 3: Scoped Implementation<br/>files_in_scope only"]
    S3 --> S4["Stage 4: Verification<br/>testing-verification"]
    S4 --> Receipt["Certified Receipt<br/>.agents/receipts/TASK-XX.json"]
```

1. **Understand (Stage 1):** Produce `.agents/artifacts/<TASK-ID>/understanding.md`. Map the mental model, call-flow, and pass the **10-Point Concept Grill Battery** (concurrency races, partial failures, security attack vectors, Big-O limits).
2. **Design (Stage 2):** Produce `.agents/artifacts/<TASK-ID>/design.md`. Every affected file must be tagged `[NEW]`, `[MODIFY]`, or `[DELETE]`. Include a **Mermaid visual diagram** (sequence or flowchart) and calculate the blast-radius across all callers.
   - For high-risk refactors or complex bugs, invoke `narrsistic-pluto` (3–5 researched options with honest rejection reasons and rollback triggers).
   - For UI tasks, route through The Muses (`picasso` ➔ `escher` ➔ `vermeer`).
3. **The Design Pause (The Human Gate):**  
   When `understanding.md` and `design.md` are generated, **THE AGENT STOPS**. Present the plan to the user. **Zero implementation code may be written until the human developer explicitly approves.**
4. **Implement (Stage 3):** Edit strictly inside `files_in_scope`. No drive-by refactorings, no unannounced library additions.
5. **Verify (Stage 4):** Run targeted tests and write `.agents/artifacts/<TASK-ID>/verification.md` containing raw terminal output.
6. **Receipt Certification:** Generate `.agents/receipts/<TASK-ID>.json` and transition status to `complete`.

---

## 4. Evidence, Honesty & Anti-Hallucination Laws

- **Tagged Claims:** Tag every technical assertion as `[VERIFIED]` (read directly or executed), `[INFERRED]`, or `[ASSUMED]`. Never present assumptions as facts.
- **Zero Silent Mocks:** The UI/API never fabricates backend data. Missing fields or endpoints must fail loudly and be documented.
- **Fail Loudly:** Empty catch blocks, bare `except:`, and `@ts-ignore` used to suppress real failures are strictly banned.
- **2-Strike Rollback:** If a terminal command or bug fix fails twice consecutively, **halt immediately**. Run `git checkout .` to revert to baseline, and perform an Ishikawa 5-Whys Root Cause Analysis before touching code again.

---

## 5. Working Rules in `.agents/rules/`

Read the operational rule relevant to your task phase:

| Rule | File | When to Read |
|---|---|---|
| **Rule 01** | `.agents/rules/01-wbs-lifecycle.md` | Planning a task, onboarding, or managing task transitions |
| **Rule 02** | `.agents/rules/02-adr-governance.md` | Introducing libraries, choosing patterns, or changing data models |
| **Rule 03** | `.agents/rules/03-error-protocol.md` | Diagnosing crashes, test failures, or command exit errors |
| **Rule 04** | `.agents/rules/04-git-and-team.md` | Branching, pre-stage secrets scan, atomic conventional commits |

---

## 6. On-Demand Utility Aids

Developers may trigger these lightweight aids at any time:
- **`bro`**: Restate the explanation in plain, concise human language with zero enterprise jargon or corporate fluff.
- **`how`**: Rapidly trace execution call-flow and answer code placement questions (*"where should this live?"*).
- **`why`**: Run git archaeology, inspect git blame, and uncover historical design intent and postmortems.

---

## 7. Completion Checklist

A task is complete only when:
- [ ] Active task manifest exists in `.agents/tasks/`.
- [ ] `understanding.md` exists with mandatory Skill Attestation header.
- [ ] `design.md` exists with Mermaid architecture diagram and blast radius.
- [ ] Developer explicitly approved the design during the Design Pause.
- [ ] Code modifications match `files_in_scope` with zero foreign file pollution.
- [ ] `verification.md` records raw passing test output.
- [ ] Certified receipt exists in `.agents/receipts/`.
- [ ] `python .agents/guard.py validate --workspace .` returns clean green.
