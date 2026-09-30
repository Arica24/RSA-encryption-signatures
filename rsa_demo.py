"""University-inspired RSA demo: keys, PEM files, encryption and signatures."""
import tempfile
from pathlib import Path
from cryptography.exceptions import InvalidSignature
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding, rsa


def new_key():
    return rsa.generate_private_key(public_exponent=65537, key_size=2048)


def encryption_padding():
    return padding.OAEP(mgf=padding.MGF1(hashes.SHA256()),
                        algorithm=hashes.SHA256(), label=None)


def signature_padding():
    return padding.PSS(mgf=padding.MGF1(hashes.SHA256()),
                       salt_length=padding.PSS.MAX_LENGTH)


def signature_valid(public_key, signature, message):
    try:
        public_key.verify(signature, message, signature_padding(), hashes.SHA256())
        return True
    except InvalidSignature:
        return False


def run_demo(message):
    if not message:
        raise ValueError('Enter a non-empty message.')
    # RSA-OAEP/SHA-256 with a 2048-bit key can encrypt at most 190 bytes.
    if len(message) > 190:
        raise ValueError('This short-message demo accepts at most 190 UTF-8 bytes.')
    private_key = new_key()
    public_key = private_key.public_key()
    modulus = public_key.public_numbers().n
    print('RSA modulus length:', modulus.bit_length(), 'bits')
    print('RSA modulus decimal digits:', len(str(modulus)))

    # Temporary demo files are removed automatically, including on exceptions.
    with tempfile.TemporaryDirectory(prefix='rsa-learning-') as directory:
        folder = Path(directory)
        # Random passphrase retained only in memory for this demonstration.
        import secrets
        passphrase = secrets.token_bytes(32)
        (folder / 'private.pem').write_bytes(private_key.private_bytes(
            serialization.Encoding.PEM, serialization.PrivateFormat.PKCS8,
            serialization.BestAvailableEncryption(passphrase)))
        (folder / 'public.pem').write_bytes(public_key.public_bytes(
            serialization.Encoding.PEM, serialization.PublicFormat.SubjectPublicKeyInfo))
        loaded_private = serialization.load_pem_private_key(
            (folder / 'private.pem').read_bytes(), password=passphrase)
        loaded_public = serialization.load_pem_public_key(
            (folder / 'public.pem').read_bytes())
        print('Saved and reloaded public and encrypted private PEM files.')

        ciphertext = loaded_public.encrypt(message, encryption_padding())
        (folder / 'encrypted.message').write_bytes(ciphertext)
        recovered = loaded_private.decrypt(
            (folder / 'encrypted.message').read_bytes(), encryption_padding())
        assert recovered == message
        print('Decrypted message:', recovered.decode('utf-8'))

        signature = loaded_private.sign(message, signature_padding(), hashes.SHA256())
        (folder / 'signature.bin').write_bytes(signature)
        signature = (folder / 'signature.bin').read_bytes()
        correct = signature_valid(loaded_public, signature, message)
        altered = signature_valid(loaded_public, signature, message + b' altered')
        wrong = signature_valid(new_key().public_key(), signature, message)
        print('Original message signature valid:', correct)
        print('Changed message signature valid:', altered)
        print('Different public key signature valid:', wrong)
        assert correct and not altered and not wrong
    print('Temporary keys, encrypted message and signature files removed.')


if __name__ == '__main__':
    try:
        text = input('Enter a short message (or press Enter for the example): ')
        run_demo((text or 'Learning public key cryptography.').encode('utf-8'))
    except ValueError as error:
        print('Input error:', error)
    except (EOFError, KeyboardInterrupt):
        print('\nFinished.')
