# -*- coding: utf8 -*-
"""
REST API test suite - user
"""
import pytest

import json

from usmqe.api.tendrlapi import user as tendrlapi_user


"""@pylatest default
Setup
=====

Prepare USM cluster accordingly to documentation.

Further mentioned ``APIURL`` points to: ``http://USMSERVER/api/1.0``.
"""

"""@pylatest default
Teardown
========
"""


def test_user_get():
    """@pylatest api/user.get
    API-users: get user
    *******************

    .. test_metadata:: author mkudlej@redhat.com dahorak@redhat.com fbalak@redhat.com

    Description
    ===========

    Get user admin.
    """
    test = tendrlapi_user.ApiUser()
    """@pylatest api/user.get
    .. test_step:: 1
       :include: api/user.login_valid:1

    .. test_result:: 1
       :include: api/user.login_valid:1
    """
    test.login(pytest.config.getini("usm_username"),
               pytest.config.getini("usm_password"))
    """@pylatest api/user.get
    .. test_step:: 2

        Send **GET** request to ``APIURL/users``.

    .. test_result:: 2

        List of users in database is returned
    """
    test.users
    """@pylatest api/user.get
    .. test_step:: 3

        Get user info.

        Send **GET** request to ``APIURL/users/admin``.

    .. test_result:: 3

        User information for user *admin* is returned.
    """
    test.user('admin')
    test.logout()


def test_user_get_not_found(invalid_user, not_found_response):
    """@pylatest api/user.get_nonexistent
    API-users: get nonexistent user
    *******************************

    .. test_metadata:: author dahorak@redhat.com fbalak@redhat.com

    Description
    ===========

    Get users.
    """
    test = tendrlapi_user.ApiUser()
    """@pylatest api/user.get_nonexistent
    .. test_step:: 1
       :include: api/user.login_valid:1

    .. test_result:: 1
       :include: api/user.login_valid:1
    """
    test.login(pytest.config.getini("usm_username"),
               pytest.config.getini("usm_password"))

    """@pylatest api/user.get_nonexistent
    .. test_step:: 2

        Try to get information for non existent user.

        For each user, send GET request to ``APIURL/user/USER``

    .. test_result:: 2

        It should return error about unknown user.
    """
     test.user(user, asserts_in=not_found_response)

    test.logout()


def test_user_add_del(valid_user_data, not_found_response):
    """@pylatest api/user.add_delete
    API-users: add and delete
    *************************

    .. test_metadata:: author mkudlej@redhat.com dahorak@redhat.com

    Description
    ===========

    Add and remove *test* user.
    """
    test = tendrlapi_user.ApiUser()
    """@pylatest api/user.add_delete
    .. test_step:: 1
       :include: api/user.login_valid:1

    .. test_result:: 1
       :include: api/user.login_valid:1
    """
    test.login(pytest.config.getini("usm_username"),
               pytest.config.getini("usm_password"))
    """@pylatest api/user.add_delete
    .. test_step:: 2

        Add user test2.

        Send **PUT** request to ``APIURL/users/test2`` with data::

            {
              "username":"test2",
              "email":"test2@localhost",
              "role":"admin",
              "groups":[]
            }

    .. test_result:: 2

        User should be created.

        Return code should be (FIXME: 201, 202)**???** (current 200).
    """
    # add test user
    test.users_add(valid_user_data)
    """@pylatest api/user.add_delete
    .. test_step:: 3
       :include: api/user.get:2

    .. test_result:: 3
       :include: api/user.get:2
    """
    test.user(valid_user_data["username"])
    """@pylatest api/user.add_delete
    .. test_step:: 4

        Delete user test2.

        Send **DELETE** request to ``APIURL/users/test2``.

    .. test_result:: 4

        User test2 should be deleted.

        Return code should be (FIXME: 201, 202)**???** (current 200).
    """
    test.user_del(valid_user_data["username"])
    """@pylatest api/user.add_delete
    .. test_step:: 5
       :include: api/user.get:2

    .. test_result:: 5

        User test2 is not available.

        Return code should be (FIXME: 4xx)**???** (current 500) with data::

            {"Error": "can't find user"}
    """
    test.user(valid_user_data["username"], not_found_response)
    """@pylatest api/user.add_delete
    .. test_step:: 6
       :include: api/user.logout:3

    .. test_result:: 6
       :include: api/user.logout:3
    """
    test.logout()