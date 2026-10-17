---
name: framework-language-guide
description: Universal Master Learning & Framework Deep-Dive System. Automatically detects project stack, routes conceptual scope (Atomic Concept, Topic Cluster, Architectural Pattern), and builds a 3-tier cognitive ladder (Simple with Dry Run Table -> Production Idiom -> Framework Internals) with strict pseudocode discipline and an end-of-artifact Diagnostic Quiz.
version: 2.0.0
heisenberg:
  stage: understanding
  task_types: [feature, refactor, bug, algorithm, learning, framework-guide]
  artifact: framework-guide.md
  blocks: none
---

# Master Learning & Framework Deep-Dive System

> **PRIME DIRECTIVE:** Explain concepts, frameworks, and language implementations in their most intuitive form. Move systematically from first principles and mechanical step-by-step dry runs to production idioms and runtime internals. Never dump 200 lines of raw code; use signatures, data flow, state tables, and pseudocode stubs. Always conclude with a Diagnostic Quiz & Trap Test.

---

## 1. Core Teaching Philosophy: Connected Knowledge

When a developer asks about a concept, framework feature, runtime behavior, or language mechanism, do not provide an isolated encyclopedia definition. 

Teach it as a connected node in a knowledge graph:
- **Why it exists:** What bottleneck, footgun, or hardware reality forced its invention?
- **What came before:** What manual, brittle, or slow pattern did engineers use previously?
- **The Core Abstraction:** What mental model eliminates cognitive load?
- **How it executes:** Step-by-step state mutation across heap, stack, scope, and event loops.
- **Framework manifestation:** How popular frameworks (FastAPI, React Native, Tokio, etc.) expose it.
- **Trade-offs:** What does it cost in memory, CPU, latency, or conceptual overhead?

---

## 2. Automatic Project & Stack Detection

Before generating guidance, inspect the current workspace root to ground every explanation in the project's actual language and runtime conventions:

```mermaid
graph TD
    Root["Inspect Workspace Root"] --> NodeCheck{"package.json?"}
    Root --> PyCheck{"pyproject.toml / requirements.txt?"}
    Root --> RustCheck{"Cargo.toml?"}
    Root --> GoCheck{"go.mod?"}

    NodeCheck -->|Yes| JS["Stack: TypeScript / JavaScript<br/>(Node, Bun, React Native / Expo)"]
    PyCheck -->|Yes| PY["Stack: Python<br/>(FastAPI, Pydantic, asyncio, SQLAlchemy)"]
    RustCheck -->|Yes| RS["Stack: Rust<br/>(Tokio, Axum, Serde, Borrow Checker)"]
    GoCheck -->|Yes| GO["Stack: Go<br/>(Goroutines, Channels, Standard Library)"]
```

When explaining generic concepts, ground the syntax and idioms in the detected stack while keeping the underlying conceptual physics universal.

---

## 3. Scope & Mode Router

Determine the conceptual scope of the query before writing:

| Mode | Input Type | Strategy |
|---|---|---|
| **Mode A: Atomic Concept** | Single algorithm, mechanism, API, data structure, or syntax keyword (e.g., `async/await`, `Mutex`, `useMemo`, `Pydantic validator`). | Apply the full 3-Tier Cognitive Ladder directly to the mechanism. |
| **Mode B: Topic Cluster** | Strongly related group of topics (e.g., Processes vs Threads vs Event Loops; SQL Indexes vs Query Plans vs B-Trees). | 1. Identify shared problem.<br/>2. Build dependency DAG.<br/>3. Teach in dependency order; compare tradeoffs. |
| **Mode C: Architectural Pattern** | Broad system pattern or framework architecture (e.g., Guarded State Machine, SSE Streaming with Reconnect, Virtualized Lists). | 1. Central system question.<br/>2. Component responsibilities.<br/>3. Message flow & state lifecycle. |

---

## 4. The 3-Tier Cognitive Ladder & Dry-Run Protocol

Every explanation must follow the 3-Tier progression to take a junior or onboarding developer from zero intuition to deep production understanding:

```mermaid
graph LR
    T1["<b>Tier 1: Simple & Intuitive</b><br/>First principles, ELI5 metaphor,<br/>Mechanical Dry-Run Table"] --> T2["<b>Tier 2: Production Idiom</b><br/>Real-world patterns, error handling,<br/>Concurrency, ecosystem idioms"]
    T2 --> T3["<b>Tier 3: Runtime Internals</b><br/>Memory layout, event loop queues,<br/>State machines, syscalls"]
```

### 4.1 Tier 1: The Intuitive Foundation & Mechanical Dry Run
1. **The Plain-English Anchor:** Explain the concept in 2–3 sentences without buzzwords or circular definitions.
2. **Minimal Working Example (MWE):** A tiny 5-to-10 line example illustrating the core idea.
3. **The Mechanical Dry-Run Table:** Trace the execution line by line. Show exactly what variables change and where state lives:

| Step | Line # | Instruction | Stack / Local Scope | Heap / Shared State | Output / Side Effect |
|:---:|:---:|---|---|---|---|
| 1 | `L1` | `state = init()` | `state: 0x01` | `{ count: 0 }` | None |
| 2 | `L2` | `dispatch(INC)` | `action: 'INC'` | `{ count: 1 }` (mutated) | Listener notified |
| 3 | `L3` | `return state.count`| `return: 1` | Unchanged | Value 1 yielded |

### 4.2 Tier 2: Real-World Production Idiom
Show how senior engineers actually write this in production:
- Defensive validation and boundary conditions.
- Error propagation (handling failures gracefully without crashing).
- Idiomatic integration with standard library or framework conventions.
- Practical considerations: resource cleanup, context cancellation, idempotency.

### 4.3 Tier 3: Framework Internals & Engine Mechanics
Demystify what happens under the hood when the framework executes the code:
- How the runtime schedules or dispatches the work (e.g., Microtask queue vs Macrotask queue; OS thread vs Green thread).
- Memory allocation: stack vs heap, pointer indirection, cache locality, reference counting vs garbage collection.
- Internal invariants: what state machines or guards prevent corruption.

---

## 5. Signature & Pseudocode Discipline

> **ANTI-SLOP LAW:** Never paste 200 lines of boilerplate or complete implementation code into explanations. Long code blocks cause cognitive fatigue and obscure the core mental model.

Adhere to the strict structural representation rules:
- **Type Signatures First:** Show exact types, parameter names, and return contracts.
- **Variable Callouts:** Explicitly name and annotate the 2–3 critical variables holding invariant state.
- **Pseudocode Stubs:** Use concise, structured pseudocode highlighting the decision branch:

```typescript
// Focus on the invariant decision point, not the boilerplate
function reconcile<T>(prev: State<T>, next: Action): State<T> {
  // 1. Guard invariant
  if (!isValidTransition(prev.phase, next.type)) {
    throw new IllegalTransitionError(prev.phase, next.type);
  }
  // 2. Commit atomic state update
  return { ...prev, phase: next.targetPhase, version: prev.version + 1 };
}
```

---

## 6. Diagnostic Quiz & Trap Test Protocol

Every generated guide MUST conclude with a **Diagnostic Quiz** consisting of 3 to 5 targeted questions designed to test real understanding, spot edge cases, and bust common illusions of competence.

### Required Question Types:
1. **The Subtle Edge-Case Trap:** A realistic snippet with an off-by-one, race condition, closure capture trap, or unhandled rejection. Ask the user what happens and why.
2. **The Mental Model Check:** A scenario contrasting two superficially similar approaches (e.g., `useCallback` vs `useMemo`; `spawn` vs `spawn_blocking`; Task vs Thread).
3. **The "Fix the Silent Defect" Challenge:** A short 4-line snippet that compiles/runs but leaks memory or corrupts state under concurrency.
4. **The Tradeoff Evaluation:** "If our latency target is <5ms and memory budget is 50MB, why would this approach fail?"

### Answer Key Format:
Always place the answer key at the bottom inside an expandable `<details>` block or separated section with full explanations for both correct and tempting incorrect choices:

```markdown
<details>
<summary><b>View Diagnostic Quiz Answers & Explanations</b></summary>

1. **Question 1 Answer:** Option B.  
   *Explanation:* In Python/JavaScript closures, loop variables are captured by reference, not by value...
</details>
```

---

## 7. Required Artifact Structure (`framework-guide.md`)

When active in a task, emit the artifact to:
`.heisenberg/artifacts/<TASK-ID>/framework-guide.md`

Adhere strictly to this Markdown template:

```markdown
# Framework & Language Deep-Dive: <Topic Name>

> **Detected Stack:** <Language / Framework / Version>  
> **Conceptual Mode:** <Atomic Concept | Topic Cluster | Architectural Pattern>  
> **Prerequisites:** <Prerequisite A>, <Prerequisite B>

---

## 1. The Core Mental Model
- **Problem Statement:** What problem forced this into existence?
- **The Predecessor:** What did we do before this existed?
- **The Core Abstraction:** The single sentence mental model.

---

## 2. The 3-Tier Cognitive Ladder
### Tier 1: Intuitive Baseline & Dry-Run Trace
- Minimal Working Example (MWE)
- Line-by-Line Execution Trace Table (Stack / Heap / Output)

### Tier 2: Production Idioms & Patterns
- Real-world defensive patterns & standard library idioms
- Error propagation & resource hygiene

### Tier 3: Under the Hood (Engine & Runtime Internals)
- Memory lifecycle & allocation
- Execution scheduling & dispatch loop

---

## 3. Structural Specification
- Type Signatures & Interfaces
- Critical Invariant Variables
- Pseudocode Logic Stub

---

## 4. Trade-offs & Anti-Patterns
- What you trade off (Latency, Memory, Complexity)
- Common Pitfalls & Anti-Patterns

---

## 5. Diagnostic Quiz & Trap Test
1. **Question 1 (Edge-Case Trap):** ...
2. **Question 2 (Mental Model Check):** ...
3. **Question 3 (Spot the Silent Bug):** ...

<details>
<summary><b>View Answer Key & Explanations</b></summary>

...</details>
```
