import datetime
import math

from .. import timelength_utils
from .. import timestamp_utils


def get_standard_timeperiod(
    standard_timeperiod_spec=None,
    *,
    timelength_label=None,
    block_unit=None,
    block_size=None,
    timestamp=None,
    include_start=True,
    include_end=False,
    boundary_unit='second',
):
    """get standardized Timeperiod that contains a specific Timestamp

    ## Standardized Timeperiods
    - standardized boundaries are integer multiples of some block_unit
    - should specify either timelength_label or block_unit to define block unit
    - should specify block_size to define integer multiple, or use default of 1

    ## Example Usage
    timeperiod = tooltime.get_standard_timeperiod(
        timestamp=1600000000,
        block_size=5,
        block_unit='minutes',
    )
    tooltime.print_timeperiod(timeperiod)
    > [20200913_122500Z, 20200913_122959Z]

    ## Inputs
    - timelength_label: TimelengthLabel
    - block_unit: int size of block unit
    - block_size: str name of time unit
    - timestamp: Timestamp contained in timeperiod, default is now
    - include_start: bool of whether to include start boundary of timeperiod
    - include_end: bool of whether to include end boundary of timeperiod
    - boundary_unit: str name of boundary unit to be shaved off open intervals
    """

    if standard_timeperiod_spec is not None:
        if isinstance(standard_timeperiod_spec, str):
            kwargs = {'timelength_label': standard_timeperiod_spec}
        else:
            kwargs = standard_timeperiod_spec
        return get_standard_timeperiod(**kwargs)

    if (timelength_label is not None) + (block_unit is not None) != 1:
        raise Exception('must specify either timelength_label or block_unit')
    if timelength_label is not None:
        block_size = int(timelength_label[:-1])
        unit_letters_to_names = timelength_utils.unit_letters_to_names()
        block_unit = unit_letters_to_names[timelength_label[-1]]
    if block_unit is not None and block_size is None:
        block_size = 1

    # create timestamp datetime
    if timestamp is not None:
        dt = timestamp_utils.timestamp_to_datetime(timestamp)
    else:
        dt = datetime.datetime.now(datetime.timezone.utc)

    # compute from_datetime
    current_unit = getattr(dt, block_unit)
    lowest_unit_value = timestamp_utils.get_unit_lowest_value(block_unit)
    current_block = math.floor((current_unit - lowest_unit_value) / block_size)
    from_unit = current_block * block_size + lowest_unit_value
    from_datetime = timestamp_utils.floor_datetime(dt, block_unit)
    from_datetime = from_datetime.replace(**{block_unit: from_unit})

    # compute to_datetime
    if block_unit == 'month':
        # datetime.timedelta does not support months
        to_month_raw = from_datetime.month + block_size
        to_month = to_month_raw % 12
        to_year = from_datetime.year + math.floor(to_month_raw / 12)
        to_datetime = from_datetime.replace(month=to_month, year=to_year)
    else:
        block_timedelta = datetime.timedelta(**{(block_unit + 's'): block_size})
        to_datetime = from_datetime + block_timedelta

    # trim boundaries
    if not include_start:
        timedelta = datetime.timedelta(**{(boundary_unit + 's'): 1})
        from_datetime = from_datetime + timedelta
    if not include_end:
        timedelta = datetime.timedelta(**{(boundary_unit + 's'): 1})
        to_datetime = to_datetime - timedelta

    # get timestamps
    start = from_datetime.timestamp()
    end = to_datetime.timestamp()

    return {'start': start, 'end': end}

