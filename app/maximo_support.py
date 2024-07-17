#
#
#  Maximo at TSO does not have the correct configuration to enable REST API at this time.
#
#
#


import requests
from requests.auth import HTTPBasicAuth
import warnings
warnings.filterwarnings("ignore", message="Unverified HTTPS request")

class MaximoClient:
    def __init__(self, base_url, username, password):
        self.base_url = base_url
        self.username = username
        self.password = password
        self.session = requests.Session()
        self.headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        }
        try:
            self.api_key = self.authenticate_and_get_api_key()
        except requests.exceptions.HTTPError as err:
            print(f"Failed to initialize MaximoClient: {err}")
            raise

    def authenticate_and_get_api_key(self):
        # Step 1: Authenticate and get session cookie
        auth_url = f"{self.base_url}/j_security_check"
        auth_data = {
            'j_username': self.username,
            'j_password': self.password
        }
        print(f"Authenticating with URL: {auth_url}")
        auth_response = self.session.post(auth_url, data=auth_data, verify=False)
        
        if auth_response.status_code != 200:
            print(f"Authentication failed: {auth_response.status_code}")
            print(f"Response: {auth_response.text}")
            auth_response.raise_for_status()

        print("Authentication successful, fetching API key...")

        # Step 2: Use session cookie to request API key
        api_key_url = f"{self.base_url}/maxrest/rest/login"
        print(f"Requesting API key with URL: {api_key_url}")
        api_key_response = self.session.get(api_key_url, verify=False)
        
        if api_key_response.status_code != 200:
            print(f"Failed to retrieve API key: {api_key_response.status_code}")
            print(f"Response: {api_key_response.text}")
            api_key_response.raise_for_status()
        
        api_key = api_key_response.json().get('apikey')
        if not api_key:
            raise ValueError("Failed to retrieve API key")

        print("API key retrieved successfully")

        # Update headers with the API key
        self.headers['apikey'] = api_key
        return api_key

    def _request(self, method, endpoint, data=None, params=None):
        url = f"{self.base_url}/{endpoint}"
        response = self.session.request(
            method,
            url,
            headers=self.headers,
            json=data,
            params=params,
            verify=False  # Bypass SSL certificate verification
        )
        try:
            response.raise_for_status()
        except requests.exceptions.HTTPError as err:
            print(f"HTTP error occurred: {err}")
            print(f"Response text: {response.text}")
            raise
        return response.json()

    def create_record(self, object_name, data):
        endpoint = f"api/os/{object_name}"
        return self._request("POST", endpoint, data=data)

    def read_record(self, object_name, record_id):
        endpoint = f"api/os/{object_name}/{record_id}"
        return self._request("GET", endpoint)

    def update_record(self, object_name, record_id, data):
        endpoint = f"api/os/{object_name}/{record_id}"
        return self._request("PUT", endpoint, data=data)

    # MDOT Employees should not invoke delete operations, permissions prevent at user level in application.
    # def delete_record(self, object_name, record_id):
    #     endpoint = f"api/os/{object_name}/{record_id}"
    #     return self._request("DELETE", endpoint)

    def list_objects(self):
        endpoint = "api/os"
        return self._request("GET", endpoint)

# # Usage example
# if __name__ == "__main__":
#     base_url = "https://10.92.35.91/maxrest/rest"
#     username = "user"
#     password = "passwd"
#
#     try:
#         client = MaximoClient(base_url, username, password)
#     except requests.exceptions.HTTPError as err:
#         print(f"Initialization failed: {err}")
#         client = None
#
#     if client:
#         # List available objects
#         try:
#             objects = client.list_objects()
#             print("Available objects:", objects)
#         except requests.exceptions.HTTPError as err:
#             print(f"Failed to list objects: {err}")
#
#         # Create a Service Request
#         service_request_data = {
#             "description": "Test Service Request",
#             "reportdate": "2024-07-16T00:00:00Z",
#             "status": "NEW"
#         }
#         try:
#             created_service_request = client.create_record("SR", service_request_data)
#             print("Created Service Request:", created_service_request)
#
#             # Read a Service Request
#             service_request_id = created_service_request["SRID"]
#             service_request = client.read_record("SR", service_request_id)
#             print("Service Request Details:", service_request)
#
#             # Update a Service Request
#             update_data = {
#                 "status": "INPROG"
#             }
#             updated_service_request = client.update_record("SR", service_request_id, update_data)
#             print("Updated Service Request:", updated_service_request)
#
#             # Delete a Service Request
#             client.delete_record("SR", service_request_id)
#             print(f"Service Request {service_request_id} deleted")
#         except requests.exceptions.HTTPError as err:
#             print(f"Failed to perform operation: {err}")
#

            
            
            
#     $ curl -k -X POST "https://10.92.35.91/maxrest/rest/j_security_check" -d "j_username=gphillips3" -d "j_password=OMITTED" -v
# Note: Unnecessary use of -X or --request, POST is already inferred.
# *   Trying 10.92.35.91:443...
# * Connected to 10.92.35.91 (10.92.35.91) port 443
# * schannel: disabled automatic use of client certificate
# * schannel: using IP address, SNI is not supported by OS.
# * ALPN: curl offers http/1.1
# * ALPN: server did not agree on a protocol. Uses default.
# * using HTTP/1.x
# > POST /maxrest/rest/j_security_check HTTP/1.1
# > Host: 10.92.35.91
# > User-Agent: curl/8.4.0
# > Accept: */*
# > Content-Length: 48
# > Content-Type: application/x-www-form-urlencoded
# >
# * schannel: server closed the connection
# < HTTP/1.1 500 Internal Server Error
# < Date: Tue, 16 Jul 2024 16:42:47 GMT
# < X-Powered-By: Servlet/3.1
# < $WSEP:
# < Content-Length: 145
# < Connection: close
# < Content-Type: text/html;charset=ISO-8859-1
# < Content-Language: en-US
# <
# Error 500: java.lang.IllegalArgumentException: Location cannot be null in javax.servlet.http.HttpServletResponse.sendRedirect&#40;location&#41;
# * Closing connection
# * schannel: shutting down SSL/TLS connection with 10.92.35.91 port 443


