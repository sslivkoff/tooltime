import datetime
import typing


TimestampSecondsRaw = typing.SupportsFloat
TimestampSeconds = int
TimestampSecondsPrecise = float
TimestampLabel = str
TimestampISO = str
TimestampDatetime = datetime.datetime
Timestamp = typing.Union[
    TimestampSeconds,
    TimestampSecondsPrecise,
    TimestampLabel,
    TimestampISO,
    TimestampDatetime,
]
TimestampRepresentation = typing.Literal[
    'TimestampSeconds',
    'TimestampSecondsPrecise',
    'TimestampLabel',
    'TimestampISO',
    'TimestampDatetime',
]

TimestampSummary = dict[str, typing.Any]

TimelengthSeconds = int
TimelengthSecondsPrecise = float
TimelengthLabel = str
TimelengthClock = str
TimelengthPhrase = str
TimelengthClockPhrase = str
TimelengthTimedelta = datetime.timedelta
Timelength = typing.Union[
    TimelengthSeconds,
    TimelengthSecondsPrecise,
    TimelengthLabel,
    TimelengthClock,
    TimelengthPhrase,
    TimelengthClockPhrase,
    TimelengthTimedelta,
]


class TimeperiodMap(typing.TypedDict):
    start: Timestamp
    end: Timestamp


TimeperiodPair = tuple[Timestamp, Timestamp]
Timeperiod = typing.Union[TimeperiodMap, TimeperiodPair]

TimefreqeuncyFrequency = typing.Union[int, float]


class TimefrequencyCountPer(typing.TypedDict):
    count: typing.Union[int, float]
    per: Timestamp


class TimefrequencyInterval(typing.TypedDict):
    interval: Timestamp


Timefrequency = typing.Union[
    TimefreqeuncyFrequency,
    TimefrequencyCountPer,
    TimefrequencyInterval,
]

#
# # datetime
#

DatetimeUnit = typing.Literal[
    'year',
    'month',
    'day',
    'hour',
    'minute',
    'second',
    'microsecond',
]


#
# # old
#

contenttypes = {
    # Timestamp
    'Timestamp': [
        'TimestampSeconds',
        'TimestampSecondsPrecise',
        'TimestampLabel',
        'TimestampISO',
        'TimestampDatetime',
    ],
    'TimestampSeconds': 'Integer',
    'TimestampSecondsPrecise': 'Float',
    'TimestampLabel': 'Text',
    'TimestampISO': 'Text',
    'TimestampDatetime': 'Datetime',
    # Timelength
    'Timelength': [
        'TimelengthSeconds',
        'TimelengthSecondsPrecise',
        'TimelengthLabel',
        'TimelengthClock',
        'TimelengthPhrase',
        'TimelengthClockPhrase',
        'TimelengthTimedelta',
    ],
    'TimelengthSeconds': 'Integer',
    'TimelengthSecondsPrecise': 'Float',
    'TimelengthLabel': 'Text',
    'TimelengthClock': 'Text',
    'TimelengthPhrase': 'Text',
    'TimelengthClockPhrase': 'Text',
    'TimelengthTimedelta': 'Timedelta',
    # Timeperiod
    'Timeperiod': ['TimeperiodMap', 'TimeperiodPair'],
    'TimeperiodMap': {'start': 'Timestamp', 'end': 'Timestamp'},
    'TimeperiodPair': ['Timestamp', 'Timestamp'],
    # Timefrequency
    'Timefrequency': [
        'TimefrequencyFrequency',
        'TimefrequencyCountPer',
        'TimefrequencyInterval',
    ],
    'TimeFrequencyFrequency': 'Number',
    'TimeFrequencyCount': {'count': 'Number', 'per': 'Timelength'},
    'TimeFrequencyInterval': {'interval': 'Timelength'},
}


equivalent_sets = {
    'Timestamp': [
        {
            'TimestampSeconds': 1600000000,
            'TimestampSecondsPrecise': 1600000000.0,
            'TimestampLabel': '20200913_122640Z',
            'TimestampISO': '2020-09-13T12:26:40Z',
            'TimestampDatetime': datetime.datetime(
                second=40,
                minute=26,
                hour=12,
                day=13,
                month=9,
                year=2020,
                tzinfo=datetime.timezone.utc,
            ),
        },
    ],
    'Timelength': [
        {
            'TimelengthSeconds': 31,
            'TimelengthSecondsPrecise': 31.0,
            'TimelengthLabel': '31s',
            'TimelengthClock': '0:00:31',
            'TimelengthPhrase': '31 seconds',
            'TimelengthClockPhrase': '0:00:31',
            'TimelengthTimedelta': datetime.timedelta(seconds=31),
        },
        {
            'TimelengthSeconds': 86431,
            'TimelengthSecondsPrecise': 86431.0,
            'TimelengthLabel': '86431s',
            'TimelengthClock': '1:0:00:31',
            'TimelengthPhrase': '1 days, 31 seconds',
            'TimelengthClockPhrase': '1 days, 0:00:31',
            'TimelengthTimedelta': datetime.timedelta(days=1, seconds=31),
        },
    ],
    'Timeperiod': [
        {
            'TimeperiodMap': {'start': 1600000000, 'end': 1600000001},
            'TimeperiodPair': [1600000000, 1600000001],
        },
    ],
    'Timefrequency': [
        {
            'TimefrequencyFrequency': 5.0,
            'TimefrequencyCountPer': {'count': 5, 'per': '1s'},
            'TimefrequencyInterval': {'interval': 0.2},
        },
    ],
}

