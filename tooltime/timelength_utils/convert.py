import datetime
import math

from . import units
from . import identify


#
# # general conversions
#


def convert_timelength(timelength, to_representation, from_representation=None):
    """convert Timelength to a new representation

    ## Inputs
    - timelength: Timelength
    - to_representation: str of Timelength representation of input timelength
    - from_representation: str of target Timelength representation

    ## Returns
    - Timelength in specified representation
    """

    # detect timelength type
    if from_representation is None:
        from_representation = identify.detect_timelength_representation(
            timelength
        )

    # return if already in target type
    if from_representation == to_representation:
        return timelength

    # convert to seconds
    if from_representation == 'TimelengthSeconds':
        timelength_seconds = timelength
    elif from_representation == 'TimelengthSecondsPrecise':
        timelength_seconds = timelength
    elif from_representation == 'TimelengthLabel':
        timelength_seconds = timelength_label_to_seconds(timelength)
    elif from_representation == 'TimelengthClock':
        timelength_seconds = timelength_clock_to_seconds(timelength)
    elif from_representation == 'TimelengthPhrase':
        timelength_seconds = timelength_phrase_to_seconds(timelength)
    elif from_representation == 'TimelengthClockPhrase':
        timelength_seconds = timelength_clock_phrase_to_seconds(timelength)
    elif from_representation == 'TimelengthTimedelta':
        timelength_seconds = timelength_timedelta_to_seconds(timelength)
    else:
        raise Exception(
            'unknown timelength_representation: ' + str(from_representation)
        )

    # convert to target type
    if to_representation == 'TimelengthSeconds':
        to_timelength = int(timelength_seconds)
    elif to_representation == 'TimelengthSecondsPrecise':
        to_timelength = float(timelength_seconds)
    elif to_representation == 'TimelengthLabel':
        to_timelength = timelength_seconds_to_label(timelength_seconds)
    elif to_representation == 'TimelengthClock':
        to_timelength = timelength_seconds_to_clock(timelength_seconds)
    elif to_representation == 'TimelengthPhrase':
        to_timelength = timelength_seconds_to_phrase(timelength_seconds)
    elif to_representation == 'TimelengthClockPhrase':
        to_timelength = timelength_seconds_to_clock_phrase(timelength_seconds)
    elif to_representation == 'TimelengthTimedelta':
        to_timelength = timelength_seconds_to_timedelta(timelength_seconds)
    else:
        raise Exception(
            'unknown timelength_representation: ' + str(to_representation)
        )

    return to_timelength


#
# # functions with target representation specified
#


def timelength_to_seconds(timelength, from_representation=None):
    """convert Timelength to TimelengthSeconds

    ## Inputs
    - timelength: Timelength
    - from_representation: str representation name of input timelength

    ## Returns
    - TimelengthSeconds timelength
    """
    return convert_timelength(
        timelength=timelength,
        to_representation='TimelengthSeconds',
        from_representation=from_representation,
    )


def timelength_to_seconds_precise(timelength, from_representation=None):
    """convert Timelength to TimelengthSecondsPrecise

    ## Inputs
    - timelength: Timelength
    - from_representation: str representation name of input timelength

    ## Returns
    - TimelengthSecondsPrecise timelength
    """
    return convert_timelength(
        timelength=timelength,
        to_representation='TimelengthSecondsPrecise',
        from_representation=from_representation,
    )


def timelength_to_label(timelength, from_representation=None):
    """convert Timelength to TimelengthLabel

    ## Inputs
    - timelength: Timelength
    - from_representation: str representation name of input timelength

    ## Returns
    - TimelengthLabel timelength
    """
    return convert_timelength(
        timelength=timelength,
        to_representation='TimelengthLabel',
        from_representation=from_representation,
    )


def timelength_to_phrase(timelength, from_representation=None):
    """convert Timelength to TimelengthPhrase

    ## Inputs
    - timelength: Timelength
    - from_representation: str representation name of input timelength

    ## Returns
    - TimelengthPhrase timelength
    """
    return convert_timelength(
        timelength=timelength,
        to_representation='TimelengthPhrase',
        from_representation=from_representation,
    )


def timelength_to_clock(timelength, from_representation=None):
    """convert Timelength to TimelengthClock

    ## Inputs
    - timelength: Timelength
    - from_representation: str representation name of input timelength

    ## Returns
    - TimelengthClock timelength
    """
    return convert_timelength(
        timelength=timelength,
        to_representation='TimelengthClock',
        from_representation=from_representation,
    )


def timelength_to_clock_phrase(timelength, from_representation=None):
    """convert Timelength to TimelengthClockPhrase

    ## Inputs
    - timelength: Timelength
    - from_representation: str representation name of input timelength

    ## Returns
    - TimelengthClockPhrase timelength
    """
    return convert_timelength(
        timelength=timelength,
        to_representation='TimelengthClockPhrase',
        from_representation=from_representation,
    )


#
# # specific conversion functions, from seconds
#


def timelength_seconds_to_label(
    timelength_seconds, base_only=False, fuzzy_tolerance=None, base_unit=None
):
    """convert seconds to TimelengthLabel

    - matches integer multiples of base units
        - see get_base_units() for base units

    ## Inputs
    - seconds: int or float number of seconds
    - base_only: bool of whether to match only to base units
    - fuzzy_tolerance: float of how close seconds much be to a mathcing label
        - 0.1 -> '1m' would match any seconds in range [54, 66]
        - 0.1 -> '5m' would match any seconds in range [270, 330]
    - base_unit: str of base unit
    """

    seconds = timelength_seconds
    if type(seconds).__name__ in ['float', 'float64', 'float32', 'float16']:
        int_seconds = int(seconds)
        if math.isclose(int_seconds, seconds):
            seconds = int_seconds

        elif int_seconds > 5.0:
            seconds = int_seconds

    # collect possible base units
    base_units = units.get_base_units()
    if base_unit is not None:
        if base_unit not in base_units:
            raise Exception('invalid base unit: ' + str(base_unit))
        candidates = {base_unit: base_units[base_unit]}
    else:
        candidates = base_units

    # attempt matches to candidate base units in descending order
    descending = sorted(candidates.items(), key=lambda item: -item[-1])
    for base_label, base_seconds in descending:

        # attempt match to base unit
        if base_only:
            if math.isclose(seconds, base_seconds):
                return base_label
            else:
                continue

        # attempt exact match of base unit multiple
        quotient = seconds / base_seconds
        quotient_as_int = round(quotient)
        if math.isclose(quotient, quotient_as_int):
            unit_count = quotient_as_int
            unit_letter = base_label[-1]
            break

        # attempt fuzzy match of base unit multiple
        if fuzzy_tolerance is not None:
            round_quotient = round(quotient)
            upper_bound = (1 + fuzzy_tolerance) * round_quotient * base_seconds
            lower_bound = (1 - fuzzy_tolerance) * round_quotient * base_seconds
            if lower_bound <= seconds and seconds <= upper_bound:
                unit_count = round_quotient
                unit_letter = base_label[-1]
                break
    else:
        raise Exception('could not seconds convert to label')

    # create label
    label = str(unit_count) + unit_letter

    return label


def timelength_seconds_to_clock(timelength_seconds):
    """convert seconds to TimelengthClock"""
    base_units = units.get_base_units()
    n_days = math.floor(timelength_seconds / base_units['1d'])
    n_seconds_remaining = timelength_seconds % base_units['1d']
    clock = str(datetime.timedelta(seconds=n_seconds_remaining))
    if n_days > 0:
        clock = str(n_days) + ':' + clock
    return clock


def timelength_seconds_to_phrase(timelength_seconds):
    """convert seconds to TimelengthPhrase"""

    unit_names = [
        'years',
        'days',
        'hours',
        'minutes',
        'seconds',
    ]

    # compute count for each unit
    remaining = timelength_seconds
    base_units = units.get_base_units()
    unit_names_to_labels = units.get_unit_labels()
    unit_counts = []
    for unit_name in unit_names:
        unit_seconds = base_units[unit_names_to_labels[unit_name]]
        unit_count = math.floor(remaining / unit_seconds)
        unit_counts.append(unit_count)
        remaining = remaining % unit_seconds
    if not math.isclose(remaining, 0):
        unit_counts[-1] += remaining

    # assemble pieces from unit counts
    pieces = []
    for unit_count, unit_name in zip(unit_counts, unit_names):
        if unit_count > 0:
            piece = str(unit_count) + ' ' + unit_name
            pieces.append(piece)

    # assemble pieces into phrase
    if len(pieces) == 0:
        phrase = '0 ' + unit_names[-1]
    else:
        phrase = ', '.join(pieces)

    return phrase


def timelength_seconds_to_clock_phrase(timelength_seconds):
    """convert seconds to TimelengthClockPhrase"""

    base_units = units.get_base_units()
    n_years = math.floor(timelength_seconds / base_units['1y'])
    n_years_remainder = timelength_seconds % base_units['1y']
    n_days = math.floor(n_years_remainder / base_units['1d'])
    n_days_remainder = n_years_remainder % base_units['1d']

    phrase_pieces = []
    if n_years > 0:
        phrase_pieces.append(str(n_years) + ' years')
    if n_days > 0:
        phrase_pieces.append(str(n_days) + ' days')
    if n_days_remainder > 0:
        if type(n_days_remainder).__name__ == 'int64':
            n_days_remainder = int(n_days_remainder)
        phrase_pieces.append(str(datetime.timedelta(seconds=n_days_remainder)))

    phrase = ', '.join(phrase_pieces)

    return phrase


def timelength_seconds_to_timedelta(timelength_seconds):
    """convert seconds to TimelengthTimedelta"""
    return datetime.timedelta(seconds=timelength_seconds)


#
# # to seconds
#


def timelength_label_to_seconds(timelength_label):
    """convert TimelengthLabel to seconds"""
    number = int(timelength_label[:-1])
    letter = timelength_label[-1]
    base_units = units.get_base_units()
    base_seconds = base_units['1' + letter]
    seconds = number * base_seconds
    return seconds


def timelength_clock_to_seconds(timelength_clock):
    """convert TimelengthClock to seconds"""

    pieces = timelength_clock.split(':')
    piece_numbers = [float(piece) for piece in pieces]
    if len(pieces) == 3:
        days = 0
        hours = piece_numbers[0]
        minutes = piece_numbers[1]
        seconds = piece_numbers[2]
    elif len(pieces) == 4:
        days = piece_numbers[0]
        hours = piece_numbers[1]
        minutes = piece_numbers[2]
        seconds = piece_numbers[3]
    else:
        raise Exception('unknown timelength clock format')

    base_units = units.get_base_units()
    return (
        base_units['1d'] * days
        + base_units['1h'] * hours
        + base_units['1m'] * minutes
        + base_units['1s'] * seconds
    )


def timelength_phrase_to_seconds(timelength_phrase):
    """convert TimelengthPhrase to seconds"""

    bases = units.get_base_units()
    unit_names_to_labels = units.get_unit_labels()
    phrase_pieces = timelength_phrase.split(', ')

    seconds = 0
    for piece in phrase_pieces:
        unit_count, unit_name = piece.split(' ')
        unit_count = float(unit_count)
        seconds += unit_count * bases[unit_names_to_labels[unit_name]]

    return seconds


def timelength_clock_phrase_to_seconds(timelength_clock_phrase):
    """convert TimelengthClockPhrase to seconds"""

    pieces = timelength_clock_phrase.split(', ')
    phrase = ', '.join(pieces[:-1])
    if phrase != '':
        phrase_seconds = timelength_phrase_to_seconds(phrase)
    else:
        phrase_seconds = 0
    clock_seconds = timelength_clock_to_seconds(pieces[-1])
    return phrase_seconds + clock_seconds


def timelength_timedelta_to_seconds(timelength_timedelta):
    """convert TimelengthTimedelta to seconds"""
    return timelength_timedelta.total_seconds()

