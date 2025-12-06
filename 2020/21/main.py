import re

from utils import read_input


def main():
    input_file = read_input("2020/21/input.txt")
    input_tuples = [
        re.match(r"^((?:\w+ )+)\(contains (.*?)\)$", line).groups()
        for line in input_file
    ]
    # Preprocess input file -- obtain ingredient and allergen lists
    ingredients_list = [set(el.strip().split(" ")) for el, _ in input_tuples]
    allergen_list = [set(el.strip().split(", ")) for _, el in input_tuples]

    # Obtain set of all allergens and ingredients
    set_allergens = set.union(*[allergen for allergen in allergen_list])
    set_ingredients = set.union(*[ingredient for ingredient in ingredients_list])

    # Create dictionary of ids - allergen list and allergen - ids
    id_allergen_dict = {k: v for k, v in zip(range(len(allergen_list)), allergen_list)}
    allergen_id_dict = {}
    for allergen in set_allergens:
        allergen_id_dict[allergen] = {
            k for k, v in id_allergen_dict.items() if allergen in v
        }

    # Create dictionary of allergen -- ingredients
    allergen_ingredient_dict = {
        key: set.intersection(*[ingredients_list[k] for k in value])
        for key, value in allergen_id_dict.items()
    }

    # The union of the ingredients in the allergen_ingredient dictionary is the unsafe
    #  set.
    # Safe ingredients are the difference between the total set and the unsafe set
    safe_ingredients = set_ingredients - set.union(
        *[v for k, v in allergen_ingredient_dict.items()]
    )
    num_result = sum(
        [len(set.intersection(safe_ingredients, recipe)) for recipe in ingredients_list]
    )
    print(f"Result of part 1: {num_result}")
    # Find the right ingredient - allergen relationship
    # Recursively walk through the allergen_ingredient dictionary.
    #  If the set difference between the element and the confirmed ingredient-allergen
    #  pairs is 1, update the ingredient_allergen pairs
    # Else, remove the ingredient-allergen pair from the allergen_ingredient dictionary
    ingredient_allergen_dict = {}
    while len(ingredient_allergen_dict) < len(set_allergens):
        for allergen in allergen_ingredient_dict:
            set_difference = allergen_ingredient_dict[allergen].difference(
                ingredient_allergen_dict.values()
            )

            if len(set_difference) == 1:
                ingredient_allergen_dict[allergen] = list(set_difference)[0]

            allergen_ingredient_dict[allergen] = set_difference

    canonical_list = ",".join(
        [ingredient_allergen_dict[key] for key in sorted(ingredient_allergen_dict)]
    )

    print(f"Result of part 2: {canonical_list}")


if __name__ == "__main__":
    main()
