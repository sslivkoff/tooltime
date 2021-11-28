from .. import timelength_utils
from . import timefrequency_identify


def convert_timefrequency(
    timefrequency,
    to_representation,
    from_representation=None,
):
    """convert Timefrequency to a new representation

    ## Inputs
    - timefrequency: Timefrequency
    - to_representation: str of Timefrequency representation of input timefrequency
    - from_representation: str of target Timefrequency representation

    ## Returns
    - Timefrequency in specified representation
    """

    # determine current representation
    if from_representation is None:
        from_representation = (
            timefrequency_identify.detect_timefrequency_representation(
                timefrequency
            )
        )

    # check whether conversion is required
    if to_representation == from_representation:
        return timefrequency

    # perform conversion
    if to_representation == 'TimefrequencyFrequency':
        return timefrequency_to_frequency(
            timefrequency, from_representation=from_representation
        )
    elif to_representation == 'TimefrequencyCountPer':
        return timefrequency_to_count_per(
            timefrequency, from_representation=from_representation
        )
    elif to_representation == 'TimefrequencyInterval':
        return timefrequency_to_interval(
            timefrequency, from_representation=from_representation
        )
    else:
        raise Exception(
            'unknown timeperiod representation: ' + str(to_representation)
        )


def timefrequency_to_frequency(timefrequency, from_representation=None):
    """convert Timefrequency to TimefrequencyFrequency representation

    ## Inputs
    - timefrequency: Timefrequency
    - from_representation: str representation name of input timefrequency

    ## Returns
    - TimefrequencyFrequency
    """

    if from_representation is None:
        from_representation = (
            timefrequency_identify.detect_timefrequency_representation(
                timefrequency
            )
        )

    if from_representation == 'TimefrequencyFrequency':
        return timefrequency
    elif from_representation == 'TimefrequencyCountPer':
        per_seconds = timelength_utils.timelength_to_seconds_precise(
            timefrequency['per']
        )
        return timefrequency['count'] / float(per_seconds)
    elif from_representation == 'TimefrequencyInterval':
        interval_seconds = timelength_utils.timelength_to_seconds_precise(
            timefrequency['interval']
        )
        return 1 / interval_seconds
    else:
        raise Exception(
            'unknown Timefrequency representation: ' + str(from_representation)
        )


def timefrequency_to_count_per(timefrequency, from_representation=None):
    """convert Timefrequency to TimefrequencyCountPer representation

    ## Inputs
    - timefrequency: Timefrequency
    - from_representation: str representation name of input timefrequency

    ## Returns
    - TimefrequencyCountPer
    """

    if from_representation is None:
        from_representation = (
            timefrequency_identify.detect_timefrequency_representation()
        )

    if from_representation == 'TimefrequencyFrequency':
        return {'count': timefrequency, 'per': '1s'}
    elif from_representation == 'TimefrequencyCountPer':
        return timefrequency
    elif from_representation == 'TimefrequencyInterval':
        return {'count': 1, 'per': timefrequency['interval']}
    else:
        raise Exception(
            'unknown Timefrequency representation: ' + str(from_representation)
        )


def timefrequency_to_interval(timefrequency, from_representation=None):
    """convert Timefrequency to TimefrequencyInterval representation

    ## Inputs
    - timefrequency: Timefrequency
    - from_representation: str representation name of input timefrequency

    ## Returns
    - TimefrequencyInterval
    """

    if from_representation is None:
        from_representation = (
            timefrequency_identify.detect_timefrequency_representation()
        )

    if from_representation == 'TimefrequencyFrequency':
        return {'interval': 1 / float(timefrequency)}
    elif from_representation == 'TimefrequencyCountPer':
        per_seconds = timelength_utils.timelength_to_seconds(
            timefrequency['per']
        )
        return {'interval': per_seconds / timefrequency['count']}
    elif from_representation == 'TimefrequencyInterval':
        return timefrequency
    else:
        raise Exception(
            'unknown Timefrequency representation: ' + str(from_representation)
        )

