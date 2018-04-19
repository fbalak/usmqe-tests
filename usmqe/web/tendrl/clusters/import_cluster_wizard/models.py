"""
Import Cluster wizard module.
"""


from webstr.core import By, PageElement, NameRootPageElement
from webstr.core.model import WebstrModel
import webstr.patternfly.contentviews.models as contentviews

# The URL is not much usable as the correct one ends with /<cluster_id>
location = '/#/import-cluster'


class ImportClusterSummaryModel(WebstrModel):
    """
    model for Import Cluster - Summary page
    """


class HostsItemModel(contentviews.ListViewRowModel):
    """
    An item (row) in a Hosts list.
    """
    name_label = PageElement(
        by=By.XPATH,
        locator=".//div[contains(@class, 'host-name')]")
    release = PageElement(
        by=By.XPATH,
        locator=".//div[contains(@class, 'host-release')]")
    name = name_label
    role = PageElement(
        By.XPATH,
        ".//div[contains(@class, 'list-view-pf-additional-info')]/div[2]")
    _root = NameRootPageElement(
        by=By.XPATH,
        locator='({}//*[contains(concat(" ", @class, " "),'
        ' " list-group-item ")][@ng-repeat])[%d]'.format(
            contentviews.ListViewModel.LIST_XPATH))


class HostsListModel(contentviews.ListViewModel):
    """
    Page model for list of nodes/hosts.
    """
    rows = PageElement(
        by=By.XPATH,
        locator="{}//*[contains(concat(' ', @class, ' '),"
        " ' list-group-item ')][@ng-repeat]".format(
            contentviews.ListViewModel.LIST_XPATH),
        as_list=True)
