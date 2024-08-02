from pprint import pprint, pformat
from typing import Dict
from app.file_support import FileHandler 
from app.mac_address_support import MacAddressSupport
from app.cli_commands_templates import CLIExecutive
from app.application_dataclasses import *
from app.application_dataclasses_support import *


class MainDataRetrieval:

    def __init__(self, **kwargs):
        
        self._username = kwargs.get("username", None)
        self._password = kwargs.get("password", None)     
        
        self._device_connection_data_dict: Dict[str, Any] = None 
        self.region_nodes_json_file = kwargs.get("filename", r'region_nodes.json')
        
        self._load_file(self.region_nodes_json_file)
        
        self.Data:Dict[str:Any] = {}
        self.Data['network_cisco_switches'] = self._populate_cli_data(self.build_network_device_data_structure())
    
    def _load_file(self, filename):
        self.region_nodes = FileHandler.read_json(filename)
    
    def build_network_device_data_structure(self) -> List[NetworkDeviceEntry]:
        devices_list:List[NetworkDeviceEntry] = []
        for region in self.region_nodes['MDTA_Regions']:
            for node in region['nodes']:
                
                network_device = NetworkDeviceEntry(
                    switch_hostname=node["Node_Name"],
                    switch_ip_address=node["IP"],
                    switch_region=region["region_name"],
                    device_connection_data=DeviceConnectionData(**self._create_device_connection_data(host=node['IP'])),
                    )
                
                devices_list.append(network_device)
                network_device = None
        return devices_list
    
    def _populate_cli_data(self, devices:List[NetworkDeviceEntry]) -> List[NetworkDeviceEntry]: 
        updated_devices: List[NetworkDeviceEntry] = []
        for device in devices:
            updated_devices.append(self._extract_console_data_from_device(device))
        return updated_devices   
  
    def _create_device_connection_data(self, **kwargs):
        device_connection_data_dict = {
            'device_type': kwargs.get("device_type", 'cisco_ios'),
            'host': kwargs.get("host", None),  # 10.95.72.22',
            'username': kwargs.get("username", self._username),
            'password': kwargs.get("password", self._password),
            'secret': kwargs.get("secret", 'enable_password'),
        }   
        return device_connection_data_dict
  
    @staticmethod
    def _extract_console_data_from_device(device: NetworkDeviceEntry) -> NetworkDeviceEntry:
        cli = CLIExecutive()
        cli.setup_device(**device.device_connection_data.to_dict())
        cli.connect()
        if cli._is_connected == False: 
            device.device_connection_status = "Unable to Connect."
            return None
        show_interfaces_entry_list:List[ShowInterfacesEntry] = []
        for cli_record in cli.show_interfaces(cli.connection):
            show_interfaces_entry_list.append(ShowInterfacesEntry(**cli_record))
        device.show_interfaces_entry_list = show_interfaces_entry_list
        
        show_ip_arp_entry_list:List[ShowIPARPEntry] = []
        for cli_record in cli.show_ip_arp(cli.connection):
            show_ip_arp_entry_list.append(ShowIPARPEntry(**cli_record))
        device.show_ip_arp_entry_list = show_ip_arp_entry_list      

        show_mac_address_table_entry_list:List[ShowMACAddressTableEntry] = []
        for cli_record in cli.show_mac_address_table(cli.connection):
            show_mac_address_table_entry_list.append(ShowMACAddressTableEntry(**cli_record))
        device.show_mac_address_table_entry_list = show_mac_address_table_entry_list       
        
        show_interfaces_status_entry_list:List[ShowInterfacesStatusEntry] = []
        for cli_record in cli.show_interface_status(cli.connection):
            show_interfaces_status_entry_list.append(ShowInterfacesStatusEntry(**cli_record))
        device.show_interfaces_status_entry_list = show_interfaces_status_entry_list       
        
        device.device_connection_status = "Connected and Data Retrieved"
        cli.disconnect()
        device_connections_data: DeviceConnectionData = device.device_connection_data
        device_connections_data.password = "********"
        device.device_connection_data = device_connections_data
        return device
        
    # @staticmethod
    # def convert_console_data_to_dataclass(dataobject: Type, **data:Any):
    #     try:
    #
    
    def __str__(self):
        return pformat(self.Data['network_cisco_switches'])
        
        
if __name__ == "__main__":
    sample = MainDataRetrieval(filename="region_nodes.json", username="gphillips3", password="02121103!Jun24")
    print(str(sample))
    
        
