
def get_base_units():
    """return mapping {label: seconds} for standard base units of time"""
    return {
        '1s': 1,
        '1m': 60,
        '1h': 60 * 60,
        '1d': 60 * 60 * 24,
        '1w': 60 * 60 * 24 * 7,
        '1M': 60 * 60 * 24 * 30,
        '1y': 60 * 60 * 24 * 365,
    }


def get_singular_unit_labels():
    """return mapping {english_name: TimelengthLabel} for singular base units"""
    return {
        'second': '1s',
        'minute': '1m',
        'hour': '1h',
        'day': '1d',
        'week': '1w',
        'month': '1M',
        'year': '1y',
    }


def get_plural_unit_labels():
    """return mapping {english_name: TimelengthLabel} for plural base units"""
    return {
        'seconds': '1s',
        'minutes': '1m',
        'hours': '1h',
        'days': '1d',
        'weeks': '1w',
        'months': '1M',
        'years': '1y',
    }


def get_unit_labels():
    """return mapping of singular and plural unit labels"""
    return dict(get_singular_unit_labels(), **get_plural_unit_labels())


def unit_letters_to_names():
    """return mapping {TimelengthLabel: english_name} for singular base units"""
    return {v[-1]: k for k, v in get_singular_unit_labels().items()}

