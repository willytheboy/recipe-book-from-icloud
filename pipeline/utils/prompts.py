TRIAGE_PROMPT = """Classify this photo. Return strict JSON:
{"is_food": bool, "coarse_category": str|null}
coarse_category in [mezze, main, dessert, drink, breakfast, street, plated_restaurant, home_cooked, menu_card, null]."""

DEEP_TAG_PROMPT = """Analyze this food photo. Return strict JSON:
{"dish": str, "cuisine": str, "category": str,
 "ingredients": [str], "cooking_method": str|null,
 "plating_context": "home"|"restaurant"|"unknown",
 "confidence": 0..1}"""

RECIPE_PROMPT = """Write one entry of a personal recipe book.
Cluster: {label}. Cuisine: {cuisine}. Category: {category}.
Aggregated ingredients across {n} photos: {ingredients}.
Output markdown: 2-sentence headnote, ingredients (metric), numbered steps, chef notes."""
