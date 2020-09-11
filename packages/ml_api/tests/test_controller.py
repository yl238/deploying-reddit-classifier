from reddit_classifier.config.base import config
from reddit_classifier.processing.data_management import load_dataset
from reddit_classifier import __version__ as _version

import json

from api import __version__ as api_version


def test_health_endpoint_returns_200(flask_test_client):
    # When
    response = flask_test_client.get('/health')

    # Then
    assert response.status_code == 200


def test_version_endpoint_returns_version(flask_test_client):
    response = flask_test_client.get('/version')

    assert response.status_code == 200
    response_json = json.loads(response.data)
    assert response_json['model_version'] == _version
    assert response_json['api_version'] == api_version


def test_prediction_endpoint_returns_prediction(flask_test_client):
    test_data = load_dataset(file_name=config.app_config.test_data_file)

    post_json = test_data[0:1].to_json(orient='records')

    response = flask_test_client.post('/v1/predict/classification', json=json.loads(post_json))

    assert response.status_code == 200
    response_json = json.loads(response.data)
    prediction = response_json['predictions']
    response_version = response_json['version']
    assert prediction == ['live convo']
    assert response_version == _version
