#!/usr/bin/env python3
'''
    Short term code to create a pipeline. Will be replaced by Prefect or
    Airflow in the future.
'''
# from scrape.meta import Meta
from scrape.kudos import Kudos
# from db.insert_meta import DBMeta       # type: ignore
from db.insert_kudos import DBKudos     # type: ignore
# import config as cfg

# for fandom in cfg.TEST_FANDOM_LIST:
'''
print(f"Starting to scrape {fandom} meta.")
try:
    m = Meta(fandom, from_top=False)
    m.scrape()
    print(f"Finished scraping meta for : {fandom}")
except Exception as e:
    print(f"Ran into meta problem with {fandom}: {e}")

print(f"Inserting {fandom} meta into database.")
try:
    db = DBMeta(fandom)
    db.insert()
    print(f"Finished inserting meta for : {fandom}")
except Exception as e:
    print(f"Ran into problem inserting meta with {fandom}: {e}")
'''

for _ in range(24):
    print("Starting to scrape kudos.")
    k = Kudos(num_batches=1, batch_size=500)
    k.scrape()
    print("Finished scraping kudos")

    print("Inserting kudos into database.")
    db = DBKudos()
    db.insert()
    print("Finished inserting kudos.")

    print("Done one batch")


print("Done scraping and inserting kudos.")
