import requests
from typing import Dict, Any
import warnings
import time

# Disable warnings
warnings.filterwarnings("ignore", message="Unverified HTTPS request")

class IPControlAPIDevice:
    def __init__(self, base_url: str, username: str, password: str):
        """
        Initializes the IPControlAPIDevice with the base URL and authentication credentials.

        :param base_url: Base URL of the IPControl API.
        :param username: Username for API authentication.
        :param password: Password for API authentication.
        """
        self.base_url = base_url
        self.username = username
        self.password = password
        self.token = None
        self.token_expiry = 0
        self.verify = False  # Disable SSL verification
        self._authenticate()

    def _authenticate(self) -> None:
        """
        Authenticates the user and obtains a JWT token.
        """
        url = f"{self.base_url}/login"
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded',
            'Accept': 'application/json'
        }
        data = {
            'username': self.username,
            'password': self.password
        }
        response = requests.post(url, headers=headers, data=data, verify=self.verify)
        response.raise_for_status()
        token_data = response.json()
        self.token = token_data['access_token']
        self.token_expiry = time.time() + token_data['expires_in']

    def _is_token_expired(self) -> bool:
        """
        Checks if the current token is expired.

        :return: True if the token is expired, False otherwise.
        """
        return time.time() >= self.token_expiry

    def _make_request(self, method: str, endpoint: str, **kwargs) -> Dict[str, Any]:
        """
        Generalized method for making API requests.

        :param method: HTTP method (GET, POST, PUT, DELETE).
        :param endpoint: API endpoint.
        :return: JSON response from the API.
        :raises requests.exceptions.RequestException: If the request fails.
        """
        if self._is_token_expired():
            self._authenticate()

        url = f"{self.base_url}{endpoint}"
        headers = {
            'Authorization': f'Bearer {self.token}',
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        }
        response = requests.request(method, url, headers=headers, verify=self.verify, **kwargs)
        if response.status_code == 401:  # Token expired
            self._authenticate()
            headers['Authorization'] = f'Bearer {self.token}'
            response = requests.request(method, url, headers=headers, verify=self.verify, **kwargs)
        response.raise_for_status()
        return response.json()

    def create_device(self, device_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Creates a new device.

        :param device_data: Dictionary containing the device data.
        :return: JSON response from the API.
        :raises requests.exceptions.RequestException: If the request fails.
        """
        return self._make_request('POST', '/Imports/importDevice', json=device_data)

    def get_device(self, device_identifier: str, identifier_type: str = 'ipAddress') -> Dict[str, Any]:
        """
        Retrieves a device by its identifier.

        :param device_identifier: The identifier of the device (IP address, MAC address, or hostname).
        :param identifier_type: The type of identifier ('ipAddress', 'macAddress', or 'hostname').
        :return: JSON response from the API.
        :raises requests.exceptions.RequestException: If the request fails.
        """
        if identifier_type == 'ipAddress':
            endpoint = f'/Gets/getDeviceByIPAddr?ipAddress={device_identifier}'
        elif identifier_type == 'macAddress':
            endpoint = f'/Gets/getDeviceByMACAddress?macAddress={device_identifier}'
        elif identifier_type == 'hostname':
            endpoint = f'/Gets/getDeviceByHostname?hostname={device_identifier}'
        else:
            raise ValueError("Invalid identifier_type. Expected 'ipAddress', 'macAddress', or 'hostname'.")

        return self._make_request('GET', endpoint)

    def update_device(self, device_identifier: str, device_data: Dict[str, Any], identifier_type: str = 'ipAddress') -> Dict[str, Any]:
        """
        Updates a device.

        :param device_identifier: The identifier of the device (IP address, MAC address, or hostname).
        :param device_data: Dictionary containing the updated device data.
        :param identifier_type: The type of identifier ('ipAddress', 'macAddress', or 'hostname').
        :return: JSON response from the API.
        :raises requests.exceptions.RequestException: If the request fails.
        """
        return self._make_request('POST', '/Imports/importDevice', json=device_data)

    def delete_device(self, device_identifier: str, identifier_type: str = 'ipAddress') -> bool:
        """
        Deletes a device.

        :param device_identifier: The identifier of the device (IP address, MAC address, or hostname).
        :param identifier_type: The type of identifier ('ipAddress', 'macAddress', or 'hostname').
        :return: True if the deletion was successful, False otherwise.
        :raises requests.exceptions.RequestException: If the request fails.
        """
        data = {'ipAddress': device_identifier}
        if identifier_type == 'macAddress':
            data['macAddress'] = device_identifier
        elif identifier_type == 'hostname':
            data['hostname'] = device_identifier
        response = self._make_request('DELETE', '/Deletes/deleteDevice', json=data)
        return response['status'] == 204

    def modify_device_field(self, device_identifier: str, field_name: str, field_value: Any, identifier_type: str = 'ipAddress') -> Dict[str, Any]:
        """
        Modifies a specific field of a device.

        :param device_identifier: The identifier of the device (IP address, MAC address, or hostname).
        :param field_name: The name of the field to modify.
        :param field_value: The new value for the field.
        :param identifier_type: The type of identifier ('ipAddress', 'macAddress', or 'hostname').
        :return: JSON response from the API.
        :raises requests.exceptions.RequestException: If the request fails.
        """
        device_data = self.get_device(device_identifier, identifier_type)
        device_data[field_name] = field_value
        return self.update_device(device_identifier, device_data, identifier_type)

    def get_device_by_mac(self, mac_address: str) -> Dict[str, Any]:
        """
        Retrieves a device by its MAC address.

        :param mac_address: The MAC address of the device.
        :return: JSON response from the API.
        :raises requests.exceptions.RequestException: If the request fails.
        """
        return self.get_device(mac_address, identifier_type='macAddress')

    def get_device_by_hostname(self, hostname: str) -> Dict[str, Any]:
        """
        Retrieves a device by its hostname.

        :param hostname: The hostname of the device.
        :return: JSON response from the API.
        :raises requests.exceptions.RequestException: If the request fails.
        """
        return self.get_device(hostname, identifier_type='hostname')


# Initialize the API client
api_client = IPControlAPIDevice(base_url="https://10.92.36.40:8443/inc-rest/api/v1", username="su_gphillips3", password="W@y2get1n")


# Example usage function
from pprint import pprint
def example_usage(api_client: IPControlAPIDevice) -> None:
    try:
        # # Create a new device
        # new_device: Dict[str, Any] = {
        #     "ipAddress": "192.168.1.10",
        #     "hostname": "new-device",
        #     "deviceType": "Router",
        #     "description": "New router in the network"
        # }
        # created_device = api_client.create_device(new_device)
        # print("Created Device:", created_device)

        # Get a device by IP address
        device = api_client.get_device("170.93.99.162")
        pprint(f"Device Info:{device}")

        # # Update a device's description
        # updated_device = api_client.modify_device_field("192.168.1.10", "description", "Updated router description")
        # print("Updated Device:", updated_device)
        #
        # # Delete a device by IP address
        # delete_status = api_client.delete_device("192.168.1.10")
        # print("Delete Status:", delete_status)
        #
        # # Get a device by MAC address
        # device_by_mac = api_client.get_device_by_mac("00:1A:2B:3C:4D:5E")
        # print("Device Info by MAC:", device_by_mac)
        #
        # # Get a device by hostname
        # device_by_hostname = api_client.get_device_by_hostname("new-device")
        # print("Device Info by Hostname:", device_by_hostname)

    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")

# Run the example usage function
example_usage(api_client)
