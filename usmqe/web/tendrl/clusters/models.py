"""
Common page models for clusters.
"""


from webstr.core import By, PageElement
from webstr.common.form import models as form
import webstr.patternfly.contentviews.models as contentviews

from usmqe.web.tendrl.auxiliary.models import FilterListMenuModel,\
    OrderListMenuModel
from usmqe.web.utils import StatusIcon


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
    status_icon = StatusIcon(
        By.XPATH,
        './/i[@ng-class="clusterCntrl.getClass(cluster)"]')

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

    hosts_nr = PageElement(
        by=By.XPATH,
        locator='.//div[contains(text(),"Hosts")]/following-sibling::*')

    # unavailable before import
    volumes_nr = PageElement(
        by=By.XPATH,
        locator='.//div[contains(text(),"Volumes")]/following-sibling::*')

    # unavailable before import
    alerts_nr = PageElement(
        by=By.XPATH,
        locator='.//div[contains(text(),"Alerts")]/following-sibling::*')

    # unavailable before import
    volume_profile = PageElement(
        by=By.XPATH,
        locator='.//div[contains(text(),"Volume Profiling")]'
        '/following-sibling::*')

    # unavailable during a task run or if the task fail
    cluster_state = PageElement(
        by=By.XPATH,
        locator='(.//div[contains(@class, "cluster-text")]/p)[1]')

    # unavalable only when some task is running or if it's failed
    view_details = PageElement(
        by=By.LINK_TEXT,
        locator='View Details')

    # unavailable after import
    import_btn = form.Button(
        By.XPATH,
        './/button[@ng-click="clusterCntrl.goToImportFlow(cluster)"]')

    hosts_link = PageElement(
        By.XPATH,
        '//a[@ng-click="clusterCntrl.openHostModal(cluster)"]')
# TODO
# add link to grafana
    # unavailable before import
#    dashboard_btn

# TODO
# add link to submenu with unmanage, expand, enable/dusable cluster profiling


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
