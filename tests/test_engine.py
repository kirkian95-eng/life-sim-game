import pytest
from simulation.engine import Ecosystem
from simulation.species import Species, SpeciesConfig, create_default_species
from simulation.food_web import FoodWeb


class TestEcosystemInit:
    def test_starts_at_tick_zero(self):
        eco = Ecosystem()
        assert eco.tick_count == 0

    def test_has_all_species(self):
        eco = Ecosystem()
        assert set(eco.species.keys()) == {"grass", "rabbit", "deer", "snake", "wolf", "eagle"}

    def test_history_starts_with_one_snapshot(self):
        eco = Ecosystem()
        assert len(eco.history) == 1

    def test_get_state_returns_tick_and_populations(self):
        eco = Ecosystem()
        state = eco.get_state()
        assert state["tick"] == 0
        assert "populations" in state
        assert "grass" in state["populations"]


class TestSingleTick:
    def test_tick_increments_counter(self):
        eco = Ecosystem()
        eco.tick()
        assert eco.tick_count == 1

    def test_tick_adds_to_history(self):
        eco = Ecosystem()
        eco.tick()
        assert len(eco.history) == 2

    def test_tick_returns_state(self):
        eco = Ecosystem()
        state = eco.tick()
        assert state["tick"] == 1
        assert "populations" in state

    def test_populations_change_after_tick(self):
        eco = Ecosystem()
        before = eco._snapshot()
        eco.tick()
        after = eco._snapshot()
        # At least some populations should change
        changed = any(before[k] != after[k] for k in before)
        assert changed


class TestGrassGrowth:
    def test_grass_grows_when_below_capacity(self):
        eco = Ecosystem()
        # Remove all herbivores so grass only grows
        eco.species["rabbit"].population = 0.0
        eco.species["deer"].population = 0.0
        initial = eco.species["grass"].population
        eco._phase_growth()
        assert eco.species["grass"].population > initial

    def test_grass_growth_slows_near_capacity(self):
        eco = Ecosystem()
        eco.species["rabbit"].population = 0.0
        eco.species["deer"].population = 0.0
        cap = eco.species["grass"].config.max_population

        # Growth from low population (20% of capacity)
        low_pop = cap * 0.2
        eco.species["grass"].population = low_pop
        eco._phase_growth()
        growth_low = eco.species["grass"].population - low_pop

        # Growth from high population (90% of capacity)
        high_pop = cap * 0.9
        eco.species["grass"].population = high_pop
        eco._phase_growth()
        growth_high = eco.species["grass"].population - high_pop

        assert growth_low > growth_high


class TestFeeding:
    def test_feeding_reduces_prey_population(self):
        eco = Ecosystem()
        initial_rabbit = eco.species["rabbit"].population
        eco._phase_feeding()
        assert eco.species["rabbit"].population < initial_rabbit

    def test_feeding_reduces_grass(self):
        eco = Ecosystem()
        initial_grass = eco.species["grass"].population
        eco._phase_feeding()
        assert eco.species["grass"].population < initial_grass

    def test_fed_ratio_is_between_zero_and_one(self):
        eco = Ecosystem()
        fed = eco._phase_feeding()
        for name, ratio in fed.items():
            assert 0.0 <= ratio <= 1.0, f"{name} fed ratio out of range: {ratio}"

    def test_extinct_predator_gets_zero_fed_ratio(self):
        eco = Ecosystem()
        eco.species["eagle"].population = 0.0
        fed = eco._phase_feeding()
        assert fed["eagle"] == 0.0


class TestStarvation:
    def test_hungry_animals_die(self):
        eco = Ecosystem()
        initial = eco.species["wolf"].population
        # Simulate no food
        fed = {"wolf": 0.0, "eagle": 1.0, "snake": 1.0, "rabbit": 1.0, "deer": 1.0}
        eco._phase_starvation(fed)
        assert eco.species["wolf"].population < initial

    def test_well_fed_animals_dont_starve(self):
        eco = Ecosystem()
        initial = eco.species["wolf"].population
        fed = {"wolf": 1.0, "eagle": 1.0, "snake": 1.0, "rabbit": 1.0, "deer": 1.0}
        eco._phase_starvation(fed)
        assert eco.species["wolf"].population == initial


class TestReproduction:
    def test_well_fed_animals_reproduce(self):
        eco = Ecosystem()
        eco.species["rabbit"].population = 100.0  # Below max to allow births
        initial = eco.species["rabbit"].population
        fed = {"rabbit": 1.0, "deer": 1.0, "snake": 1.0, "wolf": 1.0, "eagle": 1.0}
        eco._phase_reproduction(fed)
        assert eco.species["rabbit"].population > initial

    def test_starving_animals_dont_reproduce(self):
        eco = Ecosystem()
        initial = eco.species["wolf"].population
        fed = {"wolf": 0.0, "eagle": 0.0, "snake": 0.0, "rabbit": 0.0, "deer": 0.0}
        eco._phase_reproduction(fed)
        assert eco.species["wolf"].population == initial

    def test_no_reproduction_at_max_capacity(self):
        eco = Ecosystem()
        eco.species["rabbit"].population = eco.species["rabbit"].config.max_population
        initial = eco.species["rabbit"].population
        fed = {"rabbit": 1.0, "deer": 1.0, "snake": 1.0, "wolf": 1.0, "eagle": 1.0}
        eco._phase_reproduction(fed)
        assert eco.species["rabbit"].population == initial


class TestReset:
    def test_reset_restores_initial_populations(self):
        eco = Ecosystem()
        for _ in range(10):
            eco.tick()
        eco.reset()
        assert eco.tick_count == 0
        defaults = create_default_species()
        for name, sp in eco.species.items():
            assert sp.population == defaults[name].population

    def test_reset_clears_history(self):
        eco = Ecosystem()
        for _ in range(10):
            eco.tick()
        eco.reset()
        assert len(eco.history) == 1


class TestStability:
    """Run the simulation for many ticks and verify no species goes extinct."""

    def test_no_extinction_in_200_ticks(self):
        eco = Ecosystem()
        for _ in range(200):
            eco.tick()
        for name, sp in eco.species.items():
            assert sp.population > 0, f"{name} went extinct after 200 ticks"

    def test_populations_stay_bounded_in_200_ticks(self):
        eco = Ecosystem()
        for _ in range(200):
            eco.tick()
        for name, sp in eco.species.items():
            cap = sp.config.max_population
            assert sp.population < cap * 3, (
                f"{name} population {sp.population:.0f} exceeded 3x its cap {cap}"
            )

    def test_grass_never_fully_depleted(self):
        eco = Ecosystem()
        for i in range(200):
            eco.tick()
            assert eco.species["grass"].population > 0, f"Grass depleted at tick {i+1}"
