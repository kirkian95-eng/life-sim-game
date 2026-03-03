# Architecture & Design Decisions

This file tracks major decisions made during development of life-sim-game. Every significant architecture choice, dependency addition, or resource tradeoff is logged here for later evaluation.

**Format**: Each entry includes the decision, alternatives considered, tradeoffs, and reasoning.

---

## Decision Log

### 001 — Project bootstrapping approach (2026-03-03)

**Decision**: Start with a minimal repo (README + CLAUDE.md) and let the tech stack emerge from requirements rather than picking a framework upfront.

**Alternatives considered**:
- Start with a full game engine (Unity, Godot, Phaser)
- Start with a web framework + canvas (React + HTML5 Canvas, plain JS + Canvas)
- Start with a terminal/text-based prototype

**Tradeoffs**:
- (+) No premature commitment to a stack that might not fit the game's needs
- (+) Lets early design decisions inform tooling choices
- (-) No runnable code yet — first real feature will require a stack decision

**Status**: Superseded by 002

---

### 002 — Python + Flask for simulation backend (2026-03-03)

**Decision**: Use Python with Flask as the tech stack. Python for the simulation engine, Flask for a lightweight REST API layer.

**Alternatives considered**:
- JavaScript/TypeScript with Node.js (would share language with future frontend)
- Rust or Go (better performance for large simulations)
- Python with FastAPI (async, auto-docs)

**Tradeoffs**:
- (+) Python is ideal for scientific/simulation code — NumPy/SciPy available if needed later
- (+) Flask is minimal and doesn't impose structure — good for a vibe-coded project
- (+) Fast to prototype and iterate on simulation parameters
- (-) Python is slower than compiled languages for tight simulation loops
- (-) Flask is synchronous — could matter if simulation ticks are expensive

**Status**: Active

---

### 003 — Tick-based discrete simulation model (2026-03-03)

**Decision**: Use a discrete tick-based simulation where each tick runs 5 sequential phases: growth → feeding → starvation → reproduction → natural death.

**Alternatives considered**:
- Continuous ODE-based model (Lotka-Volterra differential equations)
- Event-driven simulation (events scheduled on a priority queue)
- Agent-based model (individual creatures with state machines)

**Tradeoffs**:
- (+) Simple to implement, debug, and test
- (+) Each phase is independent and testable in isolation
- (+) Easy to add new phases later
- (-) Less realistic than continuous models — dynamics depend on tick granularity
- (-) No individual variation between creatures of the same species

**Status**: Active

---

### 004 — Holling Type II functional response for predation (2026-03-03)

**Decision**: Use a Holling Type II functional response curve for predation: `density_factor = prey_pop / (prey_pop + half_saturation)`. This reduces predation efficiency when prey is scarce, creating a natural refuge effect.

**Alternatives considered**:
- Linear predation: `max_catchable = prey_pop * hunt_success` (original approach — caused prey extinction)
- Hard prey floor: prevent any species from dropping below a minimum count
- Lotka-Volterra style: predation proportional to predator × prey product

**Tradeoffs**:
- (+) Prevents extinction spirals — prey recovers when scarce
- (+) Ecologically realistic — mimics predator difficulty finding sparse prey
- (+) Creates natural oscillations rather than requiring artificial floors
- (-) Adds a tuning parameter (half_saturation = 30% of max_pop) that affects all dynamics
- (-) Can make predator populations settle quite low if prey is the bottleneck

**Status**: Active

---

### 005 — Parameter tuning for 6-species ecosystem stability (2026-03-03)

**Decision**: After multiple rounds of tuning, settled on these key parameter choices:
- Grass: high capacity (5000), fast regrowth (0.60), initial 3000
- Rabbits: prolific breeders (repro=0.45), low food needs (2 grass), high max pop (400)
- Predator hunt success kept low (0.30-0.40) to prevent prey collapse
- Eagle diet: 70% rabbit / 30% snake (originally 60/40 then 40/60)
- Wolf diet: 70% deer / 30% rabbit

**Key tuning lessons**:
- Original params had herbivore consumption (1550/tick) vastly exceeding grass supply (800 total) — grass died instantly
- Rabbit is the keystone prey species (eaten by 3 predators) — needs highest reproduction
- Eagles depending on scarce snakes caused extinction — shifted diet toward abundant rabbits
- Holling Type II response was essential for preventing extinction cascades

**Equilibrium reached** (500 ticks): grass=3376, rabbit=299, deer=20, snake=3, wolf=3, eagle=1

**Status**: Active — parameters will need retuning as new features are added

---

<!-- TEMPLATE — copy this for new entries

### NNN — Short title (YYYY-MM-DD)

**Decision**: What was decided.

**Alternatives considered**:
- Option A
- Option B

**Tradeoffs**:
- (+) Benefits
- (-) Drawbacks

**Status**: Active | Superseded by NNN | Revisit

-->
