import json
from sys import argv
from json import loads

import random
import ssl


def main():
    people = []
    load_people(argv[2], people)
    load_blacklist(argv[3], people)
    random.shuffle(people)

    for i in range(len(people)):
        print(people[i])

    for i in range(len(people)):
        while people[i].get("gifts_to") is None:
            for j in range(len(people)):
                if i != j and people[j].get("email") not in people[i].get("refuses"):
                    people[i]["gifts_to"] = people[j].get("email")
                    append_refused_email_to_person_in_people(people, j, people[i].get("email"))
                    break

    for i in range(len(people)):
        print(people[i])

    creds = get_email_context(argv[1])


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


def get_person_index_by_email(people: [],
                              email: str) -> int:
    for i in range(len(people)):
        if people[i].get("email") == email:
            return i
    return -1


def append_refused_email_to_person_in_people(people: [],
                                             index: int,
                                             email: str) -> None:
    people[index]["refuses"].append(email)


def load_blacklist(filename: str,
                   people_list: []) -> None:
    with open(filename, "r", encoding="utf-8") as f:
        tuples = f.read().split("\n")
        for i in range(len(tuples)):
            emails = tuples[i].split(";")
            p1_index = get_person_index_by_email(people_list, emails[0])
            append_refused_email_to_person_in_people(people_list, p1_index, emails[1]) if p1_index >= 0 else None
            p2_index = get_person_index_by_email(people_list, emails[1])
            append_refused_email_to_person_in_people(people_list, p2_index, emails[0]) if p2_index >= 0 else None
        f.close()


def get_email_context(filename: str) -> dict:
    with open(argv[1], "r", encoding="utf-8") as f:
        creds = loads(f.read())
        f.close()
    return {
        "email": creds["email"],
        "password": creds["password"],
        "server": creds["server"],
        "context": ssl.create_default_context()
    }


if __name__ == "__main__":
    main()
