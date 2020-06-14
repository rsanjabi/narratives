from typing import Generator, Any
import json
import psycopg2

from pathlib import Path

import utils.paths as paths
from db.ao3_db import AO3DB


class DBMeta(AO3DB):
    def __init__(self, fandom: str) -> None:
        self.meta_path: Path = paths.meta_path(fandom)
        l_path: Path = paths.meta_log_path(fandom)
        super().__init__(fandom + "meta_db", l_path)
        self._table_creation()

    def insert(self) -> None:
        # self.logger.info(f"Opening {self.meta_path}")
        rows = self._rows()
        for row in rows:
            if self.fanwork_exists(row["work_id"]):
                sql = """
                    UPDATE staging_meta
                    SET
                        title = %(title)s,
                        author = %(author)s,
                        gifted = %(gifted)s,
                        rating = %(rating)s,
                        warnings = %(warnings)s,
                        category = %(category)s,
                        status = %(status)s,
                        fandom = %(fandom)s,
                        relationships = %(relationships)s,
                        characters = %(characters)s,
                        freeforms = %(freeforms)s,
                        summary = %(summary)s,
                        language = %(language)s,
                        words = %(words)s,
                        chapters = %(chapters)s,
                        collections = %(collections)s,
                        comments = %(comments)s,
                        kudos = %(kudos)s,
                        bookmarks = %(bookmarks)s,
                        hits = %(hits)s,
                        series_part = %(series_part)s,
                        series_name = %(series_name)s,
                        updated = %(updated)s,
                        scrape_date = %(scrape_date)s
                    WHERE
                        work_id = %(work_id)s;
                    """
            else:
                sql = """
                    INSERT INTO staging_meta
                    VALUES (
                        %(work_id)s,
                        %(title)s,
                        %(author)s,
                        %(gifted)s,
                        %(rating)s,
                        %(warnings)s,
                        %(category)s,
                        %(status)s,
                        %(fandom)s,
                        %(relationships)s,
                        %(characters)s,
                        %(freeforms)s,
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
                    );
                    """

            self.cursor.execute(sql, ({**row}))
            self.connect.commit()
            # self.logger.info(f"{row['work_id']}'s meta added to db.")
            '''
            self.cursor.execute("""
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
                    relationships,
                    characters,
                    freeforms,
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
                    %(relationships)s,
                    %(characters)s,
                    %(freeforms)s,
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
                    relationships,
                    characters,
                    freeforms,
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
                    EXCLUDED.work_id,
                    EXCLUDED.title,
                    EXCLUDED.author,
                    EXCLUDED.gifted,
                    EXCLUDED.rating,
                    EXCLUDED.warnings,
                    EXCLUDED.category,
                    EXCLUDED.status,
                    EXCLUDED.fandom,
                    EXCLUDED.relationships,
                    EXCLUDED.characters,
                    EXCLUDED.freeforms,
                    EXCLUDED.summary,
                    EXCLUDED.language,
                    EXCLUDED.words,
                    EXCLUDED.chapters,
                    EXCLUDED.collections,
                    EXCLUDED.comments,
                    EXCLUDED.kudos,
                    EXCLUDED.bookmarks,
                    EXCLUDED.hits,
                    EXCLUDED.series_part,
                    EXCLUDED.series_name,
                    EXCLUDED.updated,
                    EXCLUDED.scrape_date
                );
            """, ({**row}))
            self.connect.commit()
            '''

    def _table_creation(self) -> None:
        try:
            self.cursor.execute(
                """
                CREATE TABLE staging_meta (
                    work_id             TEXT PRIMARY KEY,
                    title               TEXT,
                    author              TEXT [],
                    gifted              TEXT [],
                    rating              TEXT,
                    warnings            TEXT [],
                    category            TEXT [],
                    status              TEXT,
                    fandom              TEXT [],
                    relationships       TEXT [],
                    characters          TEXT [],
                    freeforms           TEXT [],
                    summary             TEXT,
                    language            TEXT,
                    words               TEXT,
                    chapters            TEXT,
                    collections         INT,
                    comments            INT,
                    kudos               INT,
                    bookmarks           INT,
                    hits                INT,
                    series_part         TEXT,
                    series_name         TEXT,
                    updated             DATE,
                    scrape_date         TIMESTAMP,
                    kudo_givers         TEXT [],
                    kudo_scr_date       TIMESTAMP
                );
            """
            )
            self.connect.commit()
            # self.logger.info("Created new table")
        except psycopg2.errors.DuplicateTable:
            self.connect.commit()
            # self.logger.info("Table already exists.")

    def _table_drop(self) -> None:
        try:
            sql = "DROP TABLE staging_meta;"
            self.cursor.execute(sql)
            self.connect.commit()
            # self.logger.info("Table dropped")
        except Exception:
            self.logger.error("Error dropping table.")

    def _rows(self) -> Generator[Any, None, None]:
        with open(self.meta_path, "r") as f_in:
            for row in f_in:
                yield json.loads(row)
