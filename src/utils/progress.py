'''
    Progress reads and writes a single line from a file in order to store
    the last page that the Scraper classes have processed.

    Pages are stored in the fandom path directory as .meta or .kudos.

    It holds two values:
        * An int corresponding to page number or work_id.
        * Second value is the date and time that value was scraped.

    TODO: check for wrong param add throw exception for ValueException

'''

import os
from typing import Tuple
import datetime
from pathlib import Path
import config as cfg


class Progress():

    def __init__(self, tag_path: Path):

        self.unscraped_flag = '-1'   # constant for when unscraped
        self.file_path = tag_path.joinpath(cfg.PROGRESS_TRACK)
        date = datetime.datetime.now().strftime("%d/%b/%Y %H:%M")

        if os.path.exists(self.file_path) is False:
            with open(self.file_path, 'w') as f_out:
                f_out.write(f"{self.unscraped_flag}, {date}")

    def write(self, page: str) -> None:
        date = datetime.datetime.now().strftime("%d/%b/%Y %H:%M")
        with open(self.file_path, 'w') as f_out:
            f_out.write(page + ', ' + date)

    def read(self) -> Tuple[str, str]:
        with open(self.file_path, 'r') as f_in:
            last_page, date = f_in.read().split(',')
        return last_page, date
