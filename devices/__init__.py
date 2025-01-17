"""
devices

Contains definitions for devices, allowing the script to interface with them

Authors:
* Miguel Guthridge [hdsq@outlook.com.au, HDSQ#2154]
"""

__all__ = [
    'Device',
    'DeviceShadow',
    'EventCallback',
    'IControlMatcher',
    'BasicControlMatcher',
]

from .matchers import IControlMatcher, BasicControlMatcher
from .device import Device
from .deviceshadow import DeviceShadow, EventCallback

# Device manufacturers
from . import (
    novation,
    maudio
)
del (
    novation,
    maudio
)
