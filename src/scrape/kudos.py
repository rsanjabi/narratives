''' In progress refactoring of meta scraping functionality.'''
import time
import datetime
import csv
from typing import Generator, Tuple, List

from bs4 import BeautifulSoup
from requests.exceptions import ConnectTimeout, HTTPError

from scrape.page import Page
import utils.paths as paths
import config as cfg


class Kudos(Page):

    def __init__(self, fandom: str, from_top: bool = True):
        self.log_path = paths.kudo_log_path(fandom)
        self.kudo_path = paths.kudo_path(fandom)
        self.input_path = paths.meta_path(fandom)
        url = (f'https://archiveofourown.org/works/')
        super().__init__(fandom, 'kudos',
                         self.log_path,
                         self.kudo_path,
                         url,
                         from_top)

    def scrape(self):
        header = ['work_id', 'user', 'scrape_date']
        super().scrape(header)

    def _pages(self) -> Generator[Tuple[BeautifulSoup, str], None, None]:

        if self.from_top is True or self.last == self.progress.unscraped_flag:
            encountered = True
        else:
            encountered = False

        errors = 0

        with open(self.input_path, 'r') as f_in:
            reader = csv.reader(f_in)
            for i, row in enumerate(reader):
                # Skip header row
                if i == 0:
                    continue
                # Write out rows again once we've encountered the work
                if not encountered:
                    if row[0] == self.last:
                        encountered = True
                    continue
                url = self.base_url + row[0] + '/kudos'
                self.fandom_id = row[0]
                try:
                    soup = self._get_soup(url)
                    self.logger.info(f"Scraped id: {self.fandom_id}")
                except HTTPError:
                    self.logger.info(f"HTTPError/skipping: {self.fandom_id}")
                except ConnectTimeout:
                    self.logger.error(f"ConnectionTimeout "
                                      f"on: {self.fandom_id}")
                    if errors > cfg.MAX_ERRORS:
                        self.logger.error(f"{cfg.MAX_ERRORS} "
                                          f"encountered. Aborting.")
                        return
                    self.logger.error(f"{cfg.MAX_ERRORS-errors} errors left.")
                    errors += 1
                    time.sleep(cfg.DELAY*errors*10)    # Increase sleep time
                else:
                    yield soup, self.fandom_id
                finally:
                    time.sleep(cfg.DELAY)

    def _page_elements(self, soup: BeautifulSoup) -> Generator[List[str],
                                                               None, None]:
        kudo_soup = soup.find(id="kudos").find_all('a')
        # Convert to set to remove dups due to AO3 kudo errors
        for kudo in set(kudo_soup):
            yield ([self.fandom_id] + [kudo.text] +
                   [datetime.datetime.now().strftime("%d/%b/%Y %H:%M")])
