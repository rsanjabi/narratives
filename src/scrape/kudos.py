''' In progress refactoring of meta scraping functionality.'''
import time
from datetime import datetime
import json
from typing import List
from mypy_extensions import TypedDict

from bs4 import BeautifulSoup
from requests.exceptions import ConnectTimeout, HTTPError

from scrape.page import Page
import utils.paths as paths
import config as cfg
from db.ao3_db import AO3DB     # type: ignore

KudosJson = TypedDict('KudosJson', {
                     'work_id': str,
                     'kudos': List[str],
                     'scrape_date': str})


class Kudos(Page):

    def __init__(self, num_batches: int = 1):
        self.num_batches = num_batches
        self.log_path = paths.kudo_log_path()
        self.base_url = ('https://archiveofourown.org/works/')
        super().__init__('kudos', self.log_path)

    def scrape(self) -> None:
        db = AO3DB('kudos', self.log_path)
        for i in range(self.num_batches):
            batch_num = str(i)     # TODO: gen this number
            kudo_list = db.missing_kudos('1000')
            batch_path = paths.kudo_path(batch_num)
            with open(batch_path, 'w') as f_out:
                for work_id in kudo_list:
                    page = self._pages(work_id)
                    kudos = self._page_elements(page, work_id)
                    print(kudos)
                    f_out.write(json.dumps(kudos)+'\n')
                    self.logger.info(f'scraped {work_id}')
            self.logger.info(f'scraped {i} batch')
        return

    def _pages(self, work_id: str) -> BeautifulSoup:

        url = self.base_url + work_id + '/kudos'
        print(url)
        errors = 0

        while errors < cfg.MAX_ERRORS:
            try:
                time.sleep(cfg.DELAY)
                soup = self._get_soup(url)
                self.logger.info(f"Scraped id: {work_id}")
            except HTTPError:
                self.logger.info(f"HTTPError: {work_id}")
                errors += 1
                time.sleep(cfg.DELAY*errors*10)    # Increase sleep time
            # except 404 error:
            #   print work_id to tbdeleted log
            except ConnectTimeout:
                self.logger.error(f"ConnectionTimeout on: {work_id}")
                self.logger.error(f"{cfg.MAX_ERRORS-errors} errors left.")
                errors += 1
                time.sleep(cfg.DELAY*errors*10)    # Increase sleep time
            else:
                return soup
        return None

    def _page_elements(self, soup: BeautifulSoup, id: str) -> KudosJson:
        k_d: KudosJson = {}       # type: ignore
        k_d['work_id'] = id
        k_d['kudos'] = [x.text for x in soup.find(id="kudos").find_all('a')]
        k_d['scrape_date'] = datetime.now().strftime("%d/%b/%Y %H:%M")
        return k_d
