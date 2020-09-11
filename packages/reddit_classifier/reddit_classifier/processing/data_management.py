import pandas as pd

from reddit_classifier.config.base import config, DATASET_DIR, TRAINED_MODEL_DIR

def load_dataset(file_name=None):
    data = pd.read_csv(f"{DATASET_DIR}/{file_name}")
    return data


def save_pipeline():
    pass