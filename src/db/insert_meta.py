# from typing import List
# import logging
# from logging import Logger
# from pathlib import Path
# import csv
# import utils.paths as paths
import config as cfg
# from scrape.progress import Progress

import sys
import psycopg2
# from psycopg2 import connect, sql
from db.ao3_db import AO3DB


class Meta(AO3DB):

    def __init__(self, fandom: str):
        super().__init__(fandom)
        # check for existence of tables, creating if necessary

    def open(self):
        ''' Open database connection. Returns cursor and connection '''
        try:
            print("Opening connection...")
            connect = psycopg2.connect(
                            host=cfg.HOST,
                            database=cfg.DATABASE,
                            user=cfg.USER,
                            password=cfg.PASSWORD,
            )
            cur = connect.cursor()

            # Set search path to look for 'one_most_recent' schema
            # cur.execute("SET search_path TO one_most_recent,public;")
            # connect.commit()

            print(f"SUCCESS")

        except Exception as e:
            print("There was an error connecting to the database: ", e)
            sys.exit()

        return cur, connect

    def close(self):
        self.cursor.close()
        self.connect.close()
        print(f"Connection closed.")

    def insert_from_csv(self):
        pass

    def insert_str(self):
        pass

    def table_creation(self):
        pass
