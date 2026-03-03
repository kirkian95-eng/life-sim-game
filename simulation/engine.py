from simulation.species import Species, create_default_species
from simulation.food_web import FoodWeb


class Ecosystem:
    """Runs the tick-based ecology simulation."""

    def __init__(
        self,
        species: dict[str, Species] | None = None,
        food_web: FoodWeb | None = None,
    ):
        self.species = species or create_default_species()
        self.food_web = food_web or FoodWeb()
        self.tick_count: int = 0
        self.history: list[dict[str, float]] = [self._snapshot()]

    def _snapshot(self) -> dict[str, float]:
        return {name: sp.population for name, sp in self.species.items()}

    def get_state(self) -> dict:
        return {
            "tick": self.tick_count,
            "populations": self._snapshot(),
        }

    def tick(self) -> dict:
        """Advance the simulation by one step."""
        self._phase_growth()
        fed_status = self._phase_feeding()
        self._phase_starvation(fed_status)
        self._phase_reproduction(fed_status)
        self._phase_natural_death()
        self._clamp_populations()

        self.tick_count += 1
        self.history.append(self._snapshot())
        return self.get_state()

    def _phase_growth(self):
        """Logistic growth for producers (grass)."""
        for sp in self.species.values():
            if sp.config.trophic_level != 0:
                continue
            cap = sp.config.max_population
            rate = sp.config.reproduction_rate
            # Logistic growth: dP = r * P * (1 - P/K)
            growth = rate * sp.population * (1.0 - sp.population / cap)
            sp.population += max(0.0, growth)

    def _phase_feeding(self) -> dict[str, float]:
        """Each predator eats prey top-down. Returns fed ratio per species (0-1)."""
        fed_ratio: dict[str, float] = {}

        for predator_name in self.food_web.feeding_order():
            predator = self.species.get(predator_name)
            if predator is None or not predator.is_alive:
                fed_ratio[predator_name] = 0.0
                continue

            total_food_needed = predator.population * predator.config.food_needed
            total_food_obtained = 0.0

            for edge in self.food_web.get_prey(predator_name):
                prey = self.species.get(edge.prey)
                if prey is None or not prey.is_alive:
                    continue

                # How much of the diet this prey fulfills
                food_wanted = total_food_needed * edge.preference

                # Holling Type II functional response:
                # Predation efficiency drops when prey is scarce, creating a
                # natural refuge at low populations that prevents extinction
                half_sat = prey.config.max_population * 0.3
                density_factor = prey.population / (prey.population + half_sat)
                max_catchable = prey.population * predator.config.hunt_success_rate * density_factor

                food_obtained = min(food_wanted, max_catchable)

                # For animal prey, each unit of food = 1 individual killed
                # For grass, food units are biomass
                prey.apply_deaths(food_obtained)
                total_food_obtained += food_obtained

            if total_food_needed > 0:
                fed_ratio[predator_name] = min(1.0, total_food_obtained / total_food_needed)
            else:
                fed_ratio[predator_name] = 1.0

        return fed_ratio

    def _phase_starvation(self, fed_ratio: dict[str, float]):
        """Hungry animals die."""
        for name, sp in self.species.items():
            if sp.config.trophic_level == 0:
                continue
            ratio = fed_ratio.get(name, 0.0)
            if ratio >= 1.0:
                continue
            # The hungrier they are, the more die
            hunger = 1.0 - ratio
            deaths = sp.population * sp.config.starvation_rate * hunger
            sp.apply_deaths(deaths)

    def _phase_reproduction(self, fed_ratio: dict[str, float]):
        """Well-fed animals reproduce. Producers handled in growth phase."""
        for name, sp in self.species.items():
            if sp.config.trophic_level == 0:
                continue
            ratio = fed_ratio.get(name, 0.0)
            # Only reproduce if fed enough; births scale with how well-fed
            crowding = sp.crowding_factor()
            births = sp.population * sp.config.reproduction_rate * ratio * (1.0 - crowding)
            if births > 0:
                sp.apply_births(births)

    def _phase_natural_death(self):
        """Background mortality from aging, disease, etc."""
        for sp in self.species.values():
            if sp.config.trophic_level == 0:
                continue
            deaths = sp.population * sp.config.natural_death_rate
            # Crowding increases death rate
            crowding_deaths = sp.population * sp.config.natural_death_rate * sp.crowding_factor()
            sp.apply_deaths(deaths + crowding_deaths)

    def _clamp_populations(self):
        """Floor populations at 0, and kill off anything below 1 individual."""
        for sp in self.species.values():
            if sp.population < 1.0:
                sp.population = 0.0

    def reset(self):
        """Reset to initial conditions."""
        self.species = create_default_species()
        self.tick_count = 0
        self.history = [self._snapshot()]
