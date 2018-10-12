# -*- coding: utf8 -*-
"""
Pytest plugin to handle usmqe ini config files.

.. moduleauthor:: Martin Kudlej <mkudlej@redhat.com>
.. moduleauthor:: Filip Balak <fbalak@redhat.com>
"""


import pytest
import os
import yaml
from collections.abc import Iterable
from py.path import local
from ansible.inventory.manager import InventoryManager
from ansible.parsing.dataloader import DataLoader


class UsmConfig(object):
    """
    Configuration object containing inventory hosts file and configuration
    specified in usm yaml configuration files. Main configuration is defined
    in conf/MAIN.yaml.
    """

    def __init__(self):
        self.inventory = {}
        self.config = {}

        base_path = local(os.path.abspath(__file__)).new(basename='..')
        # get default configuration from conf/MAIN.yaml
        try:
            config_file = os.path.join(str(base_path), "conf", "MAIN.yaml")
        except FileNotFoundError() as err:
            print("conf/MAIN.yaml configuration file does not exist.")
        self.config = self.load_config(config_file)

        if self.config["configuration_files"]:
            for new_config in self.config["configuration_files"]:
                if not os.path.isabs(new_config):
                    new_config = os.path.join(str(base_path), new_config)
                self.config.update(self.load_config(new_config))

        # load inventory file to ansible interface
        # referenced in this class instance
        if self.config['inventory_file']:
            if isinstance(self.config['inventory_file'], Iterable):
                inventory_file = self.config['inventory_file'][0]
            else:
                inventory_file = self.config['inventory_file']
            if not os.path.isabs(inventory_file):
                inventory_file = os.path.join(str(base_path), inventory_file)
        else:
            raise FileNotFoundError(
                "No inventory file was provided in configuration "
                "(inventory_file in configuration file).")
        if not os.path.isfile(inventory_file):
            raise IOError("Could not find provided inventory file {}".format(
                inventory_file))
        loader = DataLoader()
        self.inventory = InventoryManager(
            loader=loader,
            sources=inventory_file)

    def load_config(self, config_file):
        """
        Loads configuration from pytest.yaml file.
        """
        with open(config_file, "r") as stream:
            try:
                conf = yaml.load(stream)
            except yaml.YAMLError as exc:
                print(exc)
        return conf
