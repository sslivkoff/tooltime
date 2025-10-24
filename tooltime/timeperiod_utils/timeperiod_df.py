from __future__ import annotations

import typing

from tooltime import spec

if typing.TYPE_CHECKING:
    import datetime
    import polars as pl


def get_intervals(
    start: spec.Timestamp,
    end: spec.Timestamp,
    interval: str,
    *,
    include_incomplete: bool = True,
    label: typing.Literal['open', 'closed', 'start'] | None = None,
    clip_inward: bool = False,
    include_end: bool = False,
    resolution: typing.Literal['ms', 'us', 'ns'] = 'ms',
) -> pl.DataFrame:
    """return standardized, integer-aligned time intervals over range

    - clip_inward: clip incomplete intervals to fall between start and end

    - interval is in str format '{number}{time_unit}'
        - alternatives can be {second, minute, hour, day, week, month, year}
        - number = integer
        - time_unit = s, m, h, d, w, M, q, y
    - end column timestamp is considered non-inclusive in range
        - range labels are considered inclusive, according to the interval unit
    - intervals are standardized to be integer offsets from January 1 1970
        - week are the exception, weeks begin on sunday
            - December 28, 1969 is sunday 0
            - January 4, 170 is sunday 1
    """
    import datetime
    import math
    import tooltime
    import polars as pl

    # convert literal names
    if interval == 'second':
        interval = '1s'
    elif interval == 'minute':
        interval = '1m'
    elif interval == 'hour':
        interval = '1h'
    elif interval == 'day':
        interval = '1d'
    elif interval == 'week':
        interval = '1w'
    elif interval == 'month':
        interval = '1M'
    elif interval == 'quarter':
        interval = '1q'
    elif interval == 'year':
        interval = '1y'

    interval_nicknames = {
        'second': 's',
        'minute': 'm',
        'hour': 'h',
        'day': 'd',
        'week': 'w',
        'month': 'M',
        'quarter': 'q',
        'year': 'y',
        'mo': 'M',
    }
    for nickname, actual_name in interval_nicknames.items():
        if interval.endswith(nickname):
            interval = interval[:-2] + actual_name
            break

    # parse interval
    count = int(interval[:-1])
    unit = interval[-1]
    if unit == 'q':
        count = 3 * count
        unit = 'M'

    # create float and datetime representations of bounds
    start = tooltime.timestamp_to_seconds_precise(start)
    end = tooltime.timestamp_to_seconds_precise(end)
    start_dt = tooltime.timestamp_to_datetime(start)
    end_dt = tooltime.timestamp_to_datetime(end)

    if unit in ['s', 'm', 'h', 'd']:
        # simple units are just an integer number of seconds
        if unit == 's':
            duration = count
        elif unit == 'm':
            duration = 60 * count
        elif unit == 'h':
            duration = 3600 * count
        elif unit == 'd':
            duration = 86400 * count
        else:
            raise Exception('invalid interval unit')
        start = math.floor(start / duration) * duration
        end = math.ceil(end / duration) * duration
        timestamps = []
        for seconds in range(start, end + duration, duration):
            timestamps.append(_seconds_to_dt(seconds))
        if include_end:
            timestamps.append(_seconds_to_dt(end + duration))

        if unit == 'd':
            label_col = _create_label(count, '%Y-%m-%d', '-1d', label)
        else:
            label_col = _create_label(count, '%Y-%m-%d %T', '-1' + unit, label)
    elif unit == 'w':
        # weeks require an offset from unix genesis in order to land on sunday
        # unix genesis was a thursday, subtract 4 days
        first_sunday = 0 - 4 * 86400
        duration = 86400 * 7 * count
        start_week = math.floor((start - first_sunday) / duration)
        end_week = math.ceil((end - first_sunday) / duration)
        raw_timestamps = range(
            start_week * duration + first_sunday,
            end_week * duration + first_sunday + duration,
            duration,
        )
        timestamps = [_seconds_to_dt(timestamp) for timestamp in raw_timestamps]
        if include_end:
            timestamps.append(
                _seconds_to_dt(end_week * duration + first_sunday + duration)
            )
        label_col = _create_label(count, '%Y-%m-%d', '-1d', label)
    elif unit == 'M':
        # compute months from unix genesis and then divide into years
        start_month = (start_dt.year - 1970) * 12 + start_dt.month - 1
        start_month = math.floor(start_month / count) * count

        if end_dt == datetime.datetime(
            year=end_dt.year,
            month=end_dt.month,
            day=1,
            tzinfo=datetime.timezone.utc,
        ):
            end_month = (end_dt.year - 1970) * 12 + end_dt.month - 1
        else:
            end_month = (end_dt.year - 1970) * 12 + end_dt.month - 1 + 1
        end_month = math.ceil(end_month / count) * count

        timestamps = []
        if include_end:
            end_range_month = end_month + count + count
        else:
            end_range_month = end_month + count
        for month in range(start_month, end_range_month, count):
            dt = _to_dt(1970 + math.floor(month / 12), month % 12 + 1, 1)
            timestamps.append(dt)
        label_col = _create_label(count, '%Y-%m', '-1mo', label)
    elif unit == 'y':
        # compute years from unix genesis
        start_year = math.floor(start_dt.year / count) * count
        if end_dt == _to_dt(year=end_dt.year, month=1, day=1):
            end_year = math.ceil(end_dt.year / count) * count
        else:
            end_year = math.ceil((end_dt.year + 1) / count) * count
        timestamps = []
        for year in range(start_year, end_year + count, count):
            timestamps.append(_to_dt(year=year, month=1, day=1))
        if include_end:
            timestamps.append(_to_dt(year=end_year + count, month=1, day=1))
        label_col = _create_label(count, '%Y', '-1y', label)
    else:
        raise Exception('invalid unit')

    # generate dataframe
    timezone = 'utc'
    df = pl.DataFrame(
        {'start': timestamps[:-1], 'end': timestamps[1:]},
        schema={
            'start': pl.Datetime(resolution, timezone),
            'end': pl.Datetime(resolution, timezone),
        },
    )

    # trim extraneous
    if include_end:
        df = df.filter(pl.col.start.cast(pl.Int64) <= end * 1000)

    # add completeness label
    df = df.with_columns(
        completeness=pl.when(
            pl.col.start >= start * 1000, pl.col.end <= end * 1000
        )
        .then(pl.lit('complete'))
        .otherwise(pl.lit('incomplete'))
    )

    # handle incomplete intervals
    if clip_inward:
        df = df.with_columns(
            start=pl.when(pl.col.start <= start * 1000)
            .then(pl.lit(start * 1000).cast(pl.Datetime('ms')))
            .otherwise('start'),
            end=pl.when(pl.col.end > end * 1000)
            .then(pl.lit(end * 1000).cast(pl.Datetime('ms')))
            .otherwise('end'),
            completeness=pl.col.completeness.replace({'incomplete': 'clipped'}),
        )
    elif not include_incomplete:
        df = df.filter(pl.col.completeness != 'incomplete')

    # add label
    df = df.select(label_col.alias('label'), 'start', 'end', 'completeness')

    return df


def _to_dt(year: int, month: int, day: int) -> datetime.datetime:
    import datetime

    return datetime.datetime(
        year=year, month=month, day=day, tzinfo=datetime.timezone.utc
    )


def _seconds_to_dt(seconds: int | float) -> datetime.datetime:
    import datetime

    return datetime.datetime.fromtimestamp(seconds, datetime.timezone.utc)


def _create_label(
    count: int,
    format: str,
    offset: str,
    label: typing.Literal['open', 'closed', 'start'] | None,
) -> pl.Expr:
    import polars as pl

    if label is None:
        if count is None:
            label = 'start'
        else:
            label = 'open'

    if label == 'start':
        return pl.col.start.dt.to_string(format)
    elif label == 'open':
        return (
            '['
            + pl.col.start.dt.to_string(format)
            + ', '
            + (pl.col.end.dt.to_string(format))
            + ')'
        )
    elif label == 'closed':
        return (
            '['
            + pl.col.start.dt.to_string(format)
            + ', '
            + (pl.col.end.dt.offset_by(offset).dt.to_string(format))
            + ']'
        )
    else:
        raise Exception()


# TODO: turn these into a test suite

# def validate_chunks(
#     chunks: pl.DataFrame,
#     chunk_size: str,
#     start_time: int | float,
#     end_time: int | float,
#     skip_incomplete_intervals: bool,
# ) -> None:
#     min_seconds, max_seconds = get_duration_min_max_seconds(chunk_size)

#     # no gaps between chunks
#     assert chunks['starts'][1:].eq(chunks['end'][:-1]).all()

#     # chunks fall within min and max sizes
#     assert chunks.select((pl.col.duration <= max_seconds).all())['duration'][0]
#     assert chunks.select((pl.col.duration >= min_seconds).all())['duration'][0]

#     # start_time and end_time are indexed correctly inside chunks
#     start_index = chunks['start'].search_sorted(start_time)
#     end_index = chunks['end'].search_sorted(end_time, 'right')
#     if skip_incomplete_intervals:
#         # start time is before first interval or lower bound of first interval
#         assert start_time == chunks['start'][0] or start_index == 0

#         # end time is in last interval or upper bound of last interval
#         assert end_time == chunks['end'][-1] or end_index == len(chunks) - 1
#     else:
#         # start time is in first interval or lower bound of first interval
#         assert start_time == chunks['start'][0] or start_index == 1

#         # end time is in last interval or upper bound of last interval
#         assert end_time == chunks['end'][-1] or end_index == len(chunks['end'])

#     # start_time is less than chunk_size away from first chunk start
#     assert abs(start_time - chunks['start'][0]) < max_seconds

#     # end_time is less than chunk_size away from last chunk end
#     assert abs(end_time - chunks['end'][-1]) < max_seconds


# def get_duration_min_max_seconds(duration: str) -> tuple[int, int]:
#     count = int(duration[:-1])
#     unit = duration[-1]
#     if unit == 'h':
#         return (count * 3600, count * 3600)
#     elif unit == 'd':
#         return (count * 86400, count * 86400)
#     elif unit == 'w':
#         return (count * 86400 * 7, count * 86400 * 7)
#     elif unit == 'M':
#         return (count * 86400 * 28, count * 86400 * 31)
#     elif unit == 'y':
#         return (count * 86400 * 365, count * 86400 * 366)
#     else:
#         raise Exception('invalid duration unit: ' + str(unit))
