from typing import List
# import json
import psycopg2.extras

from db.ao3_db import AO3DB


class DBFandoms(AO3DB):

    def __init__(self):
        self.cursor, self.connect = super().open()
        self._table_creation()

    def insert(self, fandoms: List):
        rows = [{"fandom": "07-Ghost", "total": {"date": "24/May/2020 08:13", "count": "210"}},
                {"fandom": "1 Pound no Fukuin | One-Pound Gospel", "total": {"date": "24/May/2020 08:14", "count": "5"}}]

        # iter_rows = ({**rows} for row in rows)      # type: ignore
        psycopg2.extras.execute_batch(self.cursor, """
            INSERT INTO staging_fandoms VALUES (
                %(fandom)s,
                %(total)s
            );
        """, ({**rows}), page_size=1000)

        return []

    def _table_creation(self) -> None:
        try:
            self.cursor.execute("""
                    CREATE TABLE staging_fandoms (
                    fandom             TEXT NOT NULL PRIMARY KEY,
                    counts               json
                    );
            """)
            self.connect.commit()
            print("Created new fandom table")
        except psycopg2.errors.DuplicateTable:
            self.connect.commit()
            print("Fandom table already exists.")
