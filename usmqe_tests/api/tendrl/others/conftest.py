import pytest

@pytest.fixture(params=[
    {"name":"Tom Hardy",
    "username":"thardy",
    "email":"thardy@tendrl.org",
    "role":"admin",
    "password":"pass1234",
    "password_confirmation":"pass1234"}])
def valid_user_import(request):
    """Generate valid data that can be imported into tendrl as a new user.

    ``params`` parameter takes list of dictionaries where each dictionary
        contains ``username`` and ``password`` as keys.
    """

    return request.param
