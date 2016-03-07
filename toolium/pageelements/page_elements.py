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

from toolium.driver_wrapper import DriverWrappersPool
from toolium.pageelements.button_page_element import Button
from toolium.pageelements.checkbox_page_element import Checkbox
from toolium.pageelements.input_radio_page_element import InputRadio
from toolium.pageelements.input_text_page_element import InputText
from toolium.pageelements.link_page_element import Link
from toolium.pageelements.page_element import PageElement
from toolium.pageelements.select_page_element import Select
from toolium.pageelements.text_page_element import Text


class PageElements(object):
    """Class to represent multiple web or mobile page elements

    :type driver_wrapper: toolium.driver_wrapper.DriverWrapper
    :type driver: selenium.webdriver.remote.webdriver.WebDriver or appium.webdriver.webdriver.WebDriver
    :type config: toolium.config_parser.ExtendedConfigParser
    :type utils: toolium.utils.Utils
    :type locator: (selenium.webdriver.common.by.By or appium.webdriver.common.mobileby.MobileBy, str)
    :type parent: selenium.webdriver.remote.webelement.WebElement or appium.webdriver.webelement.WebElement
                  or toolium.pageelements.PageElement
                  or (selenium.webdriver.common.by.By or appium.webdriver.common.mobileby.MobileBy, str)
    :type page_element_class: class
    """
    driver_wrapper = None  #: driver wrapper instance
    driver = None  #: webdriver instance
    config = None  #: driver configuration
    utils = None  #: test utils instance
    locator = None  #: tuple with locator type and locator value
    parent = None  #: element from which to find actual elements
    page_element_class = PageElement  #: class of page elements (PageElement, Button...)
    _web_elements = None
    _page_elements = None

    def __init__(self, by, value, parent=None):
        """Initialize the PageElements object with the given locator components.

        If parent is not None, find_elements will be performed over it, instead of
        using the driver's method, so it can find nested elements.

        :param by: locator type
        :param value: locator value
        :param page_element_class: class of page elements (PageElement, Button...)
        """
        self.locator = (by, value)
        self.parent = parent
        self.set_driver_wrapper()

    def set_driver_wrapper(self, driver_wrapper=None):
        """Initialize driver_wrapper, driver, config and utils

        :param driver_wrapper: driver wrapper instance
        """
        self.driver_wrapper = driver_wrapper if driver_wrapper else DriverWrappersPool.get_default_wrapper()
        # Add some driver_wrapper attributes to page elements instance
        self.driver = self.driver_wrapper.driver
        self.config = self.driver_wrapper.config
        self.utils = self.driver_wrapper.utils
        # Reset web and page elements
        self._web_elements = None
        self._page_elements = None

    @property
    def web_elements(self):
        """Find multiple WebElements using element locator

        :returns: list of web element objects
        :rtype: list of selenium.webdriver.remote.webelement.WebElement
                or list of appium.webdriver.webelement.WebElement
        """
        if not self._web_elements:
            if self.parent:
                self._web_elements = self.utils.get_web_element(self.parent).find_elements(*self.locator)
            else:
                self._web_elements = self.driver.find_elements(*self.locator)
        return self._web_elements

    def reset_web_elements(self):
        """Reset web element object"""
        self._web_elements = None

    @property
    def page_elements(self):
        """Find multiple PageElement using element locator

        :returns: list of page element objects
        :rtype: list of toolium.pageelements.PageElement
        """
        if not self._page_elements:
            self._page_elements = []
            for web_element in self.web_elements:
                # Create multiple PageElement with original locator
                page_element = self.page_element_class(self.locator[0], self.locator[1], self.parent)
                page_element.set_driver_wrapper(self.driver_wrapper)
                page_element._web_element = web_element
                self._page_elements.append(page_element)
        return self._page_elements


class Buttons(PageElements):
    page_element_class = Button


class Checkboxes(PageElements):
    page_element_class = Checkbox


class InputRadios(PageElements):
    page_element_class = InputRadio


class InputTexts(PageElements):
    page_element_class = InputText


class Links(PageElements):
    page_element_class = Link


class Selects(PageElements):
    page_element_class = Select


class Texts(PageElements):
    page_element_class = Text
