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

    def __init__(self, num_batches: int = 1, batch_size: int = 500):
        self.num_batches = num_batches
        self.batch_size = batch_size
        self.log_path = paths.kudo_log_path()
        self.base_url = ('https://archiveofourown.org/works/')
        super().__init__('kudo', self.log_path)

    def scrape(self) -> None:
        db = AO3DB('kudo', self.log_path, self.logger)
        for i in range(self.num_batches):
            kudo_list = db.missing_kudos(self.batch_size)
            batch_path = paths.kudo_path(time.strftime("%Y%m%d-%H%M%S"))
            with open(batch_path, 'w') as f_out:
                for work_id in kudo_list:
                    page = self._pages(work_id)
                    kudos = self._page_elements(page, work_id)
                    f_out.write(json.dumps(kudos)+'\n')
            self.logger.info(f'scraped {i} batch')
        return

    def _pages(self, work_id: str) -> BeautifulSoup:

        url = self.base_url + work_id + '/kudos'
        errors = 0

        while errors < cfg.MAX_ERRORS:
            try:
                time.sleep(cfg.DELAY)
                soup = self._get_soup(url)
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
