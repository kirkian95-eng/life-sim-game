from simulation.food_web import FoodWeb, FeedingEdge


class TestFoodWeb:
    def setup_method(self):
        self.web = FoodWeb()

    def test_eagle_eats_rabbit_and_snake(self):
        prey = self.web.get_prey("eagle")
        prey_names = {e.prey for e in prey}
        assert prey_names == {"rabbit", "snake"}

    def test_wolf_eats_rabbit_and_deer(self):
        prey = self.web.get_prey("wolf")
        prey_names = {e.prey for e in prey}
        assert prey_names == {"rabbit", "deer"}

    def test_snake_eats_rabbit(self):
        prey = self.web.get_prey("snake")
        assert len(prey) == 1
        assert prey[0].prey == "rabbit"

    def test_rabbit_eats_grass(self):
        prey = self.web.get_prey("rabbit")
        assert len(prey) == 1
        assert prey[0].prey == "grass"

    def test_deer_eats_grass(self):
        prey = self.web.get_prey("deer")
        assert len(prey) == 1
        assert prey[0].prey == "grass"

    def test_grass_has_no_prey(self):
        prey = self.web.get_prey("grass")
        assert prey == []

    def test_rabbit_has_multiple_predators(self):
        predators = self.web.get_predators("rabbit")
        pred_names = {e.predator for e in predators}
        assert pred_names == {"eagle", "wolf", "snake"}

    def test_grass_predators_are_herbivores(self):
        predators = self.web.get_predators("grass")
        pred_names = {e.predator for e in predators}
        assert pred_names == {"rabbit", "deer"}

    def test_eagle_preferences_sum_to_one(self):
        prey = self.web.get_prey("eagle")
        total = sum(e.preference for e in prey)
        assert abs(total - 1.0) < 0.001

    def test_wolf_preferences_sum_to_one(self):
        prey = self.web.get_prey("wolf")
        total = sum(e.preference for e in prey)
        assert abs(total - 1.0) < 0.001

    def test_feeding_order_returns_all_consumers(self):
        order = self.web.feeding_order()
        assert "eagle" in order
        assert "wolf" in order
        assert "snake" in order
        assert "rabbit" in order
        assert "deer" in order

    def test_custom_food_web(self):
        edges = [FeedingEdge(predator="cat", prey="mouse", preference=1.0)]
        web = FoodWeb(edges)
        assert web.get_prey("cat")[0].prey == "mouse"
        assert web.get_predators("mouse")[0].predator == "cat"
