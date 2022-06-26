import pytest

import tooltime


tests = [
    (
        {'start_time': 1, 'end_time': 10, 'sample_interval': 4},
        [1, 5, 9],
    ),
    (
        {
            'start_time': 1,
            'end_time': 10,
            'sample_interval': 4,
            'include_misaligned_bound': True,
        },
        [1, 5, 9, 10],
    ),
    (
        {
            'start_time': 1,
            'end_time': 10,
            'sample_interval': 4,
            'include_misaligned_overflow': True,
        },
        [1, 5, 9, 13],
    ),
    (
        {
            'start_time': 1,
            'end_time': 10,
            'sample_interval': 4,
            'align_to': 'end',
        },
        [2, 6, 10],
    ),
    (
        {
            'start_time': 1,
            'end_time': 10,
            'sample_interval': 4,
            'align_to': 'end',
            'include_misaligned_bound': True,
        },
        [1, 2, 6, 10],
    ),
    (
        {
            'start_time': 1,
            'end_time': 10,
            'sample_interval': 4,
            'align_to': 'end',
            'include_misaligned_overflow': True,
        },
        [-2, 2, 6, 10],
    ),
]


@pytest.mark.parametrize('test', tests)
def test_sample_timestamps(test):
    inputs, outputs = test
    actual_outputs = tooltime.sample_timestamps(**inputs)
    assert outputs == actual_outputs
