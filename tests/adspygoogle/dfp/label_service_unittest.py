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

"""Unit tests to cover LabelService."""

__author__ = 'api.shamjeff@gmail.com (Jeff Sham)'

import os
import sys
sys.path.insert(0, os.path.join('..', '..', '..'))
import unittest

from adspygoogle.common import Utils
from tests.adspygoogle.dfp import client
from tests.adspygoogle.dfp import HTTP_PROXY
from tests.adspygoogle.dfp import SERVER_V201108
from tests.adspygoogle.dfp import SERVER_V201111
from tests.adspygoogle.dfp import TEST_VERSION_V201108
from tests.adspygoogle.dfp import TEST_VERSION_V201111
from tests.adspygoogle.dfp import VERSION_V201108
from tests.adspygoogle.dfp import VERSION_V201111


class LabelServiceTestV201108(unittest.TestCase):

  """Unittest suite for LabelService using v201108."""

  SERVER = SERVER_V201108
  VERSION = VERSION_V201108
  client.debug = False
  service = None
  label1 = None
  label2 = None

  def setUp(self):
    """Prepare unittest."""
    print self.id()
    if not self.__class__.service:
      self.__class__.service = client.GetLabelService(
          self.__class__.SERVER, self.__class__.VERSION, HTTP_PROXY)

  def testCreateLabel(self):
    """Test whether we can create a label."""
    label = {
        'name': 'Label #%s' % Utils.GetUniqueName(),
        'description': 'a label',
        'isActive': 'True',
        'type': 'COMPETITIVE_EXCLUSION'
    }
    self.assert_(isinstance(
        self.__class__.service.CreateLabel(label), tuple))

  def testCreateLabels(self):
    """Test whether we can create a list of labels."""
    labels = [
        {
            'name': 'Label #%s' % Utils.GetUniqueName(),
            'description': 'a label',
            'isActive': 'True',
            'type': 'COMPETITIVE_EXCLUSION'
        },
        {
            'name': 'Label #%s' % Utils.GetUniqueName(),
            'description': 'a label',
            'isActive': 'True',
            'type': 'COMPETITIVE_EXCLUSION'
        }
    ]
    labels = self.__class__.service.CreateLabels(labels)
    self.__class__.label1 = labels[0]
    self.__class__.label2 = labels[1]
    self.assert_(isinstance(labels, tuple))

  def testGetLabel(self):
    """Test whether we can fetch an existing label."""
    if not self.__class__.label1:
      self.testCreateLabels()
    self.assert_(isinstance(self.__class__.service.GetLabel(
        self.__class__.label1['id']), tuple))

  def testGetLabelsByStatement(self):
    """Test whether we can fetch a list of existing labels that match given
    statement."""
    if not self.__class__.label1:
      self.testCreateLabels()
    filter_statement = {'query': 'WHERE id = \'%s\' LIMIT 500'
                        % self.__class__.label1['id']}
    self.assert_(isinstance(
        self.__class__.service.GetLabelsByStatement(filter_statement),
        tuple))

  def testPerformLabelAction(self):
    """Test whether we can activate a label."""
    if not self.__class__.label1:
      self.testCreateLabels()
    action = {'type': 'ActivateLabels'}
    filter_statement = {'query': 'WHERE id = \'%s\''
                        % self.__class__.label1['id']}
    self.assert_(isinstance(
        self.__class__.service.PerformLabelAction(action, filter_statement),
        tuple))

  def testUpdateLabel(self):
    """Test whether we can update a label."""
    if not self.__class__.label1:
      self.testCreateLabels()
    self.__class__.label1['description'] = 'updated description'
    label = self.__class__.service.UpdateLabel(self.__class__.label1)
    self.assert_(isinstance(label, tuple))
    self.assertEqual(label[0]['description'],
                     self.__class__.label1['description'])

  def testUpdateLabels(self):
    """Test whether we can update a list of labels."""
    if not self.__class__.label1 or not self.__class__.label2:
      self.testCreateLabels()
    updated_description = 'updated description'
    self.__class__.label1['description'] = updated_description
    self.__class__.label2['description'] = updated_description
    labels = self.__class__.service.UpdateLabels([
        self.__class__.label1, self.__class__.label2])
    self.assert_(isinstance(labels, tuple))
    for label in labels:
      self.assertEqual(label['description'], updated_description)


class LabelServiceTestV201111(unittest.TestCase):

  """Unittest suite for LabelService using v201111."""

  SERVER = SERVER_V201111
  VERSION = VERSION_V201111
  client.debug = False
  service = None
  label1 = None
  label2 = None

  def setUp(self):
    """Prepare unittest."""
    print self.id()
    if not self.__class__.service:
      self.__class__.service = client.GetLabelService(
          self.__class__.SERVER, self.__class__.VERSION, HTTP_PROXY)

  def testCreateLabel(self):
    """Test whether we can create a label."""
    label = {
        'name': 'Label #%s' % Utils.GetUniqueName(),
        'description': 'a label',
        'isActive': 'True',
        'type': 'COMPETITIVE_EXCLUSION'
    }
    self.assert_(isinstance(
        self.__class__.service.CreateLabel(label), tuple))

  def testCreateLabels(self):
    """Test whether we can create a list of labels."""
    labels = [
        {
            'name': 'Label #%s' % Utils.GetUniqueName(),
            'description': 'a label',
            'isActive': 'True',
            'type': 'COMPETITIVE_EXCLUSION'
        },
        {
            'name': 'Label #%s' % Utils.GetUniqueName(),
            'description': 'a label',
            'isActive': 'True',
            'type': 'COMPETITIVE_EXCLUSION'
        }
    ]
    labels = self.__class__.service.CreateLabels(labels)
    self.__class__.label1 = labels[0]
    self.__class__.label2 = labels[1]
    self.assert_(isinstance(labels, tuple))

  def testGetLabel(self):
    """Test whether we can fetch an existing label."""
    if not self.__class__.label1:
      self.testCreateLabels()
    self.assert_(isinstance(self.__class__.service.GetLabel(
        self.__class__.label1['id']), tuple))

  def testGetLabelsByStatement(self):
    """Test whether we can fetch a list of existing labels that match given
    statement."""
    if not self.__class__.label1:
      self.testCreateLabels()
    filter_statement = {'query': 'WHERE id = \'%s\' LIMIT 500'
                        % self.__class__.label1['id']}
    self.assert_(isinstance(
        self.__class__.service.GetLabelsByStatement(filter_statement),
        tuple))

  def testPerformLabelAction(self):
    """Test whether we can activate a label."""
    if not self.__class__.label1:
      self.testCreateLabels()
    action = {'type': 'ActivateLabels'}
    filter_statement = {'query': 'WHERE id = \'%s\''
                        % self.__class__.label1['id']}
    self.assert_(isinstance(
        self.__class__.service.PerformLabelAction(action, filter_statement),
        tuple))

  def testUpdateLabel(self):
    """Test whether we can update a label."""
    if not self.__class__.label1:
      self.testCreateLabels()
    self.__class__.label1['description'] = 'updated description'
    label = self.__class__.service.UpdateLabel(self.__class__.label1)
    self.assert_(isinstance(label, tuple))
    self.assertEqual(label[0]['description'],
                     self.__class__.label1['description'])

  def testUpdateLabels(self):
    """Test whether we can update a list of labels."""
    if not self.__class__.label1 or not self.__class__.label2:
      self.testCreateLabels()
    updated_description = 'updated description'
    self.__class__.label1['description'] = updated_description
    self.__class__.label2['description'] = updated_description
    labels = self.__class__.service.UpdateLabels([
        self.__class__.label1, self.__class__.label2])
    self.assert_(isinstance(labels, tuple))
    for label in labels:
      self.assertEqual(label['description'], updated_description)


def makeTestSuiteV201108():
  """Set up test suite using v201108.

  Returns:
    TestSuite test suite using v201108.
  """
  suite = unittest.TestSuite()
  suite.addTests(unittest.makeSuite(LabelServiceTestV201108))
  return suite


def makeTestSuiteV201111():
  """Set up test suite using v201111.

  Returns:
    TestSuite test suite using v201111.
  """
  suite = unittest.TestSuite()
  suite.addTests(unittest.makeSuite(LabelServiceTestV201111))
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
