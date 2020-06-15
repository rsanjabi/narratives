from typing import List

# import json
import psycopg2.extras

from narratives.db.ao3_db import AO3DB


class DBFandoms(AO3DB):
    def __init__(self):
        self.cursor, self.connect = super().open()
        self._table_creation()

    def insert(self, fandoms: List):

        sql = """
            INSERT INTO fandom_counts (fandom, date, count)
            VALUES (%(name)s, %(date)s, %(count)s)
            ON CONFLICT (fandom, date)
            DO NOTHING
            ;
            """

        iter_fandoms = ({**fandom,} for fandom in fandoms)

        psycopg2.extras.execute_batch(self.cursor, sql, iter_fandoms)
        self.connect.commit()
        return []

    def _table_creation(self) -> None:
        try:
            self.cursor.execute(
                """
                    CREATE TABLE fandom_counts (
                    fandom           TEXT NOT NULL,
                    date             TIMESTAMP NOT NULL,
                    count            INTEGER,
                    PRIMARY KEY (fandom, date)
                    );
            """
            )
            self.connect.commit()
            print("Created new table: fandom_counts")
        except psycopg2.errors.DuplicateTable:
            self.connect.commit()
            print("Table fandom_counts already exists.")
