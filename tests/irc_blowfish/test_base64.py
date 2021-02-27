import pytest

from irc_blowfish.base64 import base64_decode, base64_encode


class TestBase64Encode:
    @pytest.mark.parametrize(
        ("decoded", "encoded"),
        (
            (b"asdfasdf", b"AfQqv/AfQqv/"),
            (b"asdf\0\0\0\0", b"......AfQqv/"),
            (b"", b""),
        ),
    )
    def test_encodes_bytes(self, decoded: bytes, encoded: bytes) -> None:
        assert base64_encode(decoded) == encoded

    @pytest.mark.parametrize(
        "decoded",
        (
            (b"1",),
            (b"12",),
            (b"123",),
            (b"1234",),
            (b"12345",),
            (b"123456",),
            (b"1234567",),
            (b"123456789",),
        ),
    )
    def test_raises_on_incorrect_length(self, decoded: bytes) -> None:
        with pytest.raises(ValueError, match="iterable is not divisible by n."):
            base64_encode(decoded)


class TestBase64Decode:
    @pytest.mark.parametrize(
        ("encoded", "decoded"),
        (
            (b"AfQqv/AfQqv/", b"asdfasdf"),
            (b"......AfQqv/", b"asdf\0\0\0\0"),
            (b"", b""),
        ),
    )
    def test_decodes_bytes(self, encoded: bytes, decoded: bytes) -> None:
        assert base64_decode(encoded) == decoded

    @pytest.mark.parametrize(
        "encoded",
        (
            (b"1",),
            (b"12",),
            (b"123",),
            (b"1234",),
            (b"12345",),
            (b"123456",),
            (b"1234567",),
            (b"12345678",),
            (b"123456789",),
            (b"1234567890",),
            (b"12345678901",),
            (b"1234567890123",),
        ),
    )
    def test_raises_on_incorrect_length(self, encoded: bytes) -> None:
        with pytest.raises(ValueError, match="iterable is not divisible by n."):
            base64_decode(encoded)
