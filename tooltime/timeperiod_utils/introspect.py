from .. import timestamp_utils
from . import convert


def print_timeperiod(
    timeperiod, timestamp_representation='TimestampLabel', print_kwargs=None
):
    """print Timeperiod

    ## Inputs
    - timeperiod: Timeperiod
    - timestamp_representation: str name of Timestamp representation to print
    - print_kwargs: kwargs passed to print()
    """

    start, end = convert.timeperiod_to_pair(timeperiod)
    start_label = timestamp_utils.convert_timestamp(
        start, to_representation=timestamp_representation,
    )
    end_label = timestamp_utils.convert_timestamp(
        end, to_representation=timestamp_representation,
    )

    if print_kwargs is None:
        print_kwargs = {}
    print('[' + str(start_label) + ', ' + str(end_label) + ']', **print_kwargs)

