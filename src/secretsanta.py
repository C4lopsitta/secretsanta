import math
from sys import argv
from json import loads
from random import shuffle

import ssl


def main():
    with open(argv[1], "r", encoding="utf-8") as f:
        creds = loads(f.read())
        f.close()

    context = ssl.create_default_context()

    people = []
    load_people(argv[2], people)

    with open(argv[3], "r", encoding="utf-8") as f:
        blacklist_tuples = []
        tuples = f.read().split("\n")
        for i in range(len(tuples)):
            blacklist_tuples.append(tuples[i].split(";"))
        f.close()

    # The actual matching happens by making a circular list of people that reference one another

    return


def load_people(filename: str,
                people_list: []) -> None:
    with open(filename, "r", encoding="utf-8") as f:
        tuples = f.read().split("\n")
        for i in range(len(tuples)):
            person = tuples[i].split(";")
            people_list.append({
                "name": person[1],
                "email": person[0],
                "refuses": None
            })
        f.close()


def swap(elements: [],
         index1: int,
         index2: int) -> None:
    temp = elements[index1]
    elements[index1] = elements[index2]
    elements[index2] = temp


if __name__ == "__main__":
    main()
