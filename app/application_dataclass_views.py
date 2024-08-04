from dataclasses import dataclass, field, fields, asdict, is_dataclass
from typing import Dict, List, Any, Optional
from app.application_dataclasses_support import InfoErrorFlags
from app.application_dataclasses import DataclassDunderMethods
from pickle import NONE

@dataclass 
class PortSecurityViewEntry(DataclassDunderMethods):
    switch_hostname:Optional[str] = None
    switch_ip_address:Optional[str] = None
    switch_region:Optional[str] = None
    converted_last_input: Optional[str] = NONE
    converted_last_output: Optional[str] = NONE
    mac_vendor:Optional[str] = None
    INTERFACE: Optional[str] = None
    LINK_STATUS: Optional[str] = None
    PROTOCOL_STATUS: Optional[str] = None
    HARDWARE_TYPE: Optional[str] = None
    MAC_ADDRESS: Optional[str] = None
    BIA: Optional[str] = None
    DESCRIPTION: Optional[str] = None
    IP_ADDRESS: Optional[str] = None
    PREFIX_LENGTH: Optional[str] = None
    MTU: Optional[str] = None
    DUPLEX: Optional[str] = None
    SPEED: Optional[str] = None
    MEDIA_TYPE: Optional[str] = None
    BANDWIDTH: Optional[str] = None
    DELAY: Optional[str] = None
    ENCAPSULATION: Optional[str] = None
    LAST_INPUT: Optional[str] = None
    LAST_OUTPUT: Optional[str] = None
    LAST_OUTPUT_HANG: Optional[str] = None
    QUEUE_STRATEGY: Optional[str] = None
    INPUT_RATE: Optional[str] = None
    OUTPUT_RATE: Optional[str] = None
    INPUT_PPS: Optional[str] = None
    OUTPUT_PPS: Optional[str] = None
    INPUT_PACKETS: Optional[str] = None
    OUTPUT_PACKETS: Optional[str] = None
    RUNTS: Optional[str] = None
    GIANTS: Optional[str] = None
    INPUT_ERRORS: Optional[str] = None
    CRC: Optional[str] = None
    FRAME: Optional[str] = None
    OVERRUN: Optional[str] = None
    ABORT: Optional[str] = None
    OUTPUT_ERRORS: Optional[str] = None
    VLAN_ID: Optional[str] = None
    VLAN_ID_INNER: Optional[str] = None
    VLAN_ID_OUTER: Optional[str] = None
    