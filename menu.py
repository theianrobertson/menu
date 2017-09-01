import sys
import random
import json
import yaml


def get_yaml(filename):
    """Just read a yaml file in."""
    with open(filename + '.yml') as file_open:
        return yaml.load(file_open)


def pick_options(person, count, weight=4):
    """Pick options for a person, weighting "their" menu items higher.
    
    Parameters
    ----------
    person : str
        Person's name
    count : int
        How many options to pick
    weight : int, optional
        How much to over-weight "that person's" items.
    """
    options = get_yaml('options')
    weights = []
    for option in options:
        if option.get('person') == person:
            weights.extend([option] * weight)
        elif option.get('person') is None:
            weights.extend([option])
    return random.sample(weights, k=count)


def build_menu(ian=2, kate=4):
    """Build a random weekly menu of dinners.

    Parameters
    ----------
    ian : int, optional
        How many dinners Ian will be cooking
    kate : int, optional
        How many dinners Kate will be cooking
    """
    
    to_return = {}
    if ian > 0:
        to_return['Ian'] = pick_options('Ian', ian)
    if kate > 0:
        to_return['Kate'] = pick_options('Kate', kate)
    return to_return


if __name__ == '__main__':
    args = sys.argv
    if len(args) > 1:
        menu = build_menu(ian=args[1], kate = args[2])
    else:
        menu = build_menu()
    print(json.dumps(menu, indent=2, sort_keys=True))