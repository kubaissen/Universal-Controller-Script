"""
controlsurfaces > controlshadow

Represents a "shadow" control surface, which can be modified as necessary
without affecting the original control, unless it is specifically applied

Authors:
* Miguel Guthridge [hdsq@outlook.com.au, HDSQ#2154]
"""

from typing import TYPE_CHECKING
from common.types import Color
from .controlmapping import ControlMapping

if TYPE_CHECKING:
    from . import ControlSurface


class ControlShadow:
    """
    A class representing a MIDI event mapped to a control surface

    Subclasses of this object should be generated by device modules, so that it
    can then be processed by plugin modules.
    """

    def __init__(self, control: 'ControlSurface') -> None:
        """
        Create an event object

        This should be called when recognising an event

        ### Args:
        * `control` (`ControlSurface`): control associated with this event
        """
        self._control = control
        self._value = 0.0
        self._color = Color()
        self._annotation = ""
        self._changed = False

    def __repr__(self) -> str:
        return f"Shadow of {self._control}"

    def getControl(self):
        """
        Get a reference to the control surface associated with the event

        ### Returns:
        * `ControlSurface`: control surface
        """
        return self._control

    def getMapping(self) -> ControlMapping:
        """
        Returns a ControlMapping to the control
        """
        return self._control.getMapping()

    @property
    def value(self) -> float:
        """
        Represents the value that will be applied to the control after
        the event has been processed, as a float between 0-1
        """
        return self._value

    @value.setter
    def value(self, newVal: float) -> None:
        if self._value != newVal:
            if not (0 <= newVal <= 1):
                raise ValueError("Value must be within range 0-1")
            self._value = newVal
            self._changed = True

    @property
    def color(self) -> Color:
        """
        Represents the color that will be applied to the control after the
        event has been processed.
        """
        return self._color

    @color.setter
    def color(self, newColor: Color) -> None:
        if self._color != newColor:
            self._color = newColor
            self._changed = True

    @property
    def annotation(self) -> str:
        """
        Represents the annotation that will be applied to the control after the
        event has been processed.
        """
        return self._annotation

    @annotation.setter
    def annotation(self, newAnnotation: str) -> None:
        if self._annotation != newAnnotation:
            self._annotation = newAnnotation
            self._changed = True

    @property
    def group(self) -> str:
        """
        The group that the control is in
        """
        return self._control.group

    @property
    def coordinate(self) -> tuple[int, int]:
        """
        The coordinate of the control
        """
        return self._control.coordinate

    def apply(self, thorough: bool) -> None:
        """
        Apply the configuration of the control shadow to the control it
        represents
        """
        if thorough or self._changed:
            self._control.color = self.color
            self._control.annotation = self.annotation
            self._control.value = self.value
            self._changed = False
