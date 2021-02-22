"""
--- Day 21: Allergen Assessment ---

You reach the train's last stop and the closest you can get to your vacation island
 without getting wet. There aren't even any boats here, but nothing can stop you now:
  you build a raft. You just need a few days' worth of food for your journey.

You don't speak the local language, so you can't read any ingredients lists. However,
 sometimes, allergens are listed in a language you do understand. You should be able to
  use this information to determine which ingredient contains which allergen and work
   out which foods are safe to take with you on your trip.

You start by compiling a list of foods (your puzzle input), one food per line. Each
 line includes that food's ingredients list followed by some or all of the allergens
  the food contains.

Each allergen is found in exactly one ingredient. Each ingredient contains zero or one
 allergen. Allergens aren't always marked; when they're listed (as in (contains nuts,
  shellfish) after an ingredients list), the ingredient that contains each listed
   allergen will be somewhere in the corresponding ingredients list. However, even if
    an allergen isn't listed, the ingredient that contains that allergen could still be
     present: maybe they forgot to label it, or maybe it was labeled in a language you
      don't know.

For example, consider the following list of foods:

mxmxvkd kfcds sqjhc nhms (contains dairy, fish)
trh fvjkl sbzzf mxmxvkd (contains dairy)
sqjhc fvjkl (contains soy)
sqjhc mxmxvkd sbzzf (contains fish)
The first food in the list has four ingredients (written in a language you don't
 understand): mxmxvkd, kfcds, sqjhc, and nhms. While the food might contain other
  allergens, a few allergens the food definitely contains are listed afterward: dairy
   and fish.

The first step is to determine which ingredients can't possibly contain any of the
 allergens in any food in your list. In the above example, none of the ingredients
  kfcds, nhms, sbzzf, or trh can contain an allergen. Counting the number of times any
   of these ingredients appear in any ingredients list produces 5: they all appear once
    each except sbzzf, which appears twice.

Determine which ingredients cannot possibly contain any of the allergens in your list.
 How many times do any of those ingredients appear?
"""
from utils import read_input
import re


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

    # Obtain unsafe ingredients -- do intersection of the ingredients for all the
    #  elements in the list of foods that share a certain allergen
    # Safe ingredients are the difference between the total set and the unsafe set
    safe_ingredients = set_ingredients - set.union(
        *[
            set.intersection(*[ingredients_list[k] for k in value])
            for key, value in allergen_id_dict.items()
        ]
    )
    num_result = sum(
        [len(set.intersection(safe_ingredients, recipe)) for recipe in ingredients_list]
    )
    print("Result of part 1: " f"{num_result}")


if __name__ == "__main__":
    main()
