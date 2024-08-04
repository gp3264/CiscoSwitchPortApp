from app.application_dataclasses import *
from app.application_dataclasses_support import *
from app.application_dataclass_views import PortSecurityViewEntry
from app.mac_address_support import MacAddressSupport
from app.SupportUtilities import TaskProgressIndicator
from app.console_parser import TimeParser
from pprint import pformat


class ViewBase:
    def __init__(self):
        pass

class PortSecurityView(ViewBase):
    def __init__(self, device_list:List[NetworkDeviceEntry]):
        self.mac_address_support: MacAddressSupport = MacAddressSupport()
        self._devices:List[NetworkDeviceEntry] = device_list
        self._records: List[PortSecurityViewEntry] = []
        self._task_progress:TaskProgressIndicator = TaskProgressIndicator("Building Port Security View",self.get_task_counts())
        print("\n")
        self._task_progress.start()
        self.build_records()
        
    def get_task_counts(self):
        total_task_count:int = 0
        for device in self._devices:
            total_task_count += len(device.show_interfaces_entry_list)
        return total_task_count
        
    def build_records(self):
        records:list[PortSecurityViewEntry] = []
        for device in self._devices:
            
            switch_hostname:str = device.switch_hostname
            switch_ip_address:str = device.switch_ip_address
            switch_region:str = device.switch_region
            show_interfaces_entry_list:List[ShowInterfacesEntry] = device.show_interfaces_entry_list
            
            for entry in show_interfaces_entry_list:
                
                self._task_progress.update_task_name(f"Building Port Security View")
                records.append(self.create_entry_record(switch_hostname, switch_ip_address, switch_region, entry))
                
                self._task_progress.update_progress()
        
        self._records = records
        self._task_progress.complete()
    
    def create_entry_record(self, switch_hostname:str = None, 
                             switch_ip_address:str = None, 
                             switch_region:str = None,
                             show_interfaces_entry:ShowInterfacesEntry = None) -> PortSecurityViewEntry:
        
        entry:PortSecurityViewEntry = PortSecurityViewEntry(show_interfaces_entry)
        entry.switch_hostname = switch_hostname
        entry.switch_ip_address = switch_ip_address
        entry.switch_region = switch_region
        entry.converted_last_input = TimeParser(show_interfaces_entry.LAST_INPUT).
        entry.converted_last_output = TimeParser(show_interfaces_entry.LAST_OUTPUT).time_string  
        entry.mac_vendor = self.mac_address_support.get_vendor(show_interfaces_entry.MAC_ADDRESS)  
        entry.update_attributes(show_interfaces_entry.to_dict())     
        return entry
    
    
    def __str__(self):
        return pformat(self._records)
        
        
        