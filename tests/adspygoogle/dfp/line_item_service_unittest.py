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

"""Unit tests to cover LineItemService."""

__author__ = 'api.sgrinberg@gmail.com (Stan Grinberg)'

from datetime import date
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


class LineItemServiceTestV201108(unittest.TestCase):

  """Unittest suite for LineItemService using v201108."""

  SERVER = SERVER_V201108
  VERSION = VERSION_V201108
  client.debug = False
  service = None
  order_id = '0'
  ad_unit_id = '0'
  line_item1 = None
  line_item2 = None

  def setUp(self):
    """Prepare unittest."""
    print self.id()
    if not self.__class__.service:
      self.__class__.service = client.GetLineItemService(
          self.__class__.SERVER, self.__class__.VERSION, HTTP_PROXY)

    if self.__class__.order_id == '0':
      company = {
          'name': 'Company #%s' % Utils.GetUniqueName(),
          'type': 'ADVERTISER'
      }
      advertiser_id = client.GetCompanyService(
          self.__class__.SERVER, self.__class__.VERSION,
          HTTP_PROXY).CreateCompany(company)[0]['id']
      filter_statement = {'query': 'ORDER BY name LIMIT 500'}
      users = client.GetUserService(
          self.__class__.SERVER, self.__class__.VERSION,
          HTTP_PROXY).GetUsersByStatement(filter_statement)
      trafficker_id = '0'
      for user in users[0]['results']:
        if user['roleName'] in ('Trafficker',):
          trafficker_id = user['id']
          break
      order = {
          'advertiserId': advertiser_id,
          'currencyCode': 'USD',
          'name': 'Order #%s' % Utils.GetUniqueName(),
          'traffickerId': trafficker_id
      }
      self.__class__.order_id = client.GetOrderService(
          self.__class__.SERVER, self.__class__.VERSION,
          HTTP_PROXY).CreateOrder(order)[0]['id']

    if self.__class__.ad_unit_id == '0':
      inventory_service = client.GetInventoryService(
          self.__class__.SERVER, self.__class__.VERSION,
          HTTP_PROXY)
      network_service = client.GetNetworkService(
          self.__class__.SERVER, self.__class__.VERSION,
          HTTP_PROXY)
      root_ad_unit_id = \
          network_service.GetCurrentNetwork()[0]['effectiveRootAdUnitId']
      ad_unit = {
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
          'description': 'Ad unit description.',
          'targetWindow': 'BLANK'
      }
      self.__class__.ad_unit_id = inventory_service.CreateAdUnit(
          ad_unit)[0]['id']

  def testCreateLineItem(self):
    """Test whether we can create a line item."""
    line_item = {
        'name': 'Line item #%s' % Utils.GetUniqueName(),
        'orderId': self.__class__.order_id,
        'targeting': {
            'inventoryTargeting': {
                'targetedAdUnitIds': [self.__class__.ad_unit_id]
            },
            'geoTargeting': {
                'targetedLocations': [
                    {
                        'id': '2840',
                        'xsi_type': 'CountryLocation',
                        'countryCode': 'US'
                    },
                    {
                        'id': '20123',
                        'xsi_type': 'RegionLocation',
                        'regionCode': 'CA-QC'
                    }
                ],
                'excludedLocations': [
                    {
                        'id': '1016367',
                        'xsi_type': 'CityLocation',
                        'cityName': 'Chicago',
                        'countryCode': 'US'
                    },
                    {
                        'id': '200501',
                        'xsi_type': 'MetroLocation',
                        'metroCode': '501'
                    }
                ]
            },
            'dayPartTargeting': {
                'dayParts': [
                    {
                        'dayOfWeek': 'TUESDAY',
                        'startTime': {
                            'hour': '10',
                            'minute': 'ZERO'
                        },
                        'endTime': {
                            'hour': '18',
                            'minute': 'THIRTY'
                        }
                    }
                ],
                'timeZone': 'PUBLISHER'
            },
            'userDomainTargeting': {
                'domains': ['google.com'],
                'targeted': 'false'
            },
            'technologyTargeting': {
                'browserTargeting': {
                    'browsers': [{'id': '500072'}],
                    'isTargeted': 'true'
                }
            }
        },
        'creativePlaceholders': [
            {
                'size': {
                    'width': '300',
                    'height': '250'
                }
            },
            {
                'size': {
                    'width': '120',
                    'height': '600'
                }
            }
        ],
        'lineItemType': 'STANDARD',
        'startDateTime': {
            'date': {
                'year': str(date.today().year + 1),
                'month': '9',
                'day': '1'
            },
            'hour': '0',
            'minute': '0',
            'second': '0'
        },
        'endDateTime': {
            'date': {
                'year': str(date.today().year + 1),
                'month': '9',
                'day': '30'
            },
            'hour': '0',
            'minute': '0',
            'second': '0'
        },
        'costType': 'CPM',
        'costPerUnit': {
            'currencyCode': 'USD',
            'microAmount': '2000000'
        },
        'creativeRotationType': 'EVEN',
        'discountType': 'PERCENTAGE',
        'unitsBought': '500000',
        'unitType': 'IMPRESSIONS'
    }
    self.assert_(isinstance(
        self.__class__.service.CreateLineItem(line_item), tuple))

  def testCreateLineItems(self):
    """Test whether we can create a list of line items."""
    line_items = [
        {
            'name': 'Line item #%s' % Utils.GetUniqueName(),
            'orderId': self.__class__.order_id,
            'targeting': {
                'inventoryTargeting': {
                    'targetedAdUnitIds': [self.__class__.ad_unit_id]
                },
                'geoTargeting': {
                    'targetedLocations': [
                        {
                            'id': '2840',
                            'xsi_type': 'CountryLocation',
                            'countryCode': 'US'
                        },
                        {
                            'id': '20123',
                            'xsi_type': 'RegionLocation',
                            'regionCode': 'CA-QC'
                        }
                    ],
                    'excludedLocations': [
                        {
                            'id': '1016367',
                            'xsi_type': 'CityLocation',
                            'cityName': 'Chicago',
                            'countryCode': 'US'
                        },
                        {
                            'id': '200501',
                            'xsi_type': 'MetroLocation',
                            'metroCode': '501'
                        }
                    ]
                }
            },
            'creativePlaceholders': [
                {
                    'size': {
                        'width': '300',
                        'height': '250'
                    }
                },
                {
                    'size': {
                        'width': '120',
                        'height': '600'
                    }
                }
            ],
            'lineItemType': 'STANDARD',
            'startDateTime': {
                'date': {
                    'year': str(date.today().year + 1),
                    'month': '9',
                    'day': '1'
                },
                'hour': '0',
                'minute': '0',
                'second': '0'
            },
            'endDateTime': {
                'date': {
                    'year': str(date.today().year + 1),
                    'month': '9',
                    'day': '30'
                },
                'hour': '0',
                'minute': '0',
                'second': '0'
            },
            'costType': 'CPM',
            'costPerUnit': {
                'currencyCode': 'USD',
                'microAmount': '2000000'
            },
            'creativeRotationType': 'EVEN',
            'discountType': 'PERCENTAGE',
            'unitsBought': '500000',
            'unitType': 'IMPRESSIONS'
        },
        {
            'name': 'Line item #%s' % Utils.GetUniqueName(),
            'orderId': self.__class__.order_id,
            'targeting': {
                'inventoryTargeting': {
                    'targetedAdUnitIds': [self.__class__.ad_unit_id]
                },
                'geoTargeting': {
                    'targetedLocations': [
                        {
                            'id': '2840',
                            'xsi_type': 'CountryLocation',
                            'countryCode': 'US'
                        },
                        {
                            'id': '20123',
                            'xsi_type': 'RegionLocation',
                            'regionCode': 'CA-QC'
                        }
                    ],
                    'excludedLocations': [
                        {
                            'id': '1016367',
                            'xsi_type': 'CityLocation',
                            'cityName': 'Chicago',
                            'countryCode': 'US'
                        },
                        {
                            'id': '200501',
                            'xsi_type': 'MetroLocation',
                            'metroCode': '501'
                        }
                    ]
                }
            },
            'creativePlaceholders': [
                {
                    'size': {
                        'width': '300',
                        'height': '250'
                    }
                },
                {
                    'size': {
                        'width': '120',
                        'height': '600'
                    }
                }
            ],
            'lineItemType': 'STANDARD',
            'startDateTime': {
                'date': {
                    'year': str(date.today().year + 1),
                    'month': '9',
                    'day': '1'
                },
                'hour': '0',
                'minute': '0',
                'second': '0'
            },
            'endDateTime': {
                'date': {
                    'year': str(date.today().year + 1),
                    'month': '9',
                    'day': '30'
                },
                'hour': '0',
                'minute': '0',
                'second': '0'
            },
            'costType': 'CPM',
            'costPerUnit': {
                'currencyCode': 'USD',
                'microAmount': '2000000'
            },
            'creativeRotationType': 'EVEN',
            'discountType': 'PERCENTAGE',
            'unitsBought': '500000',
            'unitType': 'IMPRESSIONS'
        }
    ]
    line_items = self.__class__.service.CreateLineItems(line_items)
    self.__class__.line_item1 = line_items[0]
    self.__class__.line_item2 = line_items[1]
    self.assert_(isinstance(line_items, tuple))

  def testGetLineItem(self):
    """Test whether we can fetch an existing line item."""
    if not self.__class__.line_item1:
      self.testCreateLineItems()
    self.assert_(isinstance(self.__class__.service.GetLineItem(
        self.__class__.line_item1['id']), tuple))

  def testGetLineItemsByStatement(self):
    """Test whether we can fetch a list of existing line items that match given
    statement."""
    if not self.__class__.line_item1:
      self.testCreateLineItems()
    filter_statement = {'query': 'WHERE orderId = \'%s\' LIMIT 500'
                        % self.__class__.order_id}
    self.assert_(isinstance(
        self.__class__.service.GetLineItemsByStatement(filter_statement),
        tuple))

  def testPerformLineItemAction(self):
    """Test whether we can activate a line item."""
    if not self.__class__.line_item1:
      self.testCreateLineItems()
    action = {'type': 'ActivateLineItems'}
    filter_statement = {'query': 'WHERE orderId = \'%s\' AND status = \'READY\''
                        % self.__class__.order_id}
    self.assert_(isinstance(
        self.__class__.service.PerformLineItemAction(action, filter_statement),
        tuple))

  def testUpdateLineItem(self):
    """Test whether we can update a line item."""
    if not self.__class__.line_item1:
      self.testCreateLineItems()
    self.__class__.line_item1['deliveryRateType'] = 'AS_FAST_AS_POSSIBLE'
    line_item = self.__class__.service.UpdateLineItem(
        self.__class__.line_item1)
    self.assert_(isinstance(line_item, tuple))
    self.assertEqual(line_item[0]['deliveryRateType'],
                     self.__class__.line_item1['deliveryRateType'])

  def testUpdateLineItems(self):
    """Test whether we can update a list of line items."""
    if not self.__class__.line_item1 or not self.__class__.line_item2:
      self.testCreateLineItems()
    amount = '3000000'
    self.__class__.line_item1['costPerUnit']['microAmount'] = amount
    self.__class__.line_item2['costPerUnit']['microAmount'] = amount
    line_items = self.__class__.service.UpdateLineItems([
        self.__class__.line_item1, self.__class__.line_item2])
    self.assert_(isinstance(line_items, tuple))
    for line_item in line_items:
      self.assertEqual(line_item['costPerUnit']['microAmount'], amount)


class LineItemServiceTestV201111(unittest.TestCase):

  """Unittest suite for LineItemService using v201111."""

  SERVER = SERVER_V201111
  VERSION = VERSION_V201111
  client.debug = False
  service = None
  order_id = '0'
  ad_unit_id = '0'
  line_item1 = None
  line_item2 = None

  def setUp(self):
    """Prepare unittest."""
    print self.id()
    if not self.__class__.service:
      self.__class__.service = client.GetLineItemService(
          self.__class__.SERVER, self.__class__.VERSION, HTTP_PROXY)

    if self.__class__.order_id == '0':
      company = {
          'name': 'Company #%s' % Utils.GetUniqueName(),
          'type': 'ADVERTISER',
          'creditStatus': 'ACTIVE'
      }
      advertiser_id = client.GetCompanyService(
          self.__class__.SERVER, self.__class__.VERSION,
          HTTP_PROXY).CreateCompany(company)[0]['id']
      filter_statement = {'query': 'ORDER BY name LIMIT 500'}
      users = client.GetUserService(
          self.__class__.SERVER, self.__class__.VERSION,
          HTTP_PROXY).GetUsersByStatement(filter_statement)
      trafficker_id = '0'
      for user in users[0]['results']:
        if user['roleName'] in ('Trafficker',):
          trafficker_id = user['id']
          break
      order = {
          'advertiserId': advertiser_id,
          'currencyCode': 'USD',
          'name': 'Order #%s' % Utils.GetUniqueName(),
          'traffickerId': trafficker_id
      }
      self.__class__.order_id = client.GetOrderService(
          self.__class__.SERVER, self.__class__.VERSION,
          HTTP_PROXY).CreateOrder(order)[0]['id']

    if self.__class__.ad_unit_id == '0':
      inventory_service = client.GetInventoryService(
          self.__class__.SERVER, self.__class__.VERSION,
          HTTP_PROXY)
      network_service = client.GetNetworkService(
          self.__class__.SERVER, self.__class__.VERSION,
          HTTP_PROXY)
      root_ad_unit_id = \
          network_service.GetCurrentNetwork()[0]['effectiveRootAdUnitId']
      ad_unit = {
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
          'description': 'Ad unit description.',
          'targetWindow': 'BLANK',
          'targetPlatform': 'WEB'
      }
      self.__class__.ad_unit_id = inventory_service.CreateAdUnit(
          ad_unit)[0]['id']

  def testCreateLineItem(self):
    """Test whether we can create a line item."""
    line_item = {
        'name': 'Line item #%s' % Utils.GetUniqueName(),
        'orderId': self.__class__.order_id,
        'targeting': {
            'inventoryTargeting': {
                'targetedAdUnits': [{'adUnitId': self.__class__.ad_unit_id}]
            },
            'geoTargeting': {
                'targetedLocations': [
                    {
                        'id': '2840',
                        'xsi_type': 'CountryLocation',
                        'countryCode': 'US'
                    },
                    {
                        'id': '20123',
                        'xsi_type': 'RegionLocation',
                        'regionCode': 'CA-QC'
                    }
                ],
                'excludedLocations': [
                    {
                        'id': '1016367',
                        'xsi_type': 'CityLocation',
                        'cityName': 'Chicago',
                        'countryCode': 'US'
                    },
                    {
                        'id': '200501',
                        'xsi_type': 'MetroLocation',
                        'metroCode': '501'
                    }
                ]
            },
            'dayPartTargeting': {
                'dayParts': [
                    {
                        'dayOfWeek': 'TUESDAY',
                        'startTime': {
                            'hour': '10',
                            'minute': 'ZERO'
                        },
                        'endTime': {
                            'hour': '18',
                            'minute': 'THIRTY'
                        }
                    }
                ],
                'timeZone': 'PUBLISHER'
            },
            'userDomainTargeting': {
                'domains': ['google.com'],
                'targeted': 'false'
            },
            'technologyTargeting': {
                'browserTargeting': {
                    'browsers': [{'id': '500072'}],
                    'isTargeted': 'true'
                }
            }
        },
        'creativePlaceholders': [
            {
                'size': {
                    'width': '300',
                    'height': '250'
                }
            },
            {
                'size': {
                    'width': '120',
                    'height': '600'
                }
            }
        ],
        'lineItemType': 'STANDARD',
        'startDateTime': {
            'date': {
                'year': str(date.today().year + 1),
                'month': '9',
                'day': '1'
            },
            'hour': '0',
            'minute': '0',
            'second': '0'
        },
        'endDateTime': {
            'date': {
                'year': str(date.today().year + 1),
                'month': '9',
                'day': '30'
            },
            'hour': '0',
            'minute': '0',
            'second': '0'
        },
        'costType': 'CPM',
        'costPerUnit': {
            'currencyCode': 'USD',
            'microAmount': '2000000'
        },
        'creativeRotationType': 'EVEN',
        'discountType': 'PERCENTAGE',
        'unitsBought': '500000',
        'unitType': 'IMPRESSIONS'
    }
    self.assert_(isinstance(
        self.__class__.service.CreateLineItem(line_item), tuple))

  def testCreateLineItems(self):
    """Test whether we can create a list of line items."""
    line_items = [
        {
            'name': 'Line item #%s' % Utils.GetUniqueName(),
            'orderId': self.__class__.order_id,
            'targeting': {
                'inventoryTargeting': {
                    'targetedAdUnits': [{'adUnitId': self.__class__.ad_unit_id}]
                },
                'geoTargeting': {
                    'targetedLocations': [
                        {
                            'id': '2840',
                            'xsi_type': 'CountryLocation',
                            'countryCode': 'US'
                        },
                        {
                            'id': '20123',
                            'xsi_type': 'RegionLocation',
                            'regionCode': 'CA-QC'
                        }
                    ],
                    'excludedLocations': [
                        {
                            'id': '1016367',
                            'xsi_type': 'CityLocation',
                            'cityName': 'Chicago',
                            'countryCode': 'US'
                        },
                        {
                            'id': '200501',
                            'xsi_type': 'MetroLocation',
                            'metroCode': '501'
                        }
                    ]
                }
            },
            'creativePlaceholders': [
                {
                    'size': {
                        'width': '300',
                        'height': '250'
                    }
                },
                {
                    'size': {
                        'width': '120',
                        'height': '600'
                    }
                }
            ],
            'lineItemType': 'STANDARD',
            'startDateTime': {
                'date': {
                    'year': str(date.today().year + 1),
                    'month': '9',
                    'day': '1'
                },
                'hour': '0',
                'minute': '0',
                'second': '0'
            },
            'endDateTime': {
                'date': {
                    'year': str(date.today().year + 1),
                    'month': '9',
                    'day': '30'
                },
                'hour': '0',
                'minute': '0',
                'second': '0'
            },
            'costType': 'CPM',
            'costPerUnit': {
                'currencyCode': 'USD',
                'microAmount': '2000000'
            },
            'creativeRotationType': 'EVEN',
            'discountType': 'PERCENTAGE',
            'unitsBought': '500000',
            'unitType': 'IMPRESSIONS'
        },
        {
            'name': 'Line item #%s' % Utils.GetUniqueName(),
            'orderId': self.__class__.order_id,
            'targeting': {
                'inventoryTargeting': {
                    'targetedAdUnits': [{'adUnitId': self.__class__.ad_unit_id}]
                },
                'geoTargeting': {
                    'targetedLocations': [
                        {
                            'id': '2840',
                            'xsi_type': 'CountryLocation',
                            'countryCode': 'US'
                        },
                        {
                            'id': '20123',
                            'xsi_type': 'RegionLocation',
                            'regionCode': 'CA-QC'
                        }
                    ],
                    'excludedLocations': [
                        {
                            'id': '1016367',
                            'xsi_type': 'CityLocation',
                            'cityName': 'Chicago',
                            'countryCode': 'US'
                        },
                        {
                            'id': '200501',
                            'xsi_type': 'MetroLocation',
                            'metroCode': '501'
                        }
                    ]
                }
            },
            'creativePlaceholders': [
                {
                    'size': {
                        'width': '300',
                        'height': '250'
                    }
                },
                {
                    'size': {
                        'width': '120',
                        'height': '600'
                    }
                }
            ],
            'lineItemType': 'STANDARD',
            'startDateTime': {
                'date': {
                    'year': str(date.today().year + 1),
                    'month': '9',
                    'day': '1'
                },
                'hour': '0',
                'minute': '0',
                'second': '0'
            },
            'endDateTime': {
                'date': {
                    'year': str(date.today().year + 1),
                    'month': '9',
                    'day': '30'
                },
                'hour': '0',
                'minute': '0',
                'second': '0'
            },
            'costType': 'CPM',
            'costPerUnit': {
                'currencyCode': 'USD',
                'microAmount': '2000000'
            },
            'creativeRotationType': 'EVEN',
            'discountType': 'PERCENTAGE',
            'unitsBought': '500000',
            'unitType': 'IMPRESSIONS'
        }
    ]
    line_items = self.__class__.service.CreateLineItems(line_items)
    self.__class__.line_item1 = line_items[0]
    self.__class__.line_item2 = line_items[1]
    self.assert_(isinstance(line_items, tuple))

  def testGetLineItem(self):
    """Test whether we can fetch an existing line item."""
    if not self.__class__.line_item1:
      self.testCreateLineItems()
    self.assert_(isinstance(self.__class__.service.GetLineItem(
        self.__class__.line_item1['id']), tuple))

  def testGetLineItemsByStatement(self):
    """Test whether we can fetch a list of existing line items that match given
    statement."""
    if not self.__class__.line_item1:
      self.testCreateLineItems()
    filter_statement = {'query': 'WHERE orderId = \'%s\' LIMIT 500'
                        % self.__class__.order_id}
    self.assert_(isinstance(
        self.__class__.service.GetLineItemsByStatement(filter_statement),
        tuple))

  def testPerformLineItemAction(self):
    """Test whether we can activate a line item."""
    if not self.__class__.line_item1:
      self.testCreateLineItems()
    action = {'type': 'ActivateLineItems'}
    filter_statement = {'query': 'WHERE orderId = \'%s\' AND status = \'READY\''
                        % self.__class__.order_id}
    self.assert_(isinstance(
        self.__class__.service.PerformLineItemAction(action, filter_statement),
        tuple))

  def testUpdateLineItem(self):
    """Test whether we can update a line item."""
    if not self.__class__.line_item1:
      self.testCreateLineItems()
    self.__class__.line_item1['deliveryRateType'] = 'AS_FAST_AS_POSSIBLE'
    line_item = self.__class__.service.UpdateLineItem(
        self.__class__.line_item1)
    self.assert_(isinstance(line_item, tuple))
    self.assertEqual(line_item[0]['deliveryRateType'],
                     self.__class__.line_item1['deliveryRateType'])

  def testUpdateLineItems(self):
    """Test whether we can update a list of line items."""
    if not self.__class__.line_item1 or not self.__class__.line_item2:
      self.testCreateLineItems()
    amount = '3000000'
    self.__class__.line_item1['costPerUnit']['microAmount'] = amount
    self.__class__.line_item2['costPerUnit']['microAmount'] = amount
    line_items = self.__class__.service.UpdateLineItems([
        self.__class__.line_item1, self.__class__.line_item2])
    self.assert_(isinstance(line_items, tuple))
    for line_item in line_items:
      self.assertEqual(line_item['costPerUnit']['microAmount'], amount)


def makeTestSuiteV201108():
  """Set up test suite using v201108.

  Returns:
    TestSuite test suite using v201108.
  """
  suite = unittest.TestSuite()
  suite.addTests(unittest.makeSuite(LineItemServiceTestV201108))
  return suite


def makeTestSuiteV201111():
  """Set up test suite using v201111.

  Returns:
    TestSuite test suite using v201111.
  """
  suite = unittest.TestSuite()
  suite.addTests(unittest.makeSuite(LineItemServiceTestV201111))
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
