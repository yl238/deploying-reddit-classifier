from io import StringIO
import pandas as pd
import pytest


from reddit_svc_classifier.config.base import config
from reddit_svc_classifier.processing.data_management import load_dataset


@pytest.fixture(scope='session')
def raw_training_data():
    data = load_dataset(file_name=config.app_config.training_data_file) 
    return data

@pytest.fixture()
def uncleaned_dataset():
    TESTDATA = StringIO("""text\nYou are $3do2a\nAbced£\nhttps://gmail.com to be\nI've box""")
    df = pd.read_table(TESTDATA)
    return df

@pytest.fixture()
def mock_dataset():
    TESTDATA = StringIO("""title,body\nright_missing,\na1234,abcd\nhome 34,b 4\n,left_missing""")
    df = pd.read_table(TESTDATA, sep=',')
    print(df)
    return df