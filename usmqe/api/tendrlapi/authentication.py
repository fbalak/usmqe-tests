"""
Tendrl REST API.
"""

import requests

import pytest

import json

from usmqe.api.tendrlapi.common import TendrlApi

LOGGER = pytest.get_logger("tendrlapi.authentication", module=True)


class Authentication(TendrlApi):
    """ Main class for interact with REST API - authentication."""

    def __init__(self):
        self.username = None
        self.access_token = None

    def login(self, username, password, asserts_in=None):
        """ Login user.

        Name:        "login",
        Method:      "GET",
        Pattern:     "login",

        Args:
            username: name of user that is going logged in
            password: password for username
            asserts_in: assert values for this call and this method
        """
        pattern = "login"
        post_data = {"username": username, "password": password}
        request = requests.post(
            pytest.config.getini("usm_api_url") + pattern, data=json.dumps(post_data))
        self.print_req_info(request)
        self.check_response(request, asserts_in)
        self.username = username
        self.role = "admin"
        LOGGER.debug("access_token:  {}".format(request.json()))
        self.access_token = request.json()["access_token"]

    def logout(self, asserts_in=None):
        """ Logout user.

        Name:        "logout",
        Method:      "DELETE",
        Pattern:     "logout",

        Args:
            asserts_in: assert values for this call and this method
        """
        pattern = "logout"
        request = requests.delete(
            pytest.config.getini("usm_api_url") + pattern)
        self.print_req_info(request)
        self.check_response(request, asserts_in)
