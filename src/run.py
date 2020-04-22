#!/usr/bin/env python3
'''
    Short term code to create a pipeline. Will be replaced by Prefect or
    Airflow in the future.
'''

# import scrape.meta as meta
import scrape.kudos as kudos
import config as cfg

# meta.scrape(cfg.TEST_FANDOM, from_the_top=True)
kudos.scrape(cfg.TEST_FANDOM, from_the_top=True)
print(f"finished scraping meta and kudos for : {cfg.TEST_FANDOM}")
