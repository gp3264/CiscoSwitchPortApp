from typing import List, Dict, Any
from sqlalchemy.exc import SQLAlchemyError
from app.models import db, Device, Interface, VersionInfo

class CLIDatabaseDriver:
    def __init__(self, device_id: int):
        """
        Initialize the CLIDatabaseDriver with a device ID.

        :param device_id: The ID of the device in the database
        """
        self.device_id = device_id

    def insert_ip_interface_brief(self, interfaces: List[Dict[str, Any]]) -> None:
        """
        Insert parsed 'show ip interface brief' data into the database.

        :param interfaces: List of dictionaries containing interface data
        :raises ValueError: If there is an issue inserting data into the database
        """
        try:
            for interface in interfaces:
                intf = Interface(
                    device_id=self.device_id,
                    name=interface['interface'],
                    ip_address=interface['ip_address'],
                    status=interface['status'],
                    protocol=interface['protocol']
                )
                db.session.add(intf)
            db.session.commit()
        except SQLAlchemyError as e:
            db.session.rollback()
            raise ValueError(f"Failed to insert 'show ip interface brief' data: {e}")

    def insert_version_info(self, version_info: Dict[str, Any]) -> None:
        """
        Insert parsed 'show version' data into the database.

        :param version_info: Dictionary containing version information
        :raises ValueError: If there is an issue inserting data into the database
        """
        try:
            ver_info = VersionInfo(
                device_id=self.device_id,
                software=version_info.get('software', ''),
                uptime=version_info.get('uptime', ''),
                system_image=version_info.get('system_image', ''),
                processor_board_id=version_info.get('processor_board_id', '')
            )
            db.session.add(ver_info)
            db.session.commit()
        except SQLAlchemyError as e:
            db.session.rollback()
            raise ValueError(f"Failed to insert 'show version' data: {e}")

    def insert_running_config(self, running_config: str) -> None:
        """
        Insert parsed 'show running-config' data into the database.

        :param running_config: The running configuration as a string
        :raises ValueError: If there is an issue inserting data into the database
        """
        # This example assumes running config is stored as a text file in the database
        try:
            # Implementation for storing running config goes here
            pass
        except SQLAlchemyError as e:
            db.session.rollback()
            raise ValueError(f"Failed to insert 'show running-config' data: {e}")

    def insert_interfaces(self, interfaces: List[Dict[str, Any]]) -> None:
        """
        Insert parsed 'show interfaces' data into the database.

        :param interfaces: List of dictionaries containing interface data
        :raises ValueError: If there is an issue inserting data into the database
        """
        try:
            for interface in interfaces:
                intf = Interface(
                    device_id=self.device_id,
                    name=interface.get('interface', ''),
                    status=interface.get('status', ''),
                    protocol=interface.get('protocol', '')
                )
                db.session.add(intf)
            db.session.commit()
        except SQLAlchemyError as e:
            db.session.rollback()
            raise ValueError(f"Failed to insert 'show interfaces' data: {e}")

    def insert_ip_route(self, routes: List[Dict[str, str]]) -> None:
        """
        Insert parsed 'show ip route' data into the database.

        :param routes: List of dictionaries containing route data
        :raises ValueError: If there is an issue inserting data into the database
        """
        try:
            # Implementation for storing IP route data goes here
            pass
        except SQLAlchemyError as e:
            db.session.rollback()
            raise ValueError(f"Failed to insert 'show ip route' data: {e}")

    def insert_arp(self, arps: List[Dict[str, str]]) -> None:
        """
        Insert parsed 'show arp' data into the database.

        :param arps: List of dictionaries containing ARP table entries
        :raises ValueError: If there is an issue inserting data into the database
        """
        try:
            # Implementation for storing ARP data goes here
            pass
        except SQLAlchemyError as e:
            db.session.rollback()
            raise ValueError(f"Failed to insert 'show arp' data: {e}")

    def insert_mac_address_table(self, mac_table: List[Dict[str, str]]) -> None:
        """
        Insert parsed 'show mac address-table' data into the database.

        :param mac_table: List of dictionaries containing MAC address table entries
        :raises ValueError: If there is an issue inserting data into the database
        """
        try:
            # Implementation for storing MAC address table data goes here
            pass
        except SQLAlchemyError as e:
            db.session.rollback()
            raise ValueError(f"Failed to insert 'show mac address-table' data: {e}")

    def insert_vlan_brief(self, vlans: List[Dict[str, str]]) -> None:
        """
        Insert parsed 'show vlan brief' data into the database.

        :param vlans: List of dictionaries containing VLAN details
        :raises ValueError: If there is an issue inserting data into the database
        """
        try:
            # Implementation for storing VLAN data goes here
            pass
        except SQLAlchemyError as e:
            db.session.rollback()
            raise ValueError(f"Failed to insert 'show vlan brief' data: {e}")

    def insert_logging(self, logs: List[str]) -> None:
        """
        Insert parsed 'show logging' data into the database.

        :param logs: List of log entries
        :raises ValueError: If there is an issue inserting data into the database
        """
        try:
            # Implementation for storing log data goes here
            pass
        except SQLAlchemyError as e:
            db.session.rollback()
            raise ValueError(f"Failed to insert 'show logging' data: {e}")

    def insert_ospf_neighbors(self, neighbors: List[Dict[str, str]]) -> None:
        """
        Insert parsed 'show ip ospf neighbor' data into the database.

        :param neighbors: List of dictionaries containing OSPF neighbor details
        :raises ValueError: If there is an issue inserting data into the database
        """
        try:
            # Implementation for storing OSPF neighbor data goes here
            pass
        except SQLAlchemyError as e:
            db.session.rollback()
            raise ValueError(f"Failed to insert 'show ip ospf neighbor' data: {e}")

# Example usage:
if __name__ == "__main__":
    from console_parser import (
        ShowIpInterfaceBriefParser, ShowVersionParser,
        # Add other necessary parsers here
    )

    # Example parsed data (replace with actual parsed output from parser classes)
    ip_int_brief_data = ShowIpInterfaceBriefParser.parse("parsed 'show ip interface brief' output here")
    version_info_data = ShowVersionParser.parse("parsed 'show version' output here")

    # Example device ID
    device_id = 1

    db_driver = CLIDatabaseDriver(device_id)
    db_driver.insert_ip_interface_brief(ip_int_brief_data)
    db_driver.insert_version_info(version_info_data)
