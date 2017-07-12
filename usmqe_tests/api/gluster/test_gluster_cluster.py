
"""
REST API test suite - gluster cluster
"""
import pytest
import json
import uuid

from usmqe.api.tendrlapi import glusterapi


LOGGER = pytest.get_logger('cluster_test', module=True)
"""@pylatest default
Setup
=====
"""

"""@pylatest default
Teardown
========
"""

"""@pylatest api/gluster.cluster_create_expand
API-gluster: cluster_create_expand
***************************

.. test_metadata:: author fbalak@redhat.com

Description
===========

Positive test for create gluster cluster and expanding it.
"""


@pytest.mark.parametrize("cluster_name, expand_nodes_count", ["ClusterName", 1])
def test_cluster_create_expand_valid(
        valid_session_credentials,
        valid_nodes,
        cluster_name,
        expand_nodes_count):
    api = glusterapi.TendrlApiGluster(auth=valid_session_credentials)
    """@pylatest api/gluster.cluster_import
        .. test_step:: 1

            Send POST request to Tendrl API ``APIURL/GlusterCreateCluster

        .. test_result:: 1

            Server should return response in JSON format:

                {
                  "job_id": job_id
                }

            Return code should be **202**
                with data ``{"message": "Accepted"}``.

        """
    nodes = []
    provisioner_ip = None
    network = pytest.config.getini("usm_network_subnet")
    node_ids = []
    ips = None
    for x in valid_nodes:
        if "tendrl/server" in x["tags"]:
            continue
        for y in x["networks"]:
            if y["subnet"] == network:
                ips = y["ipv4"]
                break
        pytest.check(
            type(ips) == list,
            "type of ip addresses returned from api have to be list,"
            " it is: {}".format(type(ips)))
        pytest.check(
            len(ips) == 1,
            "length of ipv4 addresses list have to be 1, otherwise it is not valid"
            " configuration for this test, it is: {}".format(len(ips)))
        nodes.append({
            "role": "glusterfs/node",
            "ip": ips[0],
            "node_id": x["node_id"]})
        if "provisioner/gluster" in x["tags"]:
            provisioner_ip = ips[0]
    create_nodes = nodes[:-expand_nodes_count]
    expand_nodes = nodes[-expand_nodes_count:]
    LOGGER.debug("nodes: %s" % nodes)
    LOGGER.debug("provisioner: %s" % provisioner_ip)
    """@pylatest api/gluster.cluster_create
        .. test_step:: 2

        Check if there is at least one gluster node for cluster creation.

        .. test_result:: 2

        Test passes if there is at least one gluster node.
        """
    api = glusterapi.TendrlApiGluster(auth=valid_session_credentials)
    pytest.check(
        len(create_nodes) > 0,
        "There have to be at least one gluster node."
        "There are {}".format(len(valid_nodes)))

    """@pylatest api/gluster.cluster_create
        .. test_step:: 3

        Create cluster from available nodes except one.

        .. test_result:: 3

        Test passes if there is cluster created from provided nodes.
        """
    cluster_id = str(uuid.uuid4())
    job_id = api.create_cluster(
        cluster_name,
        cluster_id,
        create_nodes,
        provisioner_ip,
        network)["job_id"]

    api.wait_for_job_status(job_id)

    integration_id = api.get_job_attribute(
        job_id=job_id,
        attribute="TendrlContext.integration_id",
        section="parameters")
    LOGGER.debug("integration_id: %s" % integration_id)

    api.get_cluster_list()
    # TODO(fbalak) remove this sleep after
    #              https://github.com/Tendrl/api/issues/159 is resolved.
    import time
    time.sleep(30)

    imported_clusters = [x for x in api.get_cluster_list()
                         if x["integration_id"] == integration_id]
    pytest.check(
        len(imported_clusters) == 1,
        "Job list integration_id '{}' should be "
        "present in cluster list.".format(integration_id))

    imported_nodes = imported_clusters[0]["nodes"]
    pytest.check(
        len(imported_nodes) == len(create_nodes),
        "In cluster should be the same amount of hosts"
        "(is {}) as is in API call for cluster creation."
        "(is {})".format(len(imported_nodes), len(create_nodes)))

    node_ids = [node["node_id"] for node in create_nodes]
    pytest.check(
        set(node_ids) == set(imported_nodes.keys()),
        "There should be imported these nodes: {}"
        "There are: {}".format(node_ids, imported_nodes.keys()))

    """@pylatest api/gluster.cluster_create
        .. test_step:: 4

        Expand created cluster with remaining node.

        .. test_result:: 4

        Test passes if the cluster is successfully expanded.
        """
    job_id = api.expand_cluster(
        cluster_id,
        expand_nodes)["job_id"]

    api.wait_for_job_status(job_id)

    api.get_cluster_list()
    # TODO(fbalak) remove this sleep after
    #              https://github.com/Tendrl/api/issues/159 is resolved.
    import time
    time.sleep(30)

    imported_clusters = [x for x in api.get_cluster_list()
                         if x["integration_id"] == integration_id]
    pytest.check(
        len(imported_clusters) == 1,
        "Job list integration_id '{}' should be "
        "present in cluster list.".format(integration_id))

    imported_nodes = imported_clusters[0]["nodes"]
    pytest.check(
        len(imported_nodes) == len(nodes),
        "In cluster should be the same amount of hosts"
        "(is {}) as is in API call for cluster creation and expand cluster."
        "(is {})".format(len(imported_nodes), len(nodes)))

    node_ids = [node["node_id"] for node in nodes]
    pytest.check(
        set(node_ids) == set(imported_nodes.keys()),
        "There should be imported these nodes: {}"
        "There are: {}".format(node_ids, imported_nodes.keys()))


"""@pylatest api/gluster.cluster_import
API-gluster: cluster_import
***************************

.. test_metadata:: author fbalak@redhat.com

Description
===========

Positive import gluster cluster.
"""


def test_cluster_import_valid(valid_session_credentials, valid_trusted_pool):
    """@pylatest api/gluster.cluster_import
        .. test_step:: 1

        Get list of ids of availible nodes.

        .. test_result:: 1

                Server should return response in JSON format:

                        {
                ...
                  {
                  "fqdn": hostname,
                  "machine_id": some_id,
                  "node_id": node_id
                  },
                ...
                        }

                Return code should be **200** with data ``{"message": "OK"}``.

        """
    api = glusterapi.TendrlApiGluster(auth=valid_session_credentials)
    """@pylatest api/gluster.cluster_import
        .. test_step:: 2

            Send POST request to Tendrl API ``APIURL/GlusterImportCluster

        .. test_result:: 2

            Server should return response in JSON format:

                {
                  "job_id": job_id
                }

            Return code should be **202**
                with data ``{"message": "Accepted"}``.

        """
    nodes = api.get_nodes()
    node_ids = None
    for cluster in nodes["clusters"]:
        if cluster["sds_name"] == "gluster":
            node_ids = cluster["node_ids"]
            break
    node_fqdns = []
    msg = "`sds_pkg_name` of node {} should be `gluster`, it is {}"
    for node in nodes["nodes"]:
        if node["node_id"] in node_ids:
            pytest.check(node["detectedcluster"]["sds_pkg_name"] == "gluster",
                         msg.format(node["fqdn"],
                         node["detectedcluster"]["sds_pkg_name"]))
            node_fqdns.append(node["fqdn"])
    node_ids = [x["node_id"] for x in nodes["nodes"]
                if x["fqdn"] in valid_trusted_pool]
    pytest.check(
        len(valid_trusted_pool) == len(node_ids),
        "number of nodes in trusted pool ({}) should correspond "
        "with number of imported nodes ({})".format(len(valid_trusted_pool),
                                                    len(node_ids)))

    job_id = api.import_cluster(node_ids)["job_id"]

    api.wait_for_job_status(job_id)

    integration_id = api.get_job_attribute(
        job_id=job_id,
        attribute="TendrlContext.integration_id",
        section="parameters")
    LOGGER.debug("integration_id: %s" % integration_id)

    imported_clusters = [x for x in api.get_cluster_list()
                         if x["integration_id"] == integration_id]
    pytest.check(
        len(imported_clusters) == 1,
        "Job list integration_id '{}' should be "
        "present in cluster list.".format(integration_id))
    # TODO add test case for checking imported machines
    msg = "In tendrl should be a same machines "\
          "as from `gluster peer status` command ({})"
    LOGGER.debug("debug imported clusters: %s" % imported_clusters)
    pytest.check(
        [x["fqdn"] in valid_trusted_pool
         for x in imported_clusters[0]["nodes"].values()],
        msg.format(valid_trusted_pool))


"""@pylatest api/gluster.cluster_import
API-gluster: cluster_import
***************************

.. test_metadata:: author fbalak@redhat.com

Description
===========

Negative import gluster cluster.
"""


@pytest.mark.parametrize("node_ids,asserts", [
    (["000000-0000-0000-0000-000000000"], {
        "json": json.loads(
            '{"errors": "Node 000000-0000-0000-0000-000000000 not found"}'),
        "cookies": None,
        "ok": False,
        "reason": 'Unprocessable Entity',
        "status": 422,
        })])
def test_cluster_import_invalid(valid_session_credentials, node_ids, asserts):
    """@pylatest api/gluster.cluster_import
        .. test_step:: 1

        Get list of ids of availible nodes.

        .. test_result:: 1

                Server should return response in JSON format:

                        {
                ...
                  {
                  "fqdn": hostname,
                  "machine_id": some_id,
                  "node_id": node_id
                  },
                ...
                        }

                Return code should be **200** with data ``{"message": "OK"}``.

        """
    api = glusterapi.TendrlApiGluster(auth=valid_session_credentials)
    """@pylatest api/gluster.cluster_import
        .. test_step:: 2

            Send POST request to Tendrl API ``APIURL/GlusterImportCluster

        .. test_result:: 2

            Server should return response in JSON format with message set in
            ``asserts`` test parameter.

        """
    api.import_cluster(node_ids,  asserts_in=asserts)
