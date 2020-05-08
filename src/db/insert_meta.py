# from typing import List, Dict
# import logging
# from logging import Logger
# from pathlib import Path
import csv
import utils.paths as paths
import config as cfg
# from scrape.progress import Progress

# import sys
import psycopg2
from psycopg2.extensions import AsIs
from db.ao3_db import AO3DB


class Meta(AO3DB):

    def __init__(self, fandom: str):
        self.meta_path = paths.meta_path(fandom)
        self.meta_db_log_path = paths.meta_db_log_path(fandom)
        super().__init__(fandom, self.meta_db_log_path, 'meta_db')

    def meta_rows(self):
        with open(self.meta_path, 'r') as f_in:
            reader = csv.reader(f_in)
            for i, row in enumerate(reader):
                if i == 0:
                    continue
                x = dict(zip(cfg.META_COLS, row))
                yield x

    def insert(self) -> None:
        self.logger.info(f"Opening {self.meta_path}")
        rows = self.meta_rows()
        for row in rows:
            print(f"********{row['work_id']}, {row['title']}, {row['author']}")

            columns = row.keys()
            values = [row[column] for column in columns]

            insert_statement = 'insert into staging_meta2 (%s) values %s'

            # cursor.execute(insert_statement,
            # (AsIs(','.join(columns)), tuple(values)))
            # print(self.cursor.mogrify(insert_statement,
            #                          (AsIs(','.join(columns)),
            #                           tuple(values))))

            sql = '''INSERT INTO staging_meta2 (%s) VALUES (%s);'''

            '''
                        %(work_id)s,
                        %(title)s,
                        %(author)s
                    )
            
                    ON CONFLICT (work_id)
                    DO UPDATE SET (
                        work_id,
                        title,
                        author
                    ) = (
                        EXCLUDED.work_id,
                        EXCLUDED.title,
                        EXCLUDED.author
                    );'''
            try:
                print(self.cursor.mogrify(sql, (AsIs(','.join(columns)), tuple(values))))
                self.cursor.execute(sql, (AsIs(','.join(columns)), tuple(values)))
                self.connect.commit()
            except psycopg2.errors.InFailedSqlTransaction as e:
                print(e)
                raise e

    def _table_creation(self):
        try:
            # self.cursor.execute("""DROP TABLE IF EXISTS staging_meta2;""")
            self.cursor.execute("""
                CREATE TABLE staging_meta2 (
                    work_id             TEXT PRIMARY KEY,
                    title               TEXT,
                    author              TEXT,
                    warnings            TEXT,
                    category            TEXT,
                    status              TEXT
                );
            """)
            self.connect.commit()
            self.logger.info("Created new table")
            print("Created new table")
        except psycopg2.errors.DuplicateTable:
            self.logger.info("Table already exists.")
            print("Table already exists.")


'''
    def insert(self) -> None:
        self.logger.info(f"Opening {self.meta_path}")
        rows = self.meta_rows()
        self.cursor.executemany("""
            INSERT INTO staging_meta (
                work_id,
                title,
                author,
                gifted,
                rating,
                warnings,
                category,
                status,
                fandom,
                relationship,
                character,
                additional_tags,
                summary,
                language,
                words,
                chapters,
                collections,
                comments,
                kudos,
                bookmarks,
                hits,
                series_part,
                series_name,
                updated,
                scrape_date
            ) VALUES (
                %(work_id)s,
                %(title)s,
                %(author)s,
                %(gifted)s,
                %(rating)s,
                %(warnings)s,
                %(category)s,
                %(status)s,
                %(fandom)s,
                %(relationship)s,
                %(character)s,
                %(additional_tags)s,
                %(summary)s,
                %(language)s,
                %(words)s,
                %(chapters)s,
                %(collections)s,
                %(comments)s,
                %(kudos)s,
                %(bookmarks)s,
                %(hits)s,
                %(series_part)s,
                %(series_name)s,
                %(updated)s,
                %(scrape_date)s
            )
            ON CONFLICT (work_id)
            DO UPDATE SET (
                work_id,
                title,
                author,
                gifted,
                rating,
                warnings,
                category,
                status,
                fandom,
                relationship,
                character,
                additional_tags,
                summary,
                language,
                words,
                chapters,
                collections,
                comments,
                kudos,
                bookmarks,
                hits,
                series_part,
                series_name,
                updated,
                scrape_date
            ) = (
                EXCLUDED.%(work_id)s,
                EXCLUDED.%(title)s,
                EXCLUDED.%(author)s,
                EXCLUDED.%(gifted)s,
                EXCLUDED.%(rating)s,
                EXCLUDED.%(warnings)s,
                EXCLUDED.%(category)s,
                EXCLUDED.%(status)s,
                EXCLUDED.%(fandom)s,
                EXCLUDED.%(relationship)s,
                EXCLUDED.%(character)s,
                EXCLUDED.%(additional_tags)s,
                EXCLUDED.%(summary)s,
                EXCLUDED.%(language)s,
                EXCLUDED.%(words)s,
                EXCLUDED.%(chapters)s,
                EXCLUDED.%(collections)s,
                EXCLUDED.%(comments)s,
                EXCLUDED.%(kudos)s,
                EXCLUDED.%(bookmarks)s,
                EXCLUDED.%(hits)s,
                EXCLUDED.%(series_part)s,
                EXCLUDED.%(series_name)s,
                EXCLUDED.%(updated)s,
                EXCLUDED.%(scrape_date)s
            );
        """, ({**row} for row in rows))
        self.connect.commit()

# DROP TABLE IF EXISTS staging_meta;

    def _table_creation(self):
        try:
            self.cursor.execute("""
                CREATE TABLE staging_meta (
                    work_id             TEXT PRIMARY KEY,
                    title               TEXT NOT NULL,
                    author              TEXT NOT NULL,
                    gifted              TEXT,
                    rating              TEXT NOT NULL,
                    warnings            TEXT NOT NULL,
                    category            TEXT,
                    status              TEXT,
                    fandom              TEXT NOT NULL,
                    relationship        TEXT,
                    character           TEXT,
                    additional_tags     TEXT,
                    summary             TEXT,
                    language            TEXT NOT NULL,
                    words               TEXT NOT NULL,
                    chapters            TEXT NOT NULL,
                    collections         TEXT,
                    comments            TEXT,
                    kudos               TEXT,
                    bookmarks           TEXT,
                    hits                TEXT,
                    series_part         TEXT,
                    series_name         TEXT,
                    updated             TEXT NOT NULL,
                    scrape_date         TEXT NOT NULL
                );
            """)
            self.connect.commit()
            self.logger.info("Created new table")
            print("Created new table")
        except psycopg2.errors.DuplicateTable:
            self.logger.info("Table already exists.")
            print("Table already exists.")

'''
'''
    def _table_creation(self) -> None:
        try:
            self.cursor.execute("CREATE TABLE fanworks "
                                "(ein text UNIQUE PRIMARY KEY)")
            self.connect.commit()

'''
