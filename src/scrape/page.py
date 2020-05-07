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
from requests.exceptions import ConnectTimeout, HTTPError, RequestException
import utils.paths as paths
import config as cfg
from scrape.progress import Progress


class Page(ABC):

    def __init__(self, page_kind: str,
                 type: str,
                 log_path: Path,
                 path: Path,
                 base_url: str,
                 from_top: bool):
        self.page_kind = page_kind  # fandom or media page
        self.type = type            # eg meta or kudos or ...
        self.log_path = log_path
        self.path = path
        self.base_url = base_url

        self.fandom_path = paths.fandom_path(page_kind)
        self.progress = Progress(self.fandom_path, self.type)
        self.last = self.progress.read()[0]
        self.logger = self._init_log()
        self.from_top = self._start_from_top(from_top)

    def scrape(self, header: List[str]) -> None:

        if self.from_top is True or self.path.is_file() is False:
            mode = 'w'
        else:
            mode = 'a'

        with open(self.path, mode) as f_out:
            self.writer = csv.writer(f_out)
            if mode == 'w':
                self.writer.writerow(header)
            pages = self._pages()
            for page, progress_num in pages:
                page_elements = self._page_elements(page)
                for element in page_elements:
                    self.writer.writerow(element)
                self.progress.write(progress_num)
        self.logger.info(f'Completed scraping "{self.page_kind}"')
        return

    @abstractmethod
    def _pages(self):
        pass

    @abstractmethod
    def _page_elements(self, soup: BeautifulSoup):
        pass

    def _get_soup(self, url: str) -> BeautifulSoup:
        ''' Scrape the page, returning success and soup.'''

        req = requests.get(url, headers=cfg.HTTP_HEADERS)
        try:
            req.raise_for_status()
        except ConnectTimeout:
            raise ConnectTimeout
        except HTTPError:
            raise HTTPError
        except RequestException:
            raise RequestException
        else:
            soup = BeautifulSoup(req.text, 'html.parser')
            return soup

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
