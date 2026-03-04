from simulation.species import Species, SpeciesConfig, create_default_species


def _make_species(population=100, max_pop=200, **overrides):
    defaults = dict(
        name="test_animal",
        trophic_level=1,
        food_needed=5.0,
        hunt_success_rate=0.9,
        reproduction_rate=0.2,
        starvation_rate=0.3,
        natural_death_rate=0.05,
        max_population=max_pop,
        min_viable_population=2,
    )
    defaults.update(overrides)
    return Species(config=SpeciesConfig(**defaults), population=population)


def _make_grass(population=1000.0, max_pop=5000.0):
    return Species(
        config=SpeciesConfig(
            name="grass", trophic_level=0, food_needed=0.0,
            hunt_success_rate=1.0, reproduction_rate=0.6,
            starvation_rate=0.0, natural_death_rate=0.0,
            max_population=max_pop, min_viable_population=0,
        ),
        population=population,
    )


class TestSpecies:
    def test_is_alive_when_population_above_one(self):
        sp = _make_species(population=5)
        assert sp.is_alive

    def test_is_not_alive_when_population_zero(self):
        sp = _make_species(population=0)
        assert not sp.is_alive

    def test_is_not_alive_below_one(self):
        # Animals should always be int, but is_alive still guards against it
        sp = _make_species(population=0, min_viable_population=0)
        assert not sp.is_alive

    def test_apply_deaths_reduces_population(self):
        sp = _make_species(population=100)
        actual = sp.apply_deaths(30.0)
        assert actual == 30
        assert sp.population == 70

    def test_apply_deaths_cannot_go_negative(self):
        sp = _make_species(population=10)
        actual = sp.apply_deaths(50.0)
        assert actual == 10
        assert sp.population == 0

    def test_apply_births_increases_population(self):
        sp = _make_species(population=100)
        sp.apply_births(20.0)
        assert sp.population == 120

    def test_crowding_factor_at_zero(self):
        sp = _make_species(population=0, max_pop=200)
        assert sp.crowding_factor() == 0.0

    def test_crowding_factor_at_half(self):
        sp = _make_species(population=100, max_pop=200)
        assert sp.crowding_factor() == 0.5

    def test_crowding_factor_capped_at_one(self):
        sp = _make_species(population=300, max_pop=200)
        assert sp.crowding_factor() == 1.0

    def test_name_property(self):
        sp = _make_species(name="rabbit")
        assert sp.name == "rabbit"


class TestIntegerPopulations:
    """Animals must have whole-number populations at all times."""

    def test_animal_deaths_are_floored(self):
        sp = _make_species(population=10)
        sp.apply_deaths(2.7)
        assert sp.population == 8  # floor(2.7) = 2 killed
        assert isinstance(sp.population, int)

    def test_animal_births_are_floored(self):
        sp = _make_species(population=10)
        sp.apply_births(3.9)
        assert sp.population == 13  # floor(3.9) = 3 born
        assert isinstance(sp.population, int)

    def test_fractional_death_below_one_kills_zero(self):
        sp = _make_species(population=10)
        sp.apply_deaths(0.7)
        assert sp.population == 10  # floor(0.7) = 0 killed

    def test_fractional_birth_below_one_births_zero(self):
        sp = _make_species(population=10)
        sp.apply_births(0.9)
        assert sp.population == 10  # floor(0.9) = 0 born

    def test_grass_allows_fractional_population(self):
        grass = _make_grass(population=100.0)
        grass.apply_deaths(2.7)
        assert grass.population == 97.3

    def test_grass_allows_fractional_births(self):
        grass = _make_grass(population=100.0)
        grass.apply_births(3.5)
        assert grass.population == 103.5

    def test_population_stays_int_after_multiple_operations(self):
        sp = _make_species(population=50)
        sp.apply_deaths(7.3)   # kills 7
        sp.apply_births(4.8)   # births 4
        sp.apply_deaths(2.1)   # kills 2
        assert sp.population == 45
        assert isinstance(sp.population, int)

    def test_default_animal_populations_are_int(self):
        species = create_default_species()
        for name, sp in species.items():
            if sp.is_animal:
                assert isinstance(sp.population, int), f"{name} population is not int"


class TestMinViablePopulation:
    """Species below minimum viable population go extinct."""

    def test_below_mvp_goes_extinct(self):
        sp = _make_species(population=1, min_viable_population=2)
        sp.check_viable()
        assert sp.population == 0

    def test_at_mvp_survives(self):
        sp = _make_species(population=2, min_viable_population=2)
        sp.check_viable()
        assert sp.population == 2

    def test_above_mvp_survives(self):
        sp = _make_species(population=10, min_viable_population=2)
        sp.check_viable()
        assert sp.population == 10

    def test_zero_mvp_allows_any_positive_population(self):
        grass = _make_grass(population=0.5)
        grass.check_viable()
        assert grass.population == 0.5

    def test_extinct_species_unaffected_by_mvp(self):
        sp = _make_species(population=0, min_viable_population=2)
        sp.check_viable()
        assert sp.population == 0

    def test_all_animals_have_mvp_of_2(self):
        species = create_default_species()
        for name, sp in species.items():
            if sp.is_animal:
                assert sp.config.min_viable_population == 2, f"{name} mvp != 2"


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
