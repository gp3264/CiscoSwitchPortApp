import sys
import inspect
import ipaddress
import csv
import re
from typing import Tuple,List, TypeVar, Any, Sequence, Optional, overload, Union , Dict, List,  TypeVar, Type
from app.UtilityLogger import UtilityLogger as CustomLogger, LOG_LEVEL_DEBUG
from rapid7vmconsole import PageInfo




    # def parse_interface_output(self, output: str) -> dict:
    #     """
    #     Parse the output of 'show interfaces' and return a dictionary with parsed values.
    #
    #     :param output: The output of 'show interfaces' command.
    #     :return: A dictionary with parsed values.
    #     """
    #     interface_data = {}
    #     last_input_match = re.search(r'Last input\s+(\S+)', output)
    #     last_output_match = re.search(r'Last output\s+(\S+)', output)
    #     last_output_hang_match = re.search(r'output hang\s+(\S+)', output)
    #
    #     if last_input_match:
    #         interface_data['last_input'] = self.parse_time_string(last_input_match.group(1))
    #     if last_output_match:
    #         interface_data['last_output'] = self.parse_time_string(last_output_match.group(1))
    #     if last_output_hang_match:
    #         interface_data['last_output_hang'] = self.parse_time_string(last_output_hang_match.group(1))
    #
    #     return interface_data




class TaskProgress:
    def __init__(self, total_steps):
        self.total_steps = total_steps
        self.current_step = 0
        
        #self.hourglass_states:Dict = {0: f'{chr(196)} ', 1: r"\ ", 2: '| ', 3: '/ '}
        #self.hourglass_states:Dict = {0: f'{chr(220)} ', 1: f'{chr(222)} ', 2: f'{chr(223)} ', 3: f'{chr(221)} '}
        #self.hourglass_states:Dict = {0: f"\u25dc ", 1: f"\u25dd ", 2: f"\u25de ", 3: f"\u25df "}
         
        # half circle spin
        self.hourglass_states:Dict = {0: f"\u25d0 ", 1: f"\u25d3 ", 2: f"\u25d1 ", 3: f"\u25d2 "} # half circle spin
        
        self.hourglass_current_state:int = 0
        self.hourglass_str = "*"

    def update_progress(self, step_increment=1):
        """Update the task progress by a specified step increment and print the current status."""
        self.current_step += step_increment
        if self.current_step > self.total_steps:
            self.current_step = self.total_steps
        msg = self.print_progress()
        return msg

    def print_progress(self)->str:
        """Print the current progress as a percentage of the total task completion on the same console line."""
        percentage = (self.current_step / self.total_steps) * 100
        msg = f"\r\t {self.hourglass_states[self.hourglass_current_state]} Task Progress: {percentage:.2f}%"
        sys.stdout.write(msg)
        sys.stdout.flush()
        self.move_hourglass()
        return msg

    def complete(self)->str:
        """Mark the task as complete and print the final status."""
        self.current_step = self.total_steps
        percentage = (self.current_step / self.total_steps) * 100
        msg = f"\r\t \u2713 Task Progress: {percentage:.2f}%"
        sys.stdout.write(msg)
        sys.stdout.flush()
        self.move_hourglass()
        print()  # Move to the next line after completion
        return msg
    
    def move_hourglass(self):
        self.hourglass_current_state += 1
        if self.hourglass_current_state > 3:
            self.hourglass_current_state = 0
        

class GenericItemCounter:
    # Class attribute to keep track of values for multiple attributes
    values_count = {}

    def __init__(self, **kwargs):
        # Process each named attribute and update the counts accordingly
        for attr_name, value in kwargs.items():
            # Initialize the dictionary for the attribute if it does not exist
            if attr_name not in GenericItemCounter.values_count:
                GenericItemCounter.values_count[attr_name] = {}
            
            # Update the count of the value for the specified attribute
            if value in GenericItemCounter.values_count[attr_name]:
                GenericItemCounter.values_count[attr_name][value] += 1
            else:
                GenericItemCounter.values_count[attr_name][value] = 1

    @classmethod
    def get_unique_counts(cls, attr_name):
        """Returns the counts of unique values for a specified attribute."""
        return cls.values_count.get(attr_name, {})

class UniqueValueCounter:
    def __init__(self, values_list):
        self.values_list = values_list
        self.value_counts = self._count_values()

    def _count_values(self):
        """Count unique values in the initial list."""
        counts = {}
        for value in self.values_list:
            if value in counts:
                counts[value] += 1
            else:
                counts[value] = 1
        return counts

    def get_counts(self):
        """Return the dictionary of value counts."""
        return self.value_counts


    

    def read_file_content(self) -> str:
        """
        Reads the entire content of a file and returns it as a string.

        :return: The content of the file as a string.
        :rtype: str
        """
        try:
            with open(self._filename, 'r', encoding='utf-8') as file:
                return file.read()
        except FileNotFoundError:
            raise FileNotFoundError(f"The file {self._filename} was not found.")
        except Exception as e:
            raise Exception(f"An error occurred while reading the file content: {e}")
        
    def read_list(self)->list:
        content = self.read_file_content()
        pre_list = content.split("\n")
        return pre_list



class Pagination:

    def __init__(self, fetch_page_func: callable, **kwargs):
        """
        
        :param fetch_page_func:
        :type fetch_page_func:
        """
        
        self._max_pages:int = None
        self._logger:CustomLogger = CustomLogger("Pagination-Monthly-Report")
        self._resource_count:int = 0
        self.resources = None
        self.current_data = []
        self.fetch_page_func = fetch_page_func
        self._init_page_info(**kwargs)
    
    def _init_page_info(self, **kwargs):
        """
        
        """
        self._page_info:PageInfo = PageInfo()
        self._page_info.number = kwargs.get('page', 0)
        self._page_info.size = kwargs.get('size', 0)
        self._page_info.size = 1
        self._page_info.number = 0
        self._page_info.total_pages = 1
        self._page_info.total_resources = 1
        
    def set_next_page(self, page:int=1, size:int=1):
        """
        
        :param page:
        :type page:
        :param size:
        :type size:
        """
        self._page_info.number = page
        self._page_info.size = size

    def fetch_next_page(self, **kwargs) -> List[Any]:
        """
        
        """
        self.current_data = None
        try:
            self.current_data = self.fetch_page_func(**kwargs)
            #print("\t", end="")
            #print(self.current_data.page.to_dict())
        except TypeError as e:
            e
            self.current_data = self.fetch_page_func
            if hasattr(self.current_data, 'resources'): 
                self._resource_count += len(self.current_data.resources)
                return self.current_data.resources
        
        
        # if isinstance(self.current_data, ReferencesWithAssetIDLink):
        #     return self.current_data.resources
        
        if hasattr(self.current_data, 'page'): 
            self._page_info:PageInfo = self.current_data.page
            if hasattr(self.current_data, 'resources'): 
                self._resource_count += len(self.current_data.resources)
                return self.current_data.resources
            else:
                raise AttributeError("Resources List Does Not Exist in the returned object.")
        else:
            
            raise AttributeError('Returning Object does not have a PageInfo object returned. ')
        
        # returning an empty list
        return list()

    def has_next_page(self) -> bool:
        """
        
        """
        self._logger.log(LOG_LEVEL_DEBUG, f"{self._resource_count}  <= {self._page_info.total_resources}")
        # self._logger.log(LOG_LEVEL_DEBUG, f"{len(self.current_data.resources)}")
        if self._resource_count < self._page_info.total_resources:
                # check for <= previous 
            return True
        return False

    def get_all_resources(self, **kwargs) -> List[Any]:
        """
        
        """
        if hasattr(kwargs, 'MAX_PAGES'):
            self._max_pages = kwargs.pop('MAX_PAGES')
            
        if isinstance(kwargs, dict): 
            if kwargs.get('MAX_PAGES') is not None:
                self._max_pages = kwargs.pop('MAX_PAGES')
        
        page_resources: List[Any] = []
        # page_data.extend(self.fetch_next_page().resources)
        while True:
            if self._max_pages is not None:
                if self._max_pages <= kwargs['page']: 
                    break
        # try:
            next_page = self.fetch_next_page(**kwargs)
            # for item in next_page:
            #     self._logger.log(LOG_LEVEL_DEBUG, pformat(item.to_dict()))  
            page_resources.extend(next_page)
            kwargs['page'] += 1
            self._logger.log(LOG_LEVEL_DEBUG, f"resource count:{len(page_resources)}")

        # except Exception as e:
        #    raise Exception(f"Get all Pages\n{e}")
               
            if (self.has_next_page()):
                continue
            
            break
            
        self._logger.log(LOG_LEVEL_DEBUG, f"Total resources found: {len(page_resources)} of {self._page_info.total_resources}")
        return page_resources

    def reset_pagination(self):
        """
        
        """
        self.current_page = 0
        self._resource_count = 0;
        self.current_data = []



class LibraryModuleClassObjectBrowser:
   
    def __init__(self, library_module:object=None): 
        
        # Set up Instance members
        # self.library_module = None
        self._library_module:object = None
        self._obj:object = None
        self._obj_class_name: str = None
        self._class_properties: list[dict] = None
        self._library_class_list: list = None
        
        # init Library Module 
        self._init_lib(library_module)
    
    def _init_lib(self, library_module:object):
        self._library_module = library_module
        self._build_library_module_class_names()
    
    def _init_obj(self, obj:object): 
        self._obj = obj
        self._obj_class_name:str = None
        self._class_properties:list[dict] = None    
            
        self._identify_object_class_name()
        self._build_library_module_class_names()
    
    @property
    def library_module(self) -> object:
        return self._library_module
    
    @library_module.setter
    def libaray_module(self, library_module:object=None):
        if LibraryModuleClassObjectBrowser._isType(library_module, None):
            return
        self._library_module = library_module
        self._build_library_module_class_names()
                
        if LibraryModuleClassObjectBrowser._isType(self._obj, self._library_module):
            self._obj_class_name = None
            self._class_properties = None        
            self._identify_object_class_name()
           
    @property
    def obj(self) -> object:
        return self._obj
    
    @obj.setter
    def obj(self, obj:object):
        self._init_obj(obj)
    
    @property 
    def class_name(self):
        return self._obj_class_name    
        
    @property
    def info(self) -> str:
        return self.__str__()
    
    @property
    def list_class_properties(self) -> list:
        if LibraryModuleClassObjectBrowser._isType(self._obj, None):
            # if self._obj.__dict__.items() is None:
            return []

        return_list:list = []
        
        if hasattr(self._obj, '__dict__'):
            for prop, value in self._obj.__dict__.items():
                return_list.append(prop)
        return return_list
 
    def get_class_property_key_value_pairs(self) -> dict:
        """
        :return 
        """
        if LibraryModuleClassObjectBrowser._isType(self._obj, None):
            return None
       
        if hasattr(self._obj, '__dict__'):
            return_dict:dict = self._obj.__dict__.items()
            return return_dict
        raise TypeError("Object __dict__.items() is {type(self._obj.__dict__.items())}, \
            Expecting dict")
        return None 
               
    def object_has_property(self, class_property:str=None) -> bool:
        """
        
        :param class_property:
        """
        
        if class_property is None or self.list_class_properties is None:
            return None
        
        value = False
        if class_property is not None:
            if class_property in self.list_class_properties:
                value = True
        return value
    
    def get_object_property_value(self, property_name:str=None) -> object:
        """
        
        :param property_name:
        """
        if property_name is None or self._obj is None:
            return None
        if self.object_has_property(property_name):
            return getattr(self._obj, property_name, None)
        return None
    
    @classmethod
    def _isType(cls, obj:object=None, type_expected:object=None) -> bool:
        return_value:bool = False
        if obj is None or type_expected is None:
            return return_value
        if type(obj) is type_expected:
            return_value = True
        else:
            # raise TypeError(f"{obj} is {type(obj)}, Expected: {type_expected} type")
            pass
        return return_value
    
    def _build_library_module_class_names(self) -> None:
        if LibraryModuleClassObjectBrowser._isType(self._library_module, None):
            return None       
        self._library_class_list = [getattr(self._library_module, attr) for attr in dir(self._library_module) if isinstance(getattr(self._library_module, attr), type)]
        return None      
     
    def _identify_object_class_name(self):
        if LibraryModuleClassObjectBrowser._isType(self._library_class_list, None):
            return None
        
        for class_item in self._library_class_list:
            if isinstance(self._obj, class_item):
                self._obj_class_name = class_item.__name__
                return
        # raise ModuleNotFoundError(f'{class_item} class is not in the loaded Library/Module: {self._library_module}.')
        return
    
    def _discovery(self):
        
        pass
    
    def _load_property_values(self) -> list[dict]:
        return_value:list = []
        property_dict:dict = {}
        
        for prop, value in self._obj.__dict__.items():
            property_dict[prop] = value 
            return_value.append(property_dict)
            property_dict = {}

        return return_value
    
    def _get_object_info(self) -> str:
        return_value:str = " - Object Info - \n"
        return_value = f'{return_value}\nClass name: {self._obj_class_name}\n({self._library_module})\n'
        return_value = f'{return_value}\nProperties:'
        return_value = f'{return_value}\n{self.list_class_properties}'
        return_value = f'{return_value}\n\nProperty Data:\n====================\n'
        for prop in self.list_class_properties:
            return_value = '{0}\n{1}:{2}\n'.format(return_value, prop, self.get_object_property_value(prop)) 
        return_value = f'{return_value}\n****\n' 
        return return_value    
    
    def __str__ (self):
        return self._get_object_info()
