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

"""Unit tests to cover Utils."""

__author__ = 'api.sgrinberg@gmail.com (Stan Grinberg)'

import os
import sys
sys.path.insert(0, os.path.join('..', '..', '..'))
import unittest

from adspygoogle.common import Utils
from adspygoogle.common.Errors import ValidationError
from adspygoogle.dfp import DfpUtils
from adspygoogle.dfp.DfpSoapBuffer import DfpSoapBuffer
from tests.adspygoogle.dfp import client
from tests.adspygoogle.dfp import HTTP_PROXY
from tests.adspygoogle.dfp import SERVER_V201108
from tests.adspygoogle.dfp import SERVER_V201111
from tests.adspygoogle.dfp import TEST_VERSION_V201108
from tests.adspygoogle.dfp import TEST_VERSION_V201111
from tests.adspygoogle.dfp import VERSION_V201108
from tests.adspygoogle.dfp import VERSION_V201111


class DfpUtilsTestV201108(unittest.TestCase):

  """Unittest suite for DfpUtils using v201108."""

  SERVER = SERVER_V201108
  VERSION = VERSION_V201108
  client.debug = False
  TRIGGER_MSG = ('502 Server Error. The server encountered a temporary error'
                 ' and could not complete yourrequest. Please try again in 30 '
                 'seconds.')

  def setUp(self):
    """Prepare unittest."""
    print self.id()

  def testError502(self):
    """Test whether we can handle and report 502 errors."""
    # Temporarily redirect STDOUT into a buffer.
    buf = DfpSoapBuffer()
    sys.stdout = buf

    html_code = Utils.ReadFile(os.path.join('data', 'http_error_502.html'))
    print html_code

    # Restore STDOUT.
    sys.stdout = sys.__stdout__

    if not buf.IsHandshakeComplete():
      data = buf.GetBufferAsStr()
    else:
      data = ''

    self.assertEqual(Utils.GetErrorFromHtml(data), self.__class__.TRIGGER_MSG)

  def testDataFileCurrencies(self):
    """Test whether csv data file with currencies is valid."""
    cols = 2
    for item in DfpUtils.GetCurrencies():
      self.assertEqual(len(item), cols)

  def testDataFileTimezones(self):
    """Test whether csv data file with timezones is valid."""
    cols = 1
    for item in DfpUtils.GetTimezones():
      self.assertEqual(len(item), cols)

  def testGetAllEntitiesByStatement(self):
    """Test whether GetAllEntitiesByStatement() does what it suppose to."""
    users = DfpUtils.GetAllEntitiesByStatement(
        client, 'User', 'ORDER BY name',
        server=self.__class__.SERVER, version=self.__class__.VERSION,
        http_proxy=HTTP_PROXY)
    self.assert_(isinstance(users, list))

  def testGetAllEntitiesByStatementWithLimit(self):
    """Test whether GetAllEntitiesByStatement() does what it suppose to do when
    LIMIT is provided as part of the query."""
    self.failUnlessRaises(
        ValidationError, DfpUtils.GetAllEntitiesByStatement,
        client, 'User', 'ORDER BY name LIMIT 1',
        server=self.__class__.SERVER, version=self.__class__.VERSION,
        http_proxy=HTTP_PROXY)

  def testGetAllEntitiesByStatementWithService(self):
    """Test whether GetAllEntitiesByStatementWithService() does what it suppose
    to."""
    user_service = client.GetUserService(self.__class__.SERVER,
                                         self.__class__.VERSION)
    users = DfpUtils.GetAllEntitiesByStatementWithService(
        user_service, 'ORDER BY name')
    self.assert_(isinstance(users, list))


class DfpUtilsTestV201111(unittest.TestCase):

  """Unittest suite for DfpUtils using v201111."""

  SERVER = SERVER_V201111
  VERSION = VERSION_V201111
  client.debug = False
  TRIGGER_MSG = ('502 Server Error. The server encountered a temporary error'
                 ' and could not complete yourrequest. Please try again in 30 '
                 'seconds.')

  def setUp(self):
    """Prepare unittest."""
    print self.id()

  def testError502(self):
    """Test whether we can handle and report 502 errors."""
    # Temporarily redirect STDOUT into a buffer.
    buf = DfpSoapBuffer()
    sys.stdout = buf

    html_code = Utils.ReadFile(os.path.join('data', 'http_error_502.html'))
    print html_code

    # Restore STDOUT.
    sys.stdout = sys.__stdout__

    if not buf.IsHandshakeComplete():
      data = buf.GetBufferAsStr()
    else:
      data = ''

    self.assertEqual(Utils.GetErrorFromHtml(data), self.__class__.TRIGGER_MSG)

  def testDataFileCurrencies(self):
    """Test whether csv data file with currencies is valid."""
    cols = 2
    for item in DfpUtils.GetCurrencies():
      self.assertEqual(len(item), cols)

  def testDataFileTimezones(self):
    """Test whether csv data file with timezones is valid."""
    cols = 1
    for item in DfpUtils.GetTimezones():
      self.assertEqual(len(item), cols)

  def testGetAllEntitiesByStatement(self):
    """Test whether GetAllEntitiesByStatement() does what it suppose to."""
    users = DfpUtils.GetAllEntitiesByStatement(
        client, 'User', 'ORDER BY name',
        server=self.__class__.SERVER, version=self.__class__.VERSION,
        http_proxy=HTTP_PROXY)
    self.assert_(isinstance(users, list))

  def testGetAllEntitiesByStatementWithLimit(self):
    """Test whether GetAllEntitiesByStatement() does what it suppose to do when
    LIMIT is provided as part of the query."""
    self.failUnlessRaises(
        ValidationError, DfpUtils.GetAllEntitiesByStatement,
        client, 'User', 'ORDER BY name LIMIT 1',
        server=self.__class__.SERVER, version=self.__class__.VERSION,
        http_proxy=HTTP_PROXY)

  def testGetAllEntitiesByStatementWithService(self):
    """Test whether GetAllEntitiesByStatementWithService() does what it suppose
    to."""
    user_service = client.GetUserService(self.__class__.SERVER,
                                         self.__class__.VERSION)
    users = DfpUtils.GetAllEntitiesByStatementWithService(
        user_service, 'ORDER BY name')
    self.assert_(isinstance(users, list))


def makeTestSuiteV201108():
  """Set up test suite using v201108.

  Returns:
    TestSuite test suite using v201108.
  """
  suite = unittest.TestSuite()
  suite.addTests(unittest.makeSuite(DfpUtilsTestV201108))
  return suite


def makeTestSuiteV201111():
  """Set up test suite using v201111.

  Returns:
    TestSuite test suite using v201111.
  """
  suite = unittest.TestSuite()
  suite.addTests(unittest.makeSuite(DfpUtilsTestV201111))
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
