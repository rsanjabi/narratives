from datetime import datetime
from typing import Optional
from pathvalidate import replace_symbol
from pathlib import Path
import config as cfg


def oldest_kudo_path() -> Optional[Path]:
    try:
        p = Path() / cfg.KUDO_PATH
        oldest = sorted(p.glob('*.json'), key=lambda x: x.stat().st_ctime)[0]
        return oldest
    except IndexError:
        return None


def remove_kudo_path(path: Path):
    path.unlink()


def kudo_log_path() -> Path:
    path = Path() / cfg.KUDO_PATH
    if not path.exists():
        path.mkdir(parents=True)
    return path.joinpath('kudos' + cfg.LOG_SUFFIX)


def kudo_path(batch: str) -> Path:
    path = Path() / cfg.KUDO_PATH
    if not path.exists():
        path.mkdir(parents=True)
    return path.joinpath(batch + cfg.DATA_SUFFIX)


def works_to_delete() -> Path:
    path = Path() / cfg.DATA_PATH
    if not path.exists():
        path.mkdir(parents=True)
    return path.joinpath(cfg.TBD_PREFIX + cfg.TXT_SUFFIX)


def fandom_log_path() -> Path:
    path = Path() / cfg.FANDOM_PATH
    if not path.exists():
        path.mkdir(parents=True)
    return path.joinpath('fandoms' + cfg.LOG_SUFFIX)


def fandom_path() -> Path:
    path = Path() / cfg.FANDOM_PATH
    if not path.exists():
        path.mkdir(parents=True)
    date = datetime.now().strftime("%d%b%Y")
    return path.joinpath(date + cfg.DATA_SUFFIX)


def tag_path(tag: str) -> Path:
    tag_dir = replace_symbol(tag)
    path = Path() / cfg.META_PATH / tag_dir
    if not path.exists():
        path.mkdir(parents=True)
    return path


def meta_path(tag: str) -> Path:
    path = tag_path(tag)
    return path.joinpath(cfg.META_PREFIX + cfg.DATA_SUFFIX)


def meta_log_path(tag: str) -> Path:
    path = tag_path(tag)
    return path.joinpath(cfg.META_PREFIX + cfg.LOG_SUFFIX)


def matrix_log_path() -> Path:
    path = Path() / cfg.basedir / cfg.MODEL_PATH
    if not path.exists():
        path.mkdir(parents=True)
    file_path = path.joinpath(cfg.MODEL_PREFIX + cfg.LOG_SUFFIX)
    return file_path


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
