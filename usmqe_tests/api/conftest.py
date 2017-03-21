import pytest

import json


@pytest.fixture
def not_found_response():
    """Generate asserts for ``404 Not found`` response."""

    return {
        "json": json.loads('{"Error": "Not found"}'),
        "cookies": None,
        "ok": False,
        "reason": 'Not Found',
        "status": 404}


@pytest.fixture
def unauthorized_response():
    """Generate asserts for ``401 Unauthorized`` response."""

    return {
        "json": json.loads('{"Error": "Unauthorized"}'),
        "cookies": None,
        "ok": False,
        "reason": 'Unauthorized',
        "status": 401}
