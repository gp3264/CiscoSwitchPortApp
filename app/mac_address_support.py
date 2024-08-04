import os
import re
import requests
from typing import Dict, Optional, List, Any

class MacAddressSupport:
    def __init__(self, mac_database_file: str = 'manuf', url: str = 'https://www.wireshark.org/download/automated/data/manuf') -> None:
        """
        Initialize the MacAddressSupport class and load the MAC address to Vendor mapping.

        :param mac_database_file: The local file to store the MAC address to Vendor mapping.
        :param url: The URL to download the MAC address to Vendor mapping file.
        :raises ValueError: If the data cannot be loaded or parsed.
        """
        self.mac_database_file = mac_database_file
        self.url = url
        self.mac_to_vendor = self.load_mac_to_vendor()
        self.short_name_to_full_name = self.build_short_name_to_full_name_mapping()

    def perform_request(self, method: str, url: str, data: Optional[Dict[str, Any]] = None, headers: Optional[Dict[str, str]] = None, verify: bool = True) -> requests.Response:
        """
        Perform an HTTP request using the specified method.

        :param method: The HTTP method to use ('GET' or 'POST').
        :param url: The URL to send the request to.
        :param data: The data to send in the request (for POST requests).
        :param headers: Optional headers to include in the request.
        :param verify: Whether to verify SSL certificates.
        :return: The HTTP response object.
        :raises ValueError: If the request fails.
        """
        try:
            if method.upper() == 'GET':
                response = requests.get(url, headers=headers, verify=verify)
            elif method.upper() == 'POST':
                response = requests.post(url, data=data, headers=headers, verify=verify)
            else:
                raise ValueError(f"Unsupported HTTP method: {method}")
            
            response.raise_for_status()
            return response
        except requests.RequestException as e:
            raise ValueError(f"Failed to perform {method} request to {url}: {e}")

    def load_mac_to_vendor(self) -> Dict[str, str]:
        """
        Load the MAC address to Vendor mapping from the specified URL or local file.

        :return: A dictionary with MAC address blocks as keys and vendor names as values.
        :raises ValueError: If the data cannot be loaded or parsed.
        """
        if not os.path.exists(self.mac_database_file):
            print(f"File {self.mac_database_file} not found. Downloading from URL...")
            self.download_mac_database()
        else:
            pass
            #print(f"File {self.mac_database_file} found. Using local file.")

        try:
            with open(self.mac_database_file, 'r', encoding='utf-8') as file:
                data = file.read()
                #print(f"Loaded {len(data)} characters from {self.mac_database_file}")
                if not data.strip():
                    #print("Local file is empty, downloading data from URL...")
                    self.download_mac_database()
                    with open(self.mac_database_file, 'r', encoding='utf-8') as file:
                        data = file.read()
                        #print(f"Loaded {len(data)} characters from {self.mac_database_file} after re-downloading")
                return self.parse_manuf_file(data)
        except Exception as e:
            raise ValueError(f"Failed to load data from {self.mac_database_file}: {e}")

    def download_mac_database(self) -> None:
        """
        Download the MAC address to Vendor mapping from the specified URL and save it to a local file.

        :raises ValueError: If the data cannot be downloaded.
        """
        try:
            response = self.perform_request('GET', self.url, verify=False)  # Bypass SSL verification
            print(f"Downloading data from {self.url}...")
            with open(self.mac_database_file, 'w', encoding='utf-8') as file:
                file.write(response.text)
            print(f"MAC database downloaded and saved to {self.mac_database_file}")
        except ValueError as e:
            raise ValueError(f"Failed to download data from {self.url}: {e}")

    def parse_manuf_file(self, data: str) -> Dict[str, str]:
        """
        Parse the MAC address to Vendor mapping file.

        :param data: The raw text data of the file.
        :return: A dictionary with MAC address blocks as keys and vendor names as values.
        :raises ValueError: If the data cannot be parsed.
        """
        mac_to_vendor = {}
        self.short_name_to_full_name = {}
        try:
            for line in data.splitlines():
                if line.startswith('#') or not line.strip():
                    continue
                parts = re.split(r'\s+', line)
                if len(parts) >= 3:
                    mac_prefix = parts[0].replace(':', '').lower()
                    short_name = parts[1]
                    full_name = ' '.join(parts[2:])
                    mac_to_vendor[mac_prefix] = short_name
                    self.short_name_to_full_name[short_name] = full_name
                else:
                    pass
                    #print(f"Skipping invalid line: {line}")
            #print(f"Parsed {len(mac_to_vendor)} entries from the MAC database")
            return mac_to_vendor
        except Exception as e:
            raise ValueError(f"Failed to parse manuf file: {e}")

    def build_short_name_to_full_name_mapping(self) -> Dict[str, str]:
        """
        Build a mapping of short vendor names to full vendor names.

        :return: A dictionary with short vendor names as keys and full vendor names as values.
        """
        return self.short_name_to_full_name

    def get_vendor(self, mac_address: str) -> Optional[str]:
        """
        Get the vendor for a given MAC address.

        :param mac_address: The MAC address to lookup.
        :return: The vendor name if found, otherwise None.
        """
        try:
            normalized_mac = self.normalize_mac_address(mac_address)
            mac_prefixes = [normalized_mac[:i] for i in (6, 7, 9)]  # 24-bit, 28-bit, 36-bit prefixes
            for prefix in mac_prefixes:
                if prefix in self.mac_to_vendor:
                    return self.mac_to_vendor[prefix]
        except ValueError as e:
            return "Invalid MAC format"
        return None

    def get_full_vendor_name(self, short_name: str) -> Optional[str]:
        """
        Get the full vendor name given a short name.

        :param short_name: The short name of the vendor.
        :return: The full vendor name if found, otherwise None.
        """
        return self.short_name_to_full_name.get(short_name)

    @staticmethod
    def normalize_mac_address(mac_address: str) -> str:
        """
        Normalize a MAC address to a common format (lowercase, no delimiters).

        :param mac_address: The MAC address to normalize.
        :return: The normalized MAC address.
        :raises ValueError: If the MAC address format is invalid.
        """
        mac = re.sub(r'[^a-fA-F0-9]', '', mac_address).lower()
        if len(mac) != 12:
            raise ValueError(f"Invalid MAC address format: {mac_address}")
        return mac

    @staticmethod
    def compare_mac_addresses(mac1: str, mac2: str) -> bool:
        """
        Compare two MAC addresses for equality.

        :param mac1: The first MAC address.
        :param mac2: The second MAC address.
        :return: True if the MAC addresses are equal, False otherwise.
        """
        try:
            return MacAddressSupport.normalize_mac_address(mac1) == MacAddressSupport.normalize_mac_address(mac2)
        except ValueError:
            return False

    def list_mac_prefixes_by_vendor(self, vendor_name: str) -> List[str]:
        """
        List all MAC prefixes for a given vendor.

        :param vendor_name: The name of the vendor.
        :return: A list of MAC prefixes for the specified vendor.
        """
        return [prefix for prefix, vendor in self.mac_to_vendor.items() if vendor_name.lower() in vendor.lower()]

    def display_menu(self) -> None:
        """
        Display a menu to look up short name, full name, or MAC address.
        Get input from the user and display the results.
        """
        print("Menu:")
        print("1. Look up MAC address")
        print("2. Look up short vendor name")
        print("3. Look up full vendor name")
        print("4. Exit")

    def handle_user_input(self) -> None:
        """
        Handle user input to look up MAC address, short name, or full name.
        """
        while True:
            self.display_menu()
            choice = input("Enter your choice: ")

            if choice == '1':
                mac_address = input("Enter MAC address: ")
                vendor = self.get_vendor(mac_address)
                if vendor:
                    print(f"Vendor for MAC address {mac_address}: {vendor}")
                else:
                    print(f"No vendor found for MAC address {mac_address}")
            elif choice == '2':
                short_name = input("Enter short vendor name: ")
                full_name = self.get_full_vendor_name(short_name)
                if full_name:
                    print(f"Full vendor name for short name {short_name}: {full_name}")
                else:
                    print(f"No full vendor name found for short name {short_name}")
            elif choice == '3':
                vendor_name = input("Enter vendor name: ")
                mac_prefixes = self.list_mac_prefixes_by_vendor(vendor_name)
                if mac_prefixes:
                    print(f"MAC prefixes for vendor {vendor_name}: {', '.join(mac_prefixes)}")
                else:
                    print(f"No MAC prefixes found for vendor {vendor_name}")
            elif choice == '4':
                print("Exiting...")
                break
            else:
                print("Invalid choice. Please try again.")

# Example usage:
if __name__ == "__main__":
    mac_support = MacAddressSupport()
    mac_support.handle_user_input()

# Example usage:
if __name__ == "__main__":
    from pprint import pprint
    mac_support = MacAddressSupport()
    mac_address = "00:00:01:02:03:04"
    print(f"Vendor for {mac_address}: {mac_support.get_vendor(mac_address)}")

    mac1 = "00:00:01:02:03:04"
    mac2 = "00-00-01-02-03-04"
    print(f"MAC addresses {mac1} and {mac2} are equal: {MacAddressSupport.compare_mac_addresses(mac1, mac2)}")

    vendor = "Xerox"
    pprint(f"MAC prefixes for vendor {vendor}: {mac_support.list_mac_prefixes_by_vendor(vendor)}")


    vendor = "Hirschmann"
    pprint(f"MAC prefixes for vendor {vendor}: {mac_support.list_mac_prefixes_by_vendor(vendor)}")


    vendor = "Axis"
    pprint(f"MAC prefixes for vendor {vendor}: {mac_support.list_mac_prefixes_by_vendor(vendor)}")

   
    mac_address = "6412.2582.f13f"
    print(f"Vendor for {mac_address}: {mac_support.get_vendor(mac_address)}")

    short_name = "Hirschmann"
    print(f"Full vendor name for short name {short_name}: {mac_support.get_full_vendor_name(short_name)}")



if __name__ == "__main__":
    mac_support = MacAddressSupport()
    mac_support.handle_user_input()
1