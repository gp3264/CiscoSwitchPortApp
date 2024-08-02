import os
import sys
import re
from typing import Any, List, Dict, Optional
from app.cli_connection import CLIConnection
from textfsm import TextFSM



class CiscoInterfaceTimeParser:
    TIME_FORMATS = [
        r'^(?P<hours>\d+):(?P<minutes>\d+):(?P<seconds>\d+)$',  # HH:MM:SS
        r'^(?P<days>\d+)d(?P<hours>\d+)h$',  # DDhHH
        r'^(?P<weeks>\d+)w(?P<days>\d+)d$',  # WWdDD
        r'^(?P<years>\d+)y(?P<weeks>\d+)w$',  # YYwWW
        r'^never$'  # never
    ]

    @staticmethod
    def parse_time_string(time_str: str) -> Optional[int]:
        """
        Parse a time string and return the number of seconds.

        :param time_str: The time string to parse.
        :return: The number of seconds, or None if the time string is 'never'.
        """
        if time_str == 'never':
            return None

        for time_format in CiscoInterfaceTimeParser.TIME_FORMATS:
            match = re.match(time_format, time_str)
            if match:
                time_dict = match.groupdict()
                return CiscoInterfaceTimeParser.calculate_seconds(time_dict)

        raise ValueError(f"Unrecognized time format: {time_str}")

    @staticmethod
    def calculate_seconds(time_dict: dict) -> int:
        """
        Calculate the number of seconds from a time dictionary.

        :param time_dict: A dictionary containing time components.
        :return: The number of seconds.
        """
        seconds = 0
        if 'seconds' in time_dict:
            seconds += int(time_dict['seconds'])
        if 'minutes' in time_dict:
            seconds += int(time_dict['minutes']) * 60
        if 'hours' in time_dict:
            seconds += int(time_dict['hours']) * 3600
        if 'days' in time_dict:
            seconds += int(time_dict['days']) * 86400
        if 'weeks' in time_dict:
            seconds += int(time_dict['weeks']) * 604800
        if 'years' in time_dict:
            seconds += int(time_dict['years']) * 31536000
        return seconds

    @staticmethod
    def is_time_over_days(time_str: str, days: int) -> bool:
        """
        Evaluate if the parsed time is over a certain number of days.

        :param time_str: The time string to parse.
        :param days: The number of days to compare against.
        :return: True if the parsed time is over the given number of days, False otherwise.
        """
        seconds = CiscoInterfaceTimeParser.parse_time_string(time_str)
        if seconds is None:
            return False  # 'never' should not be considered over any time period
        return seconds > days * 86400

    @staticmethod        
    def convert_seconds_to_time(seconds: int) -> str:
        """
        Convert a number of seconds to a human-readable time format.

        :param seconds: The number of seconds.
        :return: A string representing the time in a human-readable format.
        """
        if seconds is None:
            return 'never'
        
        years, seconds = divmod(seconds, 31536000)
        weeks, seconds = divmod(seconds, 604800)
        days, seconds = divmod(seconds, 86400)
        hours, seconds = divmod(seconds, 3600)
        minutes, seconds = divmod(seconds, 60)

        time_str = ""
        if years > 0:
            time_str += f"{years}y"
        if weeks > 0:
            time_str += f"{weeks}w"
        if days > 0:
            time_str += f"{days}d"
        if hours > 0:
            time_str += f"{hours}h"
        if minutes > 0 or (hours > 0 and seconds > 0):  # Include minutes if there are hours or seconds
            time_str += f"{minutes}m"
        if seconds > 0:
            time_str += f"{seconds}s"

        return time_str or "0s"


class CLICommandsTemplates:
    
    TEMPLATE_PATH = '../venv/Lib/site-packages/ntc_templates/templates'

    @staticmethod
    def parse_output(template_name: str, command_output: str) -> List[Dict[str, Any]]:
        """
        Parse the command output using TextFSM templates.

        :param template_name: The name of the TextFSM template
        :param command_output: The raw command output as a string
        :return: A list of dictionaries with parsed data
        :raises RuntimeError: If the parsing fails
        """
        try:
            template_path = os.path.join(os.path.dirname(__file__), 'ntc-templates', 'templates', template_name)
            template_path = f"c:/CiscoSwitchPortApp/venv/Lib/site-packages/ntc_templates/templates/{template_name}"
            
            with open(template_path) as template_file:
                fsm = TextFSM(template_file)
                parsed_output = fsm.ParseText(command_output)
                headers = fsm.header
                return [dict(zip(headers, row)) for row in parsed_output]
        except Exception as e:
            raise RuntimeError(f"Failed to parse output using template {template_name}: {e}")

    @staticmethod
    def show_ip_interface_brief(connection: CLIConnection) -> List[Dict[str, Any]]:
        """
        Run 'show ip interface brief' command and return the parsed output.

        :param connection: CLIConnection instance
        :return: Parsed output of the command
        :raises RuntimeError: If the command execution or parsing fails
        """
        try:
            output = connection.run_command('show ip interface brief')
            return CLICommandsTemplates.parse_output('cisco_ios_show_ip_interface_brief.textfsm', output)
        except Exception as e:
            raise RuntimeError("Failed to run or parse 'show ip interface brief'") from e

    @staticmethod
    def show_version(connection: CLIConnection) -> List[Dict[str, Any]]:
        """
        Run 'show version' command and return the parsed output.

        :param connection: CLIConnection instance
        :return: Parsed output of the command
        :raises RuntimeError: If the command execution or parsing fails
        """
        try:
            output = connection.run_command('show version')
            return CLICommandsTemplates.parse_output('cisco_ios_show_version.textfsm', output)
        except Exception as e:
            raise RuntimeError("Failed to run or parse 'show version'") from e

    @staticmethod
    def show_running_config(connection: CLIConnection) -> List[Dict[str, Any]]:
        """
        Run 'show running-config' command and return the parsed output.

        :param connection: CLIConnection instance
        :return: Parsed output of the command
        :raises RuntimeError: If the command execution or parsing fails
        """
        try:
            output = connection.run_command('show running-config')
            return CLICommandsTemplates.parse_output('cisco_ios_show_running-config.textfsm', output)
        except Exception as e:
            raise RuntimeError("Failed to run or parse 'show running-config'") from e

    @staticmethod
    def show_interfaces(connection: CLIConnection) -> List[Dict[str, Any]]:
        """
        Run 'show interfaces' command and return the parsed output.

        :param connection: CLIConnection instance
        :return: Parsed output of the command
        :raises RuntimeError: If the command execution or parsing fails
        """
        try:
            output = connection.run_command('show interfaces')
            #print(output)
            return CLICommandsTemplates.parse_output('cisco_ios_show_interfaces.textfsm', output)
        except Exception as e:
            raise RuntimeError("Failed to run or parse 'show interfaces'") from e
        
    @staticmethod
    def show_interfaces_switchport(connection: CLIConnection) -> List[Dict[str, Any]]:
        """
        Run 'show interfaces switchport' command and return the parsed output.

        :param connection: CLIConnection instance
        :return: Parsed output of the command
        :raises RuntimeError: If the command execution or parsing fails
        """
        try:
            output = connection.run_command('show interfaces switchport')
   
            return CLICommandsTemplates.parse_output('cisco_ios_show_interfaces_switchport.textfsm', output)
        except Exception as e:
            raise RuntimeError("Failed to run or parse 'show interfaces switchport'") from e

    @staticmethod
    def show_ip_route(connection: CLIConnection) -> List[Dict[str, Any]]:
        """
        Run 'show ip route' command and return the parsed output.

        :param connection: CLIConnection instance
        :return: Parsed output of the command
        :raises RuntimeError: If the command execution or parsing fails
        """
        try:
            output = connection.run_command('show ip route')
            return CLICommandsTemplates.parse_output('cisco_ios_show_ip_route.textfsm', output)
        except Exception as e:
            raise RuntimeError("Failed to run or parse 'show ip route'") from e

    @staticmethod
    def show_ip_arp(connection: CLIConnection) -> List[Dict[str, Any]]:
        """
        Run 'show arp' command and return the parsed output.

        :param connection: CLIConnection instance
        :return: Parsed output of the command
        :raises RuntimeError: If the command execution or parsing fails
        """
        try:
            output = connection.run_command('show arp')
            return CLICommandsTemplates.parse_output('cisco_ios_show_ip_arp.textfsm', output)
        except Exception as e:
            raise RuntimeError("Failed to run or parse 'show ip arp'") from e
    
    @staticmethod
    def show_ip_interface(connection: CLIConnection) -> List[Dict[str, Any]]:
        """
        Run 'show ip interface' command and return the parsed output.

        :param connection: CLIConnection instance
        :return: Parsed output of the command
        :raises RuntimeError: If the command execution or parsing fails
        """
        try:
            output = connection.run_command('show ip interface')
            #print(output)
            return CLICommandsTemplates.parse_output('cisco_ios_show_ip_interface.textfsm', output)
        except Exception as e:
            raise RuntimeError("Failed to run or parse 'show ip interface'") from e        
        
    
        

    @staticmethod
    def show_mac_address_table(connection: CLIConnection) -> List[Dict[str, Any]]:
        """
        Run 'show mac address-table' command and return the parsed output.

        :param connection: CLIConnection instance
        :return: Parsed output of the command
        :raises RuntimeError: If the command execution or parsing fails
        """
        try:
            output = connection.run_command('show mac address-table')
            return CLICommandsTemplates.parse_output('cisco_ios_show_mac-address-table.textfsm', output)
        except Exception as e:
            raise RuntimeError("Failed to run or parse 'show mac address-table'") from e

    @staticmethod
    def show_vlan_brief(connection: CLIConnection) -> List[Dict[str, Any]]:
        """
        Run 'show vlan brief' command and return the parsed output.

        :param connection: CLIConnection instance
        :return: Parsed output of the command
        :raises RuntimeError: If the command execution or parsing fails
        """
        try:
            output = connection.run_command('show vlan brief')
            return CLICommandsTemplates.parse_output('cisco_ios_show_vlan.textfsm', output)
        except Exception as e:
            raise RuntimeError("Failed to run or parse 'show vlan brief'") from e

    @staticmethod
    def show_logging(connection: CLIConnection) -> List[Dict[str, Any]]:
        """
        Run 'show logging' command and return the parsed output.

        :param connection: CLIConnection instance
        :return: Parsed output of the command
        :raises RuntimeError: If the command execution or parsing fails
        """
        try:
            output = connection.run_command('show logging')
            return CLICommandsTemplates.parse_output('cisco_ios_show_logging.textfsm', output)
        except Exception as e:
            raise RuntimeError("Failed to run or parse 'show logging'") from e

    @staticmethod
    def show_ip_ospf_neighbor(connection: CLIConnection) -> List[Dict[str, Any]]:
        """
        Run 'show ip ospf neighbor' command and return the parsed output.

        :param connection: CLIConnection instance
        :return: Parsed output of the command
        :raises RuntimeError: If the command execution or parsing fails
        """
        try:
            output = connection.run_command('show ip ospf neighbor')
            return CLICommandsTemplates.parse_output('cisco_ios_show_ip_ospf_neighbor.textfsm', output)
        except Exception as e:
            raise RuntimeError("Failed to run or parse 'show ip ospf neighbor'") from e

    @staticmethod
    def show_interface(connection: CLIConnection, interface: str) -> List[Dict[str, Any]]:
        """
        Run 'show interface <interface>' command and return the parsed output.

        :param connection: CLIConnection instance
        :param interface: Name of the interface to show
        :return: Parsed output of the command
        :raises RuntimeError: If the command execution or parsing fails
        """
        try:
            output = connection.run_command(f'show interface {interface}')
            return CLICommandsTemplates.parse_output('cisco_ios_show_interfaces_status.textfsm', output)
        except Exception as e:
            raise RuntimeError(f"Failed to run or parse 'show interface {interface}'") from e

    @staticmethod
    def show_interface_status(connection: CLIConnection) -> List[Dict[str, Any]]:
        """
        Run 'show interface status' command and return the parsed output.

        :param connection: CLIConnection instance
        :return: Parsed output of the command
        :raises RuntimeError: If the command execution or parsing fails
        """
        try:
            output = connection.run_command('show interface status')
            return CLICommandsTemplates.parse_output('cisco_ios_show_interfaces_status.textfsm', output)
        except Exception as e:
            raise RuntimeError("Failed to run or parse 'show interface status'") from e

    @staticmethod
    def shutdown_interface(connection: CLIConnection, interface: str) -> str:
        """
        Administratively shutdown the specified interface.

        :param connection: CLIConnection instance
        :param interface: Name of the interface to shutdown
        :return: Output of the 'show interface <interface>' command after shutdown
        :raises RuntimeError: If the command execution fails
        """
        commands = [
            f'interface {interface}',
            'shutdown'
        ]
        try:
            connection.send_config_set(commands)
            return connection.run_command(f'show interface {interface}')
        except Exception as e:
            raise RuntimeError(f"Failed to shutdown interface {interface}") from e

    @staticmethod
    def no_shutdown_interface(connection: CLIConnection, interface: str) -> str:
        """
        Administratively bring up the specified interface.

        :param connection: CLIConnection instance
        :param interface: Name of the interface to bring up
        :return: Output of the 'show interface <interface>' command after no shutdown
        :raises RuntimeError: If the command execution fails
        """
        commands = [
            f'interface {interface}',
            'no shutdown'
        ]
        try:
            connection.send_config_set(commands)
            return connection.run_command(f'show interface {interface}')
        except Exception as e:
            raise RuntimeError(f"Failed to no shutdown interface {interface}") from e

    @staticmethod
    def enter_config_mode(connection: CLIConnection) -> None:
        """
        Enter global configuration mode.

        :param connection: CLIConnection instance
        :raises RuntimeError: If entering config mode fails
        """
        try:
            connection.config_mode()
        except Exception as e:
            raise RuntimeError("Failed to enter config mode") from e

    @staticmethod
    def exit_config_mode(connection: CLIConnection) -> None:
        """
        Exit global configuration mode.

        :param connection: CLIConnection instance
        :raises RuntimeError: If exiting config mode fails
        """
        try:
            connection.exit_config_mode()
        except Exception as e:
            raise RuntimeError("Failed to exit config mode") from e


class CLIExecutive(CLICommandsTemplates):

    def __init__(self):
        self._is_connected: bool = False
        self._device: Dict[str, Any] = {}
        self._data:Any = None
        self._connection: CLIConnection = None
    
    def setup_device(self, username="user", password="password", host="0.0.0.0", secret="enable_password", device_type="cisco_ios"):
        self._device: Dict[str, Any] = {
        'device_type': device_type,
        'host': host,  # '10.95.72.22',
        'username': username,  # 'gphillips3',
        'password': password,  # '',
        'secret': secret ,  # 'enable_password',
        }
    
    def enter_enable_mode(self):
        if self._is_connected:
            self.connection.enter_enable_mode()
        else:
            print(f'Device Not connected', file=sys.stderr) 
    
    @property
    def device(self):
        return self._device
    
    @device.setter
    def device(self, **kwargs):
        self._device: Dict[str, Any] = {
        'device_type': kwargs.get('device_type', ''),
        'host': kwargs.get('host', ''),  # '10.95.72.22',
        'username': kwargs.get('username', ''),  # 'gphillips3',
        'password': kwargs.get('password', ''),  # '',
        'secret': kwargs('secret', '') ,  # 'enable_password',
        }
    
    def _is_device_connection_fields_Ok(self) -> bool:
        return ((self._device['device_type'] is not None or self._device['device_type'] != "") and   
                (self._device['host'] is None or self._device['host'] != "") and  
                (self._device['username'] is None or self._device['username'] != "")  and  
                (self._device['password'] is None or self._device['password'] != "")  and  
                (self._device['secret'] is None or self._device['secret'] != ""))
    
    def connect(self) -> bool:
        if self._is_device_connection_fields_Ok(): 
            
            try:
                self._connection = CLIConnection(**self._device)
            except Exception as e:
                self._is_connected = False 
                print(f'Connection Error: {e}', file=sys.stderr) 
                return None
            
            self._is_connected = True
            return self.connection
        else:
            
            self._is_connected = False 
            
            
            try:
                raise Exception("Device Properties not set")
            except Exception as e:
                print(f'Device Connection Error: {e}', file=sys.stderr) 
                return None
                
    def disconnect(self) -> bool:
        try:
            self._connection.disconnect()
            self._is_connected = False
            return True
        except Exception as e:
            print(f'Connection Error: {e}', file=sys.stderr) 
            return False
     
    @property
    def connected(self):
        return self._is_connected
        
    @property
    def host(self):
        return self._device['host']
    
    @host.setter
    def host(self, host:str):
        try:
            self.disconnect()
        except:
            pass
        self.setup_device(self._device['username'], self._device['password'], host, self._device['secret'], self._device['device_type'])
        
    @property
    def username(self):
        return self._device['username']
    
    @username.setter
    def username(self, username:str):
        try:
            self.disconnect()
        except:
            pass
        self.setup_device(username, self._device['password'], self._device['host'], self._device['secret'], self._device['device_type'])
    
    @property
    def password(self):
        return self._device['password']
    
    @password.setter
    def password(self, password:str):
        try:
            self.disconnect()
        except:
            pass
        self.setup_device(self._device['username'], password, self._device['host'], self._device['secret'], self._device['device_type'])
        
    @property
    def secret(self):
        return self._device['password']
    
    @secret.setter
    def secret(self, secret:str):
        try:
            self.disconnect()
        except:
            pass
        self.setup_device(self._device['username'], self._device['password'], self._device['host'], secret, self._device['device_type'])
    
    @property
    def connection(self):
        return self._connection
    
    @connection.setter
    def connection(self, connection):
        self._connection = connection
        
    @property
    def data(self) -> Any:
        return self._data
    
    @data.setter
    def data(self, data:Any):
        self._data = data


# Example usage:
if __name__ == "__main__":
#    from app.cli_connection import CLIConnection
    from pprint import pprint

    device: Dict[str, Any] = {
        'device_type': 'cisco_ios',
        'host': '0.0.0.0',
        'username': 'user',
        'password': 'password',
        'secret': 'enable_password',
    }

    connection = CLIConnection(**device)
    try:
        connection.enter_enable_mode()
    #    print("Show IP Interface Brief:")
    #    print(CLICommandsTemplates.show_ip_interface_brief(connection))

    #    print("\nShow Version:")
    #    print(CLICommandsTemplates.show_version(connection))

        # print("\nShow Running Config:")
        # print(CLICommandsTemplates.show_running_config(connection))

        print("\nShow Interfaces:")
        pprint(CLICommandsTemplates.show_interfaces(connection))

    #    print("\nShow IP Route:")
    #    print(CLICommandsTemplates.show_ip_route(connection))

    #    print("\nShow IP ARP:")
    #    print(CLICommandsTemplates.show_ip_arp(connection))

        print("\nShow MAC Address Table:")
        pprint(CLICommandsTemplates.show_mac_address_table(connection))

    #    print("\nShow VLAN Brief:")
    #    print(CLICommandsTemplates.show_vlan_brief(connection))

    #    print("\nShow Logging:")
    #    print(CLICommandsTemplates.show_logging(connection))

    #    print("\nShow IP OSPF Neighbor:")
    #    print(CLICommandsTemplates.show_ip_ospf_neighbor(connection))

#        interface = 'GigabitEthernet0/1'
#        print(f"\nShow Interface {interface}:")
#        print(CLICommandsTemplates.show_interface(connection, interface))

        # print(f"\nShow Interface Status:")
        # pprint(CLICommandsTemplates.show_interface_status(connection))

        # print(f"\nEntering config mode to shutdown Interface {interface}:")
        # CLICommandsTemplates.enter_config_mode(connection)
        # print(CLICommandsTemplates.shutdown_interface(connection, interface))
        # CLICommandsTemplates.exit_config_mode(connection)
        #
        # print(f"\nEntering config mode to bring up Interface {interface}:")
        # CLICommandsTemplates.enter_config_mode(connection)
        # print(CLICommandsTemplates.no_shutdown_interface(connection, interface))
        # CLICommandsTemplates.exit_config_mode(connection)
    finally:
        connection.disconnect()
