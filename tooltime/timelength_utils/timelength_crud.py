from . import timelength_convert


def create_timelength(seconds, to_representation=None):
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


def create_timelength_seconds(seconds):
    """create Timelength with representation TimelengthSeconds"""
    return int(seconds)


def create_timelength_seconds_precise(seconds):
    """create Timelength with representation TimelengthPrecise"""
    return float(seconds)


def create_timelength_label(seconds):
    """create Timelength with representation TimelengthLabel"""
    return timelength_convert.timelength_seconds_to_label(seconds)


def create_timelength_phrase(seconds):
    """create Timelength with representation TimelengthPhrase"""
    return timelength_convert.timelength_seconds_to_phrase(seconds)


def create_timelength_clock(seconds):
    """create Timelength with representation TimelengthClock"""
    return timelength_convert.timelength_seconds_to_clock(seconds)


def create_timelength_clock_phrase(seconds):
    """create Timelength with representation TimelengthClockPhrase"""
    return timelength_convert.timelength_seconds_to_clock_phrase(seconds)


def create_timelength_timedelta(seconds):
    """create Timelength with representation TimelengthTimedelta"""
    return timelength_convert.timelength_seconds_to_timedelta(seconds)

