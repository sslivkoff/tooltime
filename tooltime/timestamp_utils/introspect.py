from .. import timefrequency_utils
from .. import timelength_utils
from . import convert


def summarize_timestamps(timestamps):
    """create summary of timestamps

    ## Inputs
    - timestamps: iterable of Timestamp
    """

    n_t = len(timestamps)
    summary = {'n_t': n_t}

    if n_t == 1:
        summary['start'] = timestamps[0]
        summary['end'] = timestamps[0]

    elif n_t > 1:
        if timestamps[-1] < timestamps[0]:
            timestamps = timestamps[::-1]

        n_unique = len(set(timestamps))
        resolution = timefrequency_utils.detect_resolution(timestamps)
        start = convert.timestamp_to_label(timestamps[0])
        end = convert.timestamp_to_label(timestamps[-1])
        duration = timestamps[-1] - timestamps[0]
        duration_label = timelength_utils.timelength_seconds_to_clock_phrase(
            duration
        )
        n_large_outliers = resolution['outliers']['large'].shape[0]
        n_small_outliers = resolution['outliers']['small'].shape[0]
        n_outliers = n_large_outliers + n_small_outliers

        if resolution['median_dt'] > 0.0001:
            n_ideal = range(
                timestamps[0],
                timestamps[-1] + resolution['median_dt'],
                resolution['median_dt'],
            )
            n_ideal = list(n_ideal)
            n_missing = len(n_ideal) - len(timestamps)
        else:
            n_missing = 'median dt <= 0.0001'

        summary['n_unique'] = n_unique
        summary['resolution'] = resolution
        summary['start'] = start
        summary['end'] = end
        summary['duration'] = duration
        summary['duration_label'] = duration_label
        summary['n_large_outliers'] = n_large_outliers
        summary['n_small_outliers'] = n_small_outliers
        summary['n_outliers'] = n_outliers
        summary['n_missing'] = n_missing

    return summary


def print_timestamp_summary(
    *, timestamps=None, summary=None, indent=None, print_kwargs=None
):
    """print summary of timestamps

    - specify either timestamps or summary
    - timestamps should be ordered
        - todo: do not require ordering

    ## Inputs
    - timestamps: iterable of Timestamp
    - summary: dict summary created by summarize_timestamps()
    - indent: str indent of each line in summary
    - print_kwargs: kwargs passed to print()
    """

    # validate inputs
    if summary is None and timestamps is None:
        raise Exception('must specify timestamps or summary')
    if indent is None:
        indent = ''
    if print_kwargs is None:
        print_kwargs = {}

    # create summary if not provided
    if summary is None:
        summary = summarize_timestamps(timestamps)

    n_t = summary['n_t']
    print(indent + 'n_t:', n_t, **print_kwargs)

    if n_t == 1:
        print(indent + 'timestamp:', summary['start'], **print_kwargs)

    elif n_t > 1:

        n_unique = summary['n_unique']
        resolution = summary['resolution']
        start = summary['start']
        end = summary['end']
        duration = summary['duration']
        duration_label = summary['duration_label']
        n_large_outliers = summary['n_large_outliers']
        n_small_outliers = summary['n_small_outliers']
        n_outliers = summary['n_outliers']
        n_missing = summary['n_missing']
        outlier_rtol = resolution['outliers']['outlier_rtol']
        mean_dt = timelength_utils.timelength_to_label(duration / (n_t - 1))

        print(indent + 'n_unique:', n_unique, **print_kwargs)
        print(indent + 'extent:')
        print(
            '    ' + indent + 'start:',
            start,
            '(' + ('%.14g' % timestamps[0]) + ')',
            **print_kwargs
        )
        print(
            '    ' + indent + 'end:  ',
            end,
            '(' + ('%.14g' % timestamps[-1]) + ')',
            **print_kwargs
        )
        print(
            '    ' + indent + 'duration:',
            duration_label,
            '(' + ('%.14g' % duration) + ' s)',
            **print_kwargs
        )
        print(indent + 'resolution:', **print_kwargs)
        print(
            '    ' + indent + 'median_dt:', resolution['label'], **print_kwargs
        )
        print('    ' + indent + 'mean_dt:', mean_dt, **print_kwargs)
        print(
            '    ' + indent + 'missing timestamps:',
            n_missing,
            '(if median_dt maintained)',
            **print_kwargs
        )
        print('    ' + indent + 'outlier_dts:', n_outliers, **print_kwargs)
        print(
            '        ' + indent + 'small:',
            n_small_outliers,
            '       dt < median_dt / (1 + outlier_rtol)',
            **print_kwargs
        )
        print(
            '        ' + indent + 'large:',
            n_large_outliers,
            '       dt > median_dt * (1 + outlier_rtol)',
            **print_kwargs
        )
        print(
            '        ' + indent + '(outlier_rtol =',
            str(outlier_rtol) + ')',
            **print_kwargs
        )

