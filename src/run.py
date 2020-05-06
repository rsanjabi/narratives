#!/usr/bin/env python3
'''
    Short term code to create a pipeline. Will be replaced by Prefect or
    Airflow in the future.
'''

from scrape.meta import Meta
from scrape.kudos import Kudos
import config as cfg


for fandom in cfg.TEST_FANDOM_LIST:
    print(f"Starting to scrape: {fandom}")
    try:
        m = Meta(fandom, from_top=True)
        m.scrape()
        print(f"finished scraping meta for : {fandom}")
    except Exception as e:
        print(f"Ran into problem with {fandom}: {e}")
print(f"Done with meta.")

for fandom in cfg.TEST_FANDOM_LIST:
    print(f"Starting to scrape: {fandom}")
    try:
        k = Kudos(fandom, from_top=True)
        k.scrape()
        print(f"finished scraping kudos for : {fandom}")
    except Exception as e:
        print(f"Ran into problem with {fandom}: {e}")
print(f"Done with kudos.")
