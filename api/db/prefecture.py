from tinydb import TinyDB, Query
import os

where = Query()


class Prefecture:
    """
    Prefecture database
    """

    INVALID_PREFECTURE = "invalid"
    INVALID_PREFECTURE_CODE = 0

    # Schema:
    # {
    #     "prefecture": str,
    #     "pref_code": int,
    #     "aliases": list[str],
    # }
    data_db = TinyDB(
        os.path.join(os.path.dirname(__file__), "../../data/prefecture_master.json"),
        access_mode="r",
    )

    @classmethod
    def find(cls, ambiguous_name: str):
        """
        Find prefecture name from the name of a prefecture or its abbreviation.
        """

        records = cls.data_db.search(
            (where.prefecture == ambiguous_name) | (where.aliases.any([ambiguous_name]))
        )
        return records[0]["prefecture"] if len(records) != 0 else cls.INVALID_PREFECTURE

    @classmethod
    def find_code(cls, ambiguous_name: str):
        """
        Find prefecture code from the name of a prefecture or its abbreviation.
        """

        records = cls.data_db.search(
            (where.prefecture == ambiguous_name) | (where.aliases.any([ambiguous_name]))
        )
        return (
            records[0]["pref_code"]
            if len(records) != 0
            else cls.INVALID_PREFECTURE_CODE
        )
