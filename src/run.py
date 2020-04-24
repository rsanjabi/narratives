#!/usr/bin/env python3
'''
    Short term code to create a pipeline. Will be replaced by Prefect or
    Airflow in the future.
'''

import scrape.meta as meta
import scrape.kudos as kudos
import config as cfg

for fandom in cfg.TEST_FANDOM_LIST:
    try:
        meta.scrape(fandom, from_the_top=False)
        kudos.scrape(fandom, from_the_top=False)
        print(f"finished scraping meta and kudos for : {fandom}")
    except Exception as e:
        print(f"Ran into problem with {fandom}: {e}")
print(f"Done.")
