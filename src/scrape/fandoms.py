import time
from datetime import datetime
from pathlib import Path
from bs4 import BeautifulSoup
from typing import Generator, Any

from scrape.page import Page
import utils.paths as paths
import config as cfg


class Fandoms(Page):

    def __init__(self):
        log_name = 'fandoms'
        log_path = paths.fandom_log_path()
        super().__init__(log_name, log_path)

    def scrape(self):

        urls = self._pages()
        for url in urls:
            print(f"scraping url: {url}")
            time.sleep(cfg.DELAY)
            soup = self._get_soup(url)
            results = self._page_elements(soup)
            for fandom in results:
                print(fandom)
                # write results to today -date file
                pass

    def _pages(self) -> Generator[Path, None, None]:
        for page in cfg.FANDOM_PAGES:
            yield page

    def _page_elements(self,
                       soup: BeautifulSoup) -> Generator[Any, None, None]:
        letter_group = soup.find_all(class_='tags index group')
        for letter in letter_group:
            for title in letter.find_all(class_="tag"):
                yield {
                    'fandom': title.text.strip(),
                    'count': title.next_sibling.strip().replace("(", "").replace(")", ""),
                    'date': datetime.now().strftime("%d/%b/%Y %H:%M")
                }

    def insert(self):
        pass
