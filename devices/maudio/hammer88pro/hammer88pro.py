

from typing import Optional
from common.eventpattern import BasicPattern, ForwardedPattern
from common.types import eventData
from common.extensionmanager import ExtensionManager
from controlsurfaces.valuestrategies import ForwardedStrategy, ButtonData2Strategy
from devices import Device, BasicControlMatcher
from devices.controlgenerators import getNotesAllChannels, getPedals, getChannelAftertouchAllChannels

from controlsurfaces import (
    NullEvent,
    Fader,
    Knob,
    PlayButton,
    StopButton,
    RecordButton,
    FastForwardButton,
    RewindButton,
    LoopButton,
    MetronomeButton,
    StandardModWheel,
)
from .hammerpitch import HammerPitchWheel

class Hammer88Pro(Device):
    """
    Device definition for Hammer 88 Pro

    Note: this requires the presets for both DAW and User modes to be loaded
    on the device.
    """
    def __init__(self) -> None:
        matcher = BasicControlMatcher()
        # Null events
        matcher.addControl(NullEvent(
            BasicPattern(0xFA, 0x0, 0x0)
        ))
        matcher.addControl(NullEvent(
            BasicPattern(0xFC, 0x0, 0x0)
        ))
        
        # Notes and pedals
        matcher.addControls(getNotesAllChannels())
        matcher.addControls(getPedals())
        matcher.addControls(getChannelAftertouchAllChannels())
        
        # Transport buttons
        matcher.addControl(StopButton(
            ForwardedPattern(3, BasicPattern(0xBF, 102, ...)),
            ForwardedStrategy(ButtonData2Strategy())
        ))
        matcher.addControl(PlayButton(
            ForwardedPattern(3, BasicPattern(0xBF, 103, ...)),
            ForwardedStrategy(ButtonData2Strategy())
        ))
        matcher.addControl(RecordButton(
            ForwardedPattern(3, BasicPattern(0xBF, 104, ...)),
            ForwardedStrategy(ButtonData2Strategy())
        ))
        matcher.addControl(RewindButton(
            ForwardedPattern(3, BasicPattern(0xBF, 105, ...)),
            ForwardedStrategy(ButtonData2Strategy())
        ))
        matcher.addControl(FastForwardButton(
            ForwardedPattern(3, BasicPattern(0xBF, 106, ...)),
            ForwardedStrategy(ButtonData2Strategy())
        ))
        matcher.addControl(LoopButton(
            ForwardedPattern(3, BasicPattern(0xBF, 107, ...)),
            ForwardedStrategy(ButtonData2Strategy())
        ))
        matcher.addControl(MetronomeButton(
            ForwardedPattern(3, BasicPattern(0xB9, 0x74, ...)),
            ForwardedStrategy(ButtonData2Strategy())
        ))
        matcher.addControl(StandardModWheel())
        matcher.addControl(HammerPitchWheel())
        
        super().__init__(matcher)
    
    @classmethod
    def create(cls, event: Optional[eventData]) -> Device:
        return cls()
    
    @staticmethod
    def getId() -> str:
        return "Maudio.Hammer88Pro"
    
    @staticmethod
    def getUniversalEnquiryResponsePattern():
        return BasicPattern(
            [
                0xF0, # Sysex start
                0x7E, # Device response
                ..., # OS Device ID
                0x06, # Separator
                0x02, # Separator
                0x00, # Manufacturer
                0x01, # Manufacturer
                0x05, # Manufacturer
                0x00, # Family code
                0x3C, # Family code
                # Extra details omitted
                ]
        )

    @staticmethod
    def matchDeviceName(name: str) -> bool:
        """Controller can't be matched to FL device name"""
        return False

ExtensionManager.registerDevice(Hammer88Pro)