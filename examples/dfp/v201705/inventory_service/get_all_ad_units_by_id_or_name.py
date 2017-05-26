#!/usr/bin/env python
#
# Copyright 2016 Google Inc. All Rights Reserved.
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
"""This example gets all ad units.
"""

# Import appropriate modules from the client library.
from googleads import dfp


def main(client):
  # Initialize appropriate service.
  ad_unit_service = client.GetService('InventoryService', version='v201705')

  # Create a statement to select ad units by parentId.
  # values = [{
  #     'key': 'parentId',
  #     'value': {
  #         'xsi_type': 'TextValue',
  #         'value': '152817024'
  #     }
  # }]
  # query = 'WHERE parentId = :parentId'
  # statement = dfp.FilterStatement(query, values)

  # Create a statement to select ad units by parentId in array.
  # parent_ad_unit_ids = ['152817024']
  # values = [{
  #     'key': 'parentId',
  #     'value': {
  #         'xsi_type': 'TextValue',
  #         'value': parent_ad_unit_ids
  #     }
  # }]
  # query = 'WHERE parentId = :parentId'
  # statement = dfp.FilterStatement(query, values)

  # Create a statement to select ad units by name that starts with (%) specified value.
  query = "WHERE name LIKE 'en.twc.app.%'"
  statement = dfp.FilterStatement(query)

  # Get ad units by statement.
  response = ad_unit_service.getAdUnitsByStatement(
      statement.ToStatement())

  # Retrieve a small amount of ad units at a time, paging
  # through until all ad units have been retrieved.
  while True:
    response = ad_unit_service.getAdUnitsByStatement(statement.ToStatement())
    if 'results' in response:
      for ad_unit in response['results']:
        # Print out some information for each ad unit.
        print('Ad unit with ID "%s" and name "%s" was found.\n' %
              (ad_unit['id'], ad_unit['name']))
      statement.offset += dfp.SUGGESTED_PAGE_LIMIT
    else:
      break

  print '\nNumber of results found: %s' % response['totalResultSetSize']


if __name__ == '__main__':
  # Initialize client object.
  dfp_client = dfp.DfpClient.LoadFromStorage()
  main(dfp_client)
