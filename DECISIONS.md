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

**Status**: Active

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
