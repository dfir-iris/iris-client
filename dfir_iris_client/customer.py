#  IRIS Client API Source Code
#  contact@dfir-iris.org
#
#  This program is free software; you can redistribute it and/or
#  modify it under the terms of the GNU Lesser General Public
#  License as published by the Free Software Foundation; either
#  version 3 of the License, or (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
#  Lesser General Public License for more details.
#
#  You should have received a copy of the GNU Lesser General Public License
#  along with this program; if not, write to the Free Software Foundation,
#  Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.

from dfir_iris_client.helper.utils import ClientApiError, ApiResponse, ClientApiData


class Customer(object):
    """Handles the customer methods"""
    def __init__(self, session):
        self._s = session

    def lookup_customer(self, customer_name) -> ApiResponse:
        """
        Returns a customer ID if customer name is found. Customer names are unique in the database.
        Customer ID is in the data section of the API response aka id = parse_api_data(resp.get_data(), 'customer_id')

        Args:
          customer_name: Name of the customer to lookup

        Returns:
          ApiResponse object

        """
        resp = self._s.pi_get('/manage/customers/list')

        if resp.is_success():

            customer_list = resp.get_data()

            for customer in customer_list:
                if customer.get('customer_name').lower() == customer_name.lower():
                    response = ClientApiData(data=customer)
                    return ApiResponse(response=response, uri=resp.get_uri())

        return ClientApiError(f"Customer {customer_name} not found")

    def get_customer_by_id(self, customer_id: int) -> ApiResponse:
        """
        Returns a customer from its ID

        Args:
          customer_id: Customer ID to look up

        Returns:
          ApiResponse object

        """
        resp = self._s.pi_get(f'/manage/customers/{customer_id}')

        return resp

    def list_customers(self) -> ApiResponse:
        """
        Returns a list of the available customers
        
        :return: ApiResponse object

        Args:

        Returns:
            ApiResponse object
        """

        return self._s.pi_get(f'/manage/customers/list')