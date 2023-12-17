from argparse import ArgumentParser, RawTextHelpFormatter
from textwrap import dedent

from jsonschema import validate
import json

from os import path


def parse_args() -> str:
    parser = ArgumentParser(
        description=dedent("""
            Update wage database with new data.

            JSON file requirements: 
            - Array of Dict
            - Dict has fields: {
                "prefecture": string
                "wage": integer
                "date_of_issue": string in ISO format("YYYY-MM-DD")
              }               
        """).strip(),
        formatter_class=RawTextHelpFormatter,
    )

    parser.add_argument(
        "file",
        type=str,
        action="store",
        help=dedent("Path to JSON file.").strip(),
    )

    args = parser.parse_args()
    return args.file


def load(json_path: str):
    schema = json.load(open(path.dirname(__file__) + "/schema.json", "r"))

    try:
        f = open(json_path, "r")
    except Exception as e:
        print(f"File open error: {e}")
        exit(1)

    try:
        arr = json.load(f)
    except Exception as e:
        print(f"JSON load error: {e}")
        exit(1)

    try:
        validate(arr, schema)
    except Exception as e:
        print(f"Validation error: {e}")
        exit(1)

    return arr


def save(wage: dict):
    from tinydb import TinyDB, Query
    db = TinyDB(path.dirname(__file__) + "/../data/wage_master.json", ensure_ascii=False, indent=2)

    q = Query()

    if len(db.search((q.prefecture == wage["prefecture"]) & (q.date_of_issue == wage["date_of_issue"]))) != 0:
        db.update(wage, (
            (q.prefecture == wage["prefecture"]) &
            (q.date_of_issue == wage["date_of_issue"])
        ))
    else:
        db.insert(wage)


if __name__ == "__main__":
    json_path = parse_args()
    wage_list = load(json_path)

    for wage in wage_list:
        save(wage)
