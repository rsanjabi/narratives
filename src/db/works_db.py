from pathlib import Path
from db.ao3_db import AO3DB
import utils.paths as paths


class DBWorks(AO3DB):

    def __init__(self):
        l_path: Path = paths.matrix_log_path()
        super().__init__('matrix', l_path, 'works_db')
