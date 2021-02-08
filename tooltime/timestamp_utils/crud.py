import time

from . import convert


def create_timestamp(seconds=None, representation='TimestampSeconds'):
    """create Timestamp

    ## Inputs
    - seconds: int or float utc seconds
    - representation: str name of Timestamp representation

    ## Returns
    - Timestamp with specified representation
    """
    if representation == 'TimestampSeconds':
        return create_timestamp_seconds(seconds=seconds)
    elif representation == 'TimestampSecondsPrecise':
        return create_timestamp_seconds_precise(seconds=seconds)
    elif representation == 'TimestampLabel':
        return create_timestamp_label(seconds=seconds)
    elif representation == 'TimestampISO':
        return create_timestamp_iso(seconds=seconds)
    elif representation == 'TimestampDatetime':
        return create_timestamp_datetime(seconds=seconds)
    else:
        raise Exception('unknown representation: ' + str(representation))


def create_timestamp_seconds(seconds=None):
    """create Timestamp with representation TimestampSeconds"""
    if seconds is None:
        seconds = time.time()
    return int(seconds)


def create_timestamp_seconds_precise(seconds=None):
    """create Timestamp with representation TimestampSecondsPrecise"""
    if seconds is None:
        seconds = time.time()
    return float(seconds)


def create_timestamp_label(seconds=None):
    """create Timestamp with representation TimestampLabel"""
    if seconds is None:
        seconds = time.time()
    return convert.timestamp_seconds_to_label(seconds)


def create_timestamp_iso(seconds=None):
    """create Timestamp with representation TimestampISO"""
    if seconds is None:
        seconds = time.time()
    return convert.timestamp_seconds_to_iso(seconds)


def create_timestamp_datetime(seconds=None):
    """create Timestamp with representation TimestampDatetime"""
    if seconds is None:
        seconds = time.time()
    return convert.timestamp_seconds_to_datetime(seconds)

