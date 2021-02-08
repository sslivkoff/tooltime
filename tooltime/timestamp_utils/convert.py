import datetime

from . import identify


time_format = '%Y%m%d_%H%M%SZ'
precise_time_format = time_format[:-1] + '%f' + time_format[-1]


#
# # general conversion
#


def convert_timestamp(timestamp, to_representation, from_representation=None):
    """convert timestamp to a new representation

    ## Inputs
    - timestamp: Timestamp
    - to_representation: str of Timestamp representation of input timestamp
    - from_representation: str of target Timestamp representation

    ## Returns
    - Timestamp in specified representation
    """

    # determine current representation
    if from_representation is None:
        from_representation = identify.detect_timestamp_representation(
            timestamp
        )

    # check if representation is required
    if from_representation == to_representation:
        return timestamp

    # convert to seconds
    if from_representation == 'TimestampSeconds':
        timestamp_seconds = timestamp
    elif from_representation == 'TimestampSecondsPrecise':
        timestamp_seconds = timestamp
    elif from_representation == 'TimestampLabel':
        timestamp_seconds = timestamp_label_to_seconds(timestamp)
    elif from_representation == 'TimestampISO':
        timestamp_seconds = timestamp_iso_to_seconds(timestamp)
    elif from_representation == 'TimestampDatetime':
        timestamp_seconds = timestamp_datetime_to_seconds(timestamp)
    else:
        raise Exception(
            'unknown timestamp representation: ' + str(from_representation)
        )

    # convert to target representation
    if to_representation == 'TimestampSeconds':
        to_timestamp = int(timestamp_seconds)
    elif to_representation == 'TimestampSecondsPrecise':
        to_timestamp = float(timestamp_seconds)
    elif to_representation == 'TimestampLabel':
        to_timestamp = timestamp_seconds_to_label(timestamp_seconds)
    elif to_representation == 'TimestampISO':
        to_timestamp = timestamp_seconds_to_iso(timestamp_seconds)
    elif to_representation == 'TimestampDatetime':
        to_timestamp = timestamp_seconds_to_datetime(timestamp_seconds)
    else:
        raise Exception(
            'unknown timestamp representation: ' + str(to_representation)
        )

    return to_timestamp


#
# # functions with target representation specified
#


def timestamp_to_seconds(timestamp, from_representation=None):
    """convert timestamp to TimestampSeconds

    ## Inputs
    - timestamp: Timestamp
    - from_representation: str representation name of input timestamp

    ## Returns
    - TimestampSeconds timestamp
    """
    return convert_timestamp(
        timestamp,
        to_representation='TimestampSeconds',
        from_representation=from_representation,
    )


def timestamp_to_seconds_precise(timestamp, from_representation=None):
    """convert timestamp to TimestampSecondsPrecise

    ## Inputs
    - timestamp: Timestamp
    - from_representation: str representation name of input timestamp

    ## Returns
    - TimestampSecondsPrecise timestamp
    """
    return convert_timestamp(
        timestamp,
        to_representation='TimestampSecondsPrecise',
        from_representation=from_representation,
    )


def timestamp_to_label(timestamp, from_representation=None):
    """convert timestamp to TimestampLabel

    ## Inputs
    - timestamp: Timestamp
    - from_representation: str representation name of input timestamp

    ## Returns
    - TimestampLabel timestamp
    """
    return convert_timestamp(
        timestamp,
        to_representation='TimestampLabel',
        from_representation=from_representation,
    )


def timestamp_to_iso(timestamp, from_representation=None):
    """convert timestamp to TimestampISO

    ## Inputs
    - timestamp: Timestamp
    - from_representation: str representation name of input timestamp

    ## Returns
    - TimestampISO timestamp
    """
    return convert_timestamp(
        timestamp,
        to_representation='TimestampISO',
        from_representation=from_representation,
    )


def timestamp_to_datetime(timestamp, from_representation=None):
    """convert timestamp to TimestampDatetime

    ## Inputs
    - timestamp: Timestamp
    - from_representation: str representation name of input timestamp

    ## Returns
    - TimestampDatetime timestamp
    """
    return convert_timestamp(
        timestamp,
        to_representation='TimestampDatetime',
        from_representation=from_representation,
    )


#
# # specific conversion functions, from seconds
#


def timestamp_seconds_to_label(timestamp_seconds):
    """convert seconds to TimestampLabel"""
    dt = datetime.datetime.fromtimestamp(
        timestamp_seconds, datetime.timezone.utc
    )
    human_timestamp = dt.strftime(time_format)
    return human_timestamp


def timestamp_seconds_to_iso(timestamp_seconds):
    """convert seconds to TimestampISO"""
    dt = datetime.datetime.fromtimestamp(
        timestamp_seconds, datetime.timezone.utc
    )
    iso_format = "%Y-%m-%dT%H:%M:%SZ"
    iso = dt.strftime(iso_format)
    return iso


def timestamp_seconds_to_datetime(timestamp_seconds):
    """convert seconds to TimestampDatetime"""
    return datetime.datetime.fromtimestamp(
        timestamp_seconds, datetime.timezone.utc
    )


#
# # specific conversion functions, to seconds
#


def timestamp_label_to_seconds(timestamp_label):
    """convert TimestampLabel to seconds"""

    timestamp = timestamp_label

    if timestamp_label[-1] != 'Z' or len(timestamp_label) != 16:
        raise Exception('timestamp label not in format ' + str(time_format))

    dt = datetime.datetime(
        year=int(timestamp[:4]),
        month=int(timestamp[4:6]),
        day=int(timestamp[6:8]),
        hour=int(timestamp[9:11]),
        minute=int(timestamp[11:13]),
        second=int(timestamp[13:15]),
        tzinfo=datetime.timezone.utc,
    )
    timestamp = dt.timestamp()
    return timestamp


def timestamp_iso_to_seconds(timestamp_iso):
    """convert TimestampISO to seconds"""

    if '.' in timestamp_iso:
        iso_format = "%Y-%m-%dT%H:%M:%S.%fZ"
    else:
        iso_format = "%Y-%m-%dT%H:%M:%SZ"

    local_dt = datetime.datetime.strptime(timestamp_iso, iso_format)
    utc_dt = local_dt.replace(tzinfo=datetime.timezone.utc)
    seconds = utc_dt.timestamp()

    return seconds


def timestamp_datetime_to_seconds(timestamp_datetime):
    """convert TimestampDatetime to seconds"""
    return timestamp_datetime.timestamp()

