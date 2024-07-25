from __future__ import annotations

import typing

if typing.TYPE_CHECKING:
    from typing_extensions import Literal

import time

from .. import spec
from .. import timestamp_utils
from . import timelength_convert


@typing.overload
def get_age(
    timestamp: spec.Timestamp,
    to_representation: Literal['TimelengthPhrase'],
    *,
    precise: bool = False,
) -> spec.TimelengthPhrase: ...


@typing.overload
def get_age(
    timestamp: spec.Timestamp,
    to_representation: Literal['TimelengthSeconds'],
    *,
    precise: bool = False,
) -> spec.TimelengthSeconds: ...


@typing.overload
def get_age(
    timestamp: spec.Timestamp,
    to_representation: Literal['TimelengthSecondsPrecise'],
    *,
    precise: bool = False,
) -> spec.TimelengthSecondsPrecise: ...


def get_age(
    timestamp: spec.Timestamp,
    to_representation: spec.TimelengthRepresentation | None = None,
    *,
    precise: bool = False,
) -> spec.Timelength:
    now = time.time()
    if not precise:
        now = int(now)
        seconds: int | float = now - timestamp_utils.timestamp_to_seconds(
            timestamp
        )
    else:
        seconds = now - timestamp_utils.timestamp_to_seconds_precise(timestamp)
    return create_timelength(seconds, to_representation=to_representation)


def create_timelength(
    seconds: spec.TimelengthSecondsRaw,
    to_representation: spec.TimelengthRepresentation | None = None,
) -> spec.Timelength:
    """create Timelength

    ## Inputs
    - seconds: int or float seconds
    - to_reprsentation: str name of Timelength representation

    ## Returns
    - Timelength with specified representation
    """

    if to_representation is None:
        to_representation = 'TimelengthSeconds'

    if to_representation == 'TimelengthSeconds':
        return create_timelength_seconds(seconds)
    elif to_representation == 'TimelengthSecondsPrecise':
        return create_timelength_seconds_precise(seconds)
    elif to_representation == 'TimelengthLabel':
        return create_timelength_label(seconds)
    elif to_representation == 'TimelengthPhrase':
        return create_timelength_phrase(seconds)
    elif to_representation == 'TimelengthClock':
        return create_timelength_clock(seconds)
    elif to_representation == 'TimelengthClockPhrase':
        return create_timelength_clock_phrase(seconds)
    elif to_representation == 'TimelengthTimedelta':
        return create_timelength_timedelta(seconds)
    else:
        raise Exception(
            'unknown timelength representation: ' + str(to_representation)
        )


def create_timelength_seconds(
    timelength: spec.Timelength,
) -> spec.TimelengthSeconds:
    """create Timelength with representation TimelengthSeconds"""
    # return int(seconds)
    return timelength_convert.timelength_to_seconds(timelength)


def create_timelength_seconds_precise(
    timelength: spec.Timelength,
) -> spec.TimelengthSecondsPrecise:
    """create Timelength with representation TimelengthPrecise"""
    return timelength_convert.timelength_to_seconds_precise(timelength)


def create_timelength_label(
    timelength: spec.Timelength,
) -> spec.TimelengthLabel:
    """create Timelength with representation TimelengthLabel"""
    return timelength_convert.timelength_to_label(timelength)


def create_timelength_phrase(
    timelength: spec.Timelength,
) -> spec.TimelengthPhrase:
    """create Timelength with representation TimelengthPhrase"""
    return timelength_convert.timelength_to_phrase(timelength)


def create_timelength_clock(
    timelength: spec.Timelength,
) -> spec.TimelengthClock:
    """create Timelength with representation TimelengthClock"""
    return timelength_convert.timelength_to_clock(timelength)


def create_timelength_clock_phrase(
    timelength: spec.Timelength,
) -> spec.TimelengthClockPhrase:
    """create Timelength with representation TimelengthClockPhrase"""
    return timelength_convert.timelength_to_clock_phrase(timelength)


def create_timelength_timedelta(
    timelength: spec.Timelength,
) -> spec.TimelengthTimedelta:
    """create Timelength with representation TimelengthTimedelta"""
    return timelength_convert.timelength_to_timedelta(timelength)
