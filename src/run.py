#!/usr/bin/env python3
'''
    Short term code to create a pipeline. Will be replaced by Prefect or
    Airflow in the future.
'''

import scrape.meta as meta
import scrape.kudos as kudos
import config as cfg

for fandom in cfg.TEST_FANDOM_LIST:
    print(f"Starting to scrape: {fandom}")
    try:
        meta.scrape(fandom, from_the_top=True)
        kudos.scrape(fandom, from_the_top=True)
        print(f"finished scraping meta and kudos for : {fandom}")
    except Exception as e:
        print(f"Ran into problem with {fandom}: {e}")
print(f"Done.")
