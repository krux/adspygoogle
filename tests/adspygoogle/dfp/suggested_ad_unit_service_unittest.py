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

"""Unit tests to cover SuggestedAdUnitService."""

__author__ = 'api.shamjeff@gmail.com (Jeff Sham)'

import os
import sys
sys.path.insert(0, os.path.join('..', '..', '..'))
import unittest

from tests.adspygoogle.dfp import client
from tests.adspygoogle.dfp import HTTP_PROXY
from tests.adspygoogle.dfp import SERVER_V201111
from tests.adspygoogle.dfp import TEST_VERSION_V201111
from tests.adspygoogle.dfp import VERSION_V201111


class SuggestedAdUnitServiceTestV201111(unittest.TestCase):

  """Unittest suite for SuggestedAdUnitService using V201111."""

  SERVER = SERVER_V201111
  VERSION = VERSION_V201111
  client.debug = False
  service = None

  def setUp(self):
    """Prepare unittest."""
    print self.id()
    if not self.__class__.service:
      self.__class__.service = client.GetSuggestedAdUnitService(
          self.__class__.SERVER, self.__class__.VERSION, HTTP_PROXY)

  def testGetSuggestedAdUnitByStatement(self):
    """Test whether we can fetch a list of suggested ad units that
    match given statement."""
    filter_statement = {'query': 'LIMIT 500'}
    self.assert_(isinstance(
        self.__class__.service.GetSuggestedAdUnitsByStatement(
            filter_statement), tuple))


def makeTestSuiteV201111():
  """Set up test suite using v201111.

  Returns:
    TestSuite test suite using v201111.
  """
  suite = unittest.TestSuite()
  suite.addTests(unittest.makeSuite(SuggestedAdUnitServiceTestV201111))
  return suite


if __name__ == '__main__':
  suites = []
  if TEST_VERSION_V201111:
    suites.append(makeTestSuiteV201111())
  if suites:
    alltests = unittest.TestSuite(suites)
    unittest.main(defaultTest='alltests')
