from .. import timestamp_utils
from .. import timelength_utils
from . import identify


def create_timeperiod(
    start=None, end=None, length=None, to_representation=None
):
    """create Timeperiod

    ## Inputs
    - start: Timestamp
    - end: Timestamp
    - length: Timelength
    - to_reprsentation: str name of Timeperiod representation

    ## Returns
    - Timeperiod with specified representation
    """

    if to_representation is None:
        to_representation = 'TimeperiodMap'

    if to_representation == 'TimeperiodMap':
        return create_timeperiod_map(start=start, end=end, length=length)
    elif to_representation == 'TimeperiodPair':
        return create_timeperiod_pair(start=start, end=end, length=length)
    else:
        raise Exception(
            'unknown timeperiod representation: ' + str(to_representation)
        )


def create_timeperiod_pair(start=None, end=None, length=None):
    """create Timeperiod with representation TimeperiodPair

    ## Inputs
    - start: Timestamp
    - end: Timestamp
    - length: Timelength

    ## Returns
    - TimeperiodPair
    """
    start, end = compute_start_end(start=start, end=end, length=length)
    return [start, end]


def create_timeperiod_map(start=None, end=None, length=None):
    """create Timeperiod with representation TimeperiodMap

    ## Inputs
    - start: Timestamp
    - end: Timestamp
    - length: Timelength

    ## Returns
    - TimeperiodMap
    """
    start, end = compute_start_end(start=start, end=end, length=length)
    return {'start': start, 'end': end}


def compute_start_end(start=None, end=None, length=None):
    """return start and end given two of start, end, and length

    ## Inputs
    - start: Timestamp
    - end: Timestamp
    - length: Timelength

    ## Returns
    - TimeperiodPair
    """
    if [start, end, length].count(None) != 1:
        raise Exception('must specify exactly 2 inputs')

    # convert inputs to seconds
    if start is not None:
        start = timestamp_utils.timestamp_to_seconds(start)
    if end is not None:
        end = timestamp_utils.timestamp_to_seconds(end)
    if length is not None:
        if not isinstance(length, (int, float)):
            length = timelength_utils.timelength_to_seconds_precise(length)

    # compute unknown bounds
    if start is None:
        start = end - length
    if end is None:
        end = start + length

    return [start, end]


def compute_timeperiod_start_end(timeperiod):
    """compute start and end seconds of a timeperiod"""

    representation = identify.detect_timeperiod_representation(timeperiod)
    if representation == 'TimeperiodPair':
        start, end = timeperiod
    elif representation == 'TimeperiodPair':
        start = timeperiod['start']
        end = timeperiod['end']
    else:
        raise Exception('unknown timeperiod representation: ' + str(representation))

    start = timelength_utils.timelength_to_seconds_precise(start)
    end = timelength_utils.timelength_to_seconds_precise(end)

    return [start, end]

