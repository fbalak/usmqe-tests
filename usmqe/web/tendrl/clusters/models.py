"""
Common page models for clusters.
"""


from webstr.core import By, PageElement
from webstr.common.form import models as form
import webstr.patternfly.contentviews.models as contentviews

from usmqe.web.tendrl.auxiliary.models import FilterListMenuModel,\
    OrderListMenuModel
# from usmqe.web.utils import StatusIcon


LOCATION = '/#/clusters'


class ClustersMenuModel(FilterListMenuModel, OrderListMenuModel):
    """
    Clusters page top menu
    """
    header = PageElement(
        by=By.XPATH,
        locator="//h1[contains(text(),'Clusters')]")


class ClustersListModel(contentviews.ListViewModel):
    """ list of clusters with common cluster elements """
    cluster_list = PageElement(
        by=By.XPATH,
        locator='.//div[contains(@class,"list-group-item")]',
        as_list=True)


class ClustersRowModel(contentviews.ListViewRowModel):
    """
    Row in Cluster table model.
    """
#   https://github.com/Tendrl/specifications/pull/82
#
# TODO
# https://redhat.invisionapp.com/share/BR8JDCGSQ#/screens/185937524
# No status icon yet
#    status_icon = StatusIcon(By.XPATH, '')
#
    name_text = PageElement(
        by=By.XPATH,
        locator='.//div[contains(@class, "cluster-name")]')
    name = name_text

    cluster_version = PageElement(
        by=By.XPATH,
        locator='.//div[contains(text(),"Cluster Version")]'
        '/following-sibling::*')

    managed = PageElement(
        by=By.XPATH,
        locator='.//div[contains(text(),"Managed")]/following-sibling::*')

    volume_profile = PageElement(
        by=By.XPATH,
        locator='.//div[contains(text(),"Volume Profile")]'
        '/following-sibling::*')

    import_btn = form.Button(
        By.XPATH,
        '//button[@ng-click="clusterCntrl.goToImportFlow(cluster)"]')

    hosts_link = PageElement(
        By.XPATH,
        '//a[@ng-click="clusterCntrl.openHostModal(cluster)"]')
# TODO
# add link to grafana when available

class ClustersHostsListModel(contentviews.TableViewModel):
    """ list of clusters with common cluster elements """
    close_btn = form.Button(
        By.XPATH,
        '//button[@ng-click="vm.closeModal()"]')


class ClustersHostsRowModel(contentviews.TableViewRowModel):
    """
    Row in Cluster table model.
    """
    host = PageElement(
        By.XPATH,
        './/span[1]')

    address = PageElement(
        By.XPATH,
        './/span[2]')
