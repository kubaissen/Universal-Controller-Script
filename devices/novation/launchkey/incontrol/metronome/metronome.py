"""
devices > novation > launchkey > mk2 > drumpad

Definition for the Launchkey Mk2 Drumpads

Authors:
* Miguel Guthridge [hdsq@outlook.com.au, HDSQ#2154]
"""

from common.eventpattern import ForwardedPattern
from common.eventpattern.notepattern import NotePattern
from common.types import Color
from controlsurfaces.valuestrategies import NoteStrategy, ForwardedStrategy
from controlsurfaces import MetronomeButton
from ..incontrolsurface import InControlSurface


class LkMetronomeButton(InControlSurface, MetronomeButton):
    """
    Custom drum pad implementation used by Lunchkey series controllers
    to provide RGB functionality
    """
    def __init__(
        self,
        channel: int,
        note_num: int,
        colors: dict[Color, int],
    ) -> None:
        self._color_manager = InControlSurface(channel, note_num, colors)
        # Variable to keep the drumpad lights working
        self._ticker_timer = 0
        InControlSurface.__init__(
            self,
            channel,
            note_num,
            colors,
        )
        MetronomeButton.__init__(
            self,
            ForwardedPattern(2, NotePattern(note_num, channel)),
            ForwardedStrategy(NoteStrategy()),
        )
