import inspect
import ipaddress
import csv
import app

from typing import Any, Dict,  List, Tuple, TypeVar, Generic
from app import cli_commands



# Define a type variable for generic type hints
T = TypeVar('T')


class UniqueObjectList:
    @staticmethod
    def remove_duplicates(objects: List[T]) -> List[T]:
        """
        Removes duplicates from a list of objects based on their attributes.

        Args:
            objects (List[T]): The list of objects from which to remove duplicates.

        Returns:
            List[T]: A new list of objects with duplicates removed.
        """
        unique_objects = []
        seen = set()
        for obj in objects:
            # Create a hashable representation of the object's attributes
            obj_attributes = tuple(obj.__dict__.items())
            if obj_attributes not in seen:
                seen.add(obj_attributes)
                unique_objects.append(obj)
        return unique_objects






class ObjectMapper:

    def __init__(self, obj):
        """
        Initialize the ObjectMapper with an object.

        :param obj: The object to be mapped.
        """
        self.obj = obj
        self.mapping = []

    def _map_object(self, obj, depth=0):
        """
        Recursively map the object.

        :param obj: The object to map.
        :param depth: The current depth of recursion.
        """
        obj_info = {
            "class_reference": obj.__class__,
            "class_name": obj.__class__.__name__,
            "depth": depth
        }
        self.mapping.append(obj_info)

        # Depth control to avoid too deep recursion
        if depth > 10:
            return

        if isinstance(obj, dict):
            for key, value in obj.items():
                self._map_object(value, depth + 1)

        elif isinstance(obj, (list, set)):
            for item in obj:
                self._map_object(item, depth + 1)

        elif hasattr(obj, '__dict__'):
            for attr, value in obj.__dict__.items():
                self._map_object(value, depth + 1)

        # Primitives and other types are already handled by the class reference

    def map(self):
        """
        Start the mapping process.
        """
        self._map_object(self.obj)

    def __str__(self):
        """
        Return a string representation of the object mapping.

        :return: The string representation.
        """
        return str(self.mapping)

# Example usage:
# obj_mapper = ObjectMapper(some_complex_object)
# obj_mapper.map()
# print(obj_mapper)


class ObjectInspector:

    def __init__(self, obj, **kwargs):
        """
        Initialize the ObjectInspector with an object.

        :param obj: The object to be inspected.
        """
        self._MAX_DEPTH = None
        MAX_DEPTH = kwargs.get('max', 10)
        if type(MAX_DEPTH) == int:
                self._MAX_DEPTH = MAX_DEPTH
        else:
            self._MAX_DEPTH = 10    
        
        self.obj = obj
        self._output = ""
        self._seen = set()

    def _inspect(self, obj, depth=0):
        """
        Recursively inspect the object.

        :param obj: The object to inspect.
        :param depth: The current depth of recursion.
        """
        indent = "    " * depth
        obj_id = id(obj)

        if obj_id in self._seen:
            self._output += f"{indent}Circular reference detected for object id {obj_id}\n"
            return
        self._seen.add(obj_id)

        self._output += f"{indent}Type: {type(obj)}, Value: {obj}\n"

        if depth > self._MAX_DEPTH:
            self._output += f"{indent}... (Depth limit reached)\n"
            return

        if isinstance(obj, dict):
            for key, value in obj.items():
                self._output += f"{indent}Key: {key}\n"
                self._inspect(value, depth + 1)

        elif isinstance(obj, (list, set)):
            for item in obj:
                self._inspect(item, depth + 1)

        elif hasattr(obj, '__dict__'):
            for attr, value in obj.__dict__.items():
                self._output += f"{indent}Attribute: {attr}\n"
                self._inspect(value, depth + 1)

        else:
            self._output += f"{indent}Primitive/Other type: {type(obj)}\n"

    def __str__(self):
        """
        Return a string representation of the object's structure.

        :return: The string representation.
        """
        self._inspect(self.obj)
        return self._output


class ModelObjectHandler():

    def __init__(self):
        self._object_browser:LibraryModuleClassObjectBrowser = LibraryModuleClassObjectBrowser(None)
        self.object_map:ObjectInspector = None
        # self._object_browser:LibraryModuleClassObjectBrowser = LibraryModuleClassObjectBrowser(Models)
        self._logger = None
        self.api = None
        self._current_object = None
        self._object_list = []
        self._list_index = 0
    
    @property
    def obj(self) -> object:
        """
        
        """
        return self._current_object
    
    @obj.setter
    def obj(self, obj:object) -> Any:
        self._object_browser.obj = obj
        self.object_map = ObjectInspector(obj)
        self._current_object = obj
        return self._current_object
    
    def get_object_property_value(self, property_name:str) -> Any:
        if property_name in self._obj_browser.list_class_properties:
            return getattr(self._current_object, property_name)
        return None
      
    def add_object(self, obj:object):
        self._object_list.append(obj)
        self.obj = obj
        self._list_index += 1
        
    def add_objects(self, objs:object):

        if isinstance(objs, (list, set)):
            for sub_obj in objs: 
                self._object_list.append(sub_obj)
                self.obj = sub_obj
                self._list_index += 1
        else:
            self._object_list.append(objs)
            self.obj = objs
            self._list_index += 1
        
    def clear_object_list(self) -> int:
        self._object_list = []
        self._list_index = 0
        return len(self._object_list)
        
    def hasObjects(self):
        if self.object_count() > 0:
            return True
        return False
    
    def object_count(self) -> int:
        return len(self._object_list)
    
    def pop(self) -> object:
        self._list_index -= 1
        return self._object_list.pop()
    
    def next(self):
        if self.hasObjects() == False:
            self._list_index = 0;
        if self.object_count < self._list_index:
            self._list_index = 0
        self._list_index += 1
        self._current_object = self._object_list[self._list_index]
   
    def __str__(self):
        if self.hasObjects() == False:
            return "None"
        
        return_value = ""
        counter:int = 0
        for obj in self._object_list:
            counter += 1 
            self.obj = obj
            info = self._object_browser.info
            if info is None:
                return_value = f'\n{return_value}-{counter}- None \n'
            else:
                return_value = f'\n{return_value}{counter}-{info}'
        return self.object_map
    

class ModuleObjectMatcher:

    def __init__(self, module):
        """
        Initialize ModuleObjectMatcher with a module.

        :param module: The module containing classes to be matched against.
        """
        self.module = module
        self.class_list = self._extract_classes_from_module(module)

    def _extract_classes_from_module(self, module):
        """
        Extract classes from the given module.

        :param module: The module to extract classes from.
        :return: List of classes in the module.
        """
        return [cls for name, cls in inspect.getmembers(module) if inspect.isclass(cls)]

    def match_object(self, obj):
        """
        Match the given object with classes from the module.

        :param obj: The object to be matched.
        :return: List of potential class matches.
        """
        matches = []
        obj_inspector = ObjectInspector(obj)
        obj_structure = str(obj_inspector)

        for cls in self.class_list:
            cls_inspector = ObjectInspector(cls())
            cls_structure = str(cls_inspector)
            if self._structures_match(obj_structure, cls_structure):
                matches.append(cls)

        return matches

    def _structures_match(self, obj_structure, cls_structure):
        """
        Compare the structure of the object with the structure of a class.

        :param obj_structure: The structure of the object.
        :param cls_structure: The structure of the class.
        :return: Boolean indicating whether the structures match.
        """
        # Implement the logic to determine if structures match
        # This is a placeholder for comparison logic
        return obj_structure == cls_structure


class ObjectInspectorPlus(ObjectInspector):

    def __init__(self, obj, module=None, **kwargs):
        """
        Initialize the ObjectInspector with an object and optionally a module.

        :param obj: The object to be inspected.
        :param module: The module containing classes to be matched against.
        """
        self._MAX_DEPTH = kwargs.get('max', 10) if isinstance(kwargs.get('max'), int) else 10
        self.obj = obj
        self.module = module
        self._output = ""
        self._seen = set()
        if module:
            self.class_list = self._extract_classes_from_module(module)
        else:
            self.class_list = []

    # def _inspect(self, obj, depth=0):
    #     # ... [existing _inspect method implementation] ...

    def _extract_classes_from_module(self, module):
        """
        Extract classes from the given module.

        :param module: The module to extract classes from.
        :return: List of classes in the module.
        """
        return [cls for name, cls in inspect.getmembers(module) if inspect.isclass(cls)]

    def match_object(self):
        """
        Match the inspected object with classes from the module.

        :return: List of potential class matches.
        """
        matches = []
        obj_structure = str(self)

        for cls in self.class_list:
            cls_inspector = ObjectInspector(cls())
            cls_structure = str(cls_inspector)
            if self._structures_match(obj_structure, cls_structure):
                matches.append(cls)

        return matches

    def _structures_match(self, obj_structure, cls_structure):
        """
        Compare the structure of the object with the structure of a class.

        :param obj_structure: The structure of the object.
        :param cls_structure: The structure of the class.
        :return: Boolean indicating whether the structures match.
        """
        # Implement the logic to determine if structures match
        # This is a placeholder for comparison logic
        return obj_structure == cls_structure

    def __str__(self):
        """
        Return a string representation of the object's structure.

        :return: The string representation.
        """
        self._inspect(self.obj)
        return self._output

class ObjectClassFinder:
    def __init__(self, library_module:object=None, obj:object=None): 
        
        # Set up Instance members
        # self.library_module = None
        self._isInstance:bool = False
        self._library_module:object = None
        self._obj:object = None
        self._obj_class_name: str = None
        self._class_properties: list[dict] = None
        self._library_class_list: list = None
        
        # init Library Module 
        self._init_lib(library_module)
        self._init_obj(obj)
        
    @property    
    def obj(self)->object:
        return self._obj 
    
    @property
    def class_name(self)->str:
        return self._obj_class_name
    
    @property
    def library_module(self)->object:
        return self._library_module
    
    @property
    def class_object(self):
        return self.get_class()


    @property
    def obj_properties(self) -> list:
        if ObjectClassFinder._isType(self._obj, None):
            # if self._obj.__dict__.items() is None:
            return []

        return_list:list = []
        
        if hasattr(self._obj, '__dict__'):
            for prop, value in self._obj.__dict__.items():
                return_list.append(prop)
        return return_list        
    
    def _init_lib(self, library_module:object):
        self._library_module = library_module
        self._build_library_module_class_names()
    
    def _init_obj(self, obj:object): 
        self._obj = obj
        self._obj_class_name:str = None
        self._class_properties:list[dict] = None    
            
        self._identify_object_class_name()
        self._build_library_module_class_names()

    def _build_library_module_class_names(self) -> None:
        if ObjectClassFinder._isType(self._library_module, None):
            return None       
        self._library_class_list = [getattr(self._library_module, attr) for attr in dir(self._library_module) if isinstance(getattr(self._library_module, attr), type)]
        return None      
     
    def _identify_object_class_name(self):
        if ObjectClassFinder._isType(self._library_class_list, None):
            return None
        
        for class_item in self._library_class_list:
            if isinstance(self._obj, class_item):
                self._isInstance = True
                self._obj_class_name = class_item.__name__
                return class_item
        # raise ModuleNotFoundError(f'{class_item} class is not in the loaded Library/Module: {self._library_module}.')
        return None
    
    def get_class_name(self)->str:    
        return self._obj_class_name
    
    def get_class(self)->object:
        if self._identify_object_class_name() is not None:
            return self._identify_object_class_name() 
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
            raise TypeError(f"{obj} is {type(obj)}, Expected: {type_expected} type")
            pass
        return return_value
    
    def _build_library_module_class_names(self) -> None:
        if LibraryModuleClassObjectBrowser._isType(self._library_module, None):
            return None       
        self._library_class_list = [getattr(self._library_module, attr) for attr in dir(self._library_module) if isinstance(getattr(self._library_module, attr), type)]
        return None      
     
    def _identify_object_class_name(self):
        #if LibraryModuleClassObjectBrowser._isType(self._library_class_list, None):
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

