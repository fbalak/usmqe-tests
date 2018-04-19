"""
Import Cluster wizard module.
"""


import webstr.patternfly.contentviews.pages as contentviews
from webstr.core.page import WebstrPage

import usmqe.web.tendrl.clusters.\
    import_cluster_wizard.models as m_wizard
# from usmqe.ceph import ceph_cluster


class ImportClusterSummary(WebstrPage):
    """
    Import Cluster - Review Summary page
    """
    _model = m_wizard.ImportClusterSummaryModel
    _label = 'clusters import Summary page'


class HostsItem(contentviews.ListViewRow):
    """
    An item (row) in a Hosts list.
    """
    _model = m_wizard.HostsItemModel
    _label = 'clusters import host'
    _required_elems = ['name', 'release', 'role']

    @property
    def name(self):
        """
        returns host name
        """
        return self._model.name.text

    @property
    def release(self):
        """
        returns installed ceph/gluster release
        """
        return self._model.release.text

    @property
    def role(self):
        """
        returns host role
        """
        return self._model.role.text


class HostsList(contentviews.ListView):
    """
    List of nodes/hosts.
    """
    _model = m_wizard.HostsListModel
    _label = 'clusters import hosts list'
    _row_class = HostsItem
