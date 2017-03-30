"""
Tendrl REST API.
"""

import requests
import pytest
from usmqe.api.tendrlapi.common import TendrlApi

LOGGER = pytest.get_logger("glusterapi", module=True)


class TendrlApiGluster(TendrlApi):
    """ Gluster methods for Tendrl REST API.
    """

    def get_nodes(self, auth):
        """ Get list node ids.

        Name:        "get_nodes",
        Method:      "GET",
        Pattern:     "GetNodeList",
        """
        pattern = "GetNodeList"
        response = requests.get(
            pytest.config.getini("usm_api_url") + pattern,
            auth=auth)
        self.print_req_info(response)
        self.check_response(response)
        return response.json()

    def import_cluster(self, cluster_data, auth):
        """ Import gluster cluster defined by json.

        Name:        "import_cluster",
        Method:      "POST",
        Pattern:     "GlusterImportCluster",

        Args:
            cluster_data: json structure containing data that will be sent to api server
        """
        pattern = "ImportCluster"
        response = requests.post(
            pytest.config.getini("usm_api_url") + pattern,
            json=cluster_data,
            auth=auth)
        asserts = {
            "reason": 'Accepted',
            "status": 202,
        }
        self.print_req_info(response)
        self.check_response(response, asserts)
        return response.json()

    def get_cluster_list(self, auth):
        """ Get list of clusters

        Name:        "get_cluster_list",
        Method:      "GET",
        Pattern:     "GetClusterList",
        """
        pattern = "GetClusterList"
        response = requests.get(
            pytest.config.getini("usm_api_url") + pattern,
            auth=auth)
        self.print_req_info(response)
        self.check_response(response)
        return response.json()["clusters"]

# TODO: https://github.com/Tendrl/api/issues/78
# In tendrl api are not correctly shown volumes
# because after deletion they stay in the list.
    def get_volume_list(self, cluster, auth):
        """ Get list of gluster volumes specified by cluster id

        Name:        "get_volume_list",
        Method:      "GET",
        Pattern:     ":cluster_id:/GetVolumeList",

        Args:
            cluster: id of cluster where will be created volume
        """
        pattern = "{}/GetVolumeList".format(cluster)
        response = requests.get(
            pytest.config.getini("usm_api_url") + pattern,
            auth=auth)
        self.print_req_info(response)
        self.check_response(response)
        return response.json()

    def create_volume(self, cluster, volume_data, auth):
        """ Import gluster cluster defined by json.

        Name:        "create_volume",
        Method:      "POST",
        Pattern:     ":cluster_id:/GlusterCreateVolume",

        Args:
            cluster: id of a cluster where will be created volume
            volume_data: json structure containing data that will be sent to api server
        """
        pattern = "{}/GlusterCreateVolume".format(cluster)
        response = requests.post(
            pytest.config.getini("usm_api_url") + pattern,
            json=volume_data,
            auth=auth)
        asserts = {
            "reason": 'Accepted',
            "status": 202,
        }
        self.print_req_info(response)
        self.check_response(response, asserts)
        return response.json()

    def delete_volume(self, cluster, post_data, auth):
        """ Import gluster cluster defined by json.

        Name:        "delete_volume",
        Method:      "POST",
        Pattern:     ":cluster_id:/GlusterDeleteVolume",

        Args:
            cluster: id of a cluster where will be created volume
            volume_data: json structure containing data that will be sent to api server
        """
        pattern = "{}/GlusterDeleteVolume".format(cluster)
        response = requests.delete(
            pytest.config.getini("usm_api_url") + pattern,
            json=post_data,
            auth=auth)

        asserts = {
            "reason": 'Accepted',
            "status": 202,
        }
        self.print_req_info(response)
        self.check_response(response, asserts)
        return response.json()

    def start_volume(self, cluster, volume_data, auth):
        """ Start gluster volume specified by json.

        Name:        "start_volume",
        Method:      "POST",
        Pattern:     ":cluster_id:/GlusterStartVolume",

        Args:
            cluster: id of a cluster where will be created volume
            volume_data: json structure containing data that will be sent to api server
        """
        pattern = "{}/GlusterStartVolume".format(cluster)
        response = requests.post(
            pytest.config.getini("usm_api_url") + pattern,
            json=volume_data,
            auth=auth)
        asserts = {
            "reason": 'Accepted',
            "status": 202,
        }
        self.print_req_info(response)
        self.check_response(response, asserts)
        return response.json()

    def stop_volume(self, cluster, volume_data, auth):
        """ Stop gluster volume specified by json.

        Name:        "stop_volume",
        Method:      "POST",
        Pattern:     ":cluster_id:/GlusterStartVolume",

        Args:
            cluster: id of a cluster where will be created volume
            volume_data: json structure containing data that will be sent to api server
        """
        pattern = "{}/GlusterStopVolume".format(cluster)
        response = requests.post(
            pytest.config.getini("usm_api_url") + pattern,
            json=volume_data,
            auth=auth)
        asserts = {
            "reason": 'Accepted',
            "status": 202,
        }
        self.print_req_info(response)
        self.check_response(response, asserts)
        return response.json()

    def get_volume_attribute(self, cluster, volume, attribute, auth):
        """ Check if provided volume has attribute of given value.

        Args:
            cluster: id of a cluster
            volume: id of a volume
            attribute: name of the searched attribute
        """
        value = [x[attribute] for x in self.get_volume_list(cluster, auth)
                 if x["vol_id"] == volume][0]
        LOGGER.debug("{} = {}".format(attribute, value))
        return value
