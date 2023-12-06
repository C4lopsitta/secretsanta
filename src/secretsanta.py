from sys import argv
from json import loads

import random
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
            # TODO: Implement adder to refuses in people[{}]
        f.close()

    random.shuffle(people)

    for i in range(len(people)):
        while people[i].get("gifts_to") is None:
            for j in range(len(people)):
                if i != j and people[j].get("email") not in people[i].get("refuses"):
                    people[i]["gifts_to"] = people[j].get("email")
                    people[j]["refuses"].append(people[i].get("email"))
                    break

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
                "refuses": [],
                "gifts_to": None,
            })
            people_list[i]["refuses"].append(person[0])
        f.close()


def swap(elements: [],
         index1: int,
         index2: int) -> None:
    temp = elements[index1]
    elements[index1] = elements[index2]
    elements[index2] = temp


if __name__ == "__main__":
    main()
