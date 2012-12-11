#!/usr/bin/python
# -*- coding: UTF-8 -*-
#
# Copyright 2011 Google Inc. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Unit tests to cover PublisherQueryLanguageService."""

__author__ = 'api.sgrinberg@gmail.com (Stan Grinberg)'

import os
import sys
sys.path.insert(0, os.path.join('..', '..', '..'))
import unittest

from tests.adspygoogle.dfp import client
from tests.adspygoogle.dfp import HTTP_PROXY
from tests.adspygoogle.dfp import SERVER_V201108
from tests.adspygoogle.dfp import SERVER_V201111
from tests.adspygoogle.dfp import TEST_VERSION_V201108
from tests.adspygoogle.dfp import TEST_VERSION_V201111
from tests.adspygoogle.dfp import VERSION_V201108
from tests.adspygoogle.dfp import VERSION_V201111


class PublisherQueryLanguageServiceTestV201108(unittest.TestCase):

  """Unittest suite for PublisherQueryLanguageService using v201108."""

  SERVER = SERVER_V201108
  VERSION = VERSION_V201108
  client.debug = False
  service = None

  def setUp(self):
    """Prepare unittest."""
    print self.id()
    if not self.__class__.service:
      self.__class__.service = client.GetPublisherQueryLanguageService(
          self.__class__.SERVER, self.__class__.VERSION, HTTP_PROXY)

  def testGetCitiesByStatement(self):
    """Test whether we can fetch a list of existing cities that match given
    statement."""
    select_statement = {'query': 'SELECT * FROM City WHERE '
                        'targetable = true limit 10'}
    self.assert_(isinstance(
        self.__class__.service.Select(select_statement), tuple))

  def testGetCountriesByStatement(self):
    """Test whether we can fetch a list of existing countries that match given
    statement."""
    select_statement = {'query': 'SELECT * FROM Country WHERE '
                        'targetable = true limit 10'}
    self.assert_(isinstance(
        self.__class__.service.Select(select_statement), tuple))

  def testGetMetrosByStatement(self):
    """Test whether we can fetch a list of existing metros   that match given
    statement."""
    select_statement = {'query': 'SELECT * FROM Metro WHERE '
                        'targetable = true limit 10'}
    self.assert_(isinstance(
        self.__class__.service.Select(select_statement), tuple))

  def testGetRegionsByStatement(self):
    """Test whether we can fetch a list of existing regions that match given
    statement."""
    select_statement = {'query': 'SELECT * FROM Region WHERE '
                        'targetable = true limit 10'}
    self.assert_(isinstance(
        self.__class__.service.Select(select_statement), tuple))


class PublisherQueryLanguageServiceTestV201111(unittest.TestCase):

  """Unittest suite for PublisherQueryLanguageService using v201111."""

  SERVER = SERVER_V201111
  VERSION = VERSION_V201111
  client.debug = False
  service = None

  def setUp(self):
    """Prepare unittest."""
    print self.id()
    if not self.__class__.service:
      self.__class__.service = client.GetPublisherQueryLanguageService(
          self.__class__.SERVER, self.__class__.VERSION, HTTP_PROXY)

  def testGetCitiesByStatement(self):
    """Test whether we can fetch a list of existing cities that match given
    statement."""
    select_statement = {'query': 'SELECT * FROM City WHERE '
                        'targetable = true limit 10'}
    self.assert_(isinstance(
        self.__class__.service.Select(select_statement), tuple))

  def testGetCountriesByStatement(self):
    """Test whether we can fetch a list of existing countries that match given
    statement."""
    select_statement = {'query': 'SELECT * FROM Country WHERE '
                        'targetable = true limit 10'}
    self.assert_(isinstance(
        self.__class__.service.Select(select_statement), tuple))

  def testGetMetrosByStatement(self):
    """Test whether we can fetch a list of existing metros   that match given
    statement."""
    select_statement = {'query': 'SELECT * FROM Metro WHERE '
                        'targetable = true limit 10'}
    self.assert_(isinstance(
        self.__class__.service.Select(select_statement), tuple))

  def testGetRegionsByStatement(self):
    """Test whether we can fetch a list of existing regions that match given
    statement."""
    select_statement = {'query': 'SELECT * FROM Region WHERE '
                        'targetable = true limit 10'}
    self.assert_(isinstance(
        self.__class__.service.Select(select_statement), tuple))


def makeTestSuiteV201108():
  """Set up test suite using v201108.

  Returns:
    TestSuite test suite using v201108.
  """
  suite = unittest.TestSuite()
  suite.addTests(unittest.makeSuite(PublisherQueryLanguageServiceTestV201108))
  return suite


def makeTestSuiteV201111():
  """Set up test suite using v201111.

  Returns:
    TestSuite test suite using v201111.
  """
  suite = unittest.TestSuite()
  suite.addTests(unittest.makeSuite(PublisherQueryLanguageServiceTestV201111))
  return suite


if __name__ == '__main__':
  suites = []
  if TEST_VERSION_V201108:
    suites.append(makeTestSuiteV201108())
  if TEST_VERSION_V201111:
    suites.append(makeTestSuiteV201111())
  if suites:
    alltests = unittest.TestSuite(suites)
    unittest.main(defaultTest='alltests')
