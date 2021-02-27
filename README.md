# irc-blowfish-python

A library useful for encrypting and decrypting blowfish-based IRC messages.

## Getting Started

### Prerequisites

```
pip install cryptography more-itertools
```

Requires Python 3.8 for walrus.

## Examples

All processing is done on byte-strings, so encoding/decoding is left up to the user.

```python
message_ecb = b"+OK lW9QU1l/xK2/03d0u127ASF0GQtTv/.N.W4/"
key = b"sekretkey"

decrypted = decrypt_ecb(message_ecb[4:], key).decode("utf-8")
```

```python
message_cbc = b"+OK *MLRNcakJMkET6IUET1Pl5hzSuoQaK1JyoCckk7tcXd8="
key = b"sekretkey"

decrypted = decrypt_cbc(message_cbc[5:], key).decode("utf-8")
```

```python
message = "Hello, this is a test"
key = b"sekretkey"

encrypted = b"+OK " + encrypt_ecb(message.encode("utf-8"), key)
```

```python
message = "Hello, this is a test"
key = b"sekretkey"

encrypted = b"+OK *" + encrypt_cbc(message.encode("utf-8"), key)
```