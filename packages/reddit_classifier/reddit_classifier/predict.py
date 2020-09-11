import numpy as np
import pandas as pd

from reddit_classifier.processing.data_management import load_pipeline
from reddit_classifier.config.base import config
from reddit_classifier.processing.validation import validate_inputs
from reddit_classifier import __version__ as _version

import logging
import typing as t

_logger = logging.getLogger(__name__)

pipeline_file_name = f"{config.app_config.pipeline_save_file}{_version}.pkl"
_svc_pipe = load_pipeline(file_name=pipeline_file_name)

def make_prediction(*, input_data: pd.DataFrame) -> dict:
    validated_data = validate_inputs(input_data=input_data)

    prediction = _svc_pipe.predict(validated_data[config.model_config.features])

    results = {'predictions': prediction, 'version': _version}

    _logger.info(
        f"Making predictions with model version: {_version} "
        f"Inputs: {validated_data} "
        f"Predictions: {results}"
    )

    return results