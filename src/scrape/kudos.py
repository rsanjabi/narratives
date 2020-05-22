''' In progress refactoring of meta scraping functionality.'''
import time
from datetime import datetime, timedelta
import json
from typing import List
from mypy_extensions import TypedDict

from bs4 import BeautifulSoup
from requests.exceptions import ConnectTimeout, HTTPError

from scrape.page import Page
import utils.paths as paths
import config as cfg
from db.kudos_db import DBKudos     # type: ignore
from scrape.algo import FanworksBatch

KudosJson = TypedDict('KudosJson', {
                     'work_id': str,
                     'kudos': List[str],
                     'scrape_date': str})


class Kudos(Page):

    def __init__(self, num_batches: int = 1):
        self.num_batches = num_batches
        # TODO fix this inheritance issue (fandom, from top)
        fandom = 'Star Wars'
        self.log_path = paths.kudo_log_path('Star Wars')
        self.kudo_path = paths.kudo_path('Star Wars')
        url = ('https://archiveofourown.org/works/')
        super().__init__(fandom, 'kudos', url, True)

    def scrape(self) -> None:

        kudo_batch = FanworksBatch(batch_size=10)
        work_ids = kudo_batch.next_batch()
        with open(self.kudo_path, 'w') as f_out:
            for id in work_ids:
                page = self.get_page(id)
                kudos = self._page_elements(page, id)
                f_out.write(json.dumps(kudos)+'\n')
                self.progress.write(id)
        self.logger.info(f'Completed scraping "{self.page_kind}"')
        return

    def _get_page(self, page: BeautifulSoup, work_id: str) -> BeautifulSoup:

        url = self.base_url + work_id + '/kudos'
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

    def _recently_updated(self, work_id: str) -> bool:
        kudo_db = DBKudos(self.page_kind)
        scr_date = kudo_db.kudo_scrape_date(work_id)
        if scr_date is None:
            return False
        return (scr_date > (datetime.now()-timedelta(cfg.SCR_WINDOW)))
