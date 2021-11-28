from .. import timelength_utils


def detect_resolution(timestamps, use_n=None, outlier_rtol=0.5):
    """detect resolution of iterable of Timestamps

    ## Detection Algorithm
    - current algorithm: whether median dt value is close to a known value
    - dts that are +- 50% of this median are returned in 'outliers' key

    ## Inputs
    - timestamps: iterable of Timestamp
    - use_n: int or None, indicating number of timestamp values to use
        - smaller n will be faster but could be less representative
    - outlier_rtol: float of tolerance for detecting outliers
    """

    import numpy as np

    if len(timestamps) == 1:
        return None

    # preprocess
    if not isinstance(timestamps, np.ndarray):
        timestamps = np.array(timestamps)
    if use_n is not None:
        timestamps = timestamps[:use_n]

    # compute time deltas
    dts = timestamps[1:] - timestamps[:-1]
    median_dt = np.median(dts)
    outliers = {
        'small': dts[dts < 1 / (1 + outlier_rtol) * median_dt],
        'large': dts[dts > (1 + outlier_rtol) * median_dt],
        'outlier_rtol': outlier_rtol,
    }

    label = timelength_utils.timelength_seconds_to_label(median_dt)

    return {
        'label': label,
        'dts': dts,
        'use_n': use_n,
        'median_dt': median_dt,
        'outliers': outliers,
    }

