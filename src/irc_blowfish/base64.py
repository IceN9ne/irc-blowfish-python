from more_itertools import chunked

B64 = b"./0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"


def base64_encode(data: bytes) -> bytes:
    out = b""
    for chunk in chunked(data, 8, strict=True):
        # Build left and right bit-strings from decoded text
        left = sum(x << y for x, y in zip(chunk[:4], (24, 16, 8, 0)))
        right = sum(x << y for x, y in zip(chunk[4:], (24, 16, 8, 0)))

        # Convert to encoded text in 0x3F chunks
        out += bytes(B64[(right >> i) & 0x3F] for i in (0, 6, 12, 18, 24, 30))
        out += bytes(B64[(left >> i) & 0x3F] for i in (0, 6, 12, 18, 24, 30))

    return out


def base64_decode(data: bytes) -> bytes:
    out = b""
    for chunk in chunked(data, 12, strict=True):
        # Build left and right bit-strings from encoded text
        # Seems this is a bit slower than sum
        # left = reduce(operator.or_, (B64.index(x) << y for x, y in zip(chunk[:6], (0, 6, 12, 18, 24, 30))))
        # right = reduce(operator.or_, (B64.index(x) << y for x, y in zip(chunk[6:], (0, 6, 12, 18, 24, 30))))
        left = sum(B64.index(x) << y for x, y in zip(chunk[:6], (0, 6, 12, 18, 24, 30)))
        right = sum(B64.index(x) << y for x, y in zip(chunk[6:], (0, 6, 12, 18, 24, 30)))

        # Convert to decoded text in 0xFF chunks
        out += bytes((right & (0xFF << x)) >> x for x in (24, 16, 8, 0))
        out += bytes((left & (0xFF << x)) >> x for x in (24, 16, 8, 0))

    return out
