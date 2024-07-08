import re
from typing import List, Dict, Any
from datetime import datetime, timedelta

class TimeParser:
    def __init__(self, time_string: str):
        self.time_string = time_string
        self.time_data = self._parse_time_string()

    def _parse_time_string(self) -> Dict[str, int]:
        time_data = {
            'years': 0,
            'weeks': 0,
            'days': 0,
            'hours': 0,
            'minutes': 0,
            'seconds': 0,
        }
        
        # Regex patterns for different time formats
        year_week_pattern = re.compile(r'(\d+)y(\d+)w')
        week_day_pattern = re.compile(r'(\d+)w(\d+)d')
        day_hour_pattern = re.compile(r'(\d+)d(\d+)h')
        hour_minute_second_pattern = re.compile(r'(\d+):(\d+):(\d+)')
        
        if year_week_match := year_week_pattern.match(self.time_string):
            time_data['years'] = int(year_week_match.group(1))
            time_data['weeks'] = int(year_week_match.group(2))
        elif week_day_match := week_day_pattern.match(self.time_string):
            time_data['weeks'] = int(week_day_match.group(1))
            time_data['days'] = int(week_day_match.group(2))
        elif day_hour_match := day_hour_pattern.match(self.time_string):
            time_data['days'] = int(day_hour_match.group(1))
            time_data['hours'] = int(day_hour_match.group(2))
        elif hour_minute_second_match := hour_minute_second_pattern.match(self.time_string):
            time_data['hours'] = int(hour_minute_second_match.group(1))
            time_data['minutes'] = int(hour_minute_second_match.group(2))
            time_data['seconds'] = int(hour_minute_second_match.group(3))
        
        return time_data

    def get_time_data(self) -> Dict[str, int]:
        return self.time_data

    def current_date_iso(self) -> str:
        return datetime.now().isoformat()

    def start_date_iso(self) -> str:
        current_date = datetime.now()
        delta = timedelta(
            days=self.time_data['days'] + self.time_data['weeks'] * 7,
            hours=self.time_data['hours'],
            minutes=self.time_data['minutes'],
            seconds=self.time_data['seconds']
        )
        start_date = current_date - delta
        # Subtract years separately due to how timedelta works
        start_date = start_date.replace(year=start_date.year - self.time_data['years'])
        return start_date.isoformat()

# # Sample usage
# time_strings = [
#     "1y13w", "4w5d", "00:00:02", "1y13w", "47w3d", "00:01:12",
#     "7w1d", "3d04h", "14w5d", "7w1d", "00:48:15", "1d05h",
#     "47w5d", "1w6d", "1y5w", "6d02h", "1d09h", "1w6d", "5w0d",
#     "00:01:46", "39w3d", "4w1d", "10:55:28", "10:55:18", "1w1d",
#     "6d02h", "1y13w", "3w1d", "3w1d", "1d04h", "1d11h"
# ]
#
# for time_string in time_strings:
#     parser = TimeParser(time_string)
#     print(f"Current date ISO: {parser.current_date_iso()}")
#     print(f"Time string: {time_string} -> Start date ISO: {parser.start_date_iso()}")



class ConsoleParser:
    def __init__(self, console_output):
        self.console_output = console_output

    def extract_ip_addresses(self):
        """Extract all IP addresses from the console output."""
        ip_pattern = re.compile(r'\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b')
        return ip_pattern.findall(self.console_output)

    def extract_error_messages(self):
        """Extract all lines that contain the word 'error' (case insensitive)."""
        error_pattern = re.compile(r'(?i)error')
        return [line for line in self.console_output.splitlines() if error_pattern.search(line)]

    def extract_timestamps(self):
        """Extract all timestamps from the console output (assuming format 'YYYY-MM-DD HH:MM:SS')."""
        timestamp_pattern = re.compile(r'\b\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}\b')
        return timestamp_pattern.findall(self.console_output)

    def summary(self):
        """Return a summary of the console output, including counts of IP addresses, errors, and timestamps."""
        ip_addresses = self.extract_ip_addresses()
        errors = self.extract_error_messages()
        timestamps = self.extract_timestamps()
        return {
            'ip_address_count': len(ip_addresses),
            'error_count': len(errors),
            'timestamp_count': len(timestamps)
        }
        
        



class ShowIpInterfaceBriefParser:
    @staticmethod
    def parse(output: str) -> List[Dict[str, str]]:
        """
        Parse the output of 'show ip interface brief' command.

        :param output: The raw command output as a string
        :return: A list of dictionaries with interface details
        :raises ValueError: If the output cannot be parsed
        """
        try:
            lines = output.splitlines()
            interfaces = []
            for line in lines[1:]:  # Skip the header line
                parts = line.split()
                if len(parts) >= 6:
                    interface = {
                        'interface': parts[0],
                        'ip_address': parts[1],
                        'ok': parts[2],
                        'method': parts[3],
                        'status': parts[4],
                        'protocol': parts[5]
                    }
                    interfaces.append(interface)
            return interfaces
        except Exception as e:
            raise ValueError(f"Failed to parse 'show ip interface brief' output: {e}")

class ShowVersionParser:
    @staticmethod
    def parse(output: str) -> Dict[str, Any]:
        """
        Parse the output of 'show version' command.

        :param output: The raw command output as a string
        :return: A dictionary with version details
        :raises ValueError: If the output cannot be parsed
        """
        try:
            version_info = {}
            lines = output.splitlines()
            for line in lines:
                if 'Cisco IOS Software' in line:
                    version_info['software'] = line
                elif 'uptime is' in line:
                    version_info['uptime'] = line.split('is')[-1].strip()
                elif 'System image file is' in line:
                    version_info['system_image'] = line.split('is')[-1].strip().strip('"')
                elif 'Processor board ID' in line:
                    version_info['processor_board_id'] = line.split('ID')[-1].strip()
            return version_info
        except Exception as e:
            raise ValueError(f"Failed to parse 'show version' output: {e}")

class ShowRunningConfigParser:
    @staticmethod
    def parse(output: str) -> str:
        """
        Parse the output of 'show running-config' command.

        :param output: The raw command output as a string
        :return: The running configuration as a string
        """
        return output  # The running config can be returned as is

class ShowInterfacesParser:
    @staticmethod
    def parse(output: str) -> List[Dict[str, str]]:
        """
        Parse the output of 'show interfaces' command.

        :param output: The raw command output as a string
        :return: A list of dictionaries with interface details
        :raises ValueError: If the output cannot be parsed
        """
        try:
            interfaces = []
            interface = {}
            for line in output.splitlines():
                if line and not line.startswith(' '):
                    if interface:
                        interfaces.append(interface)
                    interface = {'interface': line.split()[0]}
                elif 'line protocol' in line:
                    interface['line_protocol'] = line
                elif 'Hardware is' in line:
                    interface['hardware'] = line
                elif 'Internet address' in line:
                    interface['internet_address'] = line
                elif 'MTU' in line:
                    interface['mtu'] = line
            if interface:
                interfaces.append(interface)
            return interfaces
        except Exception as e:
            raise ValueError(f"Failed to parse 'show interfaces' output: {e}")

class ShowIpRouteParser:
    @staticmethod
    def parse(output: str) -> List[Dict[str, str]]:
        """
        Parse the output of 'show ip route' command.

        :param output: The raw command output as a string
        :return: A list of dictionaries with route details
        :raises ValueError: If the output cannot be parsed
        """
        try:
            routes = []
            for line in output.splitlines():
                if line.startswith('O') or line.startswith('C') or line.startswith('S'):
                    parts = line.split()
                    route = {
                        'protocol': parts[0],
                        'network': parts[1],
                        'next_hop': parts[2] if len(parts) > 2 else '',
                    }
                    routes.append(route)
            return routes
        except Exception as e:
            raise ValueError(f"Failed to parse 'show ip route' output: {e}")

class ShowArpParser:
    @staticmethod
    def parse(output: str) -> List[Dict[str, str]]:
        """
        Parse the output of 'show arp' command.

        :param output: The raw command output as a string
        :return: A list of dictionaries with ARP table entries
        :raises ValueError: If the output cannot be parsed
        """
        try:
            lines = output.splitlines()
            arps = []
            for line in lines[1:]:
                parts = line.split()
                if len(parts) >= 5:
                    arp = {
                        'protocol': parts[0],
                        'address': parts[1],
                        'age': parts[2],
                        'mac_address': parts[3],
                        'interface': parts[4]
                    }
                    arps.append(arp)
            return arps
        except Exception as e:
            raise ValueError(f"Failed to parse 'show arp' output: {e}")

class ShowMacAddressTableParser:
    @staticmethod
    def parse(output: str) -> List[Dict[str, str]]:
        """
        Parse the output of 'show mac address-table' command.

        :param output: The raw command output as a string
        :return: A list of dictionaries with MAC address table entries
        :raises ValueError: If the output cannot be parsed
        """
        try:
            lines = output.splitlines()
            mac_table = []
            for line in lines[2:]:  # Skip the header lines
                parts = line.split()
                if len(parts) >= 4:
                    mac_entry = {
                        'vlan': parts[0],
                        'mac_address': parts[1],
                        'type': parts[2],
                        'ports': parts[3]
                    }
                    mac_table.append(mac_entry)
            return mac_table
        except Exception as e:
            raise ValueError(f"Failed to parse 'show mac address-table' output: {e}")

class ShowVlanBriefParser:
    @staticmethod
    def parse(output: str) -> List[Dict[str, str]]:
        """
        Parse the output of 'show vlan brief' command.

        :param output: The raw command output as a string
        :return: A list of dictionaries with VLAN details
        :raises ValueError: If the output cannot be parsed
        """
        try:
            lines = output.splitlines()
            vlans = []
            for line in lines[2:]:  # Skip the header lines
                parts = line.split()
                if len(parts) >= 4:
                    vlan = {
                        'vlan_id': parts[0],
                        'name': parts[1],
                        'status': parts[2],
                        'ports': ' '.join(parts[3:])
                    }
                    vlans.append(vlan)
            return vlans
        except Exception as e:
            raise ValueError(f"Failed to parse 'show vlan brief' output: {e}")

class ShowLoggingParser:
    @staticmethod
    def parse(output: str) -> List[str]:
        """
        Parse the output of 'show logging' command.

        :param output: The raw command output as a string
        :return: A list of log entries
        """
        return output.splitlines()

class ShowIpOspfNeighborParser:
    @staticmethod
    def parse(output: str) -> List[Dict[str, str]]:
        """
        Parse the output of 'show ip ospf neighbor' command.

        :param output: The raw command output as a string
        :return: A list of dictionaries with OSPF neighbor details
        :raises ValueError: If the output cannot be parsed
        """
        try:
            lines = output.splitlines()
            neighbors = []
            for line in lines[1:]:
                parts = line.split()
                if len(parts) >= 6:
                    neighbor = {
                        'neighbor_id': parts[0],
                        'priority': parts[1],
                        'state': parts[2],
                        'dead_time': parts[3],
                        'address': parts[4],
                        'interface': parts[5]
                    }
                    neighbors.append(neighbor)
            return neighbors
        except Exception as e:
            raise ValueError(f"Failed to parse 'show ip ospf neighbor' output: {e}")

# Example usage of parsers:
if __name__ == "__main__":
    show_ip_int_brief_output = """
    Interface              IP-Address      OK? Method Status                Protocol
    GigabitEthernet0/1     192.168.1.1     YES manual up                    up
    GigabitEthernet0/2     192.168.2.1     YES manual administratively down down
    """

    show_version_output = """
    Cisco IOS Software, C2960S Software (C2960S-UNIVERSALK9-M), Version 15.0(2)SE2, RELEASE SOFTWARE (fc1)
    System returned to ROM by power-on
    System image file is "flash:c2960s-universalk9-mz.150-2.SE2.bin"
    Processor board ID FDO1728W0LB
    """

    show_ip_int_brief_parsed = ShowIpInterfaceBriefParser.parse(show_ip_int_brief_output)
    show_version_parsed = ShowVersionParser.parse(show_version_output)

    print("Parsed 'show ip interface brief':")
    print(show_ip_int_brief_parsed)
    print("\nParsed 'show version':")
    print(show_version_parsed)


# Example usage:
if __name__ == "__main__":
    console_output = """
    2024-06-18 20:53:43,678 ERROR in app: Exception on /login [POST]
    Traceback (most recent call last):
    2024-06-18 20:54:43,678 INFO in app: User logged in from 192.168.1.1
    """
    parser = ConsoleParser(console_output)
    print("IP Addresses:", parser.extract_ip_addresses())
    print("Error Messages:", parser.extract_error_messages())
    print("Timestamps:", parser.extract_timestamps())
    print("Summary:", parser.summary())
