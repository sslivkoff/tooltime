
# tooltime
`tooltime` makes it simple to represent and manipulate many different representations of time

`tooltime` operates on 4 abstract time datatypes:
|                 | meaning                          | example                       |
| --              | --                               | --                            |
| `Timestamp`     | a moment in time                 |  today at 3:03 PM             |
| `Timelength`    | a length of time                 | four minutes                  |
| `Timeperiod`    | a period with a start and an end | from 3:03 PM to 3:07 PM today |
| `Timefrequency` | a rate                           | every four minutes            |

Each datatype has multiple interconvertible representations using native python types

## Install
`pip install tooltime`

## Contents
- [Example Usage](#example-usage)
- [Datatype Representations](#datatype-representations)
- [Function Reference](#function-reference)
- [Frequently Asked Questions](#frequently-asked-questions)

## Example Usage

#### Convert Timelength Representations
```python
import tooltime

tooltime.timelength_to_seconds('10m')
> 600
tooltime.timelength_to_label(600)
> '10m'
tooltime.timelength_to_clock('10m')
> '0:10:00'
tooltime.timelength_to_phrase('10m')
> '10 minutes'

(
    tooltime.timelength_to_seconds(600)
    == tooltime.timelength_to_seconds('10m')
    == tooltime.timelength_to_seconds('0:10:00')
    == tooltime.timelength_to_seconds('10 minutes')
)
> True
```

#### Introspect Time Data
```python

# load data
timestamps = load_data(...)

# summarize sequence
tooltime.print_timestamp_summary(timestamps)
```
```
n_t: 216
n_unique: 216
extent:
    start: 20210117_201840Z (1610914720.757)
    end:   20210118_235708Z (1611014228.542)
    duration: 1 days, 3:38:27.785000 (99507.785000086 s)
resolution:
    median_dt: 4m
    mean_dt: 462s
    missing timestamps: 200 (if median_dt maintained)
    outlier_dts: 20
        small: 8        dt < median_dt / (1 + outlier_rtol)
        large: 12        dt > median_dt * (1 + outlier_rtol)
        (outlier_rtol = 0.5)
```

#### Create Standardized Timeperiods
Create timeperiods whose boundaries are integer multiples of some `block_unit`. These useful for placing erratically distributed timestamps into regular bins

```python

timestamp = 1600000000
block_size = 3
print('timestamp:', tooltime.timestamp_to_label(timestamp))
print()
print('standardized timeperiods containing timestamp:')
for block_unit in ['day', 'hour', 'minute']:
    timeperiod = tooltime.get_standard_timeperiod(
        timestamp=timestamp,
        block_size=block_size,
        block_unit=block_unit,
    )    
    block_str = str(block_size) + ' ' + block_unit
    timeperiod_str = tooltime.timeperiod_to_str(timeperiod)
    print('   %8s' % block_str + ':', timeperiod_str)
```
```
timestamp: 20200913_122640Z

standardized timeperiods containing timestamp:
      3 day: [20200913_000000Z, 20200915_235959Z]
     3 hour: [20200913_120000Z, 20200913_145959Z]
   3 minute: [20200913_122400Z, 20200913_122659Z]
```

## Datatype Representations

each of the 4 time datatypes has multiple interconvertible representations, and each representation is assembled from native python types:

##### `Timestamp` Representations
|                            | python type                        | example                   |
| --                         | --                                 | --                        |
| `TimestampSeconds`         | `int` seconds since UTC epoch      | `1600000000`              |
| `TimestampSecondsPrecise`  | `float` seconds since UTC epoch    | `1600000000.0`            |
| `TimestampLabel`           | `str` in format `'%Y%m%d_%H%M%SZ'` | `'20200913_122640Z'`      |
| `TimestampISO`             | `str` in ISO 8601 format           | `'2020-09-13T12:26:40Z'`  |
| `TimestampDatetime`        | `datetime.datetime` object         | `datetime.datetime.now()` |

##### `Timelength` Representations
|                            | python type                                                              | example |
| --                         | --                                                                       | -- |
| `TimelengthSeconds`        | `int` seconds                                                            | `310` |
| `TimelengthSecondsPrecise` | `float` seconds                                                          | `310.0` |
| `TimelengthLabel`          | `str` of `'{number}{time_unit}'`                                         | `'310s'` |
| `TimelengthClock`          | `str` of `'{hours}:{minutes}:{seconds}'`                                 | `'0:05:10'` |
| `TimelengthPhrase`         | `str` of comma-separated list of English amounts                         | `'5 minutes, 10 seconds'` |
| `TimelengthClockPhrase`    | `str` of `TimelengthPhrase` modulo 1 day, remainder in `TimelengthClock` | `'3 days, 0:05:10'` |
| `TimelengthTimedelta`      | `datetime.timedelta` object                                              | `datetime.timedelta(3, 310)` |

valid time units are `'s'`, `'m'`, `'h'`, `'d'`, `'w'`, `'M'`, and `'y'`, indicating seconds, minutes, hours, days, weeks, months, and years

##### `Timeperiod` Representations
|                  | python type                                                 | example                                    |
| --               | --                                                          | --                                         |
| `TimeperiodMap`  | `dict` in form `{'start': 'Timestamp', 'end': 'Timestamp'}` | `{'start': 1600000000, 'end': 1600000001}` |
| `TimeperiodPair` | `list` in form `[start, end]`                               | `[1600000000, 1600000001]`                 |

##### `Timefrequency` Representations
|                          | python type                                                       | example |
| --                       | --                                                                | -- |
| `TimefrequencyFrequency` | `int` or `float` of cycles per second                             | `5.0` |
| `TimefrequencyCountPer`  | `dict` in form `{'count': ['int', 'float'], 'per': 'Timelength'}` | `{'count': 5, 'per': '1s'}` |
| `TimefrequencyInterval`  | `dict` in form `{'interval': 'Timelength'}`                       | `{'interval': 0.2}` |

## Function Reference
- all functions can be accessed using syntax `tooltime.<function_name>(...)`
- `tooltime` contains many functions, but most derive from one of the following patterns:

| operation type | template *(functions that are more specific will have better performance)* | description |
| -- | -- | -- |
| *identification* | `is_<datatype>()`                                           | return `bool` of whether input is instance of datatype |
| *identification* | `is_<datatype>_<representation>()`                          | return `bool` of whether input is instance of specific datatype representation |
| *identification* | `detect_<datatype>_representation()`                        | return `str` of datatype representation name |
| *creation*       | `create_<datatype>()`                                       | create datatype |
| *creation*       | `create_<datatype>_<representation>()`                      | create datatype with specific representation |
| *conversion*     | `convert_<datatype>()`                                      | convert datattype representation |
| *conversion*     | `convert_<datatype>_to_<representation>()`                  | convert datatype to specific representation |
| *conversion*     | `convert_<datatype>_<representation>_to _<representation>()` | convert datatype with known representation to specific representation |

All functions for each datatype are listed below
- [Identfication Functions](#identification-functions)
- [Creation Functions](#creation-functions)
- [Conversion Functions](#conversion-functions)
- [Specialized Functions](#specialized-functions)

#### Identification Functions
|                                           | example call                                                                   | example output          |
|  --                                       | --                                                                             | --                       |
|  `is_timestamp()`                         | `is_timestamp('hello')`                                                        | `False`             |
|  `is_timestamp_seconds()`                 | `is_timestamp_seconds(610)`                                                    | `True`             |
|  `is_timestamp_label()`                   | `is_timestamp_label(610)`                                                      | `False`     |
|  `is_timestamp_iso()`                     | `is_timestamp_iso( '2020-09-13T12:26:40Z')`                                    | `True` |
|  `is_timestamp_datetime()`                | `is_timestamp_datetime(610)`                                                   | `False` |
|  `detect_timestamp _representation()`     | `detect_timestamp_representation( 610)`                                        | `'TimestampSeconds'` |
|  `is_timelength()`                        | `is_timelength('10m')`                                                         | `True`             |
|  `is_timelength_seconds()`                | `is_timelength_seconds('10m')`                                                 | `False`             |
|  `is_timelength_label()`                  | `is_timelength_label('10m')`                                                   | `True`             |
|  `is_timelength_clock()`                  | `is_timelength_clock('10m)`                                                    | `False`             |
|  `is_timelength_phrase()`                 | `is_timelength_phrase('10 minutes')`                                           | `True`             |
|  `is_timelength_clock_phrase()`           | `is_timelength_clock_phrase('10m')`                                            | `False`             |
|  `is_timelength_timedelta()`              | `is_timelength_timedelta('10 minutes')`                                        | `False`             |
|  `detect_timelength _representation()`    | `detect_timelength_representation( '10m')`                                     | `'TimelengthLabel'`             |
|  `is_timeperiod()`                        | `is_timeperiod({'start': 1600000000, 'end': 1600000001'})`                     | `True`             |
|  `is_timeperiod_map()`                    | `is_timeperiod_map({'start': 1600000000, 'end': 1600000001'})`                | `True`             |
|  `is_timeperiod_pair()`                   | `is_timeperiod_length({'start': 1600000000, 'end': 1600000001'})`             | `False`             |
|  `detect_timeperiod _representation()`    | `detect_timeperiod_representation( {'start': 1600000000, 'end': 1600000001'})` | `'TimeperiodMap'`             |
|  `is_timefrequency()`                     | `is_timefrequency({'interval': 0.2})`                                          | `True`             |
|  `is_timefrequency_frequency()`           | `is_timefrequency_frequency( {'interval': 0.2})`                               | `False` |
|  `is_timefrequency_count_per()`           | `is_timefrequency_count_per( {'interval': 0.2})`                               | `False`             |
|  `is_timefrequency_interval()`            | `is_timefrequency_interval( {'interval': 0.2})`                                | `True`             |
|  `detect_timefrequency _representation()` | `detect_timefrequency _representation({'interval': 0.2})`                     | `'TimefrequencyInterval'`             |

#### Creation Functions
|                               | example call                  | example output           |
| --                            | --                            | --                       |
| `create_timestamp_seconds()`  | `create_timestamp_seconds()`  | `1600000000`             |
| `create_timestamp_label()`    | `create_timestamp_label()`    | `'20200913_122640Z'`     |
| `create_timestamp_iso()`      | `create_timestamp_iso()`      | `'2020-09-13T12:26:40Z'` |
| `create_timestamp_datetime()` | `create_timestamp_datetime()` | `'2020-09-13T12:26:40Z'` |
| `create_timelength()`              | `create_timelength(seconds=310, to_representation= 'TimelengthLabel')` | `'310s'` |
| `create_timelength_seconds()`      | `create_timelength_seconds( seconds=310)` | `310` |
| `create_timelength_seconds_precise()`      | `create_timelength_seconds _precise(seconds=310)` | `310.0` |
| `create_timelength_label()`        | `create_timelength_label( seconds=310)` | `'310s'` |
| `create_timelength_clock()`        | `create_timelength_clock( seconds=310)` | `'0:05:10'` |
| `create_timelength_phrase()`       | `create_timelength_phrase( seconds=310)` | `'5 minutes, 10 seconds'` |
| `create_timelength_clock_phrase()` | `create_timelength_clock_phrase( seconds=310)` | `'0:05:10'` |
| `create_timelength_timedelta()`   | `create_timelength_timedelta( seconds=310)` | `datetime.timedelta(0, 310)` |
| `create_timeperiod()`      | `create_timeperiod( start=1600000000, length=1)`      | `{'start': 1600000000, 'end': 1600000001}` |
| `create_timeperiod_map()`  | `create_timeperiod_map( start=1600000000, length=1)`  | `{'start': 1600000000, 'end': 1600000001}` |
| `create_timeperiod_pair()` | `create_timeperiod_pair( start=1600000000, length=1)` | `[1600000000, 1600000001]`                 |
| `create_timefrequency()`           | `create_timefrequency(count=5, per=1)`            | `5.0` |
| `create_timefrequency_frequency()` | `create_timefrequency_frequency( count=5, per=1)` | `5.0`                    |
| `create_timefrequency_count_per()` | `create_timefrequency_count_per( count=5, per=1)` | `{'count': 5, 'per': 1}` |
| `create_timefrequency_interval()`  | `create_timefrequency_interval( interval=0.2)`    | `{'interval': 0.2}`      |

#### Conversion Functions

##### Timestamp Conversion Functions
|                                | example call                                       | example output |
| --                             | --                                                 | -- |
| `convert_timestamp()`          | `convert_timestamp(1600000000, 'TimestampLabel')`  | `'20200913_122640Z'` |
| `timestamp_to_seconds()`       | `timestamp_to_seconds( '20200913_122640Z')`         | `1600000000` |
| `timestamp_to_label()`         | `timestamp_to_label(1600000000)`                   | `'20200913_122640Z'` |
| `timestamp_to_iso()`           | `timestamp_to_iso(1600000000)`                     | `'2020-09-13T12:26:40Z'` |
| `timestamp_to_datetime()`      | `timestamp_to_datetime(1600000000)`                | `datetime.datetime(2020, 9, 13, 12, 26, 40)` |
| `timestamp_seconds_to_label()` | `timestamp_seconds_to_label( 1600000000)`           | `'20200913_122640Z'` |
| `timestamp_label_to_seconds()` | `timestamp_label_to_seconds( '20200913_122640Z')`   | `1600000000` |
| `timestamp_seconds_to_iso()`   | `timestamp_seconds_to_iso(1600000000)`             | `'2020-09-13T12:26:40Z'` |
| `timestamp_iso_to_seconds()`   | `timestamp_iso_to_seconds( '2020-09-13T12:26:40Z')` | `1600000000` |

##### Timelength Conversion Functions
|                                        | example call | example output |
| --                                     | --                                                       | -- |
| `convert_timelength()`                 | `convert_timelength(1600000000, 'TimestampLabel')`       | `'20200913_122640Z'` |
| `timelength_to_seconds()`              | `timelength_to_seconds(610)`                             | `610` |
| `timelength_to_phrase()`               | `timelength_to_phrase(610)`                              | `'10 minutes, 10 seconds'` |
| `timelength_to_clock()`                | `timelength_to_clock(610)`                               | `'0:10:10'` |
| `timelength_to_clock_phrase()`         | `timelength_to_clock_phrase( 259810)`                     | `'3 days, 0:10:10'` |
| `timelength_seconds_to_label()`        | `timelength_seconds_to_label(600)`                       | `'10m'` |
| `timelength_seconds_to_clock()`        | `timelength_seconds_to_clock(610)`                       | `'0:10:10'` |
| `timelength_seconds_to_phrase()`       | `timelength_seconds_to_phrase(610)`                      | `'10 minutes, 10 seconds'` |
| `timelength_seconds_to_clock_phrase()` | `timelength_seconds_to_clock _phrase(600)`               | `'3 days, 0:05:10'` |
| `timelength_seconds_to_timedelta()`    | `timelength_seconds_to_timedelta( 259810)`               | `datetime.timedelta( 3, 610)` |
| `timelength_label_to_seconds()`        | `timelength_label_to_seconds( '10m')`                     | `600` |
| `timelength_clock_to_seconds()`        | `timelength_clock_to_seconds( '0:10:10')`                | `610` |
| `timelength_phrase_to_seconds()`       | `timelength_phrase_to_seconds('10 minutes')`             | `610` |
| `timelength_clock_phrase_to_seconds()` | `timelength_clock_phrase_to _seconds( '3 days, 0:05:10')` | `259510` |
| `timelength_timedelta_to_seconds()`    | `timelength_timedelta_to_seconds( timedelta)` | `259510` |

##### Timeperiod Conversion Functions
|                                        | example call | example output |
| --                                     | --                                                | -- |
| `convert_timeperiod()`                 | `convert_timeperiod({'start': 1600000000, 'end': 1600000001}, 'TimePeriodStartLength')` | `{'start': 1600000000, 'length': 1}` |
| `convert_timeperiod_to_start_end()` | `convert_timeperiod_to_start_end( {'start': 1600000000, 'end': 1600000001}, 'TimePeriodStartLength')` | `{'start': 1600000000, 'end': 1600000001}` |
| `convert_timeperiod_to_start_length()` | `convert_timeperiod_to_start_length( {'start': 1600000000, 'end': 1600000001}, 'TimePeriodStartLength')` | `{'start': 1600000000, 'length': 1}` |
| `convert_timeperiod_to_end_length()` | `convert_timeperiod_to_end_length( {'start': 1600000000, 'end': 1600000001}, 'TimePeriodStartLength')` | `{'end': 1600000001, 'length': 1}` |

##### Timefrequency Conversion Functions
|                                        | example call | example output |
| --                                     | --                                                | -- |
| `convert_timefrequency()`              | `convert_timefrequency({'count': 5, 'per': '1s'}, 'TimeInterval')` | `{'interval': 0.5}` |
| `convert_timefrequency_to_frequency()` | `convert_timefrequency_to_frequency( {'interval': 0.2})` | `5.0` |
| `convert_timefrequency_to_count_per()` | `convert_timefrequency_to_count_per( {'interval': 0.2})` | `{'count': 5, 'per': '1s'}` |
| `convert_timefrequency_to_interval()`  | `convert_timefrequency_to_interval( {'count': 5, 'per': '1s'})` | `{'interval': 0.2}` |

### Specialized Functions
these are functions that are specific to each datatype
| datatype        | function                          | description |
| --              | --                                | -- |
| `Timestamp`     | `floor_datetime()`                | return floor of `datetime` to specified unit of precision |
| `Timestamp`     | `get_unit_lowest_value()`         | return int of lowest possible for value for a given time unit |
| `Timestamp` iterable | `print_timestamp_summary()`  | print a variety of summary statistics about `Timestamp`s |
| `Timeperiod`    | `timeperiods_overlap()`           | return `bool` of whether `Timeperiod`s have any overlap |
| `Timeperiod`    | `timeperiod_contains()`           | return `bool` of whether `Timeperiod` contains other `Timeperiod` |
| `Timeperiod`    | `create_superset_timeperiod()`    | create `Timeperiod` that contains all input `Timeperiod`s |
| `Timeperiod`    | `create_overlapping_timeperiod()` | create copy of `Timeperiod` with start or end trimmed or extended by relative or absolute amounts |
| `Timeperiod`    | `get_standard_timeperiod()`       | get standardized `Timeperiod` whose boundaries are integer multiples of some block_unit |
| `Timefrequency` | `detect_resolution()`             | detect resolution of iterable of `Timestamp` |

## Frequently Asked Questions

#### How are timezones handled?

All `Timestamp` representations except `TimestampDatetime` are linked to specific timezone, which in most cases is GMT (UTC). Counts of seconds since epoch (as in `TimestampSeconds` and `TimestampSecondsPrecise`) are conventionally always GMT (UTC). `TimestampLabel` and `TimestampISO` use a [military time zone abbreviation](https://en.wikipedia.org/wiki/List_of_military_time_zones) as their last characters. The `datetime` object of `TimestampDatetime` internally represents a count of seconds since epoch, but `datetime` objects can have implicit or explicit timezones depending on how they are instantiated.

#### Why not just use `datetime`?

- `datetime` does not handle timezones in a simple or explicit way.
- `datetime` does not make it easy to ingest, output, or convert representations of time using primitive python types.
- `tooltime` contains different convenience functions than `datetime` that are better suited for different workloads.

#### What do the T and Z mean in an ISO 8601 timestamp, such as "2020-09-13T12:26:40Z"?

The T character separates the date portion of the timestamp from the time portion. The Z character indicates the GMT (UTC) timezone. Each timezone has its own letter. Read more [here](https://en.wikipedia.org/wiki/List_of_military_time_zones).
