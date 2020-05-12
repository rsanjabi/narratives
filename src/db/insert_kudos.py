import utils.paths as paths
import sys
from pathlib import Path
from db.ao3_db import AO3DB


class DBKudos(AO3DB):
    def __init__(self, fandom: str) -> None:
        self.kudo_path: Path = paths.kudo_path(fandom)
        self.kudos_db_log_path: Path = paths.kudos_db_log_path(fandom)
        super().__init__(fandom,
                         self.kudo_path,
                         self.kudos_db_log_path,
                         'kudos_db')

    def insert(self) -> None:
        self.logger.info(f"Opening {self.kudo_path}")
        rows = self._rows()
        for row in rows:
            if self._fanwork_exists(row['work_id']):
                sql = """
                    UPDATE staging_meta
                    SET
                        kudo_givers = %(kudos)s,
                        kudo_scr_date = %(scrape_date)s
                    WHERE
                        work_id = %(work_id)s;
                    """
                self.cursor.execute(sql, ({**row}))
                self.logger.info(f"{row['work_id']}'s kudos added to db.'")
            else:
                self.logger.error(f"Fanwork {row['work_id']} not in database")
            self.connect.commit()

    def _table_creation(self):
        sql = """
            select exists
                (select * from information_schema.tables
                where table_name=%s)
            """
        self.cursor.execute(sql, ('staging_meta',))
        if (self.cursor.fetchone()[0]):
            self.logger.info(f"Found table to insert {self.page_kind}")
        else:
            self.logger.info("Table doesn't exist.")
            sys.exit()
        self.connect.commit()
