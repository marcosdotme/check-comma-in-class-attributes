from __future__ import annotations

import pytest

from check_comma_in_class_attributes import run


@pytest.mark.parametrize(
    ('file', 'expected_return'),
    [
        (['tests/resources/class_with_comma_in_attributes.py'], 1),
        (['tests/resources/class_without_comma_in_attributes.py'], 0),
        (['tests/resources/class_without_attributes.py'], 0),
        (['tests/resources/file_without_class.py'], 0),
        ([
            'tests/resources/class_without_comma_in_attributes.py',
            'tests/resources/class_without_attributes.py'
         ], 0
        ),
        ([
            'tests/resources/class_without_comma_in_attributes.py',
            'tests/resources/class_with_comma_in_attributes.py'
         ], 1
        ),
        ([
            'tests/resources/class_with_comma_in_attributes.py',
            'tests/resources/class_without_comma_in_attributes.py',
         ], 1
        ),
        ([
            'tests/resources/class_with_comma_in_attributes.py',
            'tests/resources/class_with_comma_in_attributes.py'
         ], 1
        )
    ]
)
def test_main(file: str, expected_return: int):
    actual_return = run(argv=file)

    assert actual_return == expected_return
