'''
    Abstract class for generic scraping actions
'''

from abc import ABC, abstractmethod
import logging
from pathlib import Path

import utils.paths as paths
# import config as cfg
from scrape.page_tracker import PageTracker


class Page(ABC):

    def __init__(self, fandom: str,
                 type: str,
                 log_path: Path,
                 path: Path):
        self.fandom = fandom
        self.type = type
        self.log_path = log_path
        self.path = path
        self.from_top = True
        self.fandom_path = paths.fandom_path(fandom)
        self.progress = PageTracker(self.fandom_path, self.type)

        self.logger = self._init_log()

    @abstractmethod
    def scrape(self):
        # scrapes webpages into csv files
        pass

    def insert(self):
        # inserts csv results into a db
        pass

    def _find_last(self):
        pass

    def _write_page(self):
        pass

    def _soup_page(self):
        pass

    def _extract(self):
        pass

    def _init_log(self):
        logger = logging.getLogger(self.fandom+self.type)
        logger.setLevel(logging.DEBUG)
        fh = logging.FileHandler(self.path, mode='a')
        formatter = logging.Formatter('%(asctime)s-%(levelname)s-%(message)s')
        fh.setFormatter(formatter)
        logger.addHandler(fh)

        return logger
