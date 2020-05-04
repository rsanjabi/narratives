'''
    Abstract class for generic scraping actions
'''

from abc import ABC, abstractmethod
from typing import List
import logging
from logging import Logger
from pathlib import Path
import csv
from bs4 import BeautifulSoup
import requests
import utils.paths as paths
import config as cfg
from scrape.page_tracker import PageTracker


class Page(ABC):

    def __init__(self, page_kind: str,
                 type: str,
                 log_path: Path,
                 path: Path,
                 base_url: str,
                 from_top: bool):
        self.page_kind = page_kind  # fandom or media page
        self.type = type
        self.log_path = log_path
        self.path = path
        self.base_url = base_url

        self.fandom_path = paths.fandom_path(page_kind)
        self.progress = PageTracker(self.fandom_path, self.type)
        self.last = self.progress.read()[0]
        self.logger = self._init_log()
        self.from_top = self._start_from_top(from_top)

    def scrape(self, header: List[str]) -> None:

        if self.from_top is True:
            mode = 'w'
        else:
            mode = 'a'

        with open(self.path, mode) as f_out:
            self.writer = csv.writer(f_out)
            if self.from_top is True or mode == 'a':
                self.writer.writerow(header)
            pages = self._get_pages()
            for page, state in pages:
                page_elements = self._get_data(page)
                for row in page_elements:
                    pass
                    # self._write_results(row)
                self.progress.write(state)
        return

    def _get_soup(self, url: str) -> BeautifulSoup:
        ''' Scrape the page, returning success and soup.'''

        req = requests.get(url, headers=cfg.HTTP_HEADERS)
        if req.status_code == 200:
            soup = BeautifulSoup(req.text, 'html.parser')
            return soup
        else:
            raise Exception("Page not found.")

    @abstractmethod
    def _get_pages(self):
        pass

    @abstractmethod
    def _get_data(self, page_text: str):
        pass

    @abstractmethod
    def _write_results(self, results):
        pass

    def _init_log(self) -> Logger:
        logger = logging.getLogger(self.page_kind+self.type)
        logger.setLevel(logging.DEBUG)
        fh = logging.FileHandler(self.log_path, mode='a')
        formatter = logging.Formatter('%(asctime)s-%(levelname)s-%(message)s')
        fh.setFormatter(formatter)
        logger.addHandler(fh)
        logger.info("********************************")

        return logger

    def _start_from_top(self, from_top: bool) -> bool:

        if from_top is True:
            self.logger.info("Scraping from the top.")
            return True
        elif self.last == self.progress.unscraped_flag:
            self.logger.info(
                f"Last scraped unknown: {self.progress.unscraped_flag}. "
                f"Scraping from the top.")
            return True
        else:
            self.logger.info(f"Picking up from {self.last} ")
            return False
