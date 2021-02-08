import datetime

from .. import exceptions
from . import units


def detect_timelength_representation(timelength):
    """return str name of Timelength representation"""
    if is_timelength_seconds(timelength):
        return 'TimelengthSeconds'
    elif is_timelength_seconds_precise(timelength):
        return 'TimelengthSecondsPrecise'
    elif is_timelength_label(timelength):
        return 'TimelengthLabel'
    elif is_timelength_clock(timelength):
        return 'TimelengthClock'
    elif is_timelength_phrase(timelength):
        return 'TimelengthPhrase'
    elif is_timelength_clock_phrase(timelength):
        return 'TimelengthClockPhrase'
    elif is_timelength_timedelta(timelength):
        return 'TimelengthTimedelta'
    else:
        raise exceptions.RepresentationDetectionException(
            'could not determine Timelength representation: ' + str(timelength)
        )


def is_timelength(timelength):
    """return bool of whether input is Timelength"""
    try:
        detect_timelength_representation(timelength)
        return True
    except exceptions.RepresentationDetectionException:
        return False


def is_timelength_seconds(timelength):
    """return bool of whether input is TimelengthSeconds"""
    return isinstance(timelength, int)


def is_timelength_seconds_precise(timelength):
    """return bool of whether input is TimelengthSecondsPrecise"""
    return isinstance(timelength, float)


def is_timelength_label(timelength):
    """return bool of whether input is TimelengthLabel"""

    if not isinstance(timelength, str) or len(timelength) < 2:
        return False

    try:
        int(timelength[:-1])
        letter = timelength[-1]
        return letter.isalnum()

    except ValueError:
        return False


def is_timelength_clock(timelength):
    """return bool of whether input is TimelengthClock"""

    if not isinstance(timelength, str):
        return False
    numbers = timelength.split(':')
    try:
        for number in numbers[:-1]:
            int(number)
        float(numbers[-1])
        return True
    except ValueError:
        return False


def is_timelength_phrase(timelength):
    """return bool of whether input is TimelengthPhrase"""

    if not isinstance(timelength, str):
        return False
    unit_names_to_labels = units.get_unit_labels()
    pieces = timelength.split(', ')
    try:
        for piece in pieces:
            amount, unit_name = piece.split(' ')
            float(amount)
            if unit_name not in unit_names_to_labels:
                return False
        return True
    except Exception:
        return False


def is_timelength_clock_phrase(timelength):
    """return bool of whether input is TimelengthClockPhrase"""

    if not isinstance(timelength, str):
        return False
    pieces = timelength.split(', ')

    if ':' in pieces[-1]:
        clock = pieces[-1]
        if not is_timelength_clock(clock):
            return False
        phrase = ', '.join(pieces[:-1])
    else:
        phrase = ', '.join(pieces)

    return is_timelength_phrase(phrase)


def is_timelength_timedelta(timelength):
    """return bool of whether input is TimelengthTimedelta"""
    return isinstance(timelength, datetime.timedelta)

