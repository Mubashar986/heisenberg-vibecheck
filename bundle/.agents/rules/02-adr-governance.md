---
name: adr-and-architecture-governance
description: Decision-first governance enforcing the tech hard-lock, competitive evaluation, platform primitives first, and a living decision register. Right-sized for the project team.
version: 3.0.0
---

# Rule 03: Decision Record Governance

> **STATUS: OPERATIONAL LAW — ZERO SILENT DEPENDENCIES**
> Spontaneous library installation, inline architectural choices, or silent
> technological shifts are prohibited. Every tool, database, SDK, or framework
> introduced into this repository must trace back to a recorded decision.
>
> **Where the records live:** `docs/DECISIONS-LOCKED.md` is the register. It is
> already populated with the closed decisions for this project (sections A–G).
> Read it before you propose a new one.

---

## 1. Why Decision Governance Exists

Without it, an AI-assisted team introduces libraries on impulse:
- Turn 3 uses `axios`.
- Turn 8 another agent uses `fetch`.
- Turn 14 a subagent adds `got`.
- Turn 22 someone alters the schema with raw SQL instead of the migration tool.

The result is an unmaintainable Frankenstein codebase with a schema nobody can
explain. The fix is not ceremony — it is **one place where a decision is written
down, once, before code depends on it.**

---

## 2. When a Record Is Required

A record is required for any change to a **locked pillar**:

| Pillar | Locked value for this project |
|---|---|
| Language / runtime / package manager | Python + FastAPI (backend), TypeScript + Expo (mobile) |
| Web / API framework | FastAPI |
| Database / ORM / migrations | Postgres + pgvector, Alembic |
| Search / indexing | Hybrid keyword + vector with track filters |
| Auth / session strategy | Google OIDC → own JWT + rotating refresh |
| State management | Mobile: MMKV + token-driven state |
| Design system primitives | Locked by the canvas — `docs/ui-reference/` |
| Queue / worker engine | Redis |
| AI model, embeddings, vector store | Model-agnostic gateway (see `DECISIONS-LOCKED.md §D`) |

If a task touches a pillar without a recorded decision, **halt and record it
first.** If the pillar is already recorded above, cite it and proceed — do not
re-litigate a closed decision.

---

## 3. The Laws

### LAW 1: The Technology Hard-Lock
The pillars in §2 cannot be chosen inline in a task. They are decided in a
record, with the user's sign-off, before code depends on them.

### LAW 2: The Zero-Inline-Decision Law
Do not run `pip install`, `npm install`, `poetry add`, or `expo install`
without citing the decision it implements:
```
npm install mmkv # Governed by DECISIONS-LOCKED E5: Local store
```

### LAW 3: The Competitive Evaluation Mandate
A **new** decision (not already closed) evaluates **2 to 5 distinct
approaches** with a real reason for each rejection. Two is acceptable for a
small, reversible choice. Five is for something high-stakes and hard to undo.

> Right-sized: this team has 2.4 weeks. Do not write a five-candidate essay to
> choose a date-formatting library.

### LAW 4: The Honest Rejection Ledger
For each option not selected, record the genuine technical reason:
- Banned: *"Option B was rejected because Option A is better."*
- Required: *"Drizzle was rejected because we need automated multi-file
  migration rollback and Prisma Studio for non-technical triage."*

### LAW 5: Platform Primitives First (The Anti-NPM Rule)
Candidate option #1 is **always the native platform primitive**:
- Native `fetch` before `axios`.
- `crypto.randomUUID()` before `uuid`.
- Native `pathlib` / `node:fs` before a file-utility package.
- CSS/RN layout primitives before a layout library.

A third-party dependency must earn its place against the built-in.

### LAW 6: Live Verification
Before finalizing a record, verify against current reality: the latest stable
version, recent breaking changes, and any open critical security issue. Do not
record a version pin you have not checked.

### LAW 7: Blast Radius & Upgrade Risk
Record the ripple effect: breaking schema change? peer-dependency conflict?
What is the upgrade risk over the next twelve months?

### LAW 8: The Quality Audit (scaled)
Score a candidate on the vectors that matter **for this choice**. The full
enterprise matrix is 17 points; the practical default set is:
security history · runtime performance · type quality · reversibility ·
maintainer health · license compatibility · transitive dependency count ·
lock-in risk.

Use the full 17 only when the decision is both high-stakes and hard to reverse.

### LAW 9: The Record Family
Decisions are classified by kind. Use the label in the register:

| Label | Covers |
|---|---|
| `ADR` | Topology, hosting, routing, frameworks |
| `DDR` | Schemas, normalization, indexes, partitioning |
| `AIDR` | Models, chunking, embedding dimensions, prompt caching |
| `FDR` | Design tokens, component primitives, motion, state stores |

### LAW 10: The Human Sign-Off Barrier
The agent may draft, research, and evaluate (`status: PROPOSED`). The agent
**cannot accept a decision**. Acceptance is the user's (`status: ACCEPTED`).
The user is the project lead and sole architecture authority.

### LAW 11: The Living Register
All decisions are recorded in `docs/DECISIONS-LOCKED.md`. New decisions are
added as a new numbered row in the relevant section, with a date and a
one-line summary. Do not create a parallel register.

### LAW 12: The Record Chassis
Every new record uses this structure:

```markdown
# [ID]: [Short Title]

- **Status:** [PROPOSED | ACCEPTED | REJECTED | SUPERSEDED by <ID>]
- **Kind:** [ADR | DDR | AIDR | FDR]
- **Date:** YYYY-MM-DD
- **Owner:** [Name / Role]

## 1. Context and Problem Statement
## 2. Decision Drivers
## 3. Considered Options (native primitive first)
## 4. Decision Outcome & Rationale
### Honest Rejection Ledger
## 5. Pros, Cons, and Trade-offs
## 6. Exit Strategy — how we remove this if it dies
```

### LAW 13: Exit Strategy (Reversibility)
Every accepted record answers: *"If this technology fails, is acquired, or is
abandoned in six months, how do we remove it without rewriting the app?"*

### LAW 14: The Adapter Seam
External SDKs and services are never called directly from core domain logic or
UI views. They are wrapped: `class ObjectStorageAdapter implements IStorage`.
This is what makes Law 13 possible.

### LAW 15: License & Dependency Audit
Viral copyleft licenses (GPL-3.0 in proprietary software) are blocked unless
explicitly waived. Packages with more than ~50 transitive dependencies need a
reason.

### LAW 16: Superseding Protocol
To replace a decision: create the new record, mark the old one
`SUPERSEDED by <new ID>`, and update the register. The history stays intact.

### LAW 17: No Fabricated Graph Sync
Earlier versions of this rule required logging each accepted decision into a
graph memory service. That service does not exist here. Record the decision in
`docs/DECISIONS-LOCKED.md` and, if it is a durable operating fact, in
`.workbuddy-ai/memory/MEMORY.md`.

---

## 4. Greenfield vs. Brownfield

- **Greenfield:** the tech-stack record was written during Stage 0. It exists —
  see `docs/DECISIONS-LOCKED.md §B, §C, §E`.
- **Brownfield:** write a baseline record documenting the pre-existing system
  before proposing changes.
