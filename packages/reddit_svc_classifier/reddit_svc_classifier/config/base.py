import pathlib

import reddit_svc_classifier

PACKAGE_ROOT = pathlib.Path(reddit_svc_classifier.__file__).resolve().parent
TRAINED_MODEL_DIR = PACKAGE_ROOT / "trained_models"
DATASET_DIR = PACKAGE_ROOT / "datasets"


class AppConfig(object):
    """
    Application-level config.
    """
    package_name = 'reddit_svc_classifier'
    pipeline_name = 'svc'
    pipeline_save_file = f"{pipeline_name}_output_v"
    training_data_file = "tokenized_text.csv"
    

class ModelConfig(object):
    """Model level config.
    """
    features = ['title', 'body']
    text_field = 'text'
    target = 'label'
    valid_labels =  [
        'live convo', 
        'bad test', 
        'mobile', 
        'other', 
        'screeners',
        'recorder', 
        'ratings', 
        'bug', 
        'payment', 
        'no test',
        'other company'
        ]
    # stopwords
    stopword_exceptions = ["whatever", "whenever", "about", "nothing", 
                       "empty", "none", "more", "somewhere", 
                       "most", "not", "never"]
    
    # Downsampling majority class
    downsample_params = {
        'target': 'label',
        'majority_class': 'other',
        'sample_fraction': 0.4
    }
    # default train/test split
    split_params = {
        'test_size': 0.2,
        'random_state': 42
    }
    vectorizer_params = {
        'ngram_range': (1, 2),
        'analyzer': 'word',
        'max_features': 1500   
    }
    model_params = {
        'C': 0.01, # SVC
        'random_state': 42,
        'class_weight': 'balanced'
    }

class Config(object):
    app_config = AppConfig()
    model_config = ModelConfig()

config = Config()