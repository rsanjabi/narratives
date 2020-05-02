"""In progress refactoring of meta scraping functionality."""
from typing import Generator

from scrape.page import Page
import utils.paths as paths


class Meta(Page):

    def __init__(self, fandom: str, from_top: bool):
        self.log_path = paths.meta_log_path(fandom)
        self.meta_path = paths.meta_path(fandom)
        super().__init__(fandom, 'meta',
                         self.log_path,
                         self.meta_path,
                         from_top)

    def insert(self):
        pass

    # def _get_pages(self) -> Generator[List[str]]:
    def _get_pages(self):
        yield [1, 2, 3]
    '''
    def debug(self, page: int) -> None:
        self.s
        self.progress.read()
    '''

    def _get_data(self):
        print(f"DEBUG1")
        pass

    def _write_results(self):
        print(f"DEBUG2")
        pass
