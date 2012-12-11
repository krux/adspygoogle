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

"""Unit tests to cover OrderService."""

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


class OrderServiceTestV201108(unittest.TestCase):

  """Unittest suite for OrderService using v201108."""

  SERVER = SERVER_V201108
  VERSION = VERSION_V201108
  client.debug = False
  service = None
  advertiser_id = '0'
  salesperson_id = '0'
  trafficker_id = '0'
  order1 = None
  order2 = None

  def setUp(self):
    """Prepare unittest."""
    print self.id()
    if not self.__class__.service:
      self.__class__.service = client.GetOrderService(
          self.__class__.SERVER, self.__class__.VERSION, HTTP_PROXY)

    if self.__class__.advertiser_id == '0':
      company = {
          'name': 'Company #%s' % Utils.GetUniqueName(),
          'type': 'ADVERTISER'
      }
      self.__class__.advertiser_id = client.GetCompanyService(
          self.__class__.SERVER, self.__class__.VERSION,
          HTTP_PROXY).CreateCompany(company)[0]['id']

    if self.__class__.trafficker_id == '0':
      filter_statement = {'query': 'ORDER BY name LIMIT 500'}
      users = client.GetUserService(
          self.__class__.SERVER, self.__class__.VERSION,
          HTTP_PROXY).GetUsersByStatement(filter_statement)
      for user in users[0]['results']:
        if user['roleName'] in ('Salesperson',):
          self.__class__.salesperson_id = user['id']
          continue
        elif user['roleName'] in ('Trafficker',):
          self.__class__.trafficker_id = user['id']
          continue

  def testCreateOrder(self):
    """Test whether we can create an order."""
    order = {
        'advertiserId': self.__class__.advertiser_id,
        'currencyCode': 'USD',
        'name': 'Order #%s' % Utils.GetUniqueName(),
        'traffickerId': self.__class__.trafficker_id
    }
    self.assert_(isinstance(
        self.__class__.service.CreateOrder(order), tuple))

  def testCreateOrders(self):
    """Test whether we can create a list of orders."""
    orders = [
        {
            'advertiserId': self.__class__.advertiser_id,
            'currencyCode': 'USD',
            'name': 'Order #%s' % Utils.GetUniqueName(),
            'traffickerId': self.__class__.trafficker_id
        },
        {
            'advertiserId': self.__class__.advertiser_id,
            'currencyCode': 'USD',
            'name': 'Order #%s' % Utils.GetUniqueName(),
            'traffickerId': self.__class__.trafficker_id
        }
    ]
    orders = self.__class__.service.CreateOrders(orders)
    self.__class__.order1 = orders[0]
    self.__class__.order2 = orders[1]
    self.assert_(isinstance(orders, tuple))

  def testGetOrder(self):
    """Test whether we can fetch an existing order."""
    if not self.__class__.order1:
      self.testCreateOrders()
    self.assert_(isinstance(self.__class__.service.GetOrder(
        self.__class__.order1['id']), tuple))

  def testGetOrdersByStatement(self):
    """Test whether we can fetch a list of existing orders that match given
    statement."""
    if not self.__class__.order1:
      self.testCreateOrders()
    filter_statement = {'query': 'WHERE advertiserId = \'%s\' LIMIT 500'
                        % self.__class__.advertiser_id}
    self.assert_(isinstance(
        self.__class__.service.GetOrdersByStatement(filter_statement),
        tuple))

  def testPerformOrderAction(self):
    """Test whether we can approve order."""
    action = {'type': 'ApproveOrders'}
    filter_statement = {'query': 'WHERE status = \'DRAFT\''}
    self.assert_(isinstance(
        self.__class__.service.PerformOrderAction(action, filter_statement),
        tuple))

  def testUpdateOrder(self):
    """Test whether we can update an order."""
    if not self.__class__.order1:
      self.testCreateOrders()
    notes = 'Spoke to advertiser. All is well.'
    self.__class__.order1['notes'] = notes
    order = self.__class__.service.UpdateOrder(self.__class__.order1)
    self.assert_(isinstance(order, tuple))
    self.assertEqual(order[0]['notes'], notes)

  def testUpdateOrders(self):
    """Test whether we can update a list of orders."""
    if not self.__class__.order1 or not self.__class__.order2:
      self.testCreateOrders()
    notes = 'Spoke to advertiser. All is well.'
    self.__class__.order1['notes'] = notes
    self.__class__.order2['notes'] = notes
    orders = self.__class__.service.UpdateOrders([self.__class__.order1,
                                                  self.__class__.order2])
    self.assert_(isinstance(orders, tuple))
    for order in orders:
      self.assertEqual(order['notes'], notes)


class OrderServiceTestV201111(unittest.TestCase):

  """Unittest suite for OrderService using v201111."""

  SERVER = SERVER_V201111
  VERSION = VERSION_V201111
  client.debug = False
  service = None
  advertiser_id = '0'
  salesperson_id = '0'
  trafficker_id = '0'
  order1 = None
  order2 = None

  def setUp(self):
    """Prepare unittest."""
    print self.id()
    if not self.__class__.service:
      self.__class__.service = client.GetOrderService(
          self.__class__.SERVER, self.__class__.VERSION, HTTP_PROXY)

    if self.__class__.advertiser_id == '0':
      company = {
          'name': 'Company #%s' % Utils.GetUniqueName(),
          'type': 'ADVERTISER',
          'creditStatus': 'ACTIVE'
      }
      self.__class__.advertiser_id = client.GetCompanyService(
          self.__class__.SERVER, self.__class__.VERSION,
          HTTP_PROXY).CreateCompany(company)[0]['id']

    if self.__class__.trafficker_id == '0':
      filter_statement = {'query': 'ORDER BY name LIMIT 500'}
      users = client.GetUserService(
          self.__class__.SERVER, self.__class__.VERSION,
          HTTP_PROXY).GetUsersByStatement(filter_statement)
      for user in users[0]['results']:
        if user['roleName'] in ('Salesperson',):
          self.__class__.salesperson_id = user['id']
          continue
        elif user['roleName'] in ('Trafficker',):
          self.__class__.trafficker_id = user['id']
          continue

  def testCreateOrder(self):
    """Test whether we can create an order."""
    order = {
        'advertiserId': self.__class__.advertiser_id,
        'currencyCode': 'USD',
        'name': 'Order #%s' % Utils.GetUniqueName(),
        'traffickerId': self.__class__.trafficker_id
    }
    self.assert_(isinstance(
        self.__class__.service.CreateOrder(order), tuple))

  def testCreateOrders(self):
    """Test whether we can create a list of orders."""
    orders = [
        {
            'advertiserId': self.__class__.advertiser_id,
            'currencyCode': 'USD',
            'name': 'Order #%s' % Utils.GetUniqueName(),
            'traffickerId': self.__class__.trafficker_id
        },
        {
            'advertiserId': self.__class__.advertiser_id,
            'currencyCode': 'USD',
            'name': 'Order #%s' % Utils.GetUniqueName(),
            'traffickerId': self.__class__.trafficker_id
        }
    ]
    orders = self.__class__.service.CreateOrders(orders)
    self.__class__.order1 = orders[0]
    self.__class__.order2 = orders[1]
    self.assert_(isinstance(orders, tuple))

  def testGetOrder(self):
    """Test whether we can fetch an existing order."""
    if not self.__class__.order1:
      self.testCreateOrders()
    self.assert_(isinstance(self.__class__.service.GetOrder(
        self.__class__.order1['id']), tuple))

  def testGetOrdersByStatement(self):
    """Test whether we can fetch a list of existing orders that match given
    statement."""
    if not self.__class__.order1:
      self.testCreateOrders()
    filter_statement = {'query': 'WHERE advertiserId = \'%s\' LIMIT 500'
                        % self.__class__.advertiser_id}
    self.assert_(isinstance(
        self.__class__.service.GetOrdersByStatement(filter_statement),
        tuple))

  def testPerformOrderAction(self):
    """Test whether we can approve order."""
    action = {'type': 'ApproveOrders'}
    filter_statement = {'query': 'WHERE status = \'DRAFT\''}
    self.assert_(isinstance(
        self.__class__.service.PerformOrderAction(action, filter_statement),
        tuple))

  def testUpdateOrder(self):
    """Test whether we can update an order."""
    if not self.__class__.order1:
      self.testCreateOrders()
    notes = 'Spoke to advertiser. All is well.'
    self.__class__.order1['notes'] = notes
    order = self.__class__.service.UpdateOrder(self.__class__.order1)
    self.assert_(isinstance(order, tuple))
    self.assertEqual(order[0]['notes'], notes)

  def testUpdateOrders(self):
    """Test whether we can update a list of orders."""
    if not self.__class__.order1 or not self.__class__.order2:
      self.testCreateOrders()
    notes = 'Spoke to advertiser. All is well.'
    self.__class__.order1['notes'] = notes
    self.__class__.order2['notes'] = notes
    orders = self.__class__.service.UpdateOrders([self.__class__.order1,
                                                  self.__class__.order2])
    self.assert_(isinstance(orders, tuple))
    for order in orders:
      self.assertEqual(order['notes'], notes)


def makeTestSuiteV201108():
  """Set up test suite using v201108.

  Returns:
    TestSuite test suite using v201108.
  """
  suite = unittest.TestSuite()
  suite.addTests(unittest.makeSuite(OrderServiceTestV201108))
  return suite


def makeTestSuiteV201111():
  """Set up test suite using v201111.

  Returns:
    TestSuite test suite using v201111.
  """
  suite = unittest.TestSuite()
  suite.addTests(unittest.makeSuite(OrderServiceTestV201111))
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
