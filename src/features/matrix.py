#!/usr/bin/env python3
'''
    Matrx.py takes fandom names and creates a sparse matrix of users who have
    given a fanwork kudos.

    Then trains a model using a Bayesian Personalized Ranking algorithm for
    implicit recommendations.

    Finally the model and lookup indices are saved as pkl objects (that can be
    then be pulled for the microservice to run inference on.)

    TODO:
        * Automate reading in all fanworks (vs. hardcoding)
        * add code to generate date sensitive models (place in sequential
            folders?)
'''

import pickle
from typing import List, Tuple, Dict, Any
from pathlib import Path

import logging
from logging import Logger

import numpy as np
import scipy.sparse as sp
import pandas as pd
from pandas import DataFrame
from implicit.bpr import BayesianPersonalizedRanking as bpr_rec

import utils.paths as paths
from db.ao3_db import AO3DB     # type: ignore
import config as cfg


def create_logger() -> Logger:
    # Logger
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)
    fh = logging.FileHandler(paths.model_log_path(), mode='w')
    formatter = logging.Formatter('%(asctime)s-%(levelname)s-%(message)s')
    fh.setFormatter(formatter)
    logger.addHandler(fh)
    return logger


def create_path_list() -> Tuple[List[Path], List[Path]]:
    # Create paths for each fandom

    cfg.TEST_FANDOM_LIST
    kudo_files = []
    meta_files = []

    for fandom in cfg.TEST_FANDOM_LIST:
        kudo_files.append(paths.kudo_path(fandom))
        meta_files.append(paths.meta_path(fandom))

    return kudo_files, meta_files


def create_megaframe(kudo_files: List[Path]) -> DataFrame:
    # Create mega dataframe

    frames = []
    for path in kudo_files:
        frames.append(pd.read_csv(path))
    df = pd.concat(frames)
    return df


def create_empty_df(df: DataFrame) -> np.ndarray:
    # Determine unique work and user sizes to make emtpy DF
    num_works = len(df['work_id'].unique())
    num_users = len(df['kudo_givers'].unique())
    # TODO add size to log
    data = np.zeros((num_works, num_users))
    return data


def invert_indices(indices: Dict[str, Any]) -> Dict[str, Any]:
    # create inverted indices for reverse lookup
    inverted_indices: Dict[str, Any] = {'work_id': {}, 'user': {}}
    inverted_indices['work_id'] = {v: k for k, v in indices['work_id'].items()}
    inverted_indices['user'] = {v: k for k, v in indices['user'].items()}

    return inverted_indices


def create_sparse_matrix(data: np.ndarray,
                         kudo_df) -> Tuple[np.ndarray, Dict[Any, Any]]:
    # create indices for work_id and users
    indices: Dict[str, Any] = {'work_id': {}, 'user': {}}

    # then go through each line of csv files for values to set to 1
    for _, row in kudo_df.iterrows():
        indices['work_id'].setdefault(row['work_id'], len(indices['work_id']))
        indices['user'].setdefault(row['kudo_givers'], len(indices['user']))
        data[indices['work_id'][row['work_id']]][indices['user'][row['kudo_givers']]] = 1   # noqa: E501
    return data, indices


def test_predictions(indices: Dict[Any, Any],
                     inverted_indices: Dict[Any, Any],
                     id: int) -> None:
    work_indice = indices['work_id'][id]
    num_to_return = 20

    # find related items
    related_BPR = modelBPR.similar_items(work_indice, num_to_return)
    for suggestion in related_BPR:
        work_id = inverted_indices['work_id'][suggestion[0]]
        print(f"http://www.archiveofourown.org/works/{work_id}")


def store_data(model: bpr_rec,
               indices: Dict[Any, Any],
               meta_df: DataFrame) -> None:
    # Write out model and indices dictionary as pkl files
    # Write out lookup_table/meta_df as csv file
    # All three will be used for infererncing

    with open(paths.pickle_path(), 'wb') as m_out:
        pickle.dump(model, m_out)

    with open(paths.inidices_path(), 'wb') as i_out:
        pickle.dump(indices, i_out)

    smaller_df = meta_df[['work_id', 'title', 'author', 'rating']]
    smaller_df.to_csv(paths.lookup_table_path(), index=False)

    return


if __name__ == "__main__":
    logger = create_logger()
    # kudo_list, meta_list = create_path_list()

    db = AO3DB('george', paths.matrix_log_path())
    kudo_df = db.kudo_matrix()
    # kudo_df = create_megaframe(kudo_list)
    # meta_df = create_megaframe(meta_list)
    meta_df = DataFrame()

    logger.info("Reading in kudos.")
    print("Reading in kudos.")
    empty_df = create_empty_df(kudo_df)

    logger.info("Creating empty matrix.")
    print("Creating empty matrix.")
    data, indices = create_sparse_matrix(empty_df, kudo_df)
    logger.info(f" completed size: {data.shape}")
    print(f"completed size: {data.shape}")

    # train the model on a sparse matrix of item/user/confidence weights
    logger.info("Training model")
    print("Training model")
    modelBPR = bpr_rec(factors=50, verify_negative_samples=True)
    modelBPR.fit(sp.csr_matrix(data))

    # test_predictions(indices, invert_indices(indices), '13484820')

    logger.info("Storing model for late inference.")
    print("Storing model for late inference.")
    store_data(modelBPR, indices, meta_df)

    logger.info("Model building and features engineering complete.")
    print("Model building and features engineering complete.")
