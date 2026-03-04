from dataclasses import dataclass


@dataclass
class FeedingEdge:
    """A predator-prey relationship with a preference weight."""
    predator: str
    prey: str
    preference: float  # 0-1, how much of diet comes from this prey


class FoodWeb:
    """Defines and resolves feeding relationships between species."""

    def __init__(self, edges: list[FeedingEdge] | None = None):
        if edges is None:
            edges = self.default_edges()
        self.edges = edges
        self._prey_map: dict[str, list[FeedingEdge]] = {}
        self._predator_map: dict[str, list[FeedingEdge]] = {}
        for edge in edges:
            self._prey_map.setdefault(edge.predator, []).append(edge)
            self._predator_map.setdefault(edge.prey, []).append(edge)

    def get_prey(self, predator: str) -> list[FeedingEdge]:
        """What does this predator eat?"""
        return self._prey_map.get(predator, [])

    def get_predators(self, prey: str) -> list[FeedingEdge]:
        """What eats this prey?"""
        return self._predator_map.get(prey, [])

    def feeding_order(self) -> list[str]:
        """Return predator names sorted by trophic priority (top predators first)."""
        # Predators with no predators of their own go first, then down
        all_predators = list(self._prey_map.keys())

        def predator_score(name: str) -> int:
            # Count how many things eat this species (more = lower priority)
            return len(self._predator_map.get(name, []))

        return sorted(all_predators, key=predator_score)

    @staticmethod
    def default_edges() -> list[FeedingEdge]:
        return [
            # Eagles eat rabbits (70%) and snakes (30%)
            FeedingEdge(predator="eagle", prey="rabbit", preference=0.70),
            FeedingEdge(predator="eagle", prey="snake", preference=0.30),
            # Wolves eat deer (70%) and rabbits (30%)
            FeedingEdge(predator="wolf", prey="deer", preference=0.70),
            FeedingEdge(predator="wolf", prey="rabbit", preference=0.30),
            # Snakes eat rabbits
            FeedingEdge(predator="snake", prey="rabbit", preference=1.00),
            # Rabbits eat grass
            FeedingEdge(predator="rabbit", prey="grass", preference=1.00),
            # Deer eat grass
            FeedingEdge(predator="deer", prey="grass", preference=1.00),
        ]
