import pytest

from dropstackframe import (
    drop_stack_frame,
    get_enable_drop_stack_frame,
    set_enable_drop_stack_frame,
)


def test_enable_drop_stack_frame() -> None:
    assert get_enable_drop_stack_frame()
    set_enable_drop_stack_frame(False)
    assert not get_enable_drop_stack_frame()
    with set_enable_drop_stack_frame(True):
        assert get_enable_drop_stack_frame()
        with set_enable_drop_stack_frame(False):
            assert not get_enable_drop_stack_frame()
            set_enable_drop_stack_frame(True)
            assert get_enable_drop_stack_frame()
        assert get_enable_drop_stack_frame()
    assert not get_enable_drop_stack_frame()

    set_enable_drop_stack_frame(False)
    try:
        with set_enable_drop_stack_frame(True):
            assert get_enable_drop_stack_frame()
            raise RuntimeError("test error")
    except RuntimeError:
        pass  # Expected
    assert not get_enable_drop_stack_frame()


def _foo(should_raise: bool) -> int:
    assert not should_raise
    return 42


def _bar(should_raise: bool) -> int:
    try:
        return _foo(should_raise)
    except Exception:
        drop_stack_frame()
        raise


def _baz(should_raise: bool) -> int:
    return _bar(should_raise)


def test_drop_stack_frame() -> None:
    assert 42 == _baz(should_raise=False)

    with pytest.raises(AssertionError) as excinfo:
        _baz(should_raise=True)
    assert [
        "test_drop_stack_frame",
        "_baz",
        # "_bar" should be dropped...
        "_foo",
    ] == [tb.name for tb in excinfo.traceback]


def test_drop_stack_frame__disabled() -> None:
    with set_enable_drop_stack_frame(False):
        assert 42 == _baz(should_raise=False)

        with pytest.raises(AssertionError) as excinfo:
            _baz(should_raise=True)
        assert [
            "test_drop_stack_frame__disabled",
            "_baz",
            "_bar",
            "_foo",
        ] == [tb.name for tb in excinfo.traceback]
