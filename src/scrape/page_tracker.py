'''
    PageTracker reads and writes a single line from a file in order to store
    the last page that the Scraper classes have processed.

    Pages are stored in the fandom path directory as .meta or .kudos.

    It holds two values:
        * An int corresponding to page number or work_id.
        * Second value is the date and time that value was scraped.

    TODO: what happens when you read an empty file?
    TODO: add time to date?
'''

import os
from typing import Tuple
import datetime
from pathlib import Path

''' TODO: add throw exception for ValueException '''


class PageTracker():

    def __init__(self, fandom_path: Path, type: str):

        self.file_path = fandom_path.joinpath('.' + type)

        if os.path.exists(self.file_path) is False:
            with open(self.file_path, 'w') as _:
                pass

    def write(self, page: int) -> None:
        date = datetime.datetime.now().strftime("%Y%b%d")
        with open(self.file_path, 'w') as f_out:
            f_out.write(str(page) + ', ' + date)

    def read(self) -> Tuple[int, str]:
        with open(self.file_path, 'r') as f_in:
            last_page, date = f_in.read().split(',')
        return int(last_page), date
