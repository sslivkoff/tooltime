from __future__ import annotations

import time
import typing

from .. import spec
from . import timestamp_convert
from . import timestamp_identify


def now(
    representation: spec.TimestampRepresentation = 'TimestampSeconds',
) -> spec.Timestamp:
    return create_timestamp(seconds=None, representation=representation)


def create_timestamp(
    seconds: typing.SupportsFloat | None = None,
    representation: spec.TimestampRepresentation = 'TimestampSeconds',
) -> spec.Timestamp:
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


def create_timestamp_seconds(
    seconds: typing.SupportsFloat | None = None,
) -> spec.TimestampSeconds:
    """create Timestamp with representation TimestampSeconds"""
    if seconds is None:
        seconds = time.time()
    return int(float(seconds))


def create_timestamp_seconds_precise(
    seconds: typing.SupportsFloat | None = None,
) -> spec.TimestampSecondsPrecise:
    """create Timestamp with representation TimestampSecondsPrecise"""
    if seconds is None:
        seconds = time.time()
    return float(seconds)


def create_timestamp_label(
    seconds: typing.SupportsFloat | None = None,
) -> spec.TimestampLabel:
    """create Timestamp with representation TimestampLabel"""
    if seconds is None:
        seconds = time.time()
    return timestamp_convert.timestamp_seconds_to_label(seconds)


def create_timestamp_iso(
    seconds: typing.SupportsFloat | None = None,
) -> spec.TimestampISO:
    """create Timestamp with representation TimestampISO"""
    if seconds is None:
        seconds = time.time()
    return timestamp_convert.timestamp_seconds_to_iso(seconds)


def create_timestamp_iso_pretty(
    seconds: typing.SupportsFloat | None = None,
) -> spec.TimestampISOPretty:
    """create Timestamp with representation TimestampISOPretty"""
    return create_timestamp_iso(seconds).replace('T', ' ')


def create_timestamp_date(
    seconds: typing.SupportsFloat | None = None,
) -> spec.TimestampDate:
    """create Timestamp with representation TimestampDate

    does not round to nearest date, takes floor of seconds to previous date
    """
    import datetime

    if seconds is None:
        dt = datetime.datetime.now(tz=datetime.timezone.utc)
    else:
        dt = datetime.datetime.fromtimestamp(
            float(seconds), tz=datetime.timezone.utc
        )

    year = dt.year
    month = dt.month
    day = dt.day
    return str(year) + '-' + ('%.02d' % month) + '-' + ('%.02d' % day)


def create_timestamp_year(
    seconds: typing.SupportsFloat | None = None,
) -> spec.TimestampYear:
    """create Timestamp with representation TimestampDate

    does not round to nearest year, takes floor of seconds to previous year
    """
    import datetime

    if seconds is None:
        dt = datetime.datetime.now(tz=datetime.timezone.utc)
    else:
        dt = datetime.datetime.fromtimestamp(
            float(seconds), tz=datetime.timezone.utc
        )

    return str(dt.year)


def create_timestamp_datetime(
    seconds: typing.SupportsFloat | None = None,
) -> spec.TimestampDatetime:
    """create Timestamp with representation TimestampDatetime"""
    if seconds is None:
        seconds = time.time()
    return timestamp_convert.timestamp_seconds_to_datetime(seconds)


def floor_timestamp(
    timestamp: spec.Timestamp,
    interval: typing.Literal['day', 'week', 'month', 'year'],
    output_format: spec.TimestampRepresentation | None = None,
) -> spec.Timestamp:
    return truncate_timestamp(
        timestamp=timestamp,
        interval=interval,
        direction='floor',
        output_format=output_format,
    )


def ceiling_timestamp(
    timestamp: spec.Timestamp,
    interval: typing.Literal['day', 'week', 'month', 'year'],
    output_format: spec.TimestampRepresentation | None = None,
) -> spec.Timestamp:
    return truncate_timestamp(
        timestamp=timestamp,
        interval=interval,
        direction='ceiling',
        output_format=output_format,
    )


def truncate_timestamp(
    timestamp: spec.Timestamp,
    interval: typing.Literal['day', 'week', 'month', 'year'],
    direction: typing.Literal['floor', 'ceiling'],
    output_format: spec.TimestampRepresentation | None = None,
) -> spec.Timestamp:
    """truncate time floorward or ceilingward, getting the floor or ceiling"""
    import datetime
    import math

    if direction not in ['floor', 'ceiling']:
        raise Exception('direction must be floor or ceiling')

    dt = timestamp_convert.timestamp_to_datetime(timestamp)
    if interval == 'day':
        dt_trunc: datetime.datetime = datetime.datetime(
            year=dt.year,
            month=dt.month,
            day=dt.day,
            tzinfo=datetime.timezone.utc,
        )
        if direction == 'floor' and dt > dt_trunc:
            dt_trunc = dt_trunc + datetime.timedelta(days=1)
    elif interval == 'week':
        seconds = timestamp_convert.timestamp_to_seconds(dt)
        sunday = (
            math.floor((seconds + 4 * 86400) / 7 / 86400) * 86400 * 7
            - 4 * 86400
        )
        if direction == 'ceiling':
            sunday = sunday + 7 * 86400
        dt_trunc = timestamp_convert.timestamp_to_datetime(sunday)
    elif interval == 'month':
        dt_trunc = datetime.datetime(
            year=dt.year, month=dt.month, day=1, tzinfo=datetime.timezone.utc
        )
        if direction == 'floor' and dt > dt_trunc:
            if dt.month == 12:
                new_year = dt.year + 1
                new_month = 1
            else:
                new_year = dt.year
                new_month = dt.month + 1
            dt_trunc = datetime.datetime(
                year=new_year,
                month=new_month,
                day=1,
                tzinfo=datetime.timezone.utc,
            )
    elif interval == 'year':
        dt_trunc = datetime.datetime(
            year=dt.year, month=1, day=1, tzinfo=datetime.timezone.utc
        )
        if direction == 'floor' and dt > dt_trunc:
            return datetime.datetime(
                year=dt.year + 1, month=1, day=1, tzinfo=datetime.timezone.utc
            )
    else:
        raise Exception('invalid interval: ' + str(interval))

    if output_format is None:
        output_format = timestamp_identify.detect_timestamp_representation(
            timestamp
        )

    return timestamp_convert.convert_timestamp(dt_trunc, output_format)
