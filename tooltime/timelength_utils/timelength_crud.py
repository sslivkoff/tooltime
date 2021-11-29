from .. import spec
from . import timelength_convert


def create_timelength(
    seconds: spec.TimelengthSecondsRaw,
    to_representation: spec.TimelengthRepresentation = None,
) -> spec.Timelength:
    """create Timelength

    ## Inputs
    - seconds: int or float seconds
    - to_reprsentation: str name of Timelength representation

    ## Returns
    - Timelength with specified representation
    """

    if to_representation is None:
        to_representation = 'TimelengthSeconds'

    if to_representation == 'TimelengthSeconds':
        return create_timelength_seconds(seconds)
    elif to_representation == 'TimelengthSecondsPrecise':
        return create_timelength_seconds_precise(seconds)
    elif to_representation == 'TimelengthLabel':
        return create_timelength_label(seconds)
    elif to_representation == 'TimelengthPhrase':
        return create_timelength_phrase(seconds)
    elif to_representation == 'TimelengthClock':
        return create_timelength_clock(seconds)
    elif to_representation == 'TimelengthClockPhrase':
        return create_timelength_clock_phrase(seconds)
    elif to_representation == 'TimelengthTimedelta':
        return create_timelength_timedelta(seconds)
    else:
        raise Exception(
            'unknown timelength representation: ' + str(to_representation)
        )


def create_timelength_seconds(
    seconds: spec.TimelengthSecondsRaw,
) -> spec.TimelengthSeconds:
    """create Timelength with representation TimelengthSeconds"""
    return int(seconds)


def create_timelength_seconds_precise(
    seconds: spec.TimelengthSecondsRaw,
) -> spec.TimelengthSecondsPrecise:
    """create Timelength with representation TimelengthPrecise"""
    return float(seconds)


def create_timelength_label(
    seconds: spec.TimelengthSecondsRaw,
) -> spec.TimelengthLabel:
    """create Timelength with representation TimelengthLabel"""
    return timelength_convert.timelength_seconds_to_label(seconds)


def create_timelength_phrase(
    seconds: spec.TimelengthSecondsRaw,
) -> spec.TimelengthPhrase:
    """create Timelength with representation TimelengthPhrase"""
    return timelength_convert.timelength_seconds_to_phrase(seconds)


def create_timelength_clock(
    seconds: spec.TimelengthSecondsRaw,
) -> spec.TimelengthClock:
    """create Timelength with representation TimelengthClock"""
    return timelength_convert.timelength_seconds_to_clock(seconds)


def create_timelength_clock_phrase(
    seconds: spec.TimelengthSecondsRaw,
) -> spec.TimelengthClockPhrase:
    """create Timelength with representation TimelengthClockPhrase"""
    return timelength_convert.timelength_seconds_to_clock_phrase(seconds)


def create_timelength_timedelta(
    seconds: spec.TimelengthSecondsRaw,
) -> spec.TimelengthTimedelta:
    """create Timelength with representation TimelengthTimedelta"""
    return timelength_convert.timelength_seconds_to_timedelta(seconds)

