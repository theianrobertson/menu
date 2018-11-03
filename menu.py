import itertools
from dataclasses import dataclass
from functools import lru_cache
import sys
import random
import json
import yaml

@lru_cache()
def get_yaml(filename):
    """Just read a yaml file in."""
    with open(filename + '.yml') as file_open:
        return yaml.load(file_open)

@dataclass
class Menu:
    items: list = None
    ian_count: int = 2
    kate_count: int = 4

    def __post_init__(self):
        self.items = self.items or []
        self.top_up_menu()
        self.get_feedback_on_menu()
        while self.unconfirmed_items:
            self.__post_init__()

    def top_up_menu(self):
        self.items = [item for item in self.items if item['confirmed']]
        self.items.extend(self.pick_options('Ian', self.ian_count - len(self.list_items('Ian'))))
        self.items.extend(self.pick_options('Kate', self.kate_count - len(self.list_items('Kate'))))

    def get_feedback_on_menu(self):
        if len(self.unconfirmed_items) > 0:
            print('Here is your menu:')
            for i, item in enumerate(self.items):
                print("#{}: {} ({})".format(i, item['item'], item['person']))
            print('\n')
            resp = input((
                'Which do you not want to make? enter numbers separated by commas like 0,2,3 '
                'or just hit return to accept all: '))
            for i, item in enumerate(self.items):
                if str(i) not in resp.split(','):
                    item['confirmed'] = True

    @property
    def item_names(self):
        return [item['item'] for item in self.items]

    @property
    def unconfirmed_items(self):
        """Just get all items that haven't been confirmed"""
        return [item for item in self.items if item['confirmed'] is False]

    def pick_options(self, person, count, weight=4):
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
            if option['item'] not in self.item_names:
                item_person = option.get('person')
                if option.get('person') == person:
                    weights.extend([option] * weight)
                elif not option.get('person'):
                    weights.extend([option])
        picks = random.sample(weights, k=count)
        return [{'confirmed': False, 'person': person, **pick} for pick in picks]

    @property
    def groceries(self):
        return itertools.chain.from_iterable([item['groceries'] for item in self.items])

    def list_items(self, person):
        return [item for item in self.items if item['person'] == person]

    def __repr__(self):
        return (
            "Ian:\n"
            "{ian_items}\n\n"
            "Kate:\n"
            "{kate_items}\n\n"
            "Groceries:\n"
            "{groceries}"
        ).format(
            ian_items=json.dumps(self.list_items('Ian'), indent=2, sort_keys=True),
            kate_items=json.dumps(self.list_items('Kate'), indent=2, sort_keys=True),
            groceries='\n'.join(self.groceries)
        )

if __name__ == '__main__':
    args = sys.argv
    if len(args) > 1:
        menu = Menu(ian=int(args[1]), kate=int(args[2]))
    else:
        menu = Menu()
    print(menu)
