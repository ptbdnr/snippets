import pytest


def test_importable():
    import src.encrypt  # noqa: F401
    from src.encrypt import mask_key  # noqa: F401


@pytest.mark.parametrize("key, beg, end", [
    ('foo', None, None),
    ('bar', 1, 1),
    ('buz', 10, 10),
    ('buz', -1, 10),
    ('buz', 1, -10),
])
def test_mask_key(key, beg, end):
    from src.encrypt import mask_key
    encryptedKey = mask_key(key, beg, end)
    assert encryptedKey != key
    assert '**' in encryptedKey
