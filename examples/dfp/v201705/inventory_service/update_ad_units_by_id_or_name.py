#!/usr/bin/env python
#
# Copyright 2015 Google Inc. All Rights Reserved.
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

"""This code example updates ad unit sizes by adding a banner ad size.

To determine which ad units exist, run get_all_ad_units.py.

The LoadFromStorage method is pulling credentials and properties from a
"googleads.yaml" file. By default, it looks for this file in your home
directory. For more information, see the "Caching authentication information"
section of our README.

"""


# Import appropriate modules from the client library.
from googleads import dfp


# Set the ID of the ad unit to get.
AD_UNIT_ID = 'INSERT_AD_UNIT_ID_HERE'


def main(client, ad_unit_id):
  # Initialize appropriate service.
  inventory_service = client.GetService('InventoryService', version='v201705')

  # # Create a statement to select a single ad unit by ID.
  # values = [{
  #     'key': 'id',
  #     'value': {
  #         'xsi_type': 'TextValue',
  #         'value': '17731344'
  #     }
  # }]
  # query = 'WHERE id = :id'
  # statement = dfp.FilterStatement(query, values)

  # Create a statement to select ad units by name that starts with (%) specified value.
  query = "WHERE name LIKE 'en.twc.app.%'"
  statement = dfp.FilterStatement(query)

  # Get ad units by statement.
  response = inventory_service.getAdUnitsByStatement(
      statement.ToStatement())

  # Update ad unit Name.
  # ad_unit_name = 'Testsite'

  if 'results' in response:
    updated_ad_units = []

    for ad_unit in response['results']:

        old_ad_unit_name = ad_unit['name']
        print(old_ad_unit_name)
        last_slash = old_ad_unit_name.rfind('/', 0, len(old_ad_unit_name))
        new_ad_unit_name = old_ad_unit_name[last_slash + 1:len(old_ad_unit_name)]

        # Update ad unit Name.
        ad_unit_name = new_ad_unit_name
        print(ad_unit_name)

        if 'name' not in ad_unit:
            ad_unit['name'] = []
        ad_unit['name'] = ad_unit_name
        updated_ad_units.append(ad_unit)

    # Update ad unit on the server.
    ad_units = inventory_service.updateAdUnits(updated_ad_units)


    # Display results.
    print ('Ad unit with ID \'%s\', ad unit code \'%s\', name \'%s\' was updated'
          % (ad_unit['id'], ad_unit['adUnitCode'], ad_unit['name']))

if __name__ == '__main__':
  # Initialize client object.
  dfp_client = dfp.DfpClient.LoadFromStorage()
  main(dfp_client, AD_UNIT_ID)
