"""
tendrl REST API.
"""

import requests

import pytest

import json

from usmqe.api.tendrlapi.common import TendrlApi

LOGGER = pytest.get_logger("tendrlapi.user", module=True)


class ApiUser(TendrlApi):
    """ Main class for interact with REST API - user."""

    def users(self, credentials, asserts_in=None):
        """ Get users.

        Name:        "GET_users",
        Method:      "GET",
        Pattern:     "users",

        Args:
            asserts_in: assert values for this call and this method
        """
        pattern = "users"
        request = requests.get(pytest.config.getini("usm_api_url") + pattern,
            headers = {"Authorization": "Bearer {}".format(credentials["access_token"])})
        self.print_req_info(request)
        self.check_response(request, asserts_in)
        if request.ok:
            defined_keys = {
                "email",
                "username",
                "name",
                "role"}
            for item in request.json(encoding='unicode'):
                user = item["username"]
                pytest.check(
                    item.keys() == defined_keys,
                    "User {0} should contain: {1}\n\tUser {0} contains: {2}"
                    .format(user, defined_keys, item.keys))
            return request.json(encoding='unicode')

    def user_edit(self, username, data, credentials, asserts_in=None):
        """ Edit a single user

        Args:
            username: name of user that is going to be updated
            data: dictionary data about user
                  have to contain: email, username, name, role
            asserts_in: assert values for this call and this method
        """
        pattern = "users/{}".format(username)
        request = requests.put(pytest.config.getini("usm_api_url") + pattern,
            json.dumps(data),
            headers = {"Authorization": "Bearer {}".format(credentials["access_token"])})
        self.print_req_info(request)
        self.check_response(request, asserts_in)
# TODO check json comparision
        return request.json(encoding='unicode')

    def user_add(self, user_in, credentials, asserts_in=None):
        """ Add user throught **users**.

        Name:        "POST_users",
        Method:      "POST",
        Pattern:     "users",

        Args:
            user_in: dictionary info about user
                     have to contain: name, username, email, role, password, password_confirmation
            asserts_in: assert values for this call and this method
        """
        pattern = "users"
        request = requests.post(pytest.config.getini("usm_api_url") + pattern,
            data=json.dumps(user_in),
            headers={"Authorization": "Bearer {}".format(credentials["access_token"])})
        self.print_req_info(request)
        self.check_response(request, asserts_in)
        user_in.pop("password", None)
        user_in.pop("password_confirmation", None)
        stored_user = self.user(user_in["username"], credentials)
        pytest.check(
            user_in == stored_user,
            "Information sent: {}, information stored in database: {}, These should match"
            .format(user_in, stored_user))
        return stored_user

    def user(self, username, credentials, asserts_in=None):
        """ Get user info..

        Name:        "GET_user",
        Method:      "GET",
        Pattern:     "users/{username}",

        Args:
            username: name of user stored in database
            asserts_in: assert values for this call and this method
        """
        pattern = "users/{}".format(username)
        request = requests.get(
            pytest.config.getini("usm_api_url") + pattern,
            headers = {"Authorization": "Bearer {}".format(credentials["access_token"])})
        self.print_req_info(request)
        self.check_response(request, asserts_in)

        defined_keys = {
            "email",
            "username",
            "name",
            "role"}
        stored_keys = request.json().keys()
        pytest.check(
            defined_keys == stored_keys,
            "Json of added user should contain: {0}\n\tIt contains: {1}"
            .format(defined_keys, stored_keys))
        return request.json(encoding='unicode')

    def user_del(self, username, credentials, asserts_in=None):
        """ Delete user.

        Name:        "DELETE_users",
        Method:      "DELETE",
        Pattern:     "users/{username}",

        Args:
            username: name of user that is going to be deleted
            asserts_in: assert values for this call and this method
        """
        pattern = "users/{}".format(username)
        request = requests.delete(
            pytest.config.getini("usm_api_url") + pattern,
            headers = {"Authorization": "Bearer {}".format(credentials["access_token"])})
        self.print_req_info(request)
        self.check_response(request, asserts_in)
