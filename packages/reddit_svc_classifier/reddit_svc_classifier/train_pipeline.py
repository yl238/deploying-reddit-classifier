from sklearn.model_selection import train_test_split

from reddit_svc_classifier.processing import preprocessor as pp
from reddit_svc_classifier.processing.data_management import (
    load_dataset,
    save_pipeline,
)
from reddit_svc_classifier.processing.model_evaluation import eval_metrics
from reddit_svc_classifier.pipeline import svc_pipeline
from reddit_svc_classifier.config.base import config
from sklearn.svm import LinearSVC

def run_training():
    # load dataset
    data = load_dataset(config.app_config.training_data_file) 

    # split train and test
    train_df, test_df = train_test_split(data, 
            stratify=data[config.model_config.target], 
            **config.model_config.split_params)
    
    downsampler = pp.MajorityClassDownsampler(**config.model_config.downsample_params)
    train_downsampled = downsampler.transform(train_df)

    X_train = train_downsampled[config.model_config.features]
    y_train = train_downsampled[config.model_config.target]

    svc_pipeline.fit(X_train, y_train)
    #save_pipeline()

    X_test = test_df[config.model_config.features]
    y_test = test_df[config.model_config.target]
    y_pred = svc_pipeline.predict(X_test)

    print(eval_metrics(y_test, y_pred))

    
if __name__ == '__main__':
    run_training()