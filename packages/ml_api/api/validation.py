from marshmallow import Schema, fields
from marshmallow import ValidationError

import typing as t
import json


class InvalidInputError(Exception):
    """Invalid model input."""


class RedditPostschema(Schema):
    title = fields.Str(allow_none=True)
    score = fields.Integer()
    num_comments = fields.Integer()
    created_at = fields.Str()
    body = fields.Str(allow_none=True)
    url = fields.Str()


def _filter_error_rows(errors: dict,
                       validated_input: t.List[dict]) -> t.List[dict]:
    """Remove input data rows with errors."""
    indexes = errors.keys()
    for index in sorted(indexes, reverse=True):
        del validated_input[index]
    return validated_input


def validate_inputs(input_data):
    """Check prediction inputs against schema"""
    schema = RedditPostschema(many=True)

    errors = {}
    try:
        schema.load(input_data)
    except ValidationError as exc:
        errors = exc.messages

    if errors:
        validate_input = _filter_error_rows(errors=errors,
                                            validated_input=input_data)
    else:
        validate_input = input_data
    return validate_input, errors