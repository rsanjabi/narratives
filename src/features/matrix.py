#!/usr/bin/env python3

import numpy as np
# import scipy.sparse as sp
import pandas as pd
# from sklearn.preprocessing import MultiLabelBinarizer
import utils.paths
import config as cfg
import sys

print(f"sys.path: {sys.path}")

path = utils.paths.kudo_file(cfg.TEST_FANDOM)
print(f"DEBUG: path: {path}")
df = pd.read_csv(path)
num_works = len(df['work_id'].unique())
num_users = len(df['user'].unique())
data = np.zeros((num_works, num_users))
print(f"{path}")
