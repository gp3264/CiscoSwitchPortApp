from netmiko import ConnectHandler
import logging
from typing import Any, Optional, Dict
from netmiko.base_connection import BaseConnection

DEVICE_TYPE = 'cisco_ios'

class CLIConnection:
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        """
        Initializes the CLIConnection instance.

        :param device_type: Type of the device (e.g., 'cisco_ios')
        :param host: Hostname or IP address of the device
        :param username: Username for SSH login
        :param password: Password for SSH login
        :param secret: Enable secret for privileged EXEC mode (optional)
        :param kwargs: Additional keyword arguments for ConnectHandler
        #"""
        #device: Dict[str, Any] = [*args, **kwargs]
        #'device_type': 'cisco_ios',
        #'host': '192.168.1.1',
        #'username': 'admin',
        #'password': 'password',
        #'secret': 'enable_password',
        #}
        
        self.connection:BaseConnection = ConnectHandler(*args, **kwargs)
        self.host = self.connection.host
        self.logger = logging.getLogger(__name__)
        #self.logger.setLevel(logging.INFO)
        self.logger.setLevel(logging.INFO)
        handler = logging.StreamHandler()
        fh = logging.FileHandler(r'..\app\cli_connection.log')
        fmt = '%(asctime)s - %(levelname)s - %(message)s'
        fh.setFormatter(logging.Formatter(fmt))
        handler.setFormatter(logging.Formatter(fmt))
        #self.logger.addHandler(handler)
        self.logger.addHandler(fh)
        self.logger.info(f"Initialized CLIConnection for {self.host}")

    def run_command(self, command: str) -> str:
        """
        Runs a command on the CLI and returns the output.

        :param command: The command to run on the CLI
        :return: The output from the command
        :raises RuntimeError: If the command execution fails
        """
        self.logger.info(f"Running command: {command}")
        try:
            output = self.connection.send_command(command)
            self.logger.info(f"Command output: {output}")
            return output
        except Exception as e:
            self.logger.error(f"Failed to run command: {e}")
            raise RuntimeError(f"Failed to run command: {command}") from e

    def enter_enable_mode(self) -> None:
        """
        Enters enable mode if the device supports it.

        :raises RuntimeError: If entering enable mode fails
        """
        self.logger.info("Entering enable mode")
        try:
            self.connection.enable()
            self.logger.info("Entered enable mode")
        except Exception as e:
            self.logger.error(f"Failed to enter enable mode: {e}")
            raise RuntimeError("Failed to enter enable mode") from e

    def disconnect(self) -> None:
        """
        Disconnects from the device.

        :raises RuntimeError: If disconnection fails
        """
        self.logger.info(f"Disconnecting from {self.host}")
        try:
            self.connection.disconnect()
            self.logger.info("Disconnected successfully")
        except Exception as e:
            self.logger.error(f"Failed to disconnect: {e}")
            raise RuntimeError("Failed to disconnect") from e

# Example usage:
if __name__ == "__main__":
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
        output = connection.run_command('show ip interface brief')
        print(output)
    finally:
        connection.disconnect()
