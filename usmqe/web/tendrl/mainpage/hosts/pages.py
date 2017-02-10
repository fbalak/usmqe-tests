"""
Hosts page abstraction.
"""


from webstr.patternfly.contentviews import pages as contentviews
import webstr.patternfly.dropdown.pages as dropdown

import usmqe.web.tendrl.mainpage.hosts.models as m_hosts
from usmqe.web.tendrl.auxiliary.pages import ListMenu


class HostsMenu(ListMenu):
    """
    page object for hosts top menu
    """
    _model = m_hosts.HostsMenuModel
    _label = 'hosts top menu'
    _required_elems = ListMenu._required_elems
    _required_elems.append('header')


class HostsItem(contentviews.ListViewRow):
    """
    An item (row) in a Hosts list.
    """
    _model = m_hosts.HostsItemModel
    _label = 'hosts row'
    _required_elems = [
        '_root',
        'status_icon',
        'name_label',
        'menu_link']

    @property
    def status(self):
        """
        find status

        Returns:
            status_icon element title
        """
        return self._model.status_icon.value

    def open_menu(self):
        """
        open row menu

        Returns:
            HostsRowMenu instance
        """
        self._model.menu_link.click()
        return HostsRowMenu(self.driver)


class HostsList(contentviews.ListView):
    """
    Base page object for List of nodes.
    """
    _model = m_hosts.HostsListModel
    _label = 'main page - hosts'
    _row_class = HostsItem


class HostsRowMenu(dropdown.DropDownMenu):
    """
    page object for hosts row menu
    """
    _model = m_hosts.HostsRowMenuModel
    _label = 'hosts row menu'
    _required_elems = ['forget_link', 'remove_link', 'replace_link']

# TODO use menu