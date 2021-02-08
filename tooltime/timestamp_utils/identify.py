import datetime

from .. import exceptions
from . import convert


def detect_timestamp_representation(timestamp):
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


def is_timestamp(timestamp):
    """return bool of whether input is Timestamp"""
    try:
        detect_timestamp_representation(timestamp)
        return True
    except Exception:
        return False


def is_timestamp_seconds(timestamp):
    """return bool of whether input is TimestampSeconds"""
    return isinstance(timestamp, int)


def is_timestamp_seconds_precise(timestamp):
    """return bool of whether input is TimestampSecondsPrecise"""
    return isinstance(timestamp, float)


def is_timestamp_label(timestamp):
    """return bool of whether input is TimestampLabel"""
    try:
        convert.timestamp_label_to_seconds(timestamp)
        return True
    except Exception:
        return False


def is_timestamp_iso(timestamp):
    """return bool of whether input is TimestampISO"""
    try:
        convert.timestamp_iso_to_seconds(timestamp)
        return True
    except Exception:
        return False


def is_timestamp_datetime(timestamp):
    """return bool of whether input is TimestampDatetime"""
    return isinstance(timestamp, datetime.datetime)

