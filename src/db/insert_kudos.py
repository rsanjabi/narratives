from typing import Generator, Any
import json
from pathlib import Path
from db.ao3_db import AO3DB
import utils.paths as paths


class DBKudos(AO3DB):
    def __init__(self) -> None:

        l_path: Path = paths.kudo_log_path()
        super().__init__("kudos", l_path)

    def _next_batch(self):
        while True:
            path = paths.oldest_kudo_path()
            if path is None:
                return
            else:
                yield path

    def insert(self):
        batches = self._next_batch()
        for batch in batches:
            print(f"Opening {batch}")
            # self.logger.info(f"Opening {batch}")
            rows = self._rows(batch)
            for row in rows:
                if super().fanwork_exists(row["work_id"]):
                    sql = """
                        UPDATE staging_meta
                        SET
                            kudo_givers = %(kudos)s,
                            kudo_scr_date = %(scrape_date)s
                        WHERE
                            work_id = %(work_id)s;
                        """
                    self.cursor.execute(sql, ({**row}))
                    print(f"{row['work_id']}'s kudos added to db.'")
                    # self.logger.info(f"{row['work_id']}'s kudos in db.'")
                else:
                    print(f"Fanwork {row['work_id']} not in db")
                    # self.logger.error(f"Fanwork {row['work_id']} not in db")
                    # to be logged to file.
                self.connect.commit()
            print(f"{batch} has been added to database. Deleting.")
            # self.logger.info(f"{batch} added to database. Deleting.")
            paths.remove_kudo_path(batch)

    def _rows(self, batch) -> Generator[Any, None, None]:
        with open(batch, "r") as f_in:
            for row in f_in:
                yield json.loads(row)
