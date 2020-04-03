#!/usr/bin/env python

import scrape.ao3_get_meta as meta
#import src.scrape.ao3_get_kudos as kudos
import config as cfg

meta.scrape(cfg.TEST_FANDOM, 'meta.csv', cfg.HEADERS, '', False)
