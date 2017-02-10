"""
REST API test suite - gluster volume
"""
import pytest

from usmqe.api.tendrlapi import tendrlapi
from usmqe.gluster import gluster


LOGGER = pytest.get_logger('volume_test', module=True)
"""@pylatest default
Setup
=====
"""

"""@pylatest default
Teardown
========
"""


# TODO create negative test case generator
# http://doc.pytest.org/en/latest/parametrize.html#basic-pytest-generate-tests-example
def test_create_volume_invalid(valid_cluster_id, invalid_volume_name, invalid_volume_bricks):
    """@pylatest api/gluster.create_volume_invalid
        API-gluster: create_volume
        ******************************

        .. test_metadata:: author fbalak@redhat.com

        Description
        ===========

        Get list of attributes needed to use in cluster volume creation with given cluster_id.

        .. test_step:: 1

                Connect to Tendrl API via POST request to ``APIURL/:cluster_id/GlusterCreateVolume``
                Where cluster_id is set to predefined value.

        .. test_result:: 1

                Server should return response in JSON format:

                Return code should be **202** with data ``{"message": "Accepted"}``.
                job should fail.
                """
    api = tendrlapi.ApiGluster()

    volume_data = {
        "Volume.volname": invalid_volume_name,
        "Volume.bricks": invalid_volume_bricks,
    }

    job_id = api.create_volume(valid_cluster_id, volume_data)["job_id"]
    # TODO check correctly server response or etcd job status
    api.wait_for_job_status(
            job_id,
            status="failed",
            issue="https://github.com/Tendrl/tendrl-api/issues/33")


def test_create_volume_valid(valid_cluster_id, valid_volume_name, valid_volume_bricks):
    """@pylatest api/gluster.create_volume_valid
        API-gluster: create_volume
        ******************************

        .. test_metadata:: author fbalak@redhat.com

        Description
        ===========

        Get list of attributes needed to use in cluster volume creation with given cluster_id.

        .. test_step:: 1

                Connect to Tendrl API via POST request to ``APIURL/:cluster_id/GlusterCreateVolume``
                Where cluster_id is set to predefined value.

        .. test_result:: 1

                Server should return response in JSON format:

                Return code should be **202** with data ``{"message": "Accepted"}``.
                job should finish.
                """
    api = tendrlapi.ApiGluster()

    volume_data = {
        "Volume.volname": valid_volume_name,
        "Volume.bricks": valid_volume_bricks
    }

    job_id = api.create_volume(valid_cluster_id, volume_data)["job_id"]
    api.wait_for_job_status(job_id)
    """@pylatest api/gluster.create_volume
        API-gluster: create_volume
        ******************************

        .. test_metadata:: author fbalak@redhat.com

        Description
        ===========

        Check if there is created volume on gluster nodes via CLI.

        .. test_step:: 2

            Connect to gluster node machine via ssh and run
            ``gluster volume info command``

        .. test_result:: 2

            There should be listed gluster volume named ``Vol_test``.

            """
    storage = gluster.GlusterCommon()
    storage.find_volume_name(valid_volume_name)

    volume_id = storage.get_volume_id(valid_volume_name)
    name = api.get_volume_list(valid_cluster_id)[0][volume_id]["name"]
    pytest.check(
        name == valid_volume_name,
        "Volume name on the machine is {}, should be {}".format(
            name, valid_volume_name))


def test_stop_volume_invalid(valid_cluster_id, invalid_volume_name):
    """@pylatest api/gluster.stop_volume_invalid
        API-gluster: stop_volume
        ******************************

        .. test_metadata:: author fbalak@redhat.com

        Description
        ===========

        Try to stop volume with given name and cluster id via API.

        .. test_step:: 1

                Connect to Tendrl API via POST request to ``APIURL/:cluster_id/GlusterStopVolume``
                Where cluster_id is set to predefined value.

        .. test_result:: 1

                Server should return response in JSON format:

                Return code should be **202** with data ``{"message": "Accepted"}``.
                Job should fail.
                """
    api = tendrlapi.ApiGluster()
    volume_data = {
        "Volume.volname": invalid_volume_name,
    }

    job_id = api.stop_volume(valid_cluster_id, volume_data)["job_id"]
    # TODO check correctly server response or etcd job status
    api.wait_for_job_status(
            job_id,
            status="failed",
            issue="https://github.com/Tendrl/tendrl-api/issues/33")


def test_stop_volume_valid(valid_cluster_id, valid_volume_name, valid_volume_id):
    """@pylatest api/gluster.stop_volume_valid
        API-gluster: stop_volume
        ******************************

        .. test_metadata:: author fbalak@redhat.com

        Description
        ===========

        Try to stop volume with given name and cluster id via API.

        .. test_step:: 1

                Connect to Tendrl API via POST request to ``APIURL/:cluster_id/GlusterStopVolume``
                Where cluster_id is set to predefined value.

        .. test_result:: 1

                Server should return response in JSON format:

                Return code should be **202** with data ``{"message": "Accepted"}``.
                job should finish.
                """
    api = tendrlapi.ApiGluster()
    volume_data = {
        "Volume.volname": valid_volume_name,
    }

    job_id = api.stop_volume(valid_cluster_id, volume_data)["job_id"]
    api.wait_for_job_status(job_id)
    test_gluster = gluster.GlusterCommon()
    test_gluster.check_status(valid_volume_name, "Stopped")
    status = api.get_volume_list(valid_cluster_id)[0][valid_volume_id]["status"]
    pytest.check(
        status == "Stopped",
        "Status from API is {}, should be 'Stopped'".format(status),
        issue="https://github.com/Tendrl/tendrl-api/issues/56")


# TODO create negative test case generator
# http://doc.pytest.org/en/latest/parametrize.html#basic-pytest-generate-tests-example
def test_start_volume_invalid(valid_cluster_id, invalid_volume_name):
    """@pylatest api/gluster.start_volume_invalid
        API-gluster: start_volume
        ******************************

        .. test_metadata:: author fbalak@redhat.com

        Description
        ===========

        Try to start volume with given name and cluster id via API.

        .. test_step:: 1

                Connect to Tendrl API via POST request to ``APIURL/:cluster_id/GlusterStartVolume``
                Where cluster_id is set to predefined value.

        .. test_result:: 1

                Server should return response in JSON format:

                Return code should be **202** with data ``{"message": "Accepted"}``.
                job should fail.
                """
    api = tendrlapi.ApiGluster()
    volume_data = {
        "Volume.volname": invalid_volume_name
    }

    job_id = api.start_volume(valid_cluster_id, volume_data)["job_id"]
    # TODO check correctly server response or etcd job status
    api.wait_for_job_status(
            job_id,
            status="failed",
            issue="https://github.com/Tendrl/tendrl-api/issues/33")


def test_start_volume_valid(valid_cluster_id, valid_volume_name, valid_volume_id):
    """@pylatest api/gluster.start_volume_valid
        API-gluster: start_volume
        ******************************

        .. test_metadata:: author fbalak@redhat.com

        Description
        ===========

        Try to start volume with given name and cluster id via API.

        .. test_step:: 1

                Connect to Tendrl API via POST request to ``APIURL/:cluster_id/GlusterStartVolume``
                Where cluster_id is set to predefined value.

        .. test_result:: 1

                Server should return response in JSON format:

                Return code should be **202** with data ``{"message": "Accepted"}``.
                job should finish.
                """
    api = tendrlapi.ApiGluster()
    volume_data = {
        "Volume.volname": valid_volume_name,
    }

    job_id = api.start_volume(valid_cluster_id, volume_data)["job_id"]
    api.wait_for_job_status(job_id)
    test_gluster = gluster.GlusterCommon()
    test_gluster.check_status(valid_volume_name, "Started")
    status = api.get_volume_list(valid_cluster_id)[0][valid_volume_id]["status"]
    pytest.check(
        status == "Started",
        "Status from API is {}, should be 'Started'".format(status),
        issue="https://github.com/Tendrl/tendrl-api/issues/55")


def test_delete_volume_invalid(valid_cluster_id, invalid_volume_id):
    """@pylatest api/gluster.delete_volume
        API-gluster: delete_volume
        ******************************

        .. test_metadata:: author fbalak@redhat.com

        Description
        ===========

        Delete gluster volume ``Vol_test`` via API.

        .. test_step:: 1

                Connect to Tendrl API via POST request to ``APIURL/:cluster_id/GlusterDeleteVolume``
                Where cluster_id is set to predefined value.

        .. test_result:: 1

                Server should return response in JSON format:

                Return code should be **202** with data ``{"message": "Accepted"}``.
                job should fail.
                """
    api = tendrlapi.ApiGluster()
    volume_data = {
        "Volume.volname": valid_cluster_id,
        "Volume.vol_id": invalid_volume_id
    }

    job_id = api.delete_volume(valid_cluster_id, volume_data)["job_id"]
    # TODO check correctly server response or etcd job status
    api.wait_for_job_status(
            job_id,
            status="failed",
            issue="https://github.com/Tendrl/tendrl-api/issues/33")


def test_delete_volume_valid(valid_cluster_id, valid_volume_name, valid_volume_id):
    """@pylatest api/gluster.delete_volume
        API-gluster: delete_volume
        ******************************

        .. test_metadata:: author fbalak@redhat.com

        Description
        ===========

        Delete gluster volume ``Vol_test`` via API.

        .. test_step:: 1

                Connect to Tendrl API via POST request to ``APIURL/:cluster_id/GlusterDeleteVolume``
                Where cluster_id is set to predefined value.

        .. test_result:: 1

                Server should return response in JSON format:

                Return code should be **202** with data ``{"message": "Accepted"}``.
                job should finish.
                """
    api = tendrlapi.ApiGluster()
    volume_data = {
        "Volume.volname": valid_volume_name,
        "Volume.vol_id": valid_volume_id
    }

    job_id = api.delete_volume(valid_cluster_id, volume_data)["job_id"]
    api.wait_for_job_status(job_id, issue="https://github.com/Tendrl/api/issues/33")
    """@pylatest api/gluster.create_volume
        API-gluster: create_volume
        ******************************

        .. test_metadata:: author fbalak@redhat.com

        Description
        ===========

        Check if there is created volume on gluster nodes via CLI.

        .. test_step:: 1

            Connect to gluster node machine via ssh and run
            ``gluster volume info command``

        .. test_result:: 1

            There should be listed gluster volume named ``Vol_test``.

            """
    test_gluster = gluster.GlusterCommon()
    test_gluster.find_volume_name(valid_volume_name, False)
    # There should be either deleted attribute or record should be removed from database
    # https://github.com/Tendrl/api/issues/78
    #
    # deleted = api.get_volume_list(valid_cluster_id)[0][valid_volume_id]["deleted"]
    # pytest.check(
    #     deleted == "True",
    #     "deleted attribute should be True, is {}".format(deleted),
    #     issue="https://github.com/Tendrl/tendrl-api/issues/33")
