"""In progress refactoring of meta scraping functionality."""

from scrape.page import Page
import utils.paths as paths


class Meta(Page):

    def __init__(self, fandom: str):
        self.log_path = paths.meta_log_path(fandom)
        self.meta_path = paths.meta_path(fandom)
        super().__init__(fandom, 'meta', self.log_path, self.meta_path)

    def scrape(self, page: int) -> None:
        self.progress.write(page)
