import pytest

# Basic tests

def test_basic():
    assert 1 == 1

# Failing tests

@pytest.mark.xfail(reason="deliberate fail")
def test_fail():
    assert 1 == 2

# Parametrization

@pytest.mark.parametrize("input,expected", [
    (1, 2),
    (2, 3),
])
def test_param(input, expected):
    assert input + 1 == expected

# Exceptions

def test_raise_exception():
    with pytest.raises(ZeroDivisionError):
        1 / 0

# Skips

@pytest.mark.skip(reason="deliberate skip")
def test_skip():
    assert 1 == 2

SKIP_IF_TRUE = True

@pytest.mark.skipif(SKIP_IF_TRUE, reason="skip if true")
def test_skip_if_true():
    assert 1 == 2

# Fixtures

@pytest.fixture()
def sample_fixture():
    return 42

def test_fixture(sample_fixture):
    assert sample_fixture == 42

@pytest.fixture()
def sample_fixture_with_teardown():
    yield 42
    print("teardown")

def test_fixture_with_teardown(sample_fixture_with_teardown):
    assert sample_fixture_with_teardown == 42

# Markers
# To run tests with a specific marker, use the -m option: pytest -m foo_marker

@pytest.mark.foo_marker
def test_marker():
    assert 1 == 1

# combine multiple marks using logical operators: pytest -m "foo_marker or bar_marker"

@pytest.mark.bar_marker
def test_marker2():
    assert 1 == 1
