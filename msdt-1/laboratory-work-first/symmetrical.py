import os

from cryptography.hazmat.primitives.ciphers import Cipher, algorithms


class SymmetricEncryption:
    """
    Class for working with text by using Symetric Encryption.
    """
    
    @staticmethod
    def generate_key() -> bytes:
        """
        Generate a random symmetric key for ChaCha20.
        Returns:
        - bytes: A randomly generated symmetric key.
        """
        return os.urandom(32)  

    @staticmethod
    def encrypt_text(symmetric_key: bytes, text: bytes) -> bytes:
        """
        Encrypt the text using the provided symmetric key and 16-byte nonce.
        Args:
        - symmetric_key (bytes): Symmetric key for encryption.
        - text (bytes): Text to be encrypted.
        Returns:
        - bytes: Encrypted text, prepended by the 16-byte nonce.
        """
        nonce = os.urandom(16)  
        cipher = Cipher(algorithms.ChaCha20(symmetric_key, nonce[:16]), mode=None) 
        encryptor = cipher.encryptor()
        encrypted_text = encryptor.update(text)
        return nonce + encrypted_text  

    @staticmethod
    def decrypt_text(symmetric_key: bytes, encrypted_text: bytes) -> bytes:
        """
        Decrypt the text using the provided symmetric key and 16-byte nonce.
        Args:
        - symmetric_key (bytes): Symmetric key for decryption.
        - encrypted_text (bytes): Encrypted text, prepended by the 16-byte nonce.
        Returns:
        - bytes: Decrypted plaintext.
        """
        nonce = encrypted_text[:16]  
        ciphertext = encrypted_text[16:]
        cipher = Cipher(algorithms.ChaCha20(symmetric_key, nonce[:16]), mode=None) 
        decryptor = cipher.decryptor()
        return decryptor.update(ciphertext)
