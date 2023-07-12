from typing import Iterable

import pytest

from dropstackframe import set_enable_drop_stack_frame


@pytest.fixture(autouse=True)
def enable() -> Iterable[None]:
    # Ensure that:
    # 1: `dropstackframe` is enabled when running these tests.
    # 2: If a test manipulates `dropstackframe` settings, they are reset after the test.
    with set_enable_drop_stack_frame(True):
        yield
