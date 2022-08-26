from __future__ import annotations

import math
import time
import typing

from .. import spec
from .. import timelength_utils
from . import timestamp_convert


def parse_timeslice(
    raw_timeslice: str,
    n: int | None = None,
    interval: spec.Timelength | None = None,
    include_misaligned_bound: bool = True,
    include_misaligned_overflow: bool = False,
) -> typing.Sequence[int | float]:

    if raw_timeslice.count(':') == 0:
        if n is None and interval is None:
            raise Exception('only start and end specified, must also provide n or interval')
        start = raw_timeslice
        end = ''

    elif raw_timeslice.count(':') == 1:
        if n is None and interval is None:
            raise Exception('only start and end specified, must also provide n or interval')
        start, end = raw_timeslice.split(':')

    elif raw_timeslice.count(':') == 2:
        if n is not None:
            raise Exception('cannot specify both interval and n')
        start, end, interval = raw_timeslice.split(':')
        if interval == '':
            raise Exception('invalid interval provided')
        if interval.isdecimal():
            interval = int(interval)

    else:
        raise Exception('cannot parse raw timeslice: ' + str(raw_timeslice))

    now = int(time.time())

    # convert start to a timestamp
    if start == '':
        raise Exception('must specify start time')
    try:
        start_timelength = timelength_utils.timelength_to_seconds(start)
        start_time = now - start_timelength
    except Exception:
        start_time = timestamp_convert.timestamp_to_seconds(start)

    # convert end to a timestamp
    if end == '':
        end_time = now
    else:
        try:
            end_timelength = timelength_utils.timelength_to_seconds(end)
            end_time = now - end_timelength
        except Exception:
            end_time = timestamp_convert.timestamp_to_seconds(end)

    return sample_timestamps(
        start_time=start_time,
        end_time=end_time,
        n_samples=n,
        sample_interval=interval,
        include_misaligned_overflow=include_misaligned_overflow,
        include_misaligned_bound=include_misaligned_bound,
    )


def sample_timestamps(
    start_time: spec.Timestamp | None = None,
    end_time: spec.Timestamp | None = None,
    n_samples: int | None = None,
    sample_interval: spec.Timelength | None = None,
    window_size: spec.Timelength | None = None,
    align_to: typing.Literal['start', 'end'] = 'start',
    include_misaligned_bound: bool = False,
    include_misaligned_overflow: bool = False,
) -> typing.Sequence[int | float]:
    """

    must specify at least one of start_time or end_time
    must specify at least one of n_samples or sample_interval

    ## Relationships
        window_size = (n_samples - 1) * sample_interval
                    = end_time - start_time

    ## Possible Inputs
    - start_time, sample_interval, n_samples
    - end_time, sample_interval, n_samples
    - start_time, end_time, n_samples
    - start_time, end_time, sample_interval
    - start_time, window_size, n_samples
    - start_time, window_size, sample_interval
    - end_time, window_size, n_samples
    - end_time, window_size, sample_interval
    """

    if start_time is not None:
        start_time = timestamp_convert.timestamp_to_numerical(start_time)
    if end_time is not None:
        end_time = timestamp_convert.timestamp_to_numerical(end_time)
    if window_size is not None:
        window_size = timelength_utils.timelength_to_numerical(window_size)
    if sample_interval is not None:
        sample_interval = timelength_utils.timelength_to_numerical(
            sample_interval
        )

    if start_time is not None and end_time is not None:
        if end_time <= start_time:
            raise Exception('end_time must come after start_time')
    if (
        start_time is not None
        and end_time is not None
        and window_size is not None
    ):
        if not math.isclose(end_time - start_time, window_size):
            raise Exception('window size does not match given start and end')
    if sample_interval is not None and n_samples is not None:
        if (
            (start_time is not None and end_time is not None)
            or (start_time is not None and window_size is not None)
            or (end_time is not None and window_size is not None)
        ):
            raise Exception('overdetermined system, specify fewer parameters')

    # determine start_time, end_time, and sample_interval
    if (
        start_time is not None
        and end_time is not None
        and sample_interval is not None
    ):
        pass
    elif (
        start_time is not None
        and end_time is not None
        and n_samples is not None
    ):
        sample_interval = (end_time - start_time) / (n_samples - 1)
    elif (
        start_time is not None
        and window_size is not None
        and sample_interval is not None
    ):
        end_time = start_time + window_size
    elif (
        end_time is not None
        and window_size is not None
        and sample_interval is not None
    ):
        start_time = end_time - window_size
    elif (
        start_time is not None
        and window_size is not None
        and n_samples is not None
    ):
        end_time = start_time + window_size
        sample_interval = (end_time - start_time) / (n_samples - 1)
    elif (
        end_time is not None
        and window_size is not None
        and n_samples is not None
    ):
        start_time = end_time - window_size
        sample_interval = (end_time - start_time) / (n_samples - 1)
    else:
        raise Exception('underdetermined system, specify more parameters')

    # create samples
    if align_to == 'start':
        samples: typing.MutableSequence[int | float] = []
        while True:
            s = len(samples)
            next_sample = start_time + s * sample_interval
            if next_sample < end_time or math.isclose(next_sample, end_time):
                samples.append(next_sample)
            else:
                break
    elif align_to == 'end':
        samples = []
        while True:
            s = len(samples)
            next_sample = end_time - s * sample_interval
            if next_sample > start_time or math.isclose(
                next_sample, start_time
            ):
                samples.append(next_sample)
            else:
                break
        samples = list(samples)[::-1]
    else:
        raise Exception('unknown alignment target: ' + str(align_to))

    # add misalignment samples
    fractional_samples = (end_time - start_time) / sample_interval + 1
    if not math.isclose(fractional_samples, int(fractional_samples)):
        if align_to == 'start':
            if include_misaligned_bound:
                samples.append(end_time)
            if include_misaligned_overflow:
                samples.append(samples[-1] + sample_interval)
        elif align_to == 'end':
            if include_misaligned_bound:
                samples.insert(0, start_time)
            if include_misaligned_overflow:
                samples.insert(0, samples[0] - sample_interval)

    return samples
