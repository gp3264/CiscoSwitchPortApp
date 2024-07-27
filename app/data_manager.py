

class DataExtrator:
    pass



from typing import Any, Union, List, Dict
from functools import cmp_to_key

class DataProcessor:
    def __init__(self, data: Any) -> None:
        """
        Initialize the processor with any Python data structure.

        :param data: Data to be processed.
        :type data: Any
        """
        self.data = data

    def sort(self, key: str = None, ascending: bool = True) -> Any:
        """
        Sort the data structure by a specified key or position. Supports nested structures.

        :param key: The key or position to sort by. Supports dot notation for nested keys.
        :type key: str
        :param ascending: True for ascending order, False for descending order.
        :type ascending: bool
        :return: Sorted data structure.
        :rtype: Any
        :raises ValueError: If data is not a list or set.
        """
        if isinstance(self.data, list):
            return sorted(self.data, key=cmp_to_key(self._get_comparator(key, ascending)))
        elif isinstance(self.data, set):
            return sorted(self.data, key=cmp_to_key(self._get_comparator(key, ascending)))
        else:
            raise ValueError("Data must be a list or set to be sorted.")

    def filter(self, key: str, value: Any) -> Any:
        """
        Filter the data structure by a specified key or position. Supports nested structures.

        :param key: The key or position to filter by. Supports dot notation for nested keys.
        :type key: str
        :param value: The value to filter by.
        :type value: Any
        :return: Filtered data structure.
        :rtype: Any
        :raises ValueError: If data is not a list, set, or dict.
        """
        if isinstance(self.data, list):
            return [item for item in self.data if self._get_nested_value(item, key.split('.')) == value]
        elif isinstance(self.data, set):
            return {item for item in self.data if self._get_nested_value(item, key.split('.')) == value}
        elif isinstance(self.data, dict):
            return {k: v for k, v in self.data.items if self._get_nested_value(v, key.split('.')) == value}
        else:
            raise ValueError("Data must be a list, set, or dict to be filtered.")

    def _get_nested_value(self, data: Any, keys: List[str]) -> Any:
        """
        Retrieve the value from a nested data structure using a list of keys.

        :param data: The data structure to retrieve the value from.
        :type data: Any
        :param keys: List of keys to access the nested value.
        :type keys: List[str]
        :return: The nested value.
        :rtype: Any
        """
        for key in keys:
            if isinstance(data, dict):
                data = data.get(key)
            elif isinstance(data, list):
                data = data[int(key)]
            elif hasattr(data, key):
                data = getattr(data, key)
            else:
                raise KeyError(f"Key '{key}' not found in data.")
        return data

    def _get_comparator(self, key: str, ascending: bool):
        """
        Generate a comparator function for sorting based on a nested key.

        :param key: The key to sort by. Supports dot notation for nested keys.
        :type key: str
        :param ascending: True for ascending order, False for descending order.
        :type ascending: bool
        :return: Comparator function for sorting.
        :rtype: function
        """
        def comparator(x, y):
            x_val = self._get_nested_value(x, key.split('.')) if key else x
            y_val = self._get_nested_value(y, key.split('.')) if key else y
            if x_val == y_val:
                return 0
            if ascending:
                return -1 if x_val < y_val else 1
            else:
                return 1 if x_val < y_val else -1
        return comparator

# # Example usage
# data = [
#     {"name": "Alice", "details": {"age": 30, "city": "New York"}},
#     {"name": "Bob", "details": {"age": 25, "city": "San Francisco"}},
#     {"name": "Charlie", "details": {"age": 35, "city": "New York"}},
#     {"name": "David", "details": {"age": 40, "city": "Chicago"}},
# ]
#
# processor = DataProcessor(data)
#
# # Sort by details.age in ascending order
# sorted_data_asc = processor.sort(key="details.age", ascending=True)
# print("Sorted by details.age (ascending):", sorted_data_asc)
#
# # Sort by details.age in descending order
# sorted_data_desc = processor.sort(key="details.age", ascending=False)
# print("Sorted by details.age (descending):", sorted_data_desc)
#
# # Filter by details.city
# filtered_data = processor.filter(key="details.city", value="New York")
# print("Filtered by details.city (New York):", filtered_data)


from typing import List, Dict, Any, Union
import operator








class DictListProcessor:
    def __init__(self, data: List[Dict[str, Any]]) -> None:
        """
        Initialize the processor with a list of dictionaries.

        :param data: List of dictionaries to be processed.
        :type data: List[Dict[str, Any]]
        :raises ValueError: If data is not a list of dictionaries.
        """
        if not isinstance(data, list) or not all(isinstance(i, dict) for i in data):
            raise ValueError("Data must be a list of dictionaries.")
        self.data = data

    def sort_by_property(self, property_name: str, ascending: bool = True) -> List[Dict[str, Any]]:
        """
        Sort the list of dictionaries by a specified property. Supports nested properties.

        :param property_name: The property name to sort by, can be nested (e.g., 'a.b.c').
        :type property_name: str
        :param ascending: True for ascending order, False for descending order.
        :type ascending: bool
        :return: Sorted list of dictionaries.
        :rtype: List[Dict[str, Any]]
        :raises KeyError: If the property_name does not exist in any dictionary.
        """
        def get_nested_value(d, keys):
            for key in keys:
                d = d[key]
            return d

        keys = property_name.split('.')
        try:
            sorted_data = sorted(self.data, key=lambda x: get_nested_value(x, keys), reverse=not ascending)
        except KeyError as e:
            raise KeyError(f"Property '{property_name}' does not exist in all dictionaries.") from e
        return sorted_data

    def filter_by_property(self, property_name: str, value: Any) -> List[Dict[str, Any]]:
        """
        Filter the list of dictionaries by a specified property value. Supports nested properties.

        :param property_name: The property name to filter by, can be nested (e.g., 'a.b.c').
        :type property_name: str
        :param value: The value to filter by.
        :type value: Any
        :return: Filtered list of dictionaries.
        :rtype: List[Dict[str, Any]]
        :raises KeyError: If the property_name does not exist in any dictionary.
        """
        def get_nested_value(d, keys):
            for key in keys:
                d = d[key]
            return d

        keys = property_name.split('.')
        try:
            filtered_data = [item for item in self.data if get_nested_value(item, keys) == value]
        except KeyError as e:
            raise KeyError(f"Property '{property_name}' does not exist in all dictionaries.") from e
        return filtered_data

# # Example usage
# data = [
#     {"name": "Alice", "details": {"age": 30, "city": "New York"}},
#     {"name": "Bob", "details": {"age": 25, "city": "San Francisco"}},
#     {"name": "Charlie", "details": {"age": 35, "city": "New York"}},
#     {"name": "David", "details": {"age": 40, "city": "Chicago"}},
# ]
#
# processor = DictListProcessor(data)
#
# # Sort by details.age in ascending order
# sorted_data_asc = processor.sort_by_property("details.age", ascending=True)
# print("Sorted by details.age (ascending):", sorted_data_asc)
#
# # Sort by details.age in descending order
# sorted_data_desc = processor.sort_by_property("details.age", ascending=False)
# print("Sorted by details.age (descending):", sorted_data_desc)
#
# # Filter by details.city
# filtered_data = processor.filter_by_property("details.city", "New York")
# print("Filtered by details.city (New York):", filtered_data)

from typing import List, Dict, Any, Union
from collections import Counter
import statistics

class DictListStatisticsReport(DictListProcessor):
    def __init__(self, data: List[Dict[str, Any]]) -> None:
        """
        Initialize the report generator with a list of dictionaries.

        :param data: List of dictionaries to be processed.
        :type data: List[Dict[str, Any]]
        """
        super().__init__(data)

    def count_values(self, property_name: str) -> Dict[Any, int]:
        """
        Count the occurrences of each value for a specified property.

        :param property_name: The property name to count values for.
        :type property_name: str
        :return: Dictionary with values as keys and their counts as values.
        :rtype: Dict[Any, int]
        """
        values = [item.get(property_name) for item in self.data]
        return dict(Counter(values))

    def get_statistics(self, property_name: str) -> Dict[str, float]:
        """
        Get statistics (mean, median, mode) for numeric values of a specified property.

        :param property_name: The property name to get statistics for.
        :type property_name: str
        :return: Dictionary with statistics.
        :rtype: Dict[str, float]
        :raises ValueError: If no numeric values are found.
        """
        values = [item.get(property_name) for item in self.data if isinstance(item.get(property_name), (int, float))]

        if not values:
            raise ValueError(f"No numeric values found for property '{property_name}'.")

        return {
            "mean": statistics.mean(values),
            "median": statistics.median(values),
            "mode": statistics.mode(values) if len(values) > 1 else values[0],
            "variance": statistics.variance(values),
            "stdev": statistics.stdev(values)
        }

    def generate_report(self, property_name: str) -> str:
        """
        Generate a formatted report from the data statistics for a specified property.

        :param property_name: The property name to generate the report for.
        :type property_name: str
        :return: Formatted report as a string.
        :rtype: str
        """
        counts = self.count_values(property_name)
        try:
            stats = self.get_statistics(property_name)
        except ValueError:
            stats = {}

        report_lines = []
        report_lines.append(f"Data Statistics Report for '{property_name}'")
        report_lines.append("=" * (len(report_lines[0])))
        report_lines.append(f"'{property_name}' Value Counts:")
        report_lines.append("-" * 20)

        for value, count in counts.items():
            report_lines.append(f"{value}: {count}")

        if stats:
            report_lines.append("\nStatistics for Numeric Values:")
            report_lines.append("-" * 30)
            for stat_name, stat_value in stats.items():
                report_lines.append(f"{stat_name.capitalize()}: {stat_value:.2f}")
        report_lines.append("\n\n")
        return "\n".join(report_lines)

# Example usage
# data = [
#     {"name": "Alice", "age": 30, "city": "New York"},
#     {"name": "Bob", "age": 25, "city": "San Francisco"},
#     {"name": "Charlie", "age": 35, "city": "New York"},
#     {"name": "David", "age": 40, "city": "Chicago"},
# ]
#
# report_generator = DictListStatisticsReport(data)
# report = report_generator.generate_report("age")
# print(report)


import csv
from typing import Any, List, Dict, Union
import collections.abc

class DataTableExporter:
    def __init__(self, data: Any) -> None:
        """
        Initialize the exporter with any Python data structure.

        :param data: Data to be processed.
        :type data: Any
        """
        self.data = data
        self.rows = []

    def _flatten_dict(self, d: Dict[str, Any], parent_key: str = '', sep: str = '.') -> Dict[str, Any]:
        """
        Flatten a nested dictionary.

        :param d: The dictionary to flatten.
        :type d: Dict[str, Any]
        :param parent_key: The base key string.
        :type parent_key: str
        :param sep: Separator between keys.
        :type sep: str
        :return: Flattened dictionary.
        :rtype: Dict[str, Any]
        """
        items = []
        for k, v in d.items():
            new_key = f"{parent_key}{sep}{k}" if parent_key else k
            if isinstance(v, collections.abc.MutableMapping):
                items.extend(self._flatten_dict(v, new_key, sep=sep).items())
            else:
                items.append((new_key, v))
        return dict(items)

    def _process_data(self, data: Any) -> None:
        """
        Process the data into a list of rows for CSV export.

        :param data: Data to be processed.
        :type data: Any
        """
        if isinstance(data, list):
            for item in data:
                self._process_data(item)
        elif isinstance(data, dict):
            flat_data = self._flatten_dict(data)
            self.rows.append(flat_data)
        else:
            raise ValueError("Unsupported data structure")

    def export_to_csv(self, file_path: str) -> None:
        """
        Export the processed data to a CSV file.

        :param file_path: Path to the CSV file.
        :type file_path: str
        """
        self._process_data(self.data)
        if not self.rows:
            raise ValueError("No data to export")

        # Extract headers from the first row
        headers = sorted(self.rows[0].keys())
        
        with open(file_path, 'w', newline='') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=headers)
            writer.writeheader()
            writer.writerows(self.rows)

# Example usage
# data = [
#     {"name": "Alice", "details": {"age": 30, "city": "New York"}},
#     {"name": "Bob", "details": {"age": 25, "city": "San Francisco"}},
#     {"name": "Charlie", "details": {"age": 35, "city": "New York"}},
#     {"name": "David", "details": {"age": 40, "city": "Chicago"}},
# ]
#
# exporter = DataTableExporter(data)
# exporter.export_to_csv("output.csv")
# print("Data exported to output.csv")


from typing import Any, Union, List, Dict
from collections import Counter
import statistics



from typing import Any, Dict

class DataStatisticsReport:
    def __init__(self, statistics_processor: 'DataStatisticsProcessor') -> None:
        """
        Initialize the report generator with a DataStatisticsProcessor instance.

        :param statistics_processor: An instance of DataStatisticsProcessor.
        :type statistics_processor: DataStatisticsProcessor
        """
        self.statistics_processor = statistics_processor

    def generate_report(self) -> str:
        """
        Generate a formatted report from the data statistics.

        :return: Formatted report as a string.
        :rtype: str
        """
        # Get counts and statistics
        counts = self.statistics_processor.count_values()
        try:
            stats = self.statistics_processor.get_statistics()
        except ValueError:
            stats = {}

        # Format the report
        report_lines = []
        report_lines.append("Data Statistics Report")
        report_lines.append("======================")
        report_lines.append("Value Counts:")
        report_lines.append("----------------------")
        
        for value, count in counts.items():
            report_lines.append(f"{value}: {count}")

        if stats:
            report_lines.append("\nStatistics for Numeric Values:")
            report_lines.append("-------------------------------")
            for stat_name, stat_value in stats.items():
                report_lines.append(f"{stat_name.capitalize()}: {stat_value:.2f}")

        return "\n".join(report_lines)

# Example usage
class DataStatisticsProcessor:
    def __init__(self, data: Any) -> None:
        self.data = data

    def count_values(self) -> Dict[Any, int]:
        flat_data = self._flatten_data(self.data)
        return dict(Counter(flat_data))

    def get_statistics(self) -> Dict[str, float]:
        flat_data = self._flatten_data(self.data)
        numeric_values = [x for x in flat_data if isinstance(x, (int, float))]

        if not numeric_values:
            raise ValueError("No numeric values found in data.")

        return {
            "mean": statistics.mean(numeric_values),
            "median": statistics.median(numeric_values),
            "mode": statistics.mode(numeric_values) if len(numeric_values) > 1 else numeric_values[0],
            "variance": statistics.variance(numeric_values),
            "stdev": statistics.stdev(numeric_values)
        }

    def _flatten_data(self, data: Any) -> List[Any]:
        if isinstance(data, dict):
            values = []
            for key, value in data.items():
                values.extend(self._flatten_data(value))
            return values
        elif isinstance(data, list) or isinstance(data, set):
            values = []
            for item in data:
                values.extend(self._flatten_data(item))
            return values
        elif hasattr(data, '__dict__'):
            return self._flatten_data(data.__dict__)
        else:
            return [data]

# Sample data
data = [
    {"name": "Alice", "details": {"age": 30, "city": "New York"}},
    {"name": "Bob", "details": {"age": 25, "city": "San Francisco"}},
    {"name": "Charlie", "details": {"age": 35, "city": "New York"}},
    {"name": "David", "details": {"age": 40, "city": "Chicago"}},
]

# Creating instances and generating the report
processor = DataStatisticsProcessor(data)
report_generator = DataStatisticsReport(processor)
report = report_generator.generate_report()
print(report)
