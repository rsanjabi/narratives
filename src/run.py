#!/usr/bin/env python3
'''
    Short term code to create a pipeline. Will be replaced by Prefect or
    Airflow in the future.
'''


from scrape.fandoms import Fandoms
from db.insert_fandoms import DBFandoms     # type: ignore

# from scrape.meta import Meta
# from scrape.kudos import Kudos
# from db.insert_meta import DBMeta       # type: ignore
# from db.insert_kudos import DBKudos     # type: ignore
# import config as cfg

scraper = Fandoms()
fandom_list = scraper.scrape()

db_obj = DBFandoms()
db_obj.insert(fandom_list)

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

k = Kudos(num_batches=1, batch_size=100)
db = DBKudos()

for _ in range(100):
    try:
        print("Starting to scrape kudos.")
        k.scrape()
        print("Finished scraping kudos")
    except Exception as e:
        print(f"Ran into a problem: {e}")

    print("Inserting kudos into database.")
    db.insert()
    print("Finished inserting kudos.")

    print("Done one batch")


print("Done scraping and inserting kudos.")
'''
pass
