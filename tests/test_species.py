from simulation.species import Species, SpeciesConfig, create_default_species


def _make_species(population=100.0, max_pop=200.0, **overrides):
    defaults = dict(
        name="test_animal",
        trophic_level=1,
        food_needed=5.0,
        hunt_success_rate=0.9,
        reproduction_rate=0.2,
        starvation_rate=0.3,
        natural_death_rate=0.05,
        max_population=max_pop,
    )
    defaults.update(overrides)
    return Species(config=SpeciesConfig(**defaults), population=population)


class TestSpecies:
    def test_is_alive_when_population_above_one(self):
        sp = _make_species(population=5.0)
        assert sp.is_alive

    def test_is_not_alive_when_population_zero(self):
        sp = _make_species(population=0.0)
        assert not sp.is_alive

    def test_is_not_alive_below_one(self):
        sp = _make_species(population=0.5)
        assert not sp.is_alive

    def test_apply_deaths_reduces_population(self):
        sp = _make_species(population=100.0)
        actual = sp.apply_deaths(30.0)
        assert actual == 30.0
        assert sp.population == 70.0

    def test_apply_deaths_cannot_go_negative(self):
        sp = _make_species(population=10.0)
        actual = sp.apply_deaths(50.0)
        assert actual == 10.0
        assert sp.population == 0.0

    def test_apply_births_increases_population(self):
        sp = _make_species(population=100.0)
        sp.apply_births(20.0)
        assert sp.population == 120.0

    def test_crowding_factor_at_zero(self):
        sp = _make_species(population=0.0, max_pop=200.0)
        assert sp.crowding_factor() == 0.0

    def test_crowding_factor_at_half(self):
        sp = _make_species(population=100.0, max_pop=200.0)
        assert sp.crowding_factor() == 0.5

    def test_crowding_factor_capped_at_one(self):
        sp = _make_species(population=300.0, max_pop=200.0)
        assert sp.crowding_factor() == 1.0

    def test_name_property(self):
        sp = _make_species(name="rabbit")
        assert sp.name == "rabbit"


class TestCreateDefaultSpecies:
    def test_returns_all_six_species(self):
        species = create_default_species()
        assert set(species.keys()) == {"grass", "rabbit", "deer", "snake", "wolf", "eagle"}

    def test_grass_is_producer(self):
        species = create_default_species()
        assert species["grass"].config.trophic_level == 0

    def test_initial_populations_are_positive(self):
        species = create_default_species()
        for sp in species.values():
            assert sp.population > 0

    def test_predators_have_lower_populations_than_prey(self):
        species = create_default_species()
        assert species["wolf"].population < species["rabbit"].population
        assert species["eagle"].population < species["rabbit"].population
        assert species["snake"].population < species["rabbit"].population
