from pprint import pprint, pformat
from typing import Dict
from app.file_support import FileHandler 
from app.mac_address_support import MacAddressSupport
from app.cli_commands_templates import CLIExecutive


class MainDataRetrieval:
    def __init__(self, **kwargs):
        self.region_nodes_json_file = kwargs.get("filename",r'region_nodes.json' )
        self.region_nodes: Dict() = {}
        self._load_file(self.region_nodes_json_file)

    
    def _load_file(self, filename):
        self.region_nodes = FileHandler.read_json(filename)
        
    def __repr__(self):
        return pprint(self.region_nodes)
    
    def __str__(self):
        return pformat(self.region_nodes)
    
    
    
    
        
        
if __name__ == "__main__":
    sample = MainDataRetrieval(filename="region_nodes.json")
    print(str(sample))
        