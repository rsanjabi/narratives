import time
import json
from datetime import datetime
from pathlib import Path
from bs4 import BeautifulSoup
from typing import Generator, Any, List

from scrape.page import Page
import utils.paths as paths
import config as cfg
from db.ao3_db import AO3DB


class Fandoms(Page):

    def __init__(self):
        self.log_name = 'fandoms'
        self.log_path = paths.fandom_log_path()
        super().__init__(self.log_name, self.log_path)

    def scrape(self) -> List:
        fandom_list = []
        urls = self._pages()
        for url in urls:
            print(f"scraping url: {url}")
            soup = self._get_soup(url)
            results = self._page_elements(soup)
            for fandom in results:
                fandom_list.append(fandom)
        with open(paths.fandom_path(), 'w') as f_out:
            f_out.write(json.dumps(fandom_list))
        return fandom_list

    def insert(self, fandoms: dict):
        db = AO3DB(self.log_name, self.log_path)
        db.insert_fandoms(fandoms)

    def _pages(self) -> Generator[Path, None, None]:
        for i, page in enumerate(cfg.FANDOM_PAGES):
            yield page
            time.sleep(cfg.DELAY)

    def _page_elements(self,
                       soup: BeautifulSoup) -> Generator[Any, None, None]:
        letter_group = soup.find_all(class_='tags index group')
        for letter in letter_group:
            for title in letter.find_all(class_="tag"):
                fandom = title.text.strip()
                date = datetime.now().strftime("%d/%b/%Y %H:%M")

                x = title.next_sibling.strip()
                count = x.replace("(", "").replace(")", "")

                yield {
                    "name": fandom,
                    "date": date,
                    "count": count
                }
