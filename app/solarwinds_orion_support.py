import requests

class SolarwindsRestClient:
    def __init__(self, base_url, username, password):
        self.base_url = base_url
        self.auth = (username, password)
        self.headers = {
            'Content-Type': 'application/json'
        }

    def get(self, endpoint):
        url = f"{self.base_url}/{endpoint}"
        response = requests.get(url, auth=self.auth, headers=self.headers)
        response.raise_for_status()
        return response.json()

    def post(self, endpoint, data):
        url = f"{self.base_url}/{endpoint}"
        response = requests.post(url, auth=self.auth, headers=self.headers, json=data)
        response.raise_for_status()
        return response.json()

# Example usage
if __name__ == "__main__":
    base_url = "http://10.92.33.200:17778/SolarWinds/InformationService/v3/Json"
    username = "mdta\gphillips3"
    password = "02121103!Jun24"

    client = SolarwindsRestClient(base_url, username, password)

    # Example GET request
    try:
        response = client.get("Query?query=SELECT+TOP+10+NodeID, Caption+FROM+Orion.Nodes")
        print(response)
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")

    # Example POST request
    try:
        data = {"some_key": "some_value"}
        response = client.post("endpoint", data)
        print(response)
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
