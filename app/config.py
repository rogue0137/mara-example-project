"""Project specific configurations"""

import pathlib
import datetime

from mara_config import declare_config

@declare_config()
def data_dir():
    """The directory where persistent input data is stored"""
    return pathlib.Path('./data')


@declare_config()
def first_date():
    """The first date for which downloading and integrating BigQuery data"""
    return datetime.date(2017, 1, 1)
