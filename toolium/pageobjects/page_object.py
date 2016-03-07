# -*- coding: utf-8 -*-
u"""
Copyright 2015 Telefónica Investigación y Desarrollo, S.A.U.
This file is part of Toolium.

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""

import logging

from toolium.driver_wrapper import DriverWrappersPool
from toolium.pageelements.page_element import PageElement
from toolium.pageelements.page_elements import PageElements


class PageObject(object):
    """Class to represent a web page or a mobile application screen

    :type driver_wrapper: toolium.driver_wrapper.DriverWrapper
    :type driver: selenium.webdriver.remote.webdriver.WebDriver or appium.webdriver.webdriver.WebDriver
    :type config: toolium.config_parser.ExtendedConfigParser
    :type utils: toolium.utils.Utils
    :type app_strings: str
    """
    driver_wrapper = None  #: driver wrapper instance
    driver = None  #: webdriver instance
    config = None  #: driver configuration
    utils = None  #: test utils instance
    app_strings = None  #:mobile application strings

    def __init__(self, driver_wrapper=None):
        """Initialize page object properties and update their page elements

        :param driver_wrapper: driver wrapper instance
        """
        self.logger = logging.getLogger(__name__)
        self.set_driver_wrapper(driver_wrapper)
        self.init_page_elements()
        self._update_page_elements()

    def set_driver_wrapper(self, driver_wrapper=None):
        """Initialize driver_wrapper, driver, config and utils

        :param driver_wrapper: driver wrapper instance
        """
        self.driver_wrapper = driver_wrapper if driver_wrapper else DriverWrappersPool.get_default_wrapper()
        # Add some driver_wrapper attributes to page object instance
        self.driver = self.driver_wrapper.driver
        self.config = self.driver_wrapper.config
        self.utils = self.driver_wrapper.utils
        self.app_strings = self.driver_wrapper.app_strings

    def init_page_elements(self):
        """Method to initialize page elements

        This method can be overridden to define page elements and will be called in page object __init__
        """
        pass

    def _get_page_elements(self):
        """Return page elements and page objects of this page object

        :returns: list of page elements and page objects
        """
        page_elements = []
        for element in list(self.__dict__.values()) + list(self.__class__.__dict__.values()):
            if isinstance(element, PageElement) or isinstance(element, PageElements) or isinstance(element, PageObject):
                page_elements.append(element)
        return page_elements

    def _update_page_elements(self):
        """Copy driver and utils instances to all page elements of this page object"""
        for element in self._get_page_elements():
            element.set_driver_wrapper(self.driver_wrapper)
            if isinstance(element, PageObject):
                # If element is a page object, update also its page elements
                element._update_page_elements()

    def reset_web_elements(self):
        """Reset web element object in all page elements"""
        for element in self._get_page_elements():
            element.reset_web_elements()
