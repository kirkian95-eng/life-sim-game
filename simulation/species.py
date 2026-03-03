from dataclasses import dataclass, field


@dataclass
class SpeciesConfig:
    """Immutable parameters defining a species' behavior."""
    name: str
    trophic_level: int          # 0=producer, 1=primary consumer, 2+=predator
    food_needed: float          # units of food per individual per tick
    hunt_success_rate: float    # probability of catching prey (0-1)
    reproduction_rate: float    # fraction that reproduce when well-fed
    starvation_rate: float      # fraction that die when food is insufficient
    natural_death_rate: float   # base mortality per tick
    max_population: float       # soft carrying capacity


@dataclass
class Species:
    """A species in the ecosystem with config and mutable state."""
    config: SpeciesConfig
    population: float

    @property
    def name(self) -> str:
        return self.config.name

    @property
    def is_alive(self) -> bool:
        return self.population >= 1.0

    def apply_deaths(self, count: float) -> float:
        """Remove individuals from population. Returns actual deaths."""
        actual = min(count, self.population)
        self.population = max(0.0, self.population - actual)
        return actual

    def apply_births(self, count: float) -> float:
        """Add individuals to population. Returns actual births."""
        self.population += count
        return count

    def crowding_factor(self) -> float:
        """Returns 0-1 scale of how crowded the population is."""
        if self.config.max_population <= 0:
            return 0.0
        return min(1.0, self.population / self.config.max_population)


def create_default_species() -> dict[str, Species]:
    """Create the default set of species with tuned parameters."""
    configs = {
        "grass": SpeciesConfig(
            name="grass",
            trophic_level=0,
            food_needed=0.0,
            hunt_success_rate=1.0,
            reproduction_rate=0.60,
            starvation_rate=0.0,
            natural_death_rate=0.0,
            max_population=5000.0,
        ),
        "rabbit": SpeciesConfig(
            name="rabbit",
            trophic_level=1,
            food_needed=2.0,
            hunt_success_rate=0.90,
            reproduction_rate=0.45,
            starvation_rate=0.30,
            natural_death_rate=0.05,
            max_population=400.0,
        ),
        "deer": SpeciesConfig(
            name="deer",
            trophic_level=1,
            food_needed=4.0,
            hunt_success_rate=0.90,
            reproduction_rate=0.18,
            starvation_rate=0.25,
            natural_death_rate=0.03,
            max_population=150.0,
        ),
        "snake": SpeciesConfig(
            name="snake",
            trophic_level=2,
            food_needed=1.0,
            hunt_success_rate=0.30,
            reproduction_rate=0.10,
            starvation_rate=0.35,
            natural_death_rate=0.04,
            max_population=80.0,
        ),
        "wolf": SpeciesConfig(
            name="wolf",
            trophic_level=2,
            food_needed=1.5,
            hunt_success_rate=0.35,
            reproduction_rate=0.10,
            starvation_rate=0.30,
            natural_death_rate=0.03,
            max_population=50.0,
        ),
        "eagle": SpeciesConfig(
            name="eagle",
            trophic_level=2,
            food_needed=1.0,
            hunt_success_rate=0.40,
            reproduction_rate=0.10,
            starvation_rate=0.25,
            natural_death_rate=0.03,
            max_population=40.0,
        ),
    }

    populations = {
        "grass": 3000.0,
        "rabbit": 200.0,
        "deer": 80.0,
        "snake": 30.0,
        "wolf": 20.0,
        "eagle": 15.0,
    }

    return {
        name: Species(config=cfg, population=populations[name])
        for name, cfg in configs.items()
    }
