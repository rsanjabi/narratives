from pathvalidate import replace_symbol
from pathlib import Path
import config as cfg


def fandom_path(fandom: str) -> Path:
    fandom_dir = replace_symbol(fandom)
    path = Path() / cfg.DATA_PATH / fandom_dir
    if not path.exists():
        path.mkdir(parents=True)
    return path


def kudo_log_path(fandom: str) -> object:

    fandom_dir = replace_symbol(fandom)
    path = Path() / cfg.DATA_PATH / fandom_dir
    if not path.exists():
        path.mkdir(parents=True)
    return path.joinpath(cfg.KUDO_PREFIX + cfg.LOG_SUFFIX)


def kudo_path(fandom: str) -> Path:
    fandom_dir = replace_symbol(fandom)
    path = Path() / cfg.DATA_PATH / fandom_dir
    if not path.exists():
        path.mkdir(parents=True)
    return path.joinpath(cfg.KUDO_PREFIX + cfg.DATA_SUFFIX)


def meta_path(fandom: str) -> Path:
    fandom_dir = replace_symbol(fandom)
    path = Path() / cfg.DATA_PATH / fandom_dir
    if not path.exists():
        path.mkdir(parents=True)
    return path.joinpath(cfg.META_PREFIX + cfg.DATA_SUFFIX)


def meta_log_path(fandom: str) -> Path:
    fandom_dir = replace_symbol(fandom)
    path = Path() / cfg.DATA_PATH / fandom_dir
    if not path.exists():
        path.mkdir(parents=True)
    return path.joinpath(cfg.META_PREFIX + cfg.LOG_SUFFIX)


def matrix_log_path() -> Path:
    path = Path() / cfg.DATA_PATH
    if not path.exists():
        path.mkdir(parents=True)
    return path.joinpath(cfg.META_PREFIX + cfg.LOG_SUFFIX)


def model_log_path() -> Path:
    path = Path() / cfg.MODEL_PATH
    if not path.exists():
        path.mkdir(parents=True)
    return path.joinpath(cfg.MODEL_PREFIX+cfg.LOG_SUFFIX)


def pickle_path() -> Path:
    path = Path() / cfg.MODEL_PATH
    if not path.exists():
        path.mkdir(parents=True)
    return path.joinpath(cfg.MODEL_PREFIX+cfg.PICKLE_SUFFIX)


def inidices_path() -> Path:
    path = Path() / cfg.MODEL_PATH
    if not path.exists():
        path.mkdir(parents=True)
    return path.joinpath(cfg.INDICES_PREFIX+cfg.PICKLE_SUFFIX)


def lookup_table_path() -> Path:
    path = Path() / cfg.MODEL_PATH
    if not path.exists():
        path.mkdir(parents=True)
    return path.joinpath(cfg.META_PREFIX+cfg.DATA_SUFFIX)
