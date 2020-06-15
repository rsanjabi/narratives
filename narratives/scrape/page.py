"""
    Abstract class for generic scraping actions
"""
from abc import ABC, abstractmethod
import logging
from logging import Logger
from pathlib import Path
from bs4 import BeautifulSoup
import requests
from requests.exceptions import ConnectTimeout, HTTPError, RequestException
import config as cfg


class Page(ABC):
    def __init__(self, log_name: str, log_path: Path):
        self.logger = self._init_log(log_name, log_path)

    @abstractmethod
    def scrape(self):
        pass

    @abstractmethod
    def _pages(self):
        pass

    @abstractmethod
    def _page_elements(self, soup: BeautifulSoup):
        pass

    def _get_soup(self, url: str) -> BeautifulSoup:
        """ Scrape the page, returning success and soup."""

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
            soup = BeautifulSoup(req.text, "html.parser")
            return soup

    def _init_log(self, log_name: str, log_path: Path) -> Logger:
        logger = logging.getLogger(log_name)
        logger.setLevel(logging.DEBUG)
        fh = logging.FileHandler(log_path, mode="a")
        formatter = logging.Formatter("%(asctime)s-%(levelname)s-%(message)s")
        fh.setFormatter(formatter)
        logger.addHandler(fh)
        logger.info("********************************")

        return logger
