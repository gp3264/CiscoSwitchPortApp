from typing import Dict, List, Any
from app.cli_commands_templates import CLIExecutive, CLIExecutive
from app.console_parser import ShowArpParser
from app.mac_address_support import MacAddressSupport
from app.file_support import FileHandler
from pprint import pformat, pprint
from app.SupportUtilities import TaskProgress
from app.data_manager import DataProcessor, DictListProcessor, DataStatisticsReport, DictListStatisticsReport


if __name__ == '__main__':
    
    #Create Dict of Information
    
    data = dict()
    
    region = ""
    router_list = []
    
    interface_list = []
    
    console_output = ""
    
    hostname = ""
    ip_address = ""
    
    
    data['console_output'] = dict()
    
    print("show ip arp")
    
    
  
    
    file_path = r"./region_nodes.json"
    print(f"Getting a list of switches from {file_path}")
    devices_file = FileHandler.read_json(file_path)
    pprint(devices_file)
    
    
    
    # Setting Up Default Connection params
    device: Dict[str, Any] = {
        'device_type': 'cisco_ios',
        'host': '10.95.72.25', # 10.95.72.22',
        'username': 'gphillips3',
        'password': '02121103!Jun24',
        'secret': 'enable_password',
    }


        

    cli = CLIExecutive()
    cli.setup_device(device['username'], device['password'], device['host'], device['secret'], device['device_type'])
    cli.connect()
    
    data = []
    
    for region in devices_file['MDTA_Regions']:
        local_list = []
        for node in region['nodes']:
            local_list.append({"Region":region['region_name'],"Node_Name": node['Node_Name'], "Node": node['IP']})
            
            
        data.extend(local_list)
        
    #pprint(data)
    
    
    
    # processed_data = DictListProcessor(data)
    # processed_data_filtered = processed_data.filter_by_property("Region", "northern")
    # data = DictListProcessor(processed_data_filtered )
    # processed_data_sorted = data.sort_by_property("Node_Name", ascending=True)
    # pprint(processed_data_sorted)
    
    
    
    
    try:
        cli.enter_enable_mode()
        print("\nSHOW IP ARP:")
        show_ip_arp:Dict = cli.show_ip_arp(cli.connection)
        #print(pformat(show_ip_arp))
    
        print("\n\nSHOW IP INTERFACE BRIEF:")
        show_ip_interface_br:Dict = cli.show_ip_interface_brief(cli.connection)
        #print(pformat(show_ip_interface_br))
        
        
        print("\n\nSHOW INTERFACE STATUS:")
        show_interface_status:List = cli.show_interface_status(cli.connection)
        #print(pformat(show_interface_status))
    
    
        print("\n\nSHOW INTERFACES:")
        show_interfaces:List = cli.show_interfaces(cli.connection)
        #print(pformat(show_interfaces))
    
       
        # report_generator = DictListStatisticsReport(show_interfaces)
        # report = report_generator.generate_report("PROTOCOL_STATUS")
        # print(report)
        # report = report_generator.generate_report("LINK_STATUS")
        # print(report)
        # report = report_generator.generate_report("LAST_INPUT")
        # print(report)
        # report = report_generator.generate_report("LAST_OUTPUT+")
        # print(report)
        
        
        print("\n\nSHOW INTERFACES SWITCHPORT:")
        show_interfaces_switchport:List = cli.show_interfaces_switchport(cli.connection)
        print(pformat(show_interfaces))
        
        report_generator = DictListStatisticsReport(show_interfaces_switchport)
        report = report_generator.generate_report("PROTOCOL_STATUS")
        print(report)
        report = report_generator.generate_report("LINK_STATUS")
        print(report)
        report = report_generator.generate_report("LAST_INPUT")
        print(report)
        report = report_generator.generate_report("LAST_OUTPUT")
        print(report)


    
    
    finally:
        cli.disconnect()
    