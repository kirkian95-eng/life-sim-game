# CLAUDE.md — life-sim-game

## Project Overview

**life-sim-game** is a vibe-coded ecology simulation game. The project is in its early stages — treat it as a greenfield codebase.

## Repository Structure

```
life-sim-game/
├── CLAUDE.md        # This file — AI assistant guide
├── DECISIONS.md     # Architecture & dependency decision log
└── README.md        # Project description
```

> As the project grows, update this section to reflect new directories (e.g., `src/`, `assets/`, `tests/`, `public/`).

## Development Workflow

### Getting Started

1. Clone the repo and check out your feature branch
2. Install dependencies (once a package manager is configured)
3. Run the dev server (once set up)

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

> To be determined as the project takes shape. Update this section when a framework, engine, or language is chosen.

## Common Tasks

| Task | Command |
|------|---------|
| Install dependencies | _TBD_ |
| Run dev server | _TBD_ |
| Run tests | _TBD_ |
| Build for production | _TBD_ |

> Fill in commands as the toolchain is established.

## Game Design Context

This is an **ecology simulation** — key domain concepts to be aware of:

- **Ecosystems**: Environments with interacting organisms and resources
- **Food webs**: Energy flow between producers, consumers, and decomposers
- **Population dynamics**: Birth, death, carrying capacity, competition
- **Resource cycles**: Energy, nutrients, water flowing through the system

AI assistants should use domain-appropriate terminology when naming variables, functions, and modules.
