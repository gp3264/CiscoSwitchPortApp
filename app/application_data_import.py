from pprint import pprint, pformat
from typing import Dict
from app.file_support import FileHandler 
from app.mac_address_support import MacAddressSupport
from app.cli_commands_templates import CLIExecutive
from app.application_dataclasses import *
from app.application_dataclasses_support import *
from app.SupportUtilities import TaskProgressIndicator
from app.file_support import FileConverter, FileHandler
from app.application_views import PortSecurityView
import os


class MainApplication:
    pass


class MainDataImport():
    def __init__(self, **kwargs):
        self.cisco_switches:CiscoDataRetrieval = CiscoDataRetrieval(**kwargs)
        
        
class CreateViews:
    def __init__(self, **kwargs):
        devices:List[NetworkDeviceEntry] = kwargs.get("", None)
        
        if (devices):
            self.port_security_view: PortSecurityView = PortSecurityView(devices)
        

class CiscoDataRetrieval:

    def __init__(self, **kwargs):
        
        print("Clean up previous cli_connection.log...")
        file_path = r'..\app\cli_connection.log'
        
        try:
            os.remove(file_path)
            print(f"File '{file_path}' has been deleted successfully.")
        except FileNotFoundError:
            print(f"File '{file_path}' not found.")
        except PermissionError:
            print(f"Permission denied: Unable to delete file '{file_path}'.")
        except Exception as e:
            print(f"An error occurred while deleting the file: {e}")
        
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
                
                template_active_flags = InfoErrorFlags(name="tempalte_active_flags", 
                                                       description = "Bit on when template is in use")
                template_error_flags = InfoErrorFlags(name="tempalte_active_flags", 
                                                       description = "Bit on when template has error condition") 
                
                
                network_device = NetworkDeviceEntry(
                    textfsm_templates_active = template_active_flags,
                    textfsm_templates_errors = template_error_flags,
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
        device_count:int = len(devices)
        task_progress:TaskProgressIndicator = TaskProgressIndicator("CLI Load Progress", device_count)
        task_progress.start()
        counter = 0
        for device in devices:
            counter +=1
            updated_devices.append(self._extract_console_data_from_device(device))
            task_progress.update_task_name(f"CLI Loading Progress: {device.switch_hostname} {counter}/{device_count}                     ")
            task_progress.update_progress()
        task_progress.update_task_name("CLI Loading Progress")
        task_progress.complete()
    
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
        device.device_connection_status = "]"
        cli = CLIExecutive()
        cli.setup_device(**device.device_connection_data.to_dict())
        cli.connect()
        if cli._is_connected == False: 
            device.device_connection_status = "Unable to Connect."
            return None
        
        device.device_connection_status = f"{device.device_connection_status}"

        try:
            show_verion_data:ShowVersionData = ShowVersionData(cli.show_version(cli.connection))
            device.show_version_data = show_verion_data 
            device.device_connection_status = f"{device.device_connection_status}; show version: OK "   
            device.textfsm_templates_active.set_template("show_version", True)
        except TypeError as e0:
            device.show_interfaces_entry_list = []
            device.device_connection_status = f"{device.device_connection_status}; show version: TypeError {e0}"
            device.textfsm_templates_errors.set_template("show_version", True)            
        except RuntimeError as e1:
            device.show_interfaces_entry_list = []
            device.device_connection_status = f"{device.device_connection_status}; show version: Parsing Failed: {e1}"
            device.textfsm_templates_errors.set_template("show_version", True)
        except Exception as e2:
            device.device_connection_status = f"{device.device_connection_status}; show version: Error: {e2}"
            device.textfsm_templates_errors.set_template("show_version", True)
        finally:
            pass  


        
        try:
            show_interfaces_entry_list:List[ShowInterfacesEntry] = []
            for cli_record in cli.show_interfaces(cli.connection):
                show_interfaces_entry_list.append(ShowInterfacesEntry(**cli_record))
            device.show_interfaces_entry_list = show_interfaces_entry_list
            device.device_connection_status = f"{device.device_connection_status}; show interfaces: OK "   
            device.textfsm_templates_active.set_template("show_interface", True)
        except TypeError as e0:
            device.show_interfaces_entry_list = []
            device.device_connection_status = f"{device.device_connection_status}; show interfaces: TypeError {e0}"
            device.textfsm_templates_errors.set_template("show_interface", True)  
        except RuntimeError as e1:
            device.show_interfaces_entry_list = []
            device.device_connection_status = f"{device.device_connection_status}; show interfaces: Parsing Failed: {e1}"
            device.textfsm_templates_errors.set_template("show_interface", True)
        except Exception as e2:
            device.device_connection_status = f"{device.device_connection_status}; show interfaces: Error: {e2}"
            device.textfsm_templates_errors.set_template("show_interface", True)
            pass  
    
        try: 
            show_ip_arp_entry_list:List[ShowIPARPEntry] = []
            for cli_record in cli.show_ip_arp(cli.connection):
                show_ip_arp_entry_list.append(ShowIPARPEntry(**cli_record))
            device.show_ip_arp_entry_list = show_ip_arp_entry_list   
            device.device_connection_status = f"{device.device_connection_status}; show ip arp: OK "     
            device.textfsm_templates_active.set_template("show_ip_arp", True)
        except TypeError as e0:
            device.show_interfaces_entry_list = []
            device.device_connection_status = f"{device.device_connection_status}; show ip arp: TypeError {e0}"
            device.textfsm_templates_errors.set_template("show_ip_arp", True)  
        except RuntimeError as e1:
            device.show_interfaces_entry_list = []
            device.device_connection_status = f"{device.device_connection_status}; show ip arp: Parsing Failed: {e1}"
            device.textfsm_templates_errors.set_template("show_ip_arp", True)
        except Exception as e2:
            device.device_connection_status = f"{device.device_connection_status}; show ip arp: Error: {e2}"
            device.textfsm_templates_errors.set_template("show_ip_arp", True)
        finally:
            pass

        try:
            show_mac_address_table_entry_list:List[ShowMACAddressTableEntry] = []
            for cli_record in cli.show_mac_address_table(cli.connection):
                show_mac_address_table_entry_list.append(ShowMACAddressTableEntry(**cli_record))
            device.show_mac_address_table_entry_list = show_mac_address_table_entry_list 
            device.device_connection_status = f"{device.device_connection_status}; show mac address-table: OK "   
            device.textfsm_templates_active.set_template("show_mac_address_table", True)   
        except TypeError as e0:
            device.show_interfaces_entry_list = []
            device.device_connection_status = f"{device.device_connection_status}; show mac address table: TypeError {e0}"
            device.textfsm_templates_errors.set_template("show_mac_address_table", True)  
        except RuntimeError as e1:
            device.show_interfaces_entry_list = []
            device.device_connection_status = f"{device.device_connection_status}; show mac address-table: Parsing Failed: {e1}"
            device.textfsm_templates_errors.set_template("show_mac_address_table", True)
        except Exception as e2:
            device.device_connection_status = f"{device.device_connection_status}; show mac address-table: Error: {e2}"
            device.textfsm_templates_errors.set_template("show_mac_address_table", True)
        finally:
            pass

        try:
            show_interfaces_status_entry_list:List[ShowInterfacesStatusEntry] = []
            cli_records = cli.show_interface_status(cli.connection)
            for cli_record in cli_records:
                show_interfaces_status_entry_list.append(ShowInterfacesStatusEntry(**cli_record))
            device.show_interfaces_status_entry_list = show_interfaces_status_entry_list   
            device.device_connection_status = f"{device.device_connection_status}; show interfaces status: OK "   
            device.textfsm_templates_active.set_template("show_interface_status", True)  
        except TypeError as e0:
            device.show_interfaces_entry_list = []
            device.device_connection_status = f"{device.device_connection_status}; show interfaces status: TypeError {e0}"
            device.textfsm_templates_errors.set_template("show_interface_status", True)  
        except RuntimeError as e1:
            device.show_interfaces_entry_list = []
            device.device_connection_status = f"{device.device_connection_status}; show interfaces status: Parsing Failed: {e1}"
            device.textfsm_templates_errors.set_template("show_interface_status", True)
        except Exception as e2:
            device.device_connection_status = f"{device.device_connection_status}; show interfaces status: Error: {e2}"
            device.textfsm_templates_errors.set_template("show_interface_status", True)
        finally:
            pass       
        
        device.device_connection_status = f"{device.device_connection_status}; Data Retrieval Status End."
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
    sample = CiscoDataRetrieval(filename="region_nodes.json", username="gphillips3", password="02121103!Jun24")
    #print(str(sample))
    file = FileHandler.delete_txt(r"..\app\console_data.txt")
    file = FileHandler.write_txt(r"..\app\console_data.txt", str(sample))
    
    view = PortSecurityView(sample.Data['network_cisco_switches'])
    print(str(view))
        
