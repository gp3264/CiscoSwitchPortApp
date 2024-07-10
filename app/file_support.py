import csv
import json
import xml.etree.ElementTree as ET
from typing import Any, List, Dict
import os


class FileHandler:
    def __init__(self):
        pass

    # CSV Methods
    @staticmethod
    def read_csv(file_path: str) -> List[Dict[str, Any]]:
        """
        Reads a CSV file and returns a list of dictionaries.

        :param file_path: Path to the CSV file.
        :return: List of dictionaries representing the CSV data.
        :raises FileNotFoundError: If the file does not exist.
        """
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"The file {file_path} does not exist.")
        with open(file_path, mode='r', newline='') as file:
            reader = csv.DictReader(file)
            return [row for row in reader]

    @staticmethod
    def write_csv(file_path: str, data: List[Dict[str, Any]]) -> None:
        """
        Writes a list of dictionaries to a CSV file.

        :param file_path: Path to the CSV file.
        :param data: List of dictionaries representing the CSV data.
        :raises ValueError: If the data is empty.
        """
        if not data:
            raise ValueError("Data is empty.")
        with open(file_path, mode='w', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=data[0].keys())
            writer.writeheader()
            writer.writerows(data)

    @staticmethod
    def update_csv(file_path: str, data: List[Dict[str, Any]]) -> None:
        """
        Updates a CSV file with new data.

        :param file_path: Path to the CSV file.
        :param data: List of dictionaries representing the CSV data.
        :raises ValueError: If the data is empty.
        """
        FileHandler.write_csv(file_path, data)

    @staticmethod
    def delete_csv(file_path: str) -> None:
        """
        Deletes the contents of a CSV file.

        :param file_path: Path to the CSV file.
        """
        open(file_path, 'w').close()

    # JSON Methods
    @staticmethod
    def read_json(file_path: str) -> Any:
        """
        Reads a JSON file and returns the data.

        :param file_path: Path to the JSON file.
        :return: Data read from the JSON file.
        :raises FileNotFoundError: If the file does not exist.
        """
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"The file {file_path} does not exist.")
        with open(file_path, mode='r') as file:
            return json.load(file)

    @staticmethod
    def write_json(file_path: str, data: Any) -> None:
        """
        Writes data to a JSON file.

        :param file_path: Path to the JSON file.
        :param data: Data to write to the JSON file.
        """
        with open(file_path, mode='w') as file:
            json.dump(data, file, indent=4)

    @staticmethod
    def update_json(file_path: str, data: Any) -> None:
        """
        Updates a JSON file with new data.

        :param file_path: Path to the JSON file.
        :param data: Data to write to the JSON file.
        """
        FileHandler.write_json(file_path, data)

    @staticmethod
    def delete_json(file_path: str) -> None:
        """
        Deletes the contents of a JSON file.

        :param file_path: Path to the JSON file.
        """
        open(file_path, 'w').close()

    # XML Methods
    @staticmethod
    def read_xml(file_path: str) -> ET.Element:
        """
        Reads an XML file and returns the root element.

        :param file_path: Path to the XML file.
        :return: Root element of the XML file.
        :raises FileNotFoundError: If the file does not exist.
        """
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"The file {file_path} does not exist.")
        tree = ET.parse(file_path)
        return tree.getroot()

    @staticmethod
    def write_xml(file_path: str, data: ET.Element) -> None:
        """
        Writes an XML element to a file.

        :param file_path: Path to the XML file.
        :param data: XML element to write to the file.
        """
        tree = ET.ElementTree(data)
        tree.write(file_path)

    @staticmethod
    def update_xml(file_path: str, data: ET.Element) -> None:
        """
        Updates an XML file with a new XML element.

        :param file_path: Path to the XML file.
        :param data: XML element to write to the file.
        """
        FileHandler.write_xml(file_path, data)

    @staticmethod
    def delete_xml(file_path: str) -> None:
        """
        Deletes the contents of an XML file.

        :param file_path: Path to the XML file.
        """
        open(file_path, 'w').close()

    # TXT Methods
    @staticmethod
    def read_txt(file_path: str) -> str:
        """
        Reads a TXT file and returns the contents as a string.

        :param file_path: Path to the TXT file.
        :return: Contents of the TXT file.
        :raises FileNotFoundError: If the file does not exist.
        """
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"The file {file_path} does not exist.")
        with open(file_path, mode='r') as file:
            return file.read()

    @staticmethod
    def write_txt(file_path: str, data: str) -> None:
        """
        Writes a string to a TXT file.

        :param file_path: Path to the TXT file.
        :param data: String to write to the TXT file.
        """
        with open(file_path, mode='w') as file:
            file.write(data)

    @staticmethod
    def update_txt(file_path: str, data: str) -> None:
        """
        Updates a TXT file with new contents.

        :param file_path: Path to the TXT file.
        :param data: String to write to the TXT file.
        """
        FileHandler.write_txt(file_path, data)

    @staticmethod
    def delete_txt(file_path: str) -> None:
        """
        Deletes the contents of a TXT file.

        :param file_path: Path to the TXT file.
        """
        open(file_path, 'w').close()


class FileConverter:
    @staticmethod
    def csv_to_json(csv_path: str, json_path: str) -> None:
        """
        Converts a CSV file to a JSON file.

        :param csv_path: Path to the CSV file.
        :param json_path: Path to the JSON file.
        """
        data = FileHandler.read_csv(csv_path)
        FileHandler.write_json(json_path, data)

    @staticmethod
    def json_to_csv(json_path: str, csv_path: str) -> None:
        """
        Converts a JSON file to a CSV file.

        :param json_path: Path to the JSON file.
        :param csv_path: Path to the CSV file.
        """
        data = FileHandler.read_json(json_path)
        FileHandler.write_csv(csv_path, data)

    @staticmethod
    def csv_to_xml(csv_path: str, xml_path: str) -> None:
        """
        Converts a CSV file to an XML file.

        :param csv_path: Path to the CSV file.
        :param xml_path: Path to the XML file.
        """
        data = FileHandler.read_csv(csv_path)
        root = ET.Element('root')
        for row in data:
            item = ET.Element('item')
            for key, value in row.items():
                child = ET.Element(key)
                child.text = value
                item.append(child)
            root.append(item)
        FileHandler.write_xml(xml_path, root)

    @staticmethod
    def xml_to_csv(xml_path: str, csv_path: str) -> None:
        """
        Converts an XML file to a CSV file.

        :param xml_path: Path to the XML file.
        :param csv_path: Path to the CSV file.
        """
        root = FileHandler.read_xml(xml_path)
        data = []
        for item in root.findall('item'):
            row = {child.tag: child.text for child in item}
            data.append(row)
        FileHandler.write_csv(csv_path, data)

    @staticmethod
    def json_to_xml(json_path: str, xml_path: str) -> None:
        """
        Converts a JSON file to an XML file.

        :param json_path: Path to the JSON file.
        :param xml_path: Path to the XML file.
        """
        data = FileHandler.read_json(json_path)
        root = ET.Element('root')
        for item in data:
            element = ET.Element('item')
            for key, value in item.items():
                child = ET.Element(key)
                child.text = str(value)
                element.append(child)
            root.append(element)
        FileHandler.write_xml(xml_path, root)

    @staticmethod
    def xml_to_json(xml_path: str, json_path: str) -> None:
        """
        Converts an XML file to a JSON file.

        :param xml_path: Path to the XML file.
        :param json_path: Path to the JSON file.
        """
        root = FileHandler.read_xml(xml_path)
        data = []
        for item in root.findall('item'):
            row = {child.tag: child.text for child in item}
            data.append(row)
        FileHandler.write_json(json_path, data)

    @staticmethod
    def txt_to_json(txt_path: str, json_path: str) -> None:
        """
        Converts a TXT file to a JSON file.

        :param txt_path: Path to the TXT file.
        :param json_path: Path to the JSON file.
        """
        data = FileHandler.read_txt(txt_path)
        FileHandler.write_json(json_path, data)

    @staticmethod
    def json_to_txt(json_path: str, txt_path: str) -> None:
        """
        Converts a JSON file to a TXT file.

        :param json_path: Path to the JSON file.
        :param txt_path: Path to the TXT file.
        """
        data = FileHandler.read_json(json_path)
        FileHandler.write_txt(txt_path, json.dumps(data, indent=4))

    @staticmethod
    def txt_to_csv(txt_path: str, csv_path: str) -> None:
        """
        Converts a TXT file to a CSV file.

        :param txt_path: Path to the TXT file.
        :param csv_path: Path to the CSV file.
        """
        data = FileHandler.read_txt(txt_path)
        rows = data.splitlines()
        csv_data = [row.split(',') for row in rows]
        FileHandler.write_csv(csv_path, csv_data)

    @staticmethod
    def csv_to_txt(csv_path: str, txt_path: str) -> None:
        """
        Converts a CSV file to a TXT file.

        :param csv_path: Path to the CSV file.
        :param txt_path: Path to the TXT file.
        """
        data = FileHandler.read_csv(csv_path)
        txt_data = '\n'.join([','.join(map(str, row.values())) for row in data])
        FileHandler.write_txt(txt_path, txt_data)

    @staticmethod
    def txt_to_xml(txt_path: str, xml_path: str) -> None:
        """
        Converts a TXT file to an XML file.

        :param txt_path: Path to the TXT file.
        :param xml_path: Path to the XML file.
        """
        data = FileHandler.read_txt(txt_path)
        root = ET.Element('root')
        for line in data.splitlines():
            item = ET.Element('item')
            for i, value in enumerate(line.split(',')):
                child = ET.Element(f'field{i}')
                child.text = value
                item.append(child)
            root.append(item)
        FileHandler.write_xml(xml_path, root)

    @staticmethod
    def xml_to_txt(xml_path: str, txt_path: str) -> None:
        """
        Converts an XML file to a TXT file.

        :param xml_path: Path to the XML file.
        :param txt_path: Path to the TXT file.
        """
        root = FileHandler.read_xml(xml_path)
        txt_data = '\n'.join([','.join([child.text for child in item]) for item in root.findall('item')])
        FileHandler.write_txt(txt_path, txt_data)
