# CLAUDE.md — life-sim-game

## Project Overview

**life-sim-game** is a vibe-coded ecology simulation game. The project is in its early stages — treat it as a greenfield codebase.

## Repository Structure

```
life-sim-game/
├── simulation/
│   ├── __init__.py
│   ├── engine.py        # Ecosystem class — tick loop with 5 phases
│   ├── species.py       # Species/SpeciesConfig dataclasses, default params
│   └── food_web.py      # FoodWeb class — predator-prey relationships
├── tests/
│   ├── __init__.py
│   ├── test_engine.py   # Ecosystem tick, phase, and stability tests
│   ├── test_species.py  # Species behavior and default config tests
│   └── test_food_web.py # Food web relationship tests
├── app.py               # Flask REST API
├── requirements.txt     # flask, pytest
├── PLAN.md              # Design plan and parameter tables
├── DECISIONS.md         # Architecture & dependency decision log
├── CLAUDE.md            # This file — AI assistant guide
└── README.md            # Project description
```

## Development Workflow

### Getting Started

1. Clone the repo and check out your feature branch
2. `pip install -r requirements.txt`
3. `python -m pytest tests/` to verify everything works
4. `python app.py` to start the Flask dev server on port 5000

### Git Conventions

- **Branch naming**: Feature branches use `claude/<description>-<session-id>` format
- **Commit messages**: Use clear, imperative-mood messages (e.g., "Add creature spawning system", "Fix food chain energy transfer")
- **Commits**: Make small, focused commits — one logical change per commit
- **Push**: Always use `git push -u origin <branch-name>`
- **Never** force-push or push to `master` without explicit permission

### Code Style

- Keep code simple and readable — this is a vibe-coded project, so clarity over cleverness
- Prefer small, composable functions over large monolithic ones
- Name game entities and systems descriptively (e.g., `Creature`, `Ecosystem`, `FoodWeb`)
- Add comments only where the logic isn't self-evident

## Mandatory Rules

These rules apply to every session and every change:

1. **Maintain DECISIONS.md**: For every major architecture change, new dependency, or resource/tooling choice — add an entry to `DECISIONS.md` with the decision, alternatives considered, tradeoffs, and reasoning. This is non-negotiable.
2. **Keep CLAUDE.md current**: Update this file whenever the repo structure, tech stack, or workflows change.

## Key Conventions for AI Assistants

### Before Making Changes

- Read existing files before modifying them
- Understand the current architecture before proposing new patterns
- Check for existing utilities/helpers before creating new ones

### When Writing Code

- Do not over-engineer — build only what is needed right now
- Avoid introducing unnecessary dependencies
- Keep game simulation logic separate from rendering/display logic
- Prefer editing existing files over creating new ones when possible

### When Adding New Systems

- Each game system (e.g., creatures, terrain, resources) should be modular
- New systems should integrate with existing ones through clear interfaces
- Update this CLAUDE.md when adding major new directories or systems
- **Update DECISIONS.md** for every major architecture choice, new dependency, or resource tradeoff — log what was decided, what alternatives were considered, and the reasoning

### Testing

- Write tests for game logic (simulation, math, state management)
- Visual/rendering code may not need unit tests but should be manually verified
- Run all tests before committing

## Tech Stack

- **Language**: Python 3.11+
- **Web framework**: Flask 3.x (minimal REST API)
- **Testing**: pytest 8.x
- **Simulation model**: Tick-based discrete simulation with Holling Type II predation

## Common Tasks

| Task | Command |
|------|---------|
| Install dependencies | `pip install -r requirements.txt` |
| Run dev server | `python app.py` |
| Run tests | `python -m pytest tests/` |
| Run tests verbose | `python -m pytest tests/ -v` |

## Game Design Context

This is an **ecology simulation** — key domain concepts to be aware of:

- **Ecosystems**: Environments with interacting organisms and resources
- **Food webs**: Energy flow between producers, consumers, and decomposers
- **Population dynamics**: Birth, death, carrying capacity, competition
- **Resource cycles**: Energy, nutrients, water flowing through the system

AI assistants should use domain-appropriate terminology when naming variables, functions, and modules.
