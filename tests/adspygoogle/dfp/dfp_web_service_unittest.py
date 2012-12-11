#!/usr/bin/python
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

"""Unit tests to cover DfpWebService."""

__author__ = 'api.sgrinberg@gmail.com (Stan Grinberg)'

import os
import sys
sys.path.insert(0, os.path.join('..', '..', '..'))
import thread
import threading
import unittest

from adspygoogle.common import Utils
from adspygoogle.dfp.DfpErrors import DfpApiError
from adspygoogle.dfp.GenericDfpService import GenericDfpService
from tests.adspygoogle.dfp import client
from tests.adspygoogle.dfp import HTTP_PROXY
from tests.adspygoogle.dfp import SERVER_V201108
from tests.adspygoogle.dfp import SERVER_V201111
from tests.adspygoogle.dfp import TEST_VERSION_V201108
from tests.adspygoogle.dfp import TEST_VERSION_V201111
from tests.adspygoogle.dfp import VERSION_V201108
from tests.adspygoogle.dfp import VERSION_V201111


class DfpWebServiceTestV201108(unittest.TestCase):

  """Unittest suite for DfpWebService using v201108."""

  SERVER = SERVER_V201108
  VERSION = VERSION_V201108
  client.debug = False
  res = []
  MAX_THREADS = 3

  def setUp(self):
    """Prepare unittest."""
    print self.id()

  def testCallMethod(self):
    """Test whether we can call an API method indirectly."""
    filter_statement = {'query': 'ORDER BY name LIMIT 500'}
    self.assert_(isinstance(client.GetUserService(self.__class__.SERVER,
        self.__class__.VERSION, HTTP_PROXY).GetUsersByStatement(
            filter_statement), tuple))

  def testCallRawMethod(self):
    """Test whether we can call an API method by posting SOAP XML message."""
    soap_message = Utils.ReadFile(
        os.path.join('data', 'request_getusersbystatement.xml'))
    url = '/apis/ads/publisher/v201108/UserService'
    http_proxy = None

    self.assert_(isinstance(client.CallRawMethod(soap_message, url,
                            self.__class__.SERVER, http_proxy), tuple))

  def testMultiThreads(self):
    """Test whether we can safely execute multiple threads."""
    all_threads = []
    for i in xrange(self.__class__.MAX_THREADS):
      t = TestThreadV201108()
      all_threads.append(t)
      t.start()

    for t in all_threads:
      t.join()

    self.assertEqual(len(self.res), self.__class__.MAX_THREADS)


class TestThreadV201108(threading.Thread):

  """Creates TestThread using v201108.

  Responsible for defining an action for a single thread.
  """

  def run(self):
    """Represent thread's activity."""
    statement = {'query': 'ORDER BY name LIMIT 500'}
    DfpWebServiceTestV201108.res.append(client.GetUserService(
        DfpWebServiceTestV201108.SERVER, DfpWebServiceTestV201108.VERSION,
        HTTP_PROXY).GetUsersByStatement(statement))


class DfpWebServiceTestV201111(unittest.TestCase):

  """Unittest suite for DfpWebService using v201111."""

  SERVER = SERVER_V201111
  VERSION = VERSION_V201111
  client.debug = False
  res = []
  MAX_THREADS = 3

  def setUp(self):
    """Prepare unittest."""
    print self.id()

  def testCallMethod(self):
    """Test whether we can call an API method indirectly."""
    filter_statement = {'query': 'ORDER BY name LIMIT 500'}
    self.assert_(isinstance(client.GetUserService(self.__class__.SERVER,
        self.__class__.VERSION, HTTP_PROXY).GetUsersByStatement(
            filter_statement), tuple))

  def testCallRawMethod(self):
    """Test whether we can call an API method by posting SOAP XML message."""
    soap_message = Utils.ReadFile(
        os.path.join('data', 'request_getusersbystatement.xml'))
    url = '/apis/ads/publisher/v201111/UserService'
    http_proxy = None

    self.assert_(isinstance(client.CallRawMethod(soap_message, url,
                            self.__class__.SERVER, http_proxy), tuple))

  def testMultiThreads(self):
    """Test whether we can safely execute multiple threads."""
    all_threads = []
    for i in xrange(self.__class__.MAX_THREADS):
      t = TestThreadV201111()
      all_threads.append(t)
      t.start()

    for t in all_threads:
      t.join()

    self.assertEqual(len(self.res), self.__class__.MAX_THREADS)


class TestThreadV201111(threading.Thread):

  """Creates TestThread using v201111.

  Responsible for defining an action for a single thread.
  """

  def run(self):
    """Represent thread's activity."""
    statement = {'query': 'ORDER BY name LIMIT 500'}
    DfpWebServiceTestV201111.res.append(client.GetUserService(
        DfpWebServiceTestV201111.SERVER, DfpWebServiceTestV201111.VERSION,
        HTTP_PROXY).GetUsersByStatement(statement))


def makeTestSuiteV201108():
  """Set up test suite using v201108.

  Returns:
    TestSuite test suite using v201108.
  """
  suite = unittest.TestSuite()
  suite.addTests(unittest.makeSuite(DfpWebServiceTestV201108))
  return suite


def makeTestSuiteV201111():
  """Set up test suite using v201111.

  Returns:
    TestSuite test suite using v201111.
  """
  suite = unittest.TestSuite()
  suite.addTests(unittest.makeSuite(DfpWebServiceTestV201111))
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
