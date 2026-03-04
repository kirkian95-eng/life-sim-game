# Ecology Simulation — Design Plan

## Goal

Build a tick-based closed ecological simulation with a Flask API. The simulation models energy flow from the sun through a food web of 6 species, with population dynamics tuned for long-term stability.

---

## Food Web

```
         ☀ Sun
           │
           ▼
        🌿 Grass
        ╱       ╲
       ▼         ▼
   🐇 Rabbit   🦌 Deer
    ╱  |  ╲        |
   ▼   ▼   ▼      ▼
 🐍  🦅  🐺    🐺
Snake Eagle Wolf  Wolf

Eagle also eats Snake.
```

### Feeding relationships (predator → prey)

| Predator | Prey            |
|----------|-----------------|
| Rabbit   | Grass           |
| Deer     | Grass           |
| Snake    | Rabbit          |
| Wolf     | Rabbit, Deer    |
| Eagle    | Rabbit, Snake   |

### Trophic levels

1. **Producer**: Grass (solar-powered regrowth)
2. **Primary consumers**: Rabbit, Deer
3. **Secondary consumers**: Snake, Wolf, Eagle

---

## Core Simulation Rules

### Tick-based model

Each tick represents one time step. Every tick, the following phases run in order:

1. **Growth phase** — Grass regrows based on sunlight
2. **Feeding phase** — Each animal species attempts to eat (top predators first, then down)
3. **Starvation phase** — Animals that didn't eat enough lose health / die
4. **Reproduction phase** — Well-fed populations produce offspring
5. **Aging/death phase** — Natural death from old age (random chance)

### Grass mechanics

- Grass has a carrying capacity (max biomass the environment supports)
- Each tick: `grass += growth_rate * grass * (1 - grass / carrying_capacity)` (logistic growth)
- Sunlight is implicit — it controls `growth_rate` (constant for now, could vary later)
- Herbivores consume grass, reducing biomass directly

### Animal mechanics

Each species has these parameters:

| Parameter             | Description                                            |
|-----------------------|--------------------------------------------------------|
| `population`          | Current count                                          |
| `food_needed`         | Grass/prey units needed per individual per tick        |
| `hunt_success_rate`   | Probability of catching prey per attempt               |
| `reproduction_rate`   | Fraction of population that reproduces when well-fed   |
| `starvation_rate`     | Fraction that dies when food is insufficient           |
| `natural_death_rate`  | Base mortality per tick (aging, disease)                |
| `max_population`      | Soft carrying capacity (crowding increases death rate)  |

### Feeding order (highest trophic level first)

1. Eagles eat rabbits and snakes (split preference: 60% rabbit, 40% snake)
2. Wolves eat rabbits and deer (split preference: 40% rabbit, 60% deer)
3. Snakes eat rabbits
4. Rabbits eat grass
5. Deer eat grass

Feeding top-down prevents double-counting prey.

### Stability tuning — target equilibrium populations

| Species | Target Equilibrium | Rationale                                    |
|---------|--------------------|----------------------------------------------|
| Grass   | ~800 units         | Large base to support herbivores             |
| Rabbit  | ~150               | Abundant prey species, fast reproduction     |
| Deer    | ~80                | Larger, slower reproduction                  |
| Snake   | ~40                | Mid-predator, moderate population            |
| Wolf    | ~25                | Apex predator, low population                |
| Eagle   | ~20                | Apex predator, lowest population             |

### Parameter estimates (to be tuned via tests)

| Species | food_needed | hunt_success | repro_rate | starve_rate | death_rate | max_pop |
|---------|-------------|-------------|------------|-------------|------------|---------|
| Grass   | n/a         | n/a         | 0.10       | n/a         | n/a        | 1000    |
| Rabbit  | 5 grass     | 0.90        | 0.25       | 0.40        | 0.05       | 300     |
| Deer    | 10 grass    | 0.90        | 0.12       | 0.30        | 0.03       | 150     |
| Snake   | 2 rabbits   | 0.50        | 0.10       | 0.35        | 0.04       | 80      |
| Wolf    | 3 prey      | 0.45        | 0.08       | 0.30        | 0.03       | 50      |
| Eagle   | 2 prey      | 0.55        | 0.08       | 0.30        | 0.03       | 40      |

---

## Architecture

```
life-sim-game/
├── simulation/
│   ├── __init__.py
│   ├── engine.py          # Main simulation loop (Ecosystem class)
│   ├── species.py         # Species config and population state
│   └── food_web.py        # Feeding relationships and logic
├── app.py                 # Flask app — API endpoints
├── tests/
│   ├── __init__.py
│   ├── test_engine.py     # Simulation tick tests
│   ├── test_species.py    # Species behavior tests
│   └── test_food_web.py   # Feeding logic tests
├── requirements.txt       # flask, pytest
├── CLAUDE.md
├── DECISIONS.md
├── PLAN.md
└── README.md
```

### Key classes

- **`Species`** — Holds config (rates) and mutable state (population) for one species
- **`FoodWeb`** — Defines predator-prey edges and handles feeding/hunting logic
- **`Ecosystem`** — Owns all species + food web, runs tick phases, tracks history

### Flask API (minimal for now)

| Endpoint                | Method | Description                          |
|-------------------------|--------|--------------------------------------|
| `/api/simulation`       | POST   | Create a new simulation              |
| `/api/simulation/tick`  | POST   | Advance one tick                     |
| `/api/simulation/state` | GET    | Get current populations + tick count |
| `/api/simulation/history` | GET  | Get population history over time     |
| `/api/simulation/reset` | POST   | Reset to initial conditions          |

---

## Build order

1. **`simulation/species.py`** — Species dataclass with config and state
2. **`simulation/food_web.py`** — FoodWeb class with feeding logic
3. **`simulation/engine.py`** — Ecosystem class with tick loop
4. **`tests/`** — Unit tests for each module
5. **`app.py`** — Flask wrapper
6. **Tuning** — Run multi-tick stability tests and adjust parameters

---

## Stability strategy

The simulation should oscillate but not collapse. Key constraints:

- Predator populations must always be much smaller than prey
- Reproduction rates scale inversely with trophic level
- Starvation acts as a fast negative feedback (populations crash quickly without food)
- Carrying capacity provides a ceiling even without predation
- Logistic grass growth prevents infinite herbivore expansion

A 500-tick stability test should verify: no species goes extinct, no species exceeds 2x its max_population, and populations oscillate around their equilibrium targets.
