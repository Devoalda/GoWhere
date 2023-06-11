#! /usr/bin/env python3
from pprint import pprint

import argparse


class Shopping_Mall:
    def __init__(self) -> None:
        """
        Initialize the link, dataset, div-col classes, headers and call the get_malls function
        """

        self.link = "https://en.wikipedia.org/wiki/List_of_shopping_malls_in_Singapore"
        self.dataset = {}
        self.headers = ['Central', 'East', 'North', 'North East', 'North West', 'West', 'South']

    def get_malls(self) -> None:
        """
        Get all the malls from the div-col classes and store them in a dictionary as a Key-Value pair
        [Key: Region, Value: List of Malls]
        :return: None
        """
        # To ensure script can be run without BeautifulSoup
        from bs4 import BeautifulSoup
        import requests as requests
        page = requests.get(self.link)
        soup = BeautifulSoup(page.content, 'html.parser')

        # Get all the div-col classes
        div_col = soup.find_all('div', class_='div-col')

        for i, data in enumerate(div_col):
            self.dataset[self.headers[i]] = []
            if self.headers[i] == 'South':
                pass
            else:
                li = data.find_all('li')
                for item in li:
                    self.dataset[self.headers[i]] += [item.text.split('[')[0]]

        # Populate South Region manually cuz the data is not in the div-col class
        self.dataset['South'] = ['VivoCity', 'HarbourFront Centre', 'Alexandra Retail Centre']

    def __repr__(self) -> str | Exception:
        """
        :return: Dataset if it is not empty, else return "No data found"
        """
        if self.dataset:
            # Format the dataset to be printed
            data = ''
            for key, value in self.dataset.items():
                data += f'{key}: {value}\n'
            return data
        else:
            raise Exception("No data found")

    def export(self, file_type: str = 'json') -> None:
        """
        Export the dataset to a file
        :param file_type: Type of file to export to
        :return: None
        """
        if file_type == 'json':
            import json
            with open('dataset.json', 'w') as file:
                json.dump(self.dataset, file, indent=4)
        elif file_type == 'csv':
            import csv
            with open('dataset.csv', 'w') as file:
                writer = csv.writer(file)
                for key, value in self.dataset.items():
                    writer.writerow([key, value])
        elif file_type == 'txt':
            with open('dataset.txt', 'w') as file:
                for key, value in self.dataset.items():
                    file.write(f'{key}: {value}\n')
        else:
            raise Exception("Invalid file type")

    def import_file(self, file_name: str) -> None:
        """
        Import the dataset from a file
        :param file_name: Name of the file to import from
        :return: None
        """
        if file_name.endswith('.json'):
            import json
            with open(file_name, 'r') as file:
                self.dataset = json.load(file)
        elif file_name.endswith('.csv'):
            import csv
            with open(file_name, 'r') as file:
                reader = csv.reader(file)
                for row in reader:
                    self.dataset[row[0]] = row[1]
        elif file_name.endswith('.txt'):
            with open(file_name, 'r') as file:
                for line in file:
                    key, value = line.split(':')
                    self.dataset[key] = value
        else:
            print("Invalid file type, getting data from the web...")
            self.get_malls()

    def get_random_mall(self, num_malls: int = 3, region: str = None) -> dict[str, list[str]]:
        """
        Get a random mall from the dataset
        :return: A random mall
        """
        import random
        random_mall = []

        if region is None:
            random_number_region = random.randint(0, len(self.headers) - 1)
            region = self.headers[random_number_region]

            # Check if dataset has enough malls, try again if not, stop after 5 tries
            tries = 0
            while len(self.dataset[region]) < num_malls and tries < 5:
                random_number_region = random.randint(0, len(self.headers) - 1)
                region = self.headers[random_number_region]
                tries += 1

            if tries == 5:
                raise Exception("Not enough malls in the dataset")

        # Get 3 random unique malls from the random region
        while len(random_mall) < num_malls:
            random_number_mall = random.randint(0, len(self.dataset[region]) - 1)
            if self.dataset[region][random_number_mall] not in random_mall:
                random_mall.append(self.dataset[region][random_number_mall])

        return {region: random_mall}

    def human_readable(self, dataset: dict[str, list[str]] = None) -> str:
        """
        Format the dataset to be human readable
        :return: Formatted dataset
        """
        data = ''
        if dataset is None:
            for key, value in self.dataset.items():
                data += f'{key}' + '\n'
                for mall in value:
                    data += f'\t{mall}' + '\n'
        else:
            for key, value in dataset.items():
                data += f'{key}' + '\n'
                for mall in value:
                    data += f'\t{mall}' + '\n'
        return data


def test_Shopping_Mall() -> None:
    """
    Test the Shopping_Mall class
    """

    sm = Shopping_Mall()
    assert sm.dataset == {}, "Dataset should be empty"

    sm.import_file('dataset.json')
    assert sm.dataset != {}, "Dataset should not be empty"

    sm2 = Shopping_Mall()
    assert sm2.dataset == {}, "Dataset should be empty"
    sm2.get_malls()
    assert sm2.dataset != {}, "Dataset should not be empty"

    print(f"All tests passed!")


def parse_args() -> None:
    """
    Argument Parser with argparse package
    -p, --pretty: Pretty print the dataset
    -H, --human: Human readable printing
    -a, --all: Show all the malls in the dataset
    -r, --random: RANDOM = Number of malls to get
    -t, --test: Run the test function

    """
    parser = argparse.ArgumentParser(description="Get a random mall in Singapore, this uses data from Wikipedia",
                                     prog="SG_Shopping_Malls.py")
    parser.add_argument('-a', '--all', action='store_true', help='Show all the malls in Singapore')
    # Pretty print the dataset, requires another argument to be passed, either -a or -r
    parser.add_argument('-p', '--pretty', action='store_true', help='Pretty print the dataset: SG_Shopping_Malls -p -a')
    # Human-readable Printing
    parser.add_argument('-H', '--human', action='store_true', help='Human readable printing: SG_Shopping_Malls -H -r 3')
    parser.add_argument('-r', '--random', type=int, action='store',
                        help='RANDOM = Number of malls to get: SG_Shopping_Malls -r 3')
    parser.add_argument('-t', '--test', action='store_true', help='Test the Shopping_Mall class')

    args = parser.parse_args()

    sm = Shopping_Mall()
    sm.import_file('dataset.json')

    def print_pretty(sm, args):
        if args.all:
            pprint(sm)
        elif args.random:
            pprint(sm.get_random_mall(args.random))
        else:
            parser.print_help()

    def print_human_readable(sm, args):
        if args.all:
            print(sm.human_readable())
        elif args.random:
            print(sm.human_readable(sm.get_random_mall(args.random)))
        else:
            parser.print_help()

    def all(sm, args):
        print(sm)

    def random(sm, args):
        print(sm.get_random_mall(args.random))

    def test(sm, args):
        test_Shopping_Mall()

    action_map = {'pretty': print_pretty, 'human': print_human_readable, 'all': all, 'random': random, 'test': test}

    for action, func in action_map.items():
        if getattr(args, action):
            func(sm, args)
            break
    else:
        parser.print_help()


if __name__ == '__main__':
    parse_args()
