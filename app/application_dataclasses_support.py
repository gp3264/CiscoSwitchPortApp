from dataclasses import dataclass, fields, field, asdict, is_dataclass
from typing import List, Dict, Any, TypeVar, Generic, Iterator, get_type_hints, Type
from operator import attrgetter
import re

T = TypeVar('T')


@dataclass
class Person:
    """
    An example of a dataclass
    """
    name: str
    age: int
    email: str
    

@dataclass
class InfoErrorFlags:
    """
    A dataclass to represent a binary word where each bit corresponds to a specific TextFSM template or error code.
    """
    class_version:float = 1.0
    name:str = None
    description:str = None
    # Assign a bit position to each template
    show_version: int = field(default=0, metadata={"bit": 0})
    show_interface: int = field(default=0, metadata={"bit": 1})
    show_ip_route: int = field(default=0, metadata={"bit": 2})
    show_mac_address_table: int = field(default=0, metadata={"bit": 3})
    show_ip_arp: int = field(default=0, metadata={"bit": 4})
    show_vlan: int = field(default=0, metadata={"bit": 5})
    show_cdp_neighbors: int = field(default=0, metadata={"bit": 6})
    show_ip_interface_brief: int = field(default=0, metadata={"bit": 7})
    show_inventory: int = field(default=0, metadata={"bit": 8})
    show_logging: int = field(default=0, metadata={"bit": 9})
    show_interface_status: int = field(default=0, metadata={"bit": 10})
    
    def to_binary_string(self) -> str:
        """
        Returns the binary representation of the flags as a 32-bit string.
        """
        bits = [self.show_version, self.show_interface, self.show_ip_route,
                self.show_mac_address_table, self.show_ip_arp, self.show_vlan,
                self.show_cdp_neighbors, self.show_ip_interface_brief,
                self.show_inventory, self.show_logging, self.show_interface_status]

        # Create the 32-bit binary string with leading zeros
        return ''.join(map(str, bits)).zfill(32)

    def to_integer(self) -> int:
        """
        Returns the binary word as an integer.
        """
        return int(self.to_binary_string(), 2)

    def set_template(self, template_name: str, value: bool) -> None:
        """
        Sets the bit corresponding to a specific template.
        
        Args:
            template_name (str): The name of the template to set.
            value (bool): True to set the bit, False to clear it.
        """
        if hasattr(self, template_name):
            setattr(self, template_name, int(value))
        else:
            raise ValueError(f"Template {template_name} does not exist.")

    def clear_all(self) -> None:
        """
        Resets all bits to 0.
        """
        for field_name in self.__dataclass_fields__:
            setattr(self, field_name, 0)
            
    def __str__(self):
        return self.to_binary_string()





class DataclassConverter(Generic[T]):
    """
    A class to convert dataclass instances to dictionaries.
    """

    @staticmethod
    def to_dict(instance: T) -> dict:
        """
        Converts a dataclass instance to a dictionary.

        Args:
            instance (T): The dataclass instance to convert.

        Returns:
            dict: A dictionary representation of the dataclass instance.

        Raises:
            TypeError: If the instance is not a dataclass.
        """
        if not hasattr(instance, '__dataclass_fields__'):
            raise TypeError("Provided instance is not a dataclass.")
        
        return asdict(instance)
    

class DataclassPropertyAdder(Generic[T]):
    """
    A class to dynamically add properties to a dataclass instance.
    """

    def __init__(self, instance: T):
        """
        Initializes the DataclassPropertyAdder with a dataclass instance.

        Args:
            instance (T): The dataclass instance.
        """
        self.instance = instance

    def add_property(self, prop_name: str, value: Any) -> None:
        """
        Dynamically adds a property to the dataclass instance.

        Args:
            prop_name (str): The name of the property to add.
            value (Any): The value of the property to add.

        Raises:
            AttributeError: If the attribute already exists.
        """
        if hasattr(self.instance, prop_name):
            raise AttributeError(f"The attribute '{prop_name}' already exists.")
        setattr(self.instance, prop_name, value)

    def to_dict(self) -> dict:
        """
        Converts the dataclass instance to a dictionary, including dynamically added properties.

        Returns:
            dict: A dictionary representation of the dataclass instance.
        """
        base_fields = {field.name for field in fields(self.instance)}
        dynamic_fields = {key: value for key, value in self.instance.__dict__.items() if key not in base_fields}
        return {field: getattr(self.instance, field) for field in base_fields} | dynamic_fields


class DataclassSorter:
    """
    A class to sort a list of dataclass instances based on multiple properties.
    """

    def __init__(self, items: List[Any]):
        """
        Initializes the DataclassSorter with a list of items.

        Args:
            items (List[Any]): The list of dataclass instances to sort.
        """
        self.items = items

    def sort_by_properties(self, *properties: str) -> List[Any]:
        """
        Sorts the list of items based on the given properties.

        Args:
            properties (str): The properties to sort by, in order of priority.

        Returns:
            List[Any]: The sorted list of items.
        """
        if not properties:
            raise ValueError("At least one property must be specified to sort by.")
        
        for prop in properties:
            if not all(hasattr(item, prop) for item in self.items):
                raise AttributeError(f"One or more items do not have the attribute '{prop}'.")

        return sorted(self.items, key=attrgetter(*properties))


class DataclassFilter:
    """
    A class to filter a list of dataclass instances based on properties or regex.
    """

    def __init__(self, items: List[Any]):
        """
        Initializes the DataclassFilter with a list of items.

        Args:
            items (List[Any]): The list of dataclass instances to filter.
        """
        self.items = items

    def filter_by_properties(self, criteria: Dict[str, Any]) -> List[Any]:
        """
        Filters the list of items based on the given property criteria.

        Args:
            criteria (Dict[str, Any]): A dictionary where keys are attribute names and values are the values to filter by.

        Returns:
            List[Any]: The filtered list of items.
        """
        filtered_items = self.items
        for key, value in criteria.items():
            if not all(hasattr(item, key) for item in self.items):
                raise AttributeError(f"One or more items do not have the attribute '{key}'.")
            filtered_items = [item for item in filtered_items if getattr(item, key) == value]
        return filtered_items

    def filter_by_regex(self, regex_criteria: Dict[str, str]) -> List[Any]:
        """
        Filters the list of items based on the given regex criteria.

        Args:
            regex_criteria (Dict[str, str]): A dictionary where keys are attribute names and values are regex patterns to filter by.

        Returns:
            List[Any]: The filtered list of items.
        """
        filtered_items = self.items
        for key, pattern in regex_criteria.items():
            if not all(hasattr(item, key) for item in self.items):
                raise AttributeError(f"One or more items do not have the attribute '{key}'.")
            regex = re.compile(pattern)
            filtered_items = [item for item in filtered_items if regex.match(str(getattr(item, key)))]
        return filtered_items
    
    
class DataclassInspector:
    """
    A class to retrieve properties from dataclass instances, supporting nested dataclasses up to a specified depth.
    """

    @staticmethod
    def get_properties(instance: Any, depth: int=10, current_level: int=0) -> Dict[str, Any]:
        """
        Retrieves the properties of a dataclass instance, including nested dataclasses up to a specified depth.

        Args:
            instance (Any): The dataclass instance.
            depth (int): The maximum depth to retrieve nested properties. Defaults to 10.
            current_level (int): The current level of recursion. Used internally.

        Returns:
            Dict[str, Any]: A dictionary of the dataclass properties.
        """
        if not is_dataclass(instance):
            raise TypeError("Provided instance is not a dataclass.")
        
        if current_level > depth:
            return {"error": "Maximum depth reached"}

        result = {}
        for field in fields(instance):
            value = getattr(instance, field.name)
            if is_dataclass(value):
                result[field.name] = DataclassInspector.get_properties(value, depth, current_level + 1)
            elif isinstance(value, list) and len(value) > 0 and is_dataclass(value[0]):
                result[field.name] = [DataclassInspector.get_properties(item, depth, current_level + 1) for item in value]
            else:
                result[field.name] = value

        return result    





class DataclassListIterator:
    """
    A class to iterate over a list of dataclass instances.
    """

    def __init__(self, dataclass_list: List[Any]):
        """
        Initializes the iterator with a list of dataclass instances.

        Args:
            dataclass_list (List[Any]): The list of dataclass instances to iterate over.
        """
        self._dataclass_list = dataclass_list
        self._index = 0

    def __iter__(self) -> Iterator[Any]:
        """
        Returns the iterator object itself.

        Returns:
            Iterator[Any]: The iterator object.
        """
        return self

    def __next__(self) -> Any:
        """
        Returns the next dataclass instance in the list.

        Returns:
            Any: The next dataclass instance.

        Raises:
            StopIteration: When the end of the list is reached.
        """
        if self._index < len(self._dataclass_list):
            result = self._dataclass_list[self._index]
            self._index += 1
            return result
        else:
            raise StopIteration


class DataclassTypeIdentifier:
    """
    A class to identify the data types of attributes in a dataclass.
    """
    @staticmethod
    def get_attribute_types(dataclass_instance: Any) -> Dict[str, Type]:
        """
        Retrieves the types of attributes of a dataclass instance.

        Args:
            dataclass_instance (Any): The dataclass instance.

        Returns:
            Dict[str, Type]: A dictionary where keys are attribute names and values are their types.
        """
        if not hasattr(dataclass_instance, '__dataclass_fields__'):
            raise TypeError("Provided instance is not a dataclass.")
        
        type_hints = get_type_hints(dataclass_instance.__class__)
        attribute_types = {field.name: type_hints[field.name] for field in fields(dataclass_instance)}
        
        return attribute_types

class ListFilter(Generic[T]):
    """
    A class to filter a list of objects based on a dictionary of criteria.

    Attributes:
        items (List[T]): The list of items to filter.
    """

    def __init__(self, items: List[T]):
        """
        Initializes the ListFilter with a list of items.

        Args:
            items (List[T]): The list of items to filter.
        """
        self.items = items

    def filter(self, criteria: Dict[str, Any]) -> List[T]:
        """
        Filters the list of items based on the given criteria.

        Args:
            criteria (Dict[str, Any]): A dictionary where keys are attribute names and values are the values to filter by.

        Returns:
            List[T]: The filtered list of items.

        Raises:
            AttributeError: If an attribute in the criteria does not exist in the items.
        """
        filtered_items = self.items
        for key, value in criteria.items():
            try:
                filtered_items = [item for item in filtered_items if getattr(item, key) == value]
            except AttributeError as e:
                raise AttributeError(f"Attribute '{key}' does not exist in the items.") from e
        return filtered_items


class TypeIdentifier:
    """
    A class to identify the data types of attributes in any Python object, including dataclasses.
    """
    @staticmethod
    def get_attribute_types(obj: Any) -> Dict[str, Type]:
        """
        Retrieves the types of attributes of a Python object.

        Args:
            obj (Any): The Python object.

        Returns:
            Dict[str, Type]: A dictionary where keys are attribute names and values are their types.
        """
        if is_dataclass(obj):
            return TypeIdentifier._get_dataclass_attribute_types(obj)
        else:
            return TypeIdentifier._get_general_attribute_types(obj)
    
    @staticmethod
    def _get_dataclass_attribute_types(dataclass_instance: Any) -> Dict[str, Type]:
        """
        Retrieves the types of attributes of a dataclass instance.

        Args:
            dataclass_instance (Any): The dataclass instance.

        Returns:
            Dict[str, Type]: A dictionary where keys are attribute names and values are their types.
        """
        type_hints = get_type_hints(dataclass_instance.__class__)
        attribute_types = {field.name: type_hints[field.name] for field in fields(dataclass_instance)}
        return attribute_types

    @staticmethod
    def _get_general_attribute_types(obj: Any) -> Dict[str, Type]:
        """
        Retrieves the types of attributes of a general Python object.

        Args:
            obj (Any): The Python object.

        Returns:
            Dict[str, Type]: A dictionary where keys are attribute names and values are their types.
        """
        return {attr: type(getattr(obj, attr)) for attr in dir(obj) if not callable(getattr(obj, attr)) and not attr.startswith("__")}






####################################################
# USAGE EXAMPLES 
####################################################


# Example usage
# interface_data_list = [
#     InterfaceData(LINK_STATUS="up", PROTOCOL_STATUS="up", HARDWARE_TYPE="Ethernet"),
#     InterfaceData(LINK_STATUS="down", PROTOCOL_STATUS="down", HARDWARE_TYPE="Ethernet"),
#     InterfaceData(LINK_STATUS="up", PROTOCOL_STATUS="up", HARDWARE_TYPE="Ethernet")
# ]
#
# iterator = DataclassListIterator(interface_data_list)
#
# for interface in iterator:
#     print(interface)
# Output:
# InterfaceData(LINK_STATUS='up', PROTOCOL_STATUS='up', HARDWARE_TYPE='Ethernet', ...)
# InterfaceData(LINK_STATUS='down', PROTOCOL_STATUS='down', HARDWARE_TYPE='Ethernet', ...)
# InterfaceData(LINK_STATUS='up', PROTOCOL_STATUS='up', HARDWARE_TYPE='Ethernet', ...)

# # Example usage
# people = [
#     Person(name="Alice", age=30, email="alice@example.com"),
#     Person(name="Bob", age=25, email="bob@example.com"),
#     Person(name="Charlie", age=30, email="charlie@example.com"),
#     Person(name="David", age=25, email="david@example.com"),
# ]
#
# filter = DataclassFilter(people)
#
# # Filtering by properties
# filtered_people = filter.filter_by_properties({'age': 30})
# for person in filtered_people:
#     print(person)
# # Output:
# # Person(name='Alice', age=30, email='alice@example.com')
# # Person(name='Charlie', age=30, email='charlie@example.com')
#
# # Filtering by regex
# regex_filtered_people = filter.filter_by_regex({'name': '^A.*'})
# for person in regex_filtered_people:
#     print(person)
# # Output:
# # Person(name='Alice', age=30, email='alice@example.com')

# # Example usage
# people = [
#     Person(name="Alice", age=30, email="alice@example.com"),
#     Person(name="Bob", age=25, email="bob@example.com"),
#     Person(name="Charlie", age=30, email="charlie@example.com"),
#     Person(name="David", age=25, email="david@example.com"),
# ]
#
# sorter = DataclassSorter(people)
#
# # Sorting by age first, then by name
# sorted_people = sorter.sort_by_properties('age', 'name')
#
# for person in sorted_people:
#     print(person)
# Output:
# Person(name='Bob', age=25, email='bob@example.com')
# Person(name='David', age=25, email='david@example.com')
# Person(name='Alice', age=30, email='alice@example.com')
# Person(name='Charlie', age=30, email='charlie@example.com')

# # Example usage
# person = Person(name="Alice", age=30, email="alice@example.com")
# adder = DataclassPropertyAdder(person)
#
# # Adding a new property dynamically
# adder.add_property("address", "123 Main St")
#
# print(person.address)  # Output: 123 Main St
#
# # Converting to dictionary including dynamically added properties
# person_dict = adder.to_dict()
# print(person_dict)  # Output: {'name': 'Alice', 'age': 30, 'email': 'alice@example.com', 'address': '123 Main St'}

# # Example usage
# person = Person(name="Alice", age=30, email="alice@example.com")
# converter = DataclassConverter[Person]
# person_dict = converter.to_dict(person)
#
# print(person_dict)  # Output: {'name': 'Alice', 'age': 30, 'email': 'alice@example.com'}
#
#
#
#
# # Example usage
# people = [
#     Person(name="Alice", age=30, email="alice@example.com"),
#     Person(name="Bob", age=25, email="bob@example.com"),
#     Person(name="Charlie", age=30, email="charlie@example.com")
# ]
#
# filter_criteria = {"age": 30}
# list_filter = ListFilter(people)
# filtered_people = list_filter.filter(filter_criteria)
#
# print(filtered_people)  # Output: [Person(name='Alice', age=30, email='alice@example.com'), Person(name='Charlie', age=30, email='charlie@example.com')]




# # Example usage
# device_connection_data = DeviceConnectionData(
#     device_type="cisco_ios",
#     host="192.168.1.1",
#     username="admin",
#     password="password",
#     secret="secret"
# )
#
# interface_data = InterfaceData(
#     LINK_STATUS="up",
#     PROTOCOL_STATUS="up",
#     HARDWARE_TYPE="Ethernet",
#     MAC_ADDRESS="00:1A:2B:3C:4D:5E",
#     BIA="00:1A:2B:3C:4D:5E",
#     DESCRIPTION="GigabitEthernet0/1",
#     IP_ADDRESS="192.168.1.1",
#     PREFIX_LENGTH="24",
#     MTU="1500",
#     DUPLEX="full",
#     SPEED="1000Mb/s",
#     MEDIA_TYPE="RJ45",
#     BANDWIDTH="1000000",
#     DELAY="10",
#     ENCAPSULATION="ARPA",
#     LAST_INPUT="never",
#     LAST_OUTPUT="00:00:00",
#     LAST_OUTPUT_HANG="never",
#     QUEUE_STRATEGY="fifo",
#     INPUT_RATE="0",
#     OUTPUT_RATE="0",
#     INPUT_PPS="0",
#     OUTPUT_PPS="0",
#     INPUT_PACKETS="0",
#     OUTPUT_PACKETS="0",
#     RUNTS="0",
#     GIANTS="0",
#     INPUT_ERRORS="0",
#     CRC="0",
#     FRAME="0",
#     OVERRUN="0",
#     ABORT="0",
#     OUTPUT_ERRORS="0",
#     VLAN_ID="10",
#     VLAN_ID_INNER="20",
#     VLAN_ID_OUTER="30"
# )
#
# network_device_data = NetworkDeviceData(
#     switch_hostname="switch1",
#     switch_ip_address="192.168.1.2",
#     switch_region="US-West",
#     device_connection_data=device_connection_data,
#     interface_data=[interface_data]
# )
#
# user = User(
#     username="jdoe",
#     name="John Doe",
#     email="jdoe@example.com",
#     phone="123-456-7890"
# )
#
# computer = Computer(
#     hostname="comp1",
#     ip_address="192.168.1.3",
#     mac_address="00:1A:2B:3C:4D:5F",
#     users=[user]
# )

# # Example class that is not a dataclass
# class ExampleClass:
#     def __init__(self, attr1: int, attr2: str):
#         self.attr1 = attr1
#         self.attr2 = attr2
#
# example_instance = ExampleClass(attr1=42, attr2="hello")
#
# identifier = TypeIdentifier()
#
# device_connection_data_types = identifier.get_attribute_types(device_connection_data)
# interface_data_types = identifier.get_attribute_types(interface_data)
# network_device_data_types = identifier.get_attribute_types(network_device_data)
# user_types = identifier.get_attribute_types(user)
# computer_types = identifier.get_attribute_types(computer)
# example_class_types = identifier.get_attribute_types(example_instance)
#
# print("DeviceConnectionData types:", device_connection_data_types)
# print("InterfaceData types:", interface_data_types)
# print("NetworkDeviceData types:", network_device_data_types)
# print("User types:", user_types)
# print("Computer types:", computer_types)
# print("ExampleClass types:", example_class_types)
