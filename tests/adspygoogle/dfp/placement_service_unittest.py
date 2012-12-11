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

"""Unit tests to cover PlacementService."""

__author__ = 'api.sgrinberg@gmail.com (Stan Grinberg)'

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


class PlacementServiceTestV201108(unittest.TestCase):

  """Unittest suite for PlacementService using v201108."""

  SERVER = SERVER_V201108
  VERSION = VERSION_V201108
  client.debug = False
  service = None
  ad_unit_id1 = '0'
  ad_unit_id2 = '0'
  ad_unit_id3 = '0'
  ad_unit_id4 = '0'
  placement1 = None
  placement2 = None

  def setUp(self):
    """Prepare unittest."""
    print self.id()
    if not self.__class__.service:
      self.__class__.service = client.GetPlacementService(
          self.__class__.SERVER, self.__class__.VERSION, HTTP_PROXY)

    if self.__class__.ad_unit_id1 == '0' or self.__class__.ad_unit_id2 == '0':
      inventory_service = client.GetInventoryService(
          self.__class__.SERVER, self.__class__.VERSION, HTTP_PROXY)
      network_service = client.GetNetworkService(
          self.__class__.SERVER, self.__class__.VERSION,
          HTTP_PROXY)
      root_ad_unit_id = \
          network_service.GetCurrentNetwork()[0]['effectiveRootAdUnitId']
      ad_units = [
          {
              'name': 'Ad_Unit_%s' % Utils.GetUniqueName(),
              'parentId': root_ad_unit_id,
              'adUnitSizes': [
                  {
                      'size': {
                          'width': '300',
                          'height': '250'
                      }
                  }
              ]
          },
          {
              'name': 'Ad_Unit_%s' % Utils.GetUniqueName(),
              'parentId': root_ad_unit_id,
              'adUnitSizes': [
                  {
                      'size': {
                          'width': '300',
                          'height': '250'
                      }
                  }
              ]
          },
          {
              'name': 'Ad_Unit_%s' % Utils.GetUniqueName(),
              'parentId': root_ad_unit_id,
              'adUnitSizes': [
                  {
                      'size': {
                          'width': '300',
                          'height': '250'
                      }
                  }
              ]
          },
          {
              'name': 'Ad_Unit_%s' % Utils.GetUniqueName(),
              'parentId': root_ad_unit_id,
              'adUnitSizes': [
                  {
                      'size': {
                          'width': '300',
                          'height': '250'
                      }
                  }
              ]
          }
      ]
      ad_units = inventory_service.CreateAdUnits(ad_units)
      self.__class__.ad_unit_id1 = ad_units[0]['id']
      self.__class__.ad_unit_id2 = ad_units[1]['id']
      self.__class__.ad_unit_id3 = ad_units[2]['id']
      self.__class__.ad_unit_id4 = ad_units[3]['id']

  def testCreatePlacement(self):
    """Test whether we can create a placement."""
    placement = {
        'name': 'Placement #%s' % Utils.GetUniqueName(),
        'description': 'Description.',
        'targetedAdUnitIds': [self.__class__.ad_unit_id1,
                              self.__class__.ad_unit_id2]
    }
    self.assert_(isinstance(
        self.__class__.service.CreatePlacement(placement), tuple))

  def testCreatePlacements(self):
    """Test whether we can create a list of placements items."""
    placements = [
        {
            'name': 'Placement #%s' % Utils.GetUniqueName(),
            'description': 'Description.',
            'targetedAdUnitIds': [self.__class__.ad_unit_id1,
                                  self.__class__.ad_unit_id2]
        },
        {
            'name': 'Placement #%s' % Utils.GetUniqueName(),
            'description': 'Description.',
            'targetedAdUnitIds': [self.__class__.ad_unit_id1,
                                  self.__class__.ad_unit_id2]
        }
    ]
    placements = self.__class__.service.CreatePlacements(placements)
    self.assert_(isinstance(placements, tuple))
    self.__class__.placement1 = placements[0]
    self.__class__.placement2 = placements[1]

  def testGetPlacement(self):
    """Test whether we can fetch an existing placement."""
    if not self.__class__.placement1:
      self.testCreatePlacements()
    self.assert_(isinstance(self.__class__.service.GetPlacement(
        self.__class__.placement1['id']), tuple))

  def testGetPlacementsByStatement(self):
    """Test whether we can fetch a list of existing placements that match given
    statement."""
    if not self.__class__.placement1:
      self.testCreatePlacements()
    filter_statement = {'query': 'WHERE id = \'%s\' ORDER BY name LIMIT 1'
                        % self.__class__.placement1['id']}
    self.assert_(isinstance(
        self.__class__.service.GetPlacementsByStatement(filter_statement),
        tuple))

  def testPerformPlacementAction(self):
    """Test whether we can deactivate a placement."""
    if not self.__class__.placement1:
      self.testCreatePlacements()
    action = {'type': 'DeactivatePlacements'}
    filter_statement = {'query': 'WHERE status = \'ACTIVE\''}
    self.assert_(isinstance(
        self.__class__.service.PerformPlacementAction(action, filter_statement),
        tuple))

  def testUpdatePlacement(self):
    """Test whether we can update a placement."""
    if not self.__class__.placement1:
      self.testCreatePlacements()

    self.__class__.placement1['description'] += ' More description.'
    placement = self.__class__.service.UpdatePlacement(
        self.__class__.placement1)
    self.assert_(isinstance(placement, tuple))
    self.assertEqual(placement[0]['description'],
                     self.__class__.placement1['description'])

    self.__class__.placement1['targetedAdUnitIds'].append(
        self.__class__.ad_unit_id3)
    placement = self.__class__.service.UpdatePlacement(
        self.__class__.placement1)
    self.assert_(isinstance(placement, tuple))

  def testUpdatePlacements(self):
    """Test whether we can update a list of placements."""
    if not self.__class__.placement1 or not self.__class__.placement2:
      self.testCreatePlacements()

    self.__class__.placement1['description'] += ' Even more description.'
    self.__class__.placement2['description'] += ' Even more description.'
    placements = self.__class__.service.UpdatePlacements([
        self.__class__.placement1, self.__class__.placement2])
    self.assert_(isinstance(placements, tuple))

    self.__class__.placement1['targetedAdUnitIds'].append(
        self.__class__.ad_unit_id4)
    self.__class__.placement2['targetedAdUnitIds'].append(
        self.__class__.ad_unit_id4)
    placements = self.__class__.service.UpdatePlacements([
        self.__class__.placement1, self.__class__.placement2])
    self.assert_(isinstance(placements, tuple))


class PlacementServiceTestV201111(unittest.TestCase):

  """Unittest suite for PlacementService using v201111."""

  SERVER = SERVER_V201111
  VERSION = VERSION_V201111
  client.debug = False
  service = None
  ad_unit_id1 = '0'
  ad_unit_id2 = '0'
  ad_unit_id3 = '0'
  ad_unit_id4 = '0'
  placement1 = None
  placement2 = None

  def setUp(self):
    """Prepare unittest."""
    print self.id()
    if not self.__class__.service:
      self.__class__.service = client.GetPlacementService(
          self.__class__.SERVER, self.__class__.VERSION, HTTP_PROXY)

    if self.__class__.ad_unit_id1 == '0' or self.__class__.ad_unit_id2 == '0':
      inventory_service = client.GetInventoryService(
          self.__class__.SERVER, self.__class__.VERSION, HTTP_PROXY)
      network_service = client.GetNetworkService(
          self.__class__.SERVER, self.__class__.VERSION,
          HTTP_PROXY)
      root_ad_unit_id = \
          network_service.GetCurrentNetwork()[0]['effectiveRootAdUnitId']
      ad_units = [
          {
              'name': 'Ad_Unit_%s' % Utils.GetUniqueName(),
              'parentId': root_ad_unit_id,
              'adUnitSizes': [
                  {
                      'size': {
                          'width': '300',
                          'height': '250'
                      }
                  }
              ],
              'targetPlatform': 'WEB'
          },
          {
              'name': 'Ad_Unit_%s' % Utils.GetUniqueName(),
              'parentId': root_ad_unit_id,
              'adUnitSizes': [
                  {
                      'size': {
                          'width': '300',
                          'height': '250'
                      }
                  }
              ],
              'targetPlatform': 'WEB'
          },
          {
              'name': 'Ad_Unit_%s' % Utils.GetUniqueName(),
              'parentId': root_ad_unit_id,
              'adUnitSizes': [
                  {
                      'size': {
                          'width': '300',
                          'height': '250'
                      }
                  }
              ],
              'targetPlatform': 'WEB'
          },
          {
              'name': 'Ad_Unit_%s' % Utils.GetUniqueName(),
              'parentId': root_ad_unit_id,
              'adUnitSizes': [
                  {
                      'size': {
                          'width': '300',
                          'height': '250'
                      }
                  }
              ],
              'targetPlatform': 'WEB'
          }
      ]
      ad_units = inventory_service.CreateAdUnits(ad_units)
      self.__class__.ad_unit_id1 = ad_units[0]['id']
      self.__class__.ad_unit_id2 = ad_units[1]['id']
      self.__class__.ad_unit_id3 = ad_units[2]['id']
      self.__class__.ad_unit_id4 = ad_units[3]['id']

  def testCreatePlacement(self):
    """Test whether we can create a placement."""
    placement = {
        'name': 'Placement #%s' % Utils.GetUniqueName(),
        'description': 'Description.',
        'targetedAdUnitIds': [self.__class__.ad_unit_id1,
                              self.__class__.ad_unit_id2]
    }
    self.assert_(isinstance(
        self.__class__.service.CreatePlacement(placement), tuple))

  def testCreatePlacements(self):
    """Test whether we can create a list of placements items."""
    placements = [
        {
            'name': 'Placement #%s' % Utils.GetUniqueName(),
            'description': 'Description.',
            'targetedAdUnitIds': [self.__class__.ad_unit_id1,
                                  self.__class__.ad_unit_id2]
        },
        {
            'name': 'Placement #%s' % Utils.GetUniqueName(),
            'description': 'Description.',
            'targetedAdUnitIds': [self.__class__.ad_unit_id1,
                                  self.__class__.ad_unit_id2]
        }
    ]
    placements = self.__class__.service.CreatePlacements(placements)
    self.assert_(isinstance(placements, tuple))
    self.__class__.placement1 = placements[0]
    self.__class__.placement2 = placements[1]

  def testGetPlacement(self):
    """Test whether we can fetch an existing placement."""
    if not self.__class__.placement1:
      self.testCreatePlacements()
    self.assert_(isinstance(self.__class__.service.GetPlacement(
        self.__class__.placement1['id']), tuple))

  def testGetPlacementsByStatement(self):
    """Test whether we can fetch a list of existing placements that match given
    statement."""
    if not self.__class__.placement1:
      self.testCreatePlacements()
    filter_statement = {'query': 'WHERE id = \'%s\' ORDER BY name LIMIT 1'
                        % self.__class__.placement1['id']}
    self.assert_(isinstance(
        self.__class__.service.GetPlacementsByStatement(filter_statement),
        tuple))

  def testPerformPlacementAction(self):
    """Test whether we can deactivate a placement."""
    if not self.__class__.placement1:
      self.testCreatePlacements()
    action = {'type': 'DeactivatePlacements'}
    filter_statement = {'query': 'WHERE status = \'ACTIVE\''}
    self.assert_(isinstance(
        self.__class__.service.PerformPlacementAction(action, filter_statement),
        tuple))

  def testUpdatePlacement(self):
    """Test whether we can update a placement."""
    if not self.__class__.placement1:
      self.testCreatePlacements()

    self.__class__.placement1['description'] += ' More description.'
    placement = self.__class__.service.UpdatePlacement(
        self.__class__.placement1)
    self.assert_(isinstance(placement, tuple))
    self.assertEqual(placement[0]['description'],
                     self.__class__.placement1['description'])

    self.__class__.placement1['targetedAdUnitIds'].append(
        self.__class__.ad_unit_id3)
    placement = self.__class__.service.UpdatePlacement(
        self.__class__.placement1)
    self.assert_(isinstance(placement, tuple))

  def testUpdatePlacements(self):
    """Test whether we can update a list of placements."""
    if not self.__class__.placement1 or not self.__class__.placement2:
      self.testCreatePlacements()

    self.__class__.placement1['description'] += ' Even more description.'
    self.__class__.placement2['description'] += ' Even more description.'
    placements = self.__class__.service.UpdatePlacements([
        self.__class__.placement1, self.__class__.placement2])
    self.assert_(isinstance(placements, tuple))

    self.__class__.placement1['targetedAdUnitIds'].append(
        self.__class__.ad_unit_id4)
    self.__class__.placement2['targetedAdUnitIds'].append(
        self.__class__.ad_unit_id4)
    placements = self.__class__.service.UpdatePlacements([
        self.__class__.placement1, self.__class__.placement2])
    self.assert_(isinstance(placements, tuple))


def makeTestSuiteV201108():
  """Set up test suite using v201108.

  Returns:
    TestSuite test suite using v201108.
  """
  suite = unittest.TestSuite()
  suite.addTests(unittest.makeSuite(PlacementServiceTestV201108))
  return suite


def makeTestSuiteV201111():
  """Set up test suite using v201111.

  Returns:
    TestSuite test suite using v201111.
  """
  suite = unittest.TestSuite()
  suite.addTests(unittest.makeSuite(PlacementServiceTestV201111))
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
