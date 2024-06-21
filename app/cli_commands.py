from typing import Any, Dict
from app.cli_connection import CLIConnection

class CLICommands:
    @staticmethod
    def show_ip_interface_brief(connection: CLIConnection) -> str:
        """
        Run 'show ip interface brief' command and return the output.

        :param connection: CLIConnection instance
        :return: Output of the command
        :raises RuntimeError: If the command execution fails
        """
        try:
            return connection.run_command('show ip interface brief')
        except Exception as e:
            raise RuntimeError("Failed to run 'show ip interface brief'") from e

    @staticmethod
    def show_version(connection: CLIConnection) -> str:
        """
        Run 'show version' command and return the output.

        :param connection: CLIConnection instance
        :return: Output of the command
        :raises RuntimeError: If the command execution fails
        """
        try:
            return connection.run_command('show version')
        except Exception as e:
            raise RuntimeError("Failed to run 'show version'") from e

    @staticmethod
    def show_running_config(connection: CLIConnection) -> str:
        """
        Run 'show running-config' command and return the output.

        :param connection: CLIConnection instance
        :return: Output of the command
        :raises RuntimeError: If the command execution fails
        """
        try:
            return connection.run_command('show running-config')
        except Exception as e:
            raise RuntimeError("Failed to run 'show running-config'") from e

    @staticmethod
    def show_interfaces(connection: CLIConnection) -> str:
        """
        Run 'show interfaces' command and return the output.

        :param connection: CLIConnection instance
        :return: Output of the command
        :raises RuntimeError: If the command execution fails
        """
        try:
            return connection.run_command('show interfaces')
        except Exception as e:
            raise RuntimeError("Failed to run 'show interfaces'") from e

    @staticmethod
    def show_ip_route(connection: CLIConnection) -> str:
        """
        Run 'show ip route' command and return the output.

        :param connection: CLIConnection instance
        :return: Output of the command
        :raises RuntimeError: If the command execution fails
        """
        try:
            return connection.run_command('show ip route')
        except Exception as e:
            raise RuntimeError("Failed to run 'show ip route'") from e

    @staticmethod
    def show_arp(connection: CLIConnection) -> str:
        """
        Run 'show arp' command and return the output.

        :param connection: CLIConnection instance
        :return: Output of the command
        :raises RuntimeError: If the command execution fails
        """
        try:
            return connection.run_command('show arp')
        except Exception as e:
            raise RuntimeError("Failed to run 'show arp'") from e

    @staticmethod
    def show_mac_address_table(connection: CLIConnection) -> str:
        """
        Run 'show mac address-table' command and return the output.

        :param connection: CLIConnection instance
        :return: Output of the command
        :raises RuntimeError: If the command execution fails
        """
        try:
            return connection.run_command('show mac address-table')
        except Exception as e:
            raise RuntimeError("Failed to run 'show mac address-table'") from e

    @staticmethod
    def show_vlan_brief(connection: CLIConnection) -> str:
        """
        Run 'show vlan brief' command and return the output.

        :param connection: CLIConnection instance
        :return: Output of the command
        :raises RuntimeError: If the command execution fails
        """
        try:
            return connection.run_command('show vlan brief')
        except Exception as e:
            raise RuntimeError("Failed to run 'show vlan brief'") from e

    @staticmethod
    def show_logging(connection: CLIConnection) -> str:
        """
        Run 'show logging' command and return the output.

        :param connection: CLIConnection instance
        :return: Output of the command
        :raises RuntimeError: If the command execution fails
        """
        try:
            return connection.run_command('show logging')
        except Exception as e:
            raise RuntimeError("Failed to run 'show logging'") from e

    @staticmethod
    def show_ip_ospf_neighbor(connection: CLIConnection) -> str:
        """
        Run 'show ip ospf neighbor' command and return the output.

        :param connection: CLIConnection instance
        :return: Output of the command
        :raises RuntimeError: If the command execution fails
        """
        try:
            return connection.run_command('show ip ospf neighbor')
        except Exception as e:
            raise RuntimeError("Failed to run 'show ip ospf neighbor'") from e

    @staticmethod
    def show_interface(connection: CLIConnection, interface: str) -> str:
        """
        Run 'show interface <interface>' command and return the output.

        :param connection: CLIConnection instance
        :param interface: Name of the interface to show
        :return: Output of the command
        :raises RuntimeError: If the command execution fails
        """
        try:
            return connection.run_command(f'show interface {interface}')
        except Exception as e:
            raise RuntimeError(f"Failed to run 'show interface {interface}'") from e

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

# Example usage:
if __name__ == "__main__":
    from app.cli_connection import CLIConnection

    device: Dict[str, Any] = {
        'device_type': 'cisco_ios',
        'host': '192.168.1.1',
        'username': 'admin',
        'password': 'password',
        'secret': 'enable_password',
    }

    connection = CLIConnection(**device)
    try:
        connection.enter_enable_mode()
        print("Show IP Interface Brief:")
        print(CLICommands.show_ip_interface_brief(connection))

        print("\nShow Version:")
        print(CLICommands.show_version(connection))

        print("\nShow Running Config:")
        print(CLICommands.show_running_config(connection))

        print("\nShow Interfaces:")
        print(CLICommands.show_interfaces(connection))

        print("\nShow IP Route:")
        print(CLICommands.show_ip_route(connection))

        print("\nShow ARP:")
        print(CLICommands.show_arp(connection))

        print("\nShow MAC Address Table:")
        print(CLICommands.show_mac_address_table(connection))

        print("\nShow VLAN Brief:")
        print(CLICommands.show_vlan_brief(connection))

        print("\nShow Logging:")
        print(CLICommands.show_logging(connection))

        print("\nShow IP OSPF Neighbor:")
        print(CLICommands.show_ip_ospf_neighbor(connection))

        interface = 'GigabitEthernet0/1'
        print(f"\nShow Interface {interface}:")
        print(CLICommands.show_interface(connection, interface))

        print(f"\nEntering config mode to shutdown Interface {interface}:")
        CLICommands.enter_config_mode(connection)
        print(CLICommands.shutdown_interface(connection, interface))
        CLICommands.exit_config_mode(connection)

        print(f"\nEntering config mode to bring up Interface {interface}:")
        CLICommands.enter_config_mode(connection)
        print(CLICommands.no_shutdown_interface(connection, interface))
        CLICommands.exit_config_mode(connection)
    finally:
        connection.disconnect()
