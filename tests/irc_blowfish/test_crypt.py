from unittest.mock import MagicMock

import pytest
from pytest_mock import MockFixture

from irc_blowfish import decrypt_cbc, decrypt_ecb, encrypt_cbc, encrypt_ecb


@pytest.fixture()
def urandom(mocker: MockFixture) -> MagicMock:
    return mocker.patch("irc_blowfish.crypt.os.urandom")


class TestDecryptCbc:
    @pytest.mark.parametrize(
        ("encrypted", "key", "decrypted"),
        (
            (b"ODc2NTQzMjE=", b"asdf", b""),
            (b"/GbbdsBclRQBMoNpTCNWgO5vUEIJwBAD", b"aaaa", b"This is a test"),
            (b"MTIzNDU2NziYThVTrRtjMaFuagmsVzhy", b"asdfasdf", b"This is a test"),
        ),
    )
    def test_decrypts_bytes(self, encrypted: bytes, key: bytes, decrypted: bytes) -> None:
        assert decrypt_cbc(encrypted, key) == decrypted


class TestDecryptEcb:
    @pytest.mark.parametrize(
        ("encrypted", "key", "decrypted"),
        (
            (b"", b"asdfasdf", b""),
            (b"xyxLi.N8aNx1pGDAH/P1540/", b"aaaa", b"This is a test"),
        ),
    )
    def test_decrypts_bytes(self, encrypted: bytes, key: bytes, decrypted: bytes) -> None:
        assert decrypt_ecb(encrypted, key) == decrypted


class TestEncryptCbc:
    @pytest.mark.parametrize(
        ("decrypted", "key", "iv", "encrypted"),
        (
            (b"This is a test", b"asdfasdf", b"12345678", b"MTIzNDU2NziYThVTrRtjMaFuagmsVzhy"),
            (b"", b"asdf", b"87654321", b"ODc2NTQzMjE="),
        ),
    )
    def test_encrypts_bytes(
        self, decrypted: bytes, key: bytes, iv: bytes, encrypted: bytes, urandom: MagicMock
    ) -> None:
        urandom.return_value = iv
        assert encrypt_cbc(decrypted, key) == encrypted


class TestEncryptEcb:
    @pytest.mark.parametrize(
        ("decrypted", "key", "encrypted"),
        (
            (b"This is a test", b"asdfasdf", b".FcjN/3lC2j1uwgTd/1KAPM1"),
            (b"", b"asdfasdf", b""),
        ),
    )
    def test_encrypts_bytes(self, decrypted: bytes, key: bytes, encrypted: bytes) -> None:
        assert encrypt_ecb(decrypted, key) == encrypted
