from tinydb import TinyDB, Query
import os
from datetime import date as d
from itertools import groupby

from api.db.prefecture import Prefecture


class Wage:
    """
    Minimum wage database
    """

    # Schema:
    # {
    #     "prefecture": str,
    #     "wage": int,
    #     "date_of_issue": str,
    # }
    data_db = TinyDB(
        os.path.join(os.path.dirname(__file__), "../../data/wage_master.json"),
        access_mode="r",
    )

    @classmethod
    def search(cls, prefecture: str, date: d):
        """
        Search for minimum wage records
        """
        return SearchResult(
            cls.data_db.search(
                cls.prefecture_condition(prefecture) & cls.date_condition(date)
            )
        )

    @staticmethod
    def prefecture_condition(prefecture_name: str):
        """
        Prefecture where clause

        `prefecture_name` can be "all" or the name of a prefecture or its abbreviation.
        """

        where = Query()
        if prefecture_name == "all":
            return where.noop()
        else:
            return where.prefecture == Prefecture.find(prefecture_name)

    @staticmethod
    def date_condition(date: d):
        """
        Date where clause

        Filter on or before the specified date.
        Maybe need to go back several years if there is no minimum wage data available for the specified year (if it hasn't been changed).
        """

        where = Query()
        return where.date_of_issue <= date.isoformat()


class SearchResult:
    """
    Search result of minimum wage records

    Provides method to aggregate and format search results.
    """

    def __init__(self, records: list[dict]):
        self.records = records

    def to_response(self):
        """
        Convert search results to response
        """

        agg_dict = self.group_by_prefecture(self.records)
        return [
            self.latest_by_date(list(agg_dict[int(k)])) for k in sorted(agg_dict.keys())
        ]

    @staticmethod
    def group_by_prefecture(records: list[dict]):
        """
        Group records by prefecture
        """

        key_func = lambda record: Prefecture.find_code(record["prefecture"])
        sorted_records = sorted(records, key=key_func)
        return {key: list(val) for key, val in groupby(sorted_records, key=key_func)}

    @staticmethod
    def latest_by_date(records: list[dict]):
        """
        Get the latest record by date
        """

        return max(records, key=lambda record: d.fromisoformat(record["date_of_issue"]))
