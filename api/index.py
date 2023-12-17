from fastapi import FastAPI
from tinydb import TinyDB, Query

import os
import time
from os import path
from datetime import date as d
from typing import Union
from itertools import groupby

os.environ["TZ"] = "Asia/Tokyo"
time.tzset()

# Schema:
# {
#     "prefecture": str,
#     "wage": int,
#     "date_of_issue": str,
# }
data_db = TinyDB(f"{path.dirname(__file__)}/../data/wage_master.json", access_mode='r')

# Schema:
# {
#     "prefecture": str,
#     "pref_code": int,
#     "aliases": list[str],
# }
master_db = TinyDB(f"{path.dirname(__file__)}/../data/prefecture_master.json", access_mode='r')

where = Query()

app = FastAPI()


def date_key(record: dict) -> d:
    # Date sorting key
    return d.fromisoformat(record["date_of_issue"])


def prefecture_key(record: dict) -> int:
    # Prefecture sorting key
    records = master_db.search(where.prefecture == record["prefecture"])
    return (records[0]["pref_code"] if len(records) != 0 else 0)


def prefecture_where(name: str):
    # Prefecture where clause
    # If name is "all", return no filters
    # If name is not found, return invalid filter
    # Otherwise, return prefecture filter
    if name == "all":
        return where.noop()
    else:
        results = master_db.search(
            (where.prefecture == name) |
            (where.aliases.any([name]))
        )
        name = results[0]["prefecture"] if len(results) != 0 else "invalid"
        return where.prefecture == name


def date_where(date: d):
    # Date where clause
    return (where.date_of_issue <= date.isoformat())


def group_by_prefecture(records: list[dict]):
    # Group records by prefecture
    sorted_records = sorted(records, key=prefecture_key)
    return {key:  list(val) for key, val in groupby(sorted_records, key=prefecture_key)}


def latest_record(records: list[dict]):
    # Pick latest record
    return max(records, key=date_key)


@app.get("/")
async def root(prefecture: str = "all", date: Union[str, None] = None):
    try:
        date = d.today() if date is None else d.fromisoformat(date)
    except ValueError:
        return {"error": f"Invalid date format: {date}. Required format: YYYY-MM-DD"}

    results = data_db.search(prefecture_where(prefecture) & date_where(date))
    agg_dict = group_by_prefecture(results)
    return [latest_record(list(agg_dict[int(k)])) for k in sorted(agg_dict.keys())]

if __name__ == "__main__":
    import uvicorn
    import os

    port = int(os.environ.get("PORT", 8000))

    uvicorn.run(app, host="0.0.0.0", port=port)
