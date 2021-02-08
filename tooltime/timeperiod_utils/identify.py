from .. import exceptions
from .. import timestamp_utils


def detect_timeperiod_representation(timeperiod):
    """return str name of Timeperiod representation"""
    if is_timeperiod_map(timeperiod):
        return 'TimeperiodMap'
    elif is_timeperiod_pair(timeperiod):
        return 'TimeperiodPair'
    else:
        raise exceptions.RepresentationDetectionException(
            'could not detect timeperiod representation: ' + str(timeperiod)
        )


def is_timeperiod(timeperiod):
    """return bool of whether input is Timeperiod"""
    try:
        detect_timeperiod_representation(timeperiod)
        return True
    except Exception:
        return False


def is_timeperiod_map(timeperiod):
    """return bool of whether input is TimeperiodMap"""
    return (
        isinstance(timeperiod, dict)
        and len(timeperiod) == 2
        and 'start' in timeperiod
        and 'end' in timeperiod
        and timestamp_utils.is_timestamp(timeperiod['start'])
        and timestamp_utils.is_timestamp(timeperiod['end'])
    )


def is_timeperiod_pair(timeperiod):
    """return bool of whether input is TimeperiodPair"""
    return (
        isinstance(timeperiod, list)
        and len(timeperiod) == 2
        and timestamp_utils.is_timestamp(timeperiod[0])
        and timestamp_utils.is_timestamp(timeperiod[1])
    )

