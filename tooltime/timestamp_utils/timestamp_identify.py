from __future__ import annotations

import datetime
import typing

if typing.TYPE_CHECKING:
    from typing_extensions import TypeGuard

from .. import exceptions
from .. import spec
from . import timestamp_convert


def detect_timestamp_representation(
    timestamp: spec.Timestamp,
) -> spec.TimestampRepresentation:
    """return str name of Timestamp representation"""
    if is_timestamp_seconds(timestamp):
        return 'TimestampSeconds'
    elif is_timestamp_seconds_precise(timestamp):
        return 'TimestampSecondsPrecise'
    elif is_timestamp_label(timestamp):
        return 'TimestampLabel'
    elif is_timestamp_iso(timestamp):
        return 'TimestampISO'
    elif is_timestamp_datetime(timestamp):
        return 'TimestampDatetime'
    else:
        raise exceptions.RepresentationDetectionException(
            'could not detect Timestamp representation: ' + str(timestamp)
        )


def is_timestamp(timestamp: typing.Any) -> TypeGuard[spec.Timestamp]:
    """return bool of whether input is Timestamp"""
    try:
        detect_timestamp_representation(timestamp)
        return True
    except Exception:
        return False


def is_timestamp_seconds(
    timestamp: typing.Any,
) -> TypeGuard[spec.TimestampSeconds]:
    """return bool of whether input is TimestampSeconds"""
    return isinstance(timestamp, int) or type(timestamp).__name__ in [
        'int16',
        'int32',
        'int64',
    ]


def is_timestamp_seconds_precise(
    timestamp: typing.Any,
) -> TypeGuard[spec.TimestampSecondsPrecise]:
    """return bool of whether input is TimestampSecondsPrecise"""
    return isinstance(timestamp, float)


def is_timestamp_label(
    timestamp: typing.Any,
) -> TypeGuard[spec.TimestampLabel]:
    """return bool of whether input is TimestampLabel"""
    try:
        timestamp_convert.timestamp_label_to_seconds(
            typing.cast(spec.TimestampLabel, timestamp)
        )
        return True
    except Exception:
        return False


def is_timestamp_iso(
    timestamp: typing.Any,
) -> TypeGuard[spec.TimestampISO]:
    """return bool of whether input is TimestampISO"""
    try:
        timestamp_convert.timestamp_iso_to_seconds(
            typing.cast(spec.TimestampISO, timestamp)
        )
        return True
    except Exception:
        return False


def is_timestamp_datetime(
    timestamp: typing.Any,
) -> TypeGuard[spec.TimestampDatetime]:
    """return bool of whether input is TimestampDatetime"""
    return isinstance(timestamp, datetime.datetime)

