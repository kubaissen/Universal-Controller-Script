"""
common > util > snap

Contains functions to help with snapping to a default value
"""

import common

SNAP_AMOUNT = 0.02


def snap(value: float, to: float) -> float:
    """
    If a value is close to the snap to value, it will be snapped to it,
    otherwise, it is returned unadjusted

    ### Args:
    * `value` (`float`): value to snap
    * `to` (`float`): value to snap to

    ### Returns:
    * `float`: snapped value
    """

    if not common.getContext().settings.get("plugins.general.do_snap"):
        return value

    if abs(value - to) <= SNAP_AMOUNT:
        return to
    return value
