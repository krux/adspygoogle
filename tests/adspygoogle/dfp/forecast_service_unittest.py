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

"""Unit tests to cover ForecastService."""

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


class ForecastServiceTestV201108(unittest.TestCase):

  """Unittest suite for ForecastService using v201108."""

  SERVER = SERVER_V201108
  VERSION = VERSION_V201108
  client.debug = False
  service = None
  order_id = '0'
  ad_unit_id = '0'
  line_item_id = '0'

  def setUp(self):
    """Prepare unittest."""
    print self.id()
    if not self.__class__.service:
      self.__class__.service = client.GetForecastService(
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
      filter_statement = {'query': 'WHERE parentId IS NULL LIMIT 500'}
      root_ad_unit_id = inventory_service.GetAdUnitsByStatement(
          filter_statement)[0]['results'][0]['id']
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

    if self.__class__.line_item_id == '0':
      line_item_service = client.GetLineItemService(
          self.__class__.SERVER, self.__class__.VERSION,
          HTTP_PROXY)
      line_item = {
          'name': 'Line item #%s' % Utils.GetUniqueName(),
          'orderId': self.__class__.order_id,
          'targeting': {
              'inventoryTargeting': {
                  'targetedAdUnitIds': [self.__class__.ad_unit_id]
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
      self.__class__.line_item_id = line_item_service.CreateLineItem(
          line_item)[0]['id']

  def testGetForecast(self):
    """Test whether we can get a forecast for given line item."""
    line_item = {
        'name': 'Line item #%s' % Utils.GetUniqueName(),
        'orderId': self.__class__.order_id,
        'targeting': {
            'inventoryTargeting': {
                'targetedAdUnitIds': [self.__class__.ad_unit_id]
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
    self.assert_(isinstance(self.__class__.service.GetForecast(
        line_item), tuple))

  def testGetForecastById(self):
    """Test whether we can get a forecast for existing line item."""
    self.assert_(isinstance(self.__class__.service.GetForecastById(
        self.__class__.line_item_id), tuple))


class ForecastServiceTestV201111(unittest.TestCase):

  """Unittest suite for ForecastService using v201111."""

  SERVER = SERVER_V201111
  VERSION = VERSION_V201111
  client.debug = False
  service = None
  order_id = '0'
  ad_unit_id = '0'
  line_item_id = '0'

  def setUp(self):
    """Prepare unittest."""
    print self.id()
    if not self.__class__.service:
      self.__class__.service = client.GetForecastService(
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
      filter_statement = {'query': 'WHERE parentId IS NULL LIMIT 500'}
      root_ad_unit_id = inventory_service.GetAdUnitsByStatement(
          filter_statement)[0]['results'][0]['id']
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

    if self.__class__.line_item_id == '0':
      line_item_service = client.GetLineItemService(
          self.__class__.SERVER, self.__class__.VERSION,
          HTTP_PROXY)
      line_item = {
          'name': 'Line item #%s' % Utils.GetUniqueName(),
          'orderId': self.__class__.order_id,
          'targeting': {
              'inventoryTargeting': {
                  'targetedAdUnitIds': [self.__class__.ad_unit_id]
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
      self.__class__.line_item_id = line_item_service.CreateLineItem(
          line_item)[0]['id']

  def testGetForecast(self):
    """Test whether we can get a forecast for given line item."""
    line_item = {
        'name': 'Line item #%s' % Utils.GetUniqueName(),
        'orderId': self.__class__.order_id,
        'targeting': {
            'inventoryTargeting': {
                'targetedAdUnitIds': [self.__class__.ad_unit_id]
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
    self.assert_(isinstance(self.__class__.service.GetForecast(
        line_item), tuple))

  def testGetForecastById(self):
    """Test whether we can get a forecast for existing line item."""
    self.assert_(isinstance(self.__class__.service.GetForecastById(
        self.__class__.line_item_id), tuple))


def makeTestSuiteV201108():
  """Set up test suite using v201108.

  Returns:
    TestSuite test suite using v201108.
  """
  suite = unittest.TestSuite()
  suite.addTests(unittest.makeSuite(ForecastServiceTestV201108))
  return suite


def makeTestSuiteV201111():
  """Set up test suite using v201111.

  Returns:
    TestSuite test suite using v201111.
  """
  suite = unittest.TestSuite()
  suite.addTests(unittest.makeSuite(ForecastServiceTestV201111))
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
