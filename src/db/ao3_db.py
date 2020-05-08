from abc import ABC, abstractmethod
# from typing import List
# import csv
import os
import sys

import logging
from logging import Logger
from pathlib import Path
import psycopg2
# from psycopg2 import connect, sql

import config as cfg
# import utils.paths as paths
# from scrape.progress import Progress


class AO3DB(ABC):

    def __init__(self, page_kind: str, log_path: Path, type: str):
        self.page_kind = page_kind      # fandom or media kind
        self.type = type
        self.log_path = log_path
        self.cursor, self.connect = self.open()
        self.logger = self._init_log()
        self._table_creation()

    def open(self):
        ''' Open database connection. Returns cursor and connection '''
        try:
            print("Opening connection...")
            connect = psycopg2.connect(
                            host=cfg.HOST,
                            database=os.environ['DB_NAME'],
                            user=os.environ['DB_USER'],
                            password=os.environ['DB_PASS'],
            )
            cur = connect.cursor()

        except Exception as e:
            print("There was an error connecting to the database: ", e)
            sys.exit()

        return cur, connect

    def close(self):
        self.cursor.close()
        self.connect.close()
        print(f"Connection closed.")

    @abstractmethod
    def insert(self):
        pass

    @abstractmethod
    def _table_creation(self):
        pass

    def _init_log(self) -> Logger:
        logger = logging.getLogger(self.page_kind+self.type)
        logger.setLevel(logging.DEBUG)
        fh = logging.FileHandler(self.log_path, mode='a')
        formatter = logging.Formatter('%(asctime)s-%(levelname)s-%(message)s')
        fh.setFormatter(formatter)
        logger.addHandler(fh)
        logger.info("********************************")

        return logger
