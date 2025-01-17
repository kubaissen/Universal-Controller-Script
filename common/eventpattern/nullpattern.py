"""
common > nullpattern

An event pattern that matches with nothing

Authors:
* Miguel Guthridge [hdsq@outlook.com.au, HDSQ#2154]
"""

# from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from common.types import EventData
from . import IEventPattern


class NullPattern(IEventPattern):
    """
    Null patterns won't match with any events
    """

    def matchEvent(self, event: 'EventData') -> bool:
        return False
