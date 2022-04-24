"""
devices > novation > incontrol > controls > fader

Definitions for fader controls shared between Launchkey devices
"""

from typing import Optional
from common.eventpattern import BasicPattern, ForwardedPattern
from common.types import EventData
from controlsurfaces import ControlEvent, ControlSurface
from controlsurfaces import (
    Fader,
    GenericFaderButton,
    MasterGenericFaderButton,
    MasterFader,
)
from controlsurfaces.valuestrategies import (
    Data2Strategy,
    ForwardedStrategy,
)
from devices.matchers import (
    IControlMatcher,
    BasicControlMatcher,
    IndexedMatcher
)

__all__ = [
    'LkFader',
    'LkMasterFader',
    'LkFaderButton',
    'LkMasterFaderButton',
    'LkFaderSet',
]

# Fader start
F_START = 0x29
# Fader button start
FB_START = 0x33


class LkFader(Fader):
    def __init__(self, index: int) -> None:
        super().__init__(
            ForwardedPattern(2, BasicPattern(0xBF, F_START + index, ...)),
            ForwardedStrategy(Data2Strategy()),
            (0, index)
        )


class LkMasterFader(MasterFader):
    def __init__(self) -> None:
        super().__init__(
                ForwardedPattern(2, BasicPattern(0xBF, 0x07, ...)),
                ForwardedStrategy(Data2Strategy())
            )


class LkFaderButton(GenericFaderButton):
    def __init__(self, index: int) -> None:
        super().__init__(
            ForwardedPattern(2, BasicPattern(0xBF, FB_START + index, ...)),
            ForwardedStrategy(Data2Strategy()),
            (0, index)
        )


class LkMasterFaderButton(MasterGenericFaderButton):
    def __init__(self) -> None:
        super().__init__(
                    ForwardedPattern(2, BasicPattern(0xBF, 0x3B, ...)),
                    ForwardedStrategy(Data2Strategy()),
                )


class LkFaderSet(IControlMatcher):
    def __init__(self) -> None:
        matcher = BasicControlMatcher()
        matcher.addSubMatcher(IndexedMatcher(0xBF, F_START, [
            LkFader(i) for i in range(8)
        ]))
        matcher.addSubMatcher(IndexedMatcher(0xBF, FB_START, [
            LkFaderButton(i) for i in range(8)
        ]))
        matcher.addControls([
            LkMasterFader(),
            LkMasterFaderButton(),
        ])
        self.__matcher = matcher

    def matchEvent(self, event: EventData) -> Optional[ControlEvent]:
        return self.__matcher.matchEvent(event)

    def getGroups(self) -> set[str]:
        return self.__matcher.getGroups()

    def getControls(self, group: str = None) -> list[ControlSurface]:
        return self.__matcher.getControls()