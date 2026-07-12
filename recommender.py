"""Dish ranking logic kept separate from Telegram so it is easy to test."""

from dishes import DISHES, Dish


def recommend_dishes(
    selected_vegetables: set[str],
    meat: str,
    *,
    limit: int = 5,
    offset: int = 0,
) -> list[Dish]:
    """Return dishes ranked by how many selected vegetables they use.

    Protein is always an exact filter. If vegetables were selected, dishes
    sharing at least one are preferred; protein-only classics remain available
    after those matches so the user never sees an empty result.
    """
    candidates = [dish for dish in DISHES if meat in dish.proteins]

    def score(dish: Dish) -> tuple[int, int, int, str]:
        dish_vegetables = set(dish.vegetables)
        overlap = len(selected_vegetables & dish_vegetables)
        unmatched = len(dish_vegetables - selected_vegetables)
        has_match = int(not selected_vegetables or overlap > 0)
        return (has_match, overlap, -unmatched, dish.name_km)

    ranked = sorted(candidates, key=score, reverse=True)
    if not ranked or limit <= 0:
        return []

    # Cycling lets the “more suggestions” button keep working even when a
    # protein has fewer than two full pages of dishes.
    start = offset % len(ranked)
    return (ranked[start:] + ranked[:start])[:limit]


def matching_vegetables(dish: Dish, selected_vegetables: set[str]) -> set[str]:
    return selected_vegetables & set(dish.vegetables)

