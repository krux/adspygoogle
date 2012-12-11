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

"""Unit tests to cover NetworkService."""

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


class NetworkServiceTestV201108(unittest.TestCase):

  """Unittest suite for NetworkService using v201108."""

  SERVER = SERVER_V201108
  VERSION = VERSION_V201108
  client.debug = False
  service = None
  network = None

  def setUp(self):
    """Prepare unittest."""
    print self.id()
    if not self.__class__.service:
      self.__class__.service = client.GetNetworkService(
          self.__class__.SERVER, self.__class__.VERSION, HTTP_PROXY)

  def testGetAllNetworks(self):
    """Test whether we can fetch all networks."""
    self.assert_(isinstance(self.__class__.service.GetAllNetworks(), tuple))

  def testGetCurrentNetwork(self):
    """Test whether we can fetch current network."""
    self.__class__.network = self.__class__.service.GetCurrentNetwork()[0]
    self.assert_(isinstance(self.__class__.network, dict))

  def testUpdateNetwork(self):
    """Test whether we can update a network."""
    if not self.__class__.network:
      self.testGetCurrentNetwork()
    display_name = 'My test network'
    self.__class__.network['displayName'] = 'My test network'
    order = self.__class__.service.UpdateNetwork(self.__class__.network)
    self.assert_(isinstance(order, tuple))
    self.assertEqual(order[0]['displayName'], display_name)


class NetworkServiceTestV201111(unittest.TestCase):

  """Unittest suite for NetworkService using v201111."""

  SERVER = SERVER_V201111
  VERSION = VERSION_V201111
  client.debug = False
  service = None
  network = None

  def setUp(self):
    """Prepare unittest."""
    print self.id()
    if not self.__class__.service:
      self.__class__.service = client.GetNetworkService(
          self.__class__.SERVER, self.__class__.VERSION, HTTP_PROXY)

  def testGetAllNetworks(self):
    """Test whether we can fetch all networks."""
    self.assert_(isinstance(self.__class__.service.GetAllNetworks(), tuple))

  def testGetCurrentNetwork(self):
    """Test whether we can fetch current network."""
    self.__class__.network = self.__class__.service.GetCurrentNetwork()[0]
    self.assert_(isinstance(self.__class__.network, dict))

  def testUpdateNetwork(self):
    """Test whether we can update a network."""
    if not self.__class__.network:
      self.testGetCurrentNetwork()
    display_name = 'My test network'
    self.__class__.network['displayName'] = 'My test network'
    order = self.__class__.service.UpdateNetwork(self.__class__.network)
    self.assert_(isinstance(order, tuple))
    self.assertEqual(order[0]['displayName'], display_name)


def makeTestSuiteV201108():
  """Set up test suite using v201108.

  Returns:
    TestSuite test suite using v201108.
  """
  suite = unittest.TestSuite()
  suite.addTests(unittest.makeSuite(NetworkServiceTestV201108))
  return suite


def makeTestSuiteV201111():
  """Set up test suite using v201111.

  Returns:
    TestSuite test suite using v201111.
  """
  suite = unittest.TestSuite()
  suite.addTests(unittest.makeSuite(NetworkServiceTestV201111))
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
