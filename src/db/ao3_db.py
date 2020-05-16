from abc import ABC, abstractmethod
from typing import Generator, Any
import os
import sys
import json

import logging
from logging import Logger
from pathlib import Path
import psycopg2
import config as cfg


class AO3DB(ABC):

    def __init__(self, page_kind: str,
                 data_path: Path,
                 log_path: Path,
                 type: str):
        self.page_kind = page_kind      # fandom or media kind
        self.type = type
        self.data_path = data_path
        self.log_path = log_path
        self.cursor, self.connect = self.open()
        self.logger = self._init_log()
        self._table_creation()

    def open(self):
        ''' Open database connection. Returns cursor and connection '''
        try:
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
        print("Connection closed.")

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

    def _rows(self) -> Generator[Any, None, None]:
        with open(self.data_path, 'r') as f_in:
            for row in f_in:
                yield json.loads(row)

    def _fanwork_exists(self, work_id: str) -> bool:
        cur = self.connect.cursor()
        sql = "SELECT EXISTS (SELECT 1 FROM staging_meta WHERE work_id = %s);"
        cur.execute(sql, (work_id,))
        return cur.fetchone()[0]
