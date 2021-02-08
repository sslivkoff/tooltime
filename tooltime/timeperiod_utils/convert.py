from . import identify


def convert_timeperiod(timeperiod, to_representation, from_representation=None):
    """convert Timeperiod to a new representation

    ## Inputs
    - timeperiod: Timeperiod
    - to_representation: str of Timeperiod representation of input timeperiod
    - from_representation: str of target Timeperiod representation

    ## Returns
    - Timeperiod in specified representation
    """

    # determine current representation
    if from_representation is None:
        from_representation = identify.detect_timeperiod_representation(
            timeperiod
        )

    # check whether conversion is required
    if to_representation == from_representation:
        return timeperiod

    # perform conversion
    if to_representation == 'TimeperiodPair':
        return timeperiod_to_pair(
            timeperiod, from_representation=from_representation
        )
    elif to_representation == 'TimeperiodMap':
        return timeperiod_to_map(
            timeperiod, from_representation=from_representation
        )
    else:
        raise Exception(
            'unknown timeperiod representation: ' + str(to_representation)
        )


def timeperiod_to_pair(timeperiod, from_representation=None):
    """convert Timeperiod to TimeperiodPair

    ## Inputs
    - timeperiod: Timeperiod
    - from_representation: str representation name of input timeperiod

    ## Returns
    - TimeperiodPair
    """

    if from_representation is None:
        from_representation = identify.detect_timeperiod_representation(
            timeperiod
        )

    if from_representation == 'TimeperiodMap':
        start, end = timeperiod
        return [timeperiod['start'], timeperiod['end']]
    elif from_representation == 'TimeperiodPair':
        return timeperiod
    else:
        raise Exception(
            'unknown Timeperiod representation: ' + str(from_representation)
        )


def timeperiod_to_map(timeperiod, from_representation=None):
    """convert Timeperiod to TimeperiodMap

    ## Inputs
    - timeperiod: Timeperiod
    - from_representation: str representation name of input timeperiod

    ## Returns
    - TimeperiodMap
    """
    if from_representation is None:
        from_representation = identify.detect_timeperiod_representation(
            timeperiod,
        )

    if from_representation == 'TimeperiodPair':
        start, end = timeperiod
        return {'start': start, 'end': end}
    elif from_representation == 'TimeperiodMap':
        return timeperiod
    else:
        raise Exception(
            'unknown Timeperiod representation: ' + str(from_representation)
        )

