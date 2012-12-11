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

"""Unit tests to cover CreativeService."""

__author__ = 'api.sgrinberg@gmail.com (Stan Grinberg)'

import base64
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


class CreativeServiceTestV201108(unittest.TestCase):

  """Unittest suite for CreativeService using v201108."""

  SERVER = SERVER_V201108
  VERSION = VERSION_V201108
  client.debug = False
  service = None
  advertiser_id = '0'
  creative1 = None
  creative2 = None
  IMAGE_DATA1 = open(os.path.join('data', 'medium_rectangle.jpg').replace(
      '\\', '/'), 'r').read()
  IMAGE_DATA2 = open(os.path.join('data', 'inline.jpg').replace(
      '\\', '/'), 'r').read()
  IMAGE_DATA3 = open(os.path.join('data', 'skyscraper.jpg').replace(
      '\\', '/'), 'r').read()
  IMAGE_DATA1 = base64.encodestring(IMAGE_DATA1)
  IMAGE_DATA2 = base64.encodestring(IMAGE_DATA2)
  IMAGE_DATA3 = base64.encodestring(IMAGE_DATA3)

  def setUp(self):
    """Prepare unittest."""
    print self.id()
    if not self.__class__.service:
      self.__class__.service = client.GetCreativeService(
          self.__class__.SERVER, self.__class__.VERSION, HTTP_PROXY)

    if self.__class__.advertiser_id == '0':
      company = {
          'name': 'Company #%s' % Utils.GetUniqueName(),
          'type': 'ADVERTISER'
      }
      company_service = client.GetCompanyService(
          self.__class__.SERVER, self.__class__.VERSION, HTTP_PROXY)
      self.__class__.advertiser_id = company_service.CreateCompany(
          company)[0]['id']

  def testCreateCreative(self):
    """Test whether we can create a creative."""
    creative = {
        'type': 'ImageCreative',
        'name': 'Image Creative #%s' % Utils.GetUniqueName(),
        'advertiserId': self.__class__.advertiser_id,
        'destinationUrl': 'http://google.com',
        'imageName': 'image.jpg',
        'imageByteArray': self.__class__.IMAGE_DATA1,
        'size': {'width': '300', 'height': '250'}
    }
    self.assert_(isinstance(
        self.__class__.service.CreateCreative(creative), tuple))

  def testCreateCreatives(self):
    """Test whether we can create a list of creatives."""
    creatives = [
        {
            'type': 'ImageCreative',
            'name': 'Image Creative #%s' % Utils.GetUniqueName(),
            'advertiserId': self.__class__.advertiser_id,
            'destinationUrl': 'http://google.com',
            'imageName': 'inline.jpg',
            'imageByteArray': self.__class__.IMAGE_DATA2,
            'size': {'width': '300', 'height': '250'}
        },
        {
            'type': 'ImageCreative',
            'name': 'Image Creative #%s' % Utils.GetUniqueName(),
            'advertiserId': self.__class__.advertiser_id,
            'destinationUrl': 'http://google.com',
            'imageName': 'skyscraper.jpg',
            'imageByteArray': self.__class__.IMAGE_DATA3,
            'size': {'width': '120', 'height': '600'}
        }
    ]
    creatives = self.__class__.service.CreateCreatives(creatives)
    self.__class__.creative1 = creatives[0]
    self.__class__.creative2 = creatives[1]
    self.assert_(isinstance(creatives, tuple))

  def testGetCreative(self):
    """Test whether we can fetch an existing creative."""
    if not self.__class__.creative1:
      self.testCreateCreatives()
    self.assert_(isinstance(self.__class__.service.GetCreative(
        self.__class__.creative1['id']), tuple))
    self.assertEqual(self.__class__.service.GetCreative(
        self.__class__.creative1['id'])[0]['Creative_Type'],
                     'ImageCreative')

  def testGetCreativesByStatement(self):
    """Test whether we can fetch a list of existing creatives that match given
    statement."""
    if not self.__class__.creative1:
      self.testCreateCreatives()
    filter_statement = {'query': 'WHERE id = %s ORDER BY name LIMIT 1'
                        % self.__class__.creative1['id']}
    self.assert_(isinstance(
        self.__class__.service.GetCreativesByStatement(filter_statement),
        tuple))

  def testUpdateCreative(self):
    """Test whether we can update a creative."""
    if not self.__class__.creative1:
      self.testCreateCreatives()
    destination_url = 'http://news.google.com'
    image_name = 'inline.jpg'
    size = {'width': '300', 'isAspectRatio': 'false', 'height': '250'}
    self.__class__.creative1['destinationUrl'] = destination_url
    self.__class__.creative1['imageName'] = image_name
    self.__class__.creative1['size'] = size
    creative = self.__class__.service.UpdateCreative(self.__class__.creative1)
    self.assert_(isinstance(creative, tuple))
    self.assertEqual(creative[0]['destinationUrl'], destination_url)
    self.assertEqual(creative[0]['imageName'], image_name)
    self.assertEqual(creative[0]['size'], size)

  def testUpdateCreatives(self):
    """Test whether we can update a list of creatives."""
    if not self.__class__.creative1 or not self.__class__.creative2:
      self.testCreateCreatives()
    destination_url = 'http://finance.google.com'
    self.__class__.creative1['destinationUrl'] = 'http://finance.google.com'
    self.__class__.creative1['imageName'] = 'inline.jpg'
    self.__class__.creative1['size'] = {'width': '300', 'height': '250'}
    self.__class__.creative2['destinationUrl'] = 'http://finance.google.com'
    self.__class__.creative2['imageName'] = 'skyscraper.jpg'
    self.__class__.creative2['size'] = {'width': '120', 'height': '600'}
    creatives = self.__class__.service.UpdateCreatives(
        [self.__class__.creative1, self.__class__.creative2])
    self.assert_(isinstance(creatives, tuple))
    for creative in creatives:
      self.assertEqual(creative['destinationUrl'], destination_url)


class CreativeServiceTestV201111(unittest.TestCase):

  """Unittest suite for CreativeService using v201111."""

  SERVER = SERVER_V201111
  VERSION = VERSION_V201111
  client.debug = False
  service = None
  advertiser_id = '0'
  creative1 = None
  creative2 = None
  IMAGE_DATA1 = open(os.path.join('data', 'medium_rectangle.jpg').replace(
      '\\', '/'), 'r').read()
  IMAGE_DATA2 = open(os.path.join('data', 'inline.jpg').replace(
      '\\', '/'), 'r').read()
  IMAGE_DATA3 = open(os.path.join('data', 'skyscraper.jpg').replace(
      '\\', '/'), 'r').read()
  IMAGE_DATA1 = base64.encodestring(IMAGE_DATA1)
  IMAGE_DATA2 = base64.encodestring(IMAGE_DATA2)
  IMAGE_DATA3 = base64.encodestring(IMAGE_DATA3)

  def setUp(self):
    """Prepare unittest."""
    print self.id()
    if not self.__class__.service:
      self.__class__.service = client.GetCreativeService(
          self.__class__.SERVER, self.__class__.VERSION, HTTP_PROXY)

    if self.__class__.advertiser_id == '0':
      company = {
          'name': 'Company #%s' % Utils.GetUniqueName(),
          'type': 'ADVERTISER'
      }
      company_service = client.GetCompanyService(
          self.__class__.SERVER, self.__class__.VERSION, HTTP_PROXY)
      self.__class__.advertiser_id = company_service.CreateCompany(
          company)[0]['id']

  def testCreateCreative(self):
    """Test whether we can create a creative."""
    creative = {
        'type': 'ImageCreative',
        'name': 'Image Creative #%s' % Utils.GetUniqueName(),
        'advertiserId': self.__class__.advertiser_id,
        'destinationUrl': 'http://google.com',
        'imageName': 'image.jpg',
        'imageByteArray': self.__class__.IMAGE_DATA1,
        'size': {'width': '300', 'height': '250'}
    }
    self.assert_(isinstance(
        self.__class__.service.CreateCreative(creative), tuple))

  def testCreateCreatives(self):
    """Test whether we can create a list of creatives."""
    creatives = [
        {
            'type': 'ImageCreative',
            'name': 'Image Creative #%s' % Utils.GetUniqueName(),
            'advertiserId': self.__class__.advertiser_id,
            'destinationUrl': 'http://google.com',
            'imageName': 'inline.jpg',
            'imageByteArray': self.__class__.IMAGE_DATA2,
            'size': {'width': '300', 'height': '250'}
        },
        {
            'type': 'ImageCreative',
            'name': 'Image Creative #%s' % Utils.GetUniqueName(),
            'advertiserId': self.__class__.advertiser_id,
            'destinationUrl': 'http://google.com',
            'imageName': 'skyscraper.jpg',
            'imageByteArray': self.__class__.IMAGE_DATA3,
            'size': {'width': '120', 'height': '600'}
        }
    ]
    creatives = self.__class__.service.CreateCreatives(creatives)
    self.__class__.creative1 = creatives[0]
    self.__class__.creative2 = creatives[1]
    self.assert_(isinstance(creatives, tuple))

  def testGetCreative(self):
    """Test whether we can fetch an existing creative."""
    if not self.__class__.creative1:
      self.testCreateCreatives()
    self.assert_(isinstance(self.__class__.service.GetCreative(
        self.__class__.creative1['id']), tuple))
    self.assertEqual(self.__class__.service.GetCreative(
        self.__class__.creative1['id'])[0]['Creative_Type'],
                     'ImageCreative')

  def testGetCreativesByStatement(self):
    """Test whether we can fetch a list of existing creatives that match given
    statement."""
    if not self.__class__.creative1:
      self.testCreateCreatives()
    filter_statement = {'query': 'WHERE id = %s ORDER BY name LIMIT 1'
                        % self.__class__.creative1['id']}
    self.assert_(isinstance(
        self.__class__.service.GetCreativesByStatement(filter_statement),
        tuple))

  def testUpdateCreative(self):
    """Test whether we can update a creative."""
    if not self.__class__.creative1:
      self.testCreateCreatives()
    destination_url = 'http://news.google.com'
    image_name = 'inline.jpg'
    size = {'width': '300', 'isAspectRatio': 'false', 'height': '250'}
    self.__class__.creative1['destinationUrl'] = destination_url
    self.__class__.creative1['imageName'] = image_name
    self.__class__.creative1['size'] = size
    creative = self.__class__.service.UpdateCreative(self.__class__.creative1)
    self.assert_(isinstance(creative, tuple))
    self.assertEqual(creative[0]['destinationUrl'], destination_url)
    self.assertEqual(creative[0]['imageName'], image_name)
    self.assertEqual(creative[0]['size'], size)

  def testUpdateCreatives(self):
    """Test whether we can update a list of creatives."""
    if not self.__class__.creative1 or not self.__class__.creative2:
      self.testCreateCreatives()
    destination_url = 'http://finance.google.com'
    self.__class__.creative1['destinationUrl'] = 'http://finance.google.com'
    self.__class__.creative1['imageName'] = 'inline.jpg'
    self.__class__.creative1['size'] = {'width': '300', 'height': '250'}
    self.__class__.creative2['destinationUrl'] = 'http://finance.google.com'
    self.__class__.creative2['imageName'] = 'skyscraper.jpg'
    self.__class__.creative2['size'] = {'width': '120', 'height': '600'}
    creatives = self.__class__.service.UpdateCreatives(
        [self.__class__.creative1, self.__class__.creative2])
    self.assert_(isinstance(creatives, tuple))
    for creative in creatives:
      self.assertEqual(creative['destinationUrl'], destination_url)


def makeTestSuiteV201108():
  """Set up test suite using v201108.

  Returns:
    TestSuite test suite using v201108.
  """
  suite = unittest.TestSuite()
  suite.addTests(unittest.makeSuite(CreativeServiceTestV201108))
  return suite


def makeTestSuiteV201111():
  """Set up test suite using v201111.

  Returns:
    TestSuite test suite using v201111.
  """
  suite = unittest.TestSuite()
  suite.addTests(unittest.makeSuite(CreativeServiceTestV201111))
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
