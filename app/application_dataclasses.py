from dataclasses import dataclass, field, fields, asdict, is_dataclass
from typing import Dict, List, Any, Optional


class DataclassDunderMethods:
    """
    A  class to automatically generate common dunder methods for dataclasses.
    """
    def to_dict(self) -> Dict[str, Any]:
        """
        Converts the dataclass instance to a dictionary representation.

        Returns:
            Dict[str, Any]: A dictionary of the dataclass fields and their values.
        """
        result = {}
        for field in fields(self):
            value = getattr(self, field.name)
            if is_dataclass(value):
                result[field.name] = value.to_dict()  # Recursive call for nested dataclasses
            elif isinstance(value, list) and value and is_dataclass(value[0]):
                result[field.name] = [v.to_dict() if is_dataclass(v) else v for v in value]
            else:
                result[field.name] = value
        return result
    
    
    def __str__(self) -> str:
        """
        Provides a string representation of the dataclass object with its field names and values.
        """
        available_members = {k: v for k, v in asdict(self).items() if v is not None}
        members_str = ', '.join(f"{k}: {v}" for k, v in available_members.items())
        return f"{self.__class__.__name__}({members_str})"

    def __repr__(self) -> str:
        """
        Provides a detailed string representation suitable for debugging.
        """
        return self.__str__()

    def __eq__(self, other: Any) -> bool:
        """
        Checks if two dataclass objects are equal by comparing their fields.
        """
        if not isinstance(other, self.__class__):
            return False
        return all(getattr(self, f.name) == getattr(other, f.name) for f in fields(self))

    def __hash__(self) -> int:
        """
        Provides a hash value for the dataclass object, allowing it to be used in sets and as dictionary keys.
        """
        return hash(tuple(getattr(self, f.name) for f in fields(self) if getattr(self, f.name) is not None))


@dataclass
class ShowMACAddressTableEntry(DataclassDunderMethods):
    PORT: Optional[str] = None
    DESTINATION_ADDRESS: Optional[str] = None
    TYPE: Optional[str] = None
    VLAN_ID: Optional[str] = None
    DESTINATION_PORT: Optional[List[str]] = field(default_factory=list)


@dataclass
class ShowInterfacesEntry(DataclassDunderMethods):
    INTERFACE: Optional[str] = None
    LINK_STATUS: Optional[str] = None
    PROTOCOL_STATUS: Optional[str] = None
    HARDWARE_TYPE: Optional[str] = None
    MAC_ADDRESS: Optional[str] = None
    BIA: Optional[str] = None
    DESCRIPTION: Optional[str] = None
    IP_ADDRESS: Optional[str] = None
    PREFIX_LENGTH: Optional[str] = None
    MTU: Optional[str] = None
    DUPLEX: Optional[str] = None
    SPEED: Optional[str] = None
    MEDIA_TYPE: Optional[str] = None
    BANDWIDTH: Optional[str] = None
    DELAY: Optional[str] = None
    ENCAPSULATION: Optional[str] = None
    LAST_INPUT: Optional[str] = None
    LAST_OUTPUT: Optional[str] = None
    LAST_OUTPUT_HANG: Optional[str] = None
    QUEUE_STRATEGY: Optional[str] = None
    INPUT_RATE: Optional[str] = None
    OUTPUT_RATE: Optional[str] = None
    INPUT_PPS: Optional[str] = None
    OUTPUT_PPS: Optional[str] = None
    INPUT_PACKETS: Optional[str] = None
    OUTPUT_PACKETS: Optional[str] = None
    RUNTS: Optional[str] = None
    GIANTS: Optional[str] = None
    INPUT_ERRORS: Optional[str] = None
    CRC: Optional[str] = None
    FRAME: Optional[str] = None
    OVERRUN: Optional[str] = None
    ABORT: Optional[str] = None
    OUTPUT_ERRORS: Optional[str] = None
    VLAN_ID: Optional[str] = None
    VLAN_ID_INNER: Optional[str] = None
    VLAN_ID_OUTER: Optional[str] = None


@dataclass
class ShowInterfacesStatusEntry(DataclassDunderMethods):
    PORT: Optional[str] = None
    NAME: Optional[str] = None
    STATUS: Optional[str] = None
    VLAN_ID: Optional[str] = None
    DUPLEX: Optional[str] = None
    SPEED: Optional[str] = None
    TYPE: Optional[str] = None
    FC_MODE: Optional[str] = None


@dataclass
class ShowIPARPEntry(DataclassDunderMethods):
    PROTOCOL: Optional[str] = None
    IP_ADDRESS: Optional[str] = None
    AGE: Optional[str] = None
    MAC_ADDRESS: Optional[str] = None
    TYPE: Optional[str] = None
    INTERFACE: Optional[str] = None

    
@dataclass
class DeviceConnectionData(DataclassDunderMethods):
    device_type: str = 'cisco_ios'
    host:str = None
    username:str = None
    password:str = None
    secret:str = None


@dataclass
class NetworkDeviceEntry(DataclassDunderMethods):
    switch_hostname:str = None
    switch_ip_address:str = None
    switch_region:str = None
    device_connection_status: Optional[str] = None
    device_connection_data: Optional[DeviceConnectionData] = None
    show_interfaces_entry_list: Optional[List[ShowInterfacesEntry]] = field(default_factory=list)
    show_interfaces_status_entry_list: Optional[List[ShowInterfacesStatusEntry]] = field(default_factory=list)
    show_ip_arp_entry_list: Optional[List[ShowIPARPEntry]] = field(default_factory=list)
    show_mac_address_table_entry_list: Optional[List[ShowMACAddressTableEntry]] = field(default_factory=list)

@dataclass
class User(DataclassDunderMethods):
    username: Optional[str] = None 
    name: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    notes: Optional[str] = None
 
    
@dataclass
class Computer(DataclassDunderMethods):
    hostname: Optional[str] = None
    ip_address: Optional[str] = None
    mac_address: Optional[str] = None
    users: Optional[List[User]] = field(default_factory=list)
     
######################################################
# Example Dictionaries and Unpacking
#
# device_connection_data_dict = {
#     "device_type": "cisco_ios",
#     "host": "192.168.1.1",
#     "username": "admin",
#     "password": "password",
#     "secret": "secret"
# }
#
# device_connection_data = DeviceConnectionData(**device_connection_data_dict)
# print(device_connection_data)
#
# interface_data_dict = {
#     "LINK_STATUS": "up",
#     "PROTOCOL_STATUS": "up",
#     "HARDWARE_TYPE": "Ethernet",
#     "MAC_ADDRESS": "00:1A:2B:3C:4D:5E",
#     "BIA": "00:1A:2B:3C:4D:5E",
#     "DESCRIPTION": "GigabitEthernet0/1",
#     "IP_ADDRESS": "192.168.1.1",
#     "PREFIX_LENGTH": "24",
#     "MTU": "1500",
#     "DUPLEX": "full",
#     "SPEED": "1000Mb/s",
#     "MEDIA_TYPE": "RJ45",
#     "BANDWIDTH": "1000000",
#     "DELAY": "10",
#     "ENCAPSULATION": "ARPA",
#     "LAST_INPUT": "never",
#     "LAST_OUTPUT": "00:00:00",
#     "LAST_OUTPUT_HANG": "never",
#     "QUEUE_STRATEGY": "fifo",
#     "INPUT_RATE": "0",
#     "OUTPUT_RATE": "0",
#     "INPUT_PPS": "0",
#     "OUTPUT_PPS": "0",
#     "INPUT_PACKETS": "0",
#     "OUTPUT_PACKETS": "0",
#     "RUNTS": "0",
#     "GIANTS": "0",
#     "INPUT_ERRORS": "0",
#     "CRC": "0",
#     "FRAME": "0",
#     "OVERRUN": "0",
#     "ABORT": "0",
#     "OUTPUT_ERRORS": "0",
#     "VLAN_ID": "10",
#     "VLAN_ID_INNER": "20",
#     "VLAN_ID_OUTER": "30"
# }
#
# interface_data = InterfaceData(**interface_data_dict)
# print(interface_data)
#
#
# network_device_data_dict = {
#     "switch_hostname": "switch1",
#     "switch_ip_address": "192.168.1.2",
#     "switch_region": "US-West",
#     "device_connection_data": device_connection_data_dict,
#     "interface_data": [interface_data_dict]
# }
#
# network_device_data = NetworkDeviceEntry(
#     switch_hostname=network_device_data_dict["switch_hostname"],
#     switch_ip_address=network_device_data_dict["switch_ip_address"],
#     switch_region=network_device_data_dict["switch_region"],
#     device_connection_data=DeviceConnectionData(**network_device_data_dict["device_connection_data"]),
#     interface_data=[InterfaceData(**iface) for iface in network_device_data_dict["interface_data"]]
# )
# print(network_device_data)
#
#
# user_dict = {
#     "username": "jdoe",
#     "name": "John Doe",
#     "email": "jdoe@example.com",
#     "phone": "123-456-7890"
# }
#
# user = User(**user_dict)
# print(user)
#
# computer_dict = {
#     "hostname": "comp1",
#     "ip_address": "192.168.1.3",
#     "mac_address": "00:1A:2B:3C:4D:5F",
#     "users": [user_dict]
# }
#
# computer = Computer(
#     hostname=computer_dict["hostname"],
#     ip_address=computer_dict["ip_address"],
#     mac_address=computer_dict["mac_address"],
#     users=[User(**usr) for usr in computer_dict["users"]]
# )
# print(computer)

