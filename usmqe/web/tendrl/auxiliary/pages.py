"""
Some usefull pages classes for common work with tendrl web
"""


from selenium.webdriver.common.keys import Keys

from webstr.core import WebstrPage
import webstr.patternfly.dropdown.pages as dropdown

import usmqe.web.tendrl.auxiliary.models as m_auxiliary


class ListMenu(WebstrPage):
    """
    auxiliary class for work with a list menu (filter and order fields)
    """
    _model = m_auxiliary.ListMenuModel
    _label = 'list menu'
    _required_elems = [
        'filter_by',
        'filter_input',
        'order_by',
        'order_btn'
    ]

    def set_filter(self, filter_type=None, filter_input=None):
        """
        Set filter and press ENTER key

        Parameters:
            filter_type (str) - by which type of filter hosts are filtered by
            filter_input (str) - text to be filled in the filter text field
        """
        if filter_type is not None:
            self._model.filter_by.value = filter_type
        if filter_input is not None:
            self._model.filter_input.value = filter_input
        self._model.filter_input.send_keys(Keys.RETURN)

    @property
    def order_by(self):
        """ get by which elem the list is ordered

        Returns:
            order by
        """
        return self._model.order_by.value

    @order_by.setter
    def order_by(self, value):
        """ set the order by field

        Parameters:
            value (str): order by text value
        """
        self._model.order_by.value = value

    def order_order(self):
        """
        switch order of the list
        """
        self._model.order_btn.click()


class UpperMenu(WebstrPage):
    """ Common page object for upper menu """
    _model = m_auxiliary.UpperMenuModel
    _label = 'upper menu'
    _required_elems = [
        # left part of upper navbar
        'user_link',
        # right part of upper navbar
    ]

    def open_user_menu(self):
        """
        Opens user drop-down menu
        """
        self._model.user_link.click()
        return UserMenu(self.driver)


class UserMenu(dropdown.DropDownMenu):
    """
    Base page object for user pop-up menu

    Parameters:
      _model - page model
    """
    _model = m_auxiliary.UserMenuModel
    _label = 'user popup menu'
    _required_elems = ['logout']

    def logout(self):
        """ log out current user - click on logout """
        self._model.logout.click()


class Alert(WebstrPage):
    """
    page object for alert/notice message
    """
    _model = m_auxiliary.AlertModel
    _label = 'alert/notice message'
    _required_elems = ['message, close_btn']

    @property
    def message(self):
        """
        returns message text
        """
        return self._model.message.text

    def close(self):
        """
        close the alert/notice
        click on close button - X symbol
        """
        self._model.close_btn.click()
