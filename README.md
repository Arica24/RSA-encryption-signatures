# RSA Encryption and Digital Signatures

A learning project adapted from Applied Cryptography Seminar 7. It demonstrates key generation, saving and loading PEM files, encrypting and decrypting a short message, and checking digital signatures.

## Attribution and scope

The tasks and original starter code came from university seminar solutions. It uses the `cryptography` package rather than the seminar's `rsa` package, so it is an extension of the exercise, not an exact reproduction. The pasted seminar key values are not included.

## Run

Requires Python

Open a terminal in the project folder:

```bash
python3 -m venv .venv
source .venv/bin/activate
python3 -m pip install -r requirements.txt
python3 rsa_demo.py
```

On Windows:

```powershell
py -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python rsa_demo.py
```

Enter a short message, or press Enter for the example. The maximum is 190 UTF-8 bytes for this key size and encryption padding.

## What happens

1. Generate a fresh 2048-bit RSA key pair.
2. Show the bit length and decimal digit count of the RSA modulus.
3. Save the public key and an encrypted private key to temporary PEM files.
4. Reload both files into key objects.
5. Encrypt the message with the public key using OAEP and SHA-256.
6. Save and read the ciphertext, then decrypt with the private key.
7. Sign the message with the private key using PSS and SHA-256.
8. Verify it with the matching public key.
9. Show failed verification after changing the message or using a different key.
10. Remove the temporary files automatically.

The passphrase is randomly generated and kept only in memory. This demonstrates serialization; it is not a system for keeping keys across sessions.

## Expected results

```text
RSA modulus length: 2048 bits
Saved and reloaded public and encrypted private PEM files.
Decrypted message: Learning public key cryptography.
Original message signature valid: True
Changed message signature valid: False
Different public key signature valid: False
Temporary keys, encrypted message and signature files removed.
```

The program also shows the exact decimal digit count. Fresh keys and ciphertext differ on each run.

## Seminar questions explained

- **PEM:** a text representation of encoded data such as keys or certificates, with headers, footers and Base64 content. PEM describes the encoding; the contents can have different formats.
- **PKCS #1:** RSA specifications, including key structures, encryption and signature schemes. This edition exports private keys as PKCS #8 and public keys as SubjectPublicKeyInfo, both encoded as PEM.
- **`wb` / `rb`:** write bytes / read bytes. `Path.write_bytes()` and `Path.read_bytes()` provide the equivalent file operations here.
- **Why parse the key?** Reading a file returns bytes. A key-loading function interprets those bytes and returns an object with encryption or signing operations.
- **Key length:** 2048 bits refers to the modulus, not the total size of a private-key file. A private-key object holds several integers; encoded file sizes depend on format.
- **Verification output:** in the original `rsa` package, successful verification returns the hash algorithm name, while a wrong signature raises an error. Here, `cryptography` returns normally on success and raises `InvalidSignature` on failure. The helper turns that into `True` or `False`.

Encryption protects the short message's confidentiality. A signature checks its integrity and that it was signed with the private key corresponding to the supplied public key. Establishing who owns that public key is a separate concern.

## Design choices

This edition uses 2048-bit keys, OAEP for encryption and PSS for signatures. The official documentation recommends OAEP and PSS for new applications. This is a teaching demonstration; larger messages require a different design, usually combining asymmetric and symmetric encryption.

## Skills

Asymmetric cryptography, digital signatures, key serialization, binary file handling, dependency management and exception handling.

## References

- [Official RSA documentation](https://cryptography.io/en/46.0.1/hazmat/primitives/asymmetric/rsa/)
- [PKCS #1 specification](https://datatracker.ietf.org/doc/rfc8017/)
- Applied Cryptography Seminar 7 solutions supplied with the exercise.
