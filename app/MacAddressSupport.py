import re
import requests
from typing import Dict, Optional

class MacAddressSupport:
    def __init__(self, url: str = 'https://www.wireshark.org/download/automated/data/manuf') -> None:
        """
        Initialize the MacAddressSupport class and load the MAC address to Vendor mapping.

        :param url: The URL to download the MAC address to Vendor mapping file.
        :raises ValueError: If the data cannot be loaded or parsed.
        """
        self.url = url
        self.mac_to_vendor = self.load_mac_to_vendor()

    def load_mac_to_vendor(self) -> Dict[str, str]:
        """
        Load the MAC address to Vendor mapping from the specified URL.

        :return: A dictionary with MAC address blocks as keys and vendor names as values.
        :raises ValueError: If the data cannot be loaded or parsed.
        """
        try:
            response = requests.get(self.url)
            response.raise_for_status()
            return self.parse_manuf_file(response.text)
        except requests.RequestException as e:
            raise ValueError(f"Failed to load data from {self.url}: {e}")

    def parse_manuf_file(self, data: str) -> Dict[str, str]:
        """
        Parse the MAC address to Vendor mapping file.

        :param data: The raw text data of the file.
        :return: A dictionary with MAC address blocks as keys and vendor names as values.
        :raises ValueError: If the data cannot be parsed.
        """
        mac_to_vendor = {}
        try:
            for line in data.splitlines():
                if line.startswith('#') or not line.strip():
                    continue
                parts = line.split('\t')
                if len(parts) >= 3:
                    mac_prefix = parts[0].strip().replace(':', '').lower()
                    vendor = parts[2].strip()
                    mac_to_vendor[mac_prefix] = vendor
            return mac_to_vendor
        except Exception as e:
            raise ValueError(f"Failed to parse manuf file: {e}")

    def get_vendor(self, mac_address: str) -> Optional[str]:
        """
        Get the vendor for a given MAC address.

        :param mac_address: The MAC address to lookup.
        :return: The vendor name if found, otherwise None.
        """
        normalized_mac = self.normalize_mac_address(mac_address)
        mac_prefixes = [normalized_mac[:i] for i in (6, 7, 9)]  # 24-bit, 28-bit, 36-bit prefixes
        for prefix in mac_prefixes:
            if prefix in self.mac_to_vendor:
                return self.mac_to_vendor[prefix]
        return None

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

# Example usage:
if __name__ == "__main__":
    mac_support = MacAddressSupport()
    mac_address = "00:00:01:02:03:04"
    print(f"Vendor for {mac_address}: {mac_support.get_vendor(mac_address)}")

    mac1 = "00:00:01:02:03:04"
    mac2 = "00-00-01-02-03-04"
    print(f"MAC addresses {mac1} and {mac2} are equal: {MacAddressSupport.compare_mac_addresses(mac1, mac2)}")
