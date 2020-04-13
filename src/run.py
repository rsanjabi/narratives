#!/usr/bin/env python3
'''
    Short term code to create a pipeline. Will be replaced by Prefect or
    Airflow in the future.
'''

import scrape.ao3_get_meta as meta
import scrape.ao3_get_kudos as kudos
import config as cfg


meta.scrape(cfg.TEST_FANDOM, from_the_top=False)
kudos.scrape(cfg.TEST_FANDOM, from_the_top=False)
print(f"finished scraping meta and kudos for : {cfg.TEST_FANDOM}")
