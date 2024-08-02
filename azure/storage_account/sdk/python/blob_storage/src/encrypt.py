import re


def mask_key(key: str, beg: int, end: int) -> str:
    """
    Mask key by replacing the middle part with '*'
    @param key: key
    @param beg: begin index
    @param end: end index
    @return: encrypted key
    """

    if key is None or len(key) == 0:
        return key

    if beg is None or end is None:
        # if beg or end is missing
        return re.sub(r'.', '*', key)

    if beg < 0 or end < -1 * len(key):
        # if beg or end is too small
        return re.sub(r'.', '*', key)

    if len(key[:beg]) + len(key[end:]) >= len(key) or len(key[beg:end]) < 8:
        # if beg or end parts cover too much of the key
        # or the middle part is too short
        return re.sub(r'.', '*', key)

    resp_beg = key[:beg]
    resp_mid = re.sub(r'.', '*', key[beg:end])
    resp_end = key[end:]
    return str(resp_beg) + str(resp_mid) + str(resp_end)
