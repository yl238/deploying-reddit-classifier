import json

from reddit_classifier.config.base import config
from reddit_classifier.processing.data_management import load_dataset

def test_prediction_endpoint_validation_200(flask_test_client):

    test_data = load_dataset(file_name=config.app_config.test_data_file)
    post_json = test_data.to_json(orient='records')

    response = flask_test_client.post('/v1/predict/classification',
                json=json.loads(post_json))

    assert response.status_code == 200
    response_json = json.loads(response.data)

    # Check correct number of errors removed
    assert len(response_json.get('predictions')) + len(response_json.get('errors')) == len(test_data)