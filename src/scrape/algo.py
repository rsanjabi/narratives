"""
    algo.py - determines which fanworks or fandoms to scrape next
"""


class FanworksBatch():

    def __init__(self, batch_size: int = 500):
        self.batch_size = batch_size

    def compute(self):
        pass

    def next_batch(self):
        # returns a list of work_ids
        pass


class FandomBatch():
    def __init__(self):
        pass

    def compute(self):
        pass

    def next_batch(self):
        pass
