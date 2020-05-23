from typing import Generator, Any
import json
from pathlib import Path
from db.ao3_db import AO3DB
import utils.paths as paths


class DBKudos(AO3DB):
    def __init__(self, batch_num: int) -> None:

        self.kudo_path: Path = paths.kudo_path(str(batch_num))
        l_path: Path = paths.kudo_log_path()
        super().__init__('kudos', l_path)

    def insert(self):
        self.logger.info(f"Opening {self.kudo_path}")
        rows = self._rows()
        for row in rows:
            if super().fanwork_exists(row['work_id']):
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

    def _rows(self) -> Generator[Any, None, None]:
        with open(self.kudo_path, 'r') as f_in:
            for row in f_in:
                yield json.loads(row)
