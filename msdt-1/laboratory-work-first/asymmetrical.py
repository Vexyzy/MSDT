from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import serialization, hashes

class AsymmetricEncryption:
    """
    Class for working with key by using Asymetric Encryption.
    """
    
    @staticmethod
    def generate_keys() -> tuple:
        """
        Generate a pair of RSA keys (private and public) and save them to files.
        Args:
        - None.
        Returns:
        - tuple: Return private and public keys.
        """
        private_key = rsa.generate_private_key(
                public_exponent=65537,
                key_size=2048
            )
        public_key = private_key.public_key()
        return private_key, public_key

 
    @staticmethod
    def encrypt_key(public_key: rsa.RSAPublicKey, symmetric_key: bytes) -> bytes:
        """
        Encrypt the symmetric key using the provided public key.
        Args:
        - public_key: Public key for encryption.
        - symmetric_key (bytes): Symmetric key to be encrypted.
        Returns:
        - bytes: Encrypted symmetric key.
        """
        return public_key.encrypt(
            symmetric_key,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        ) 

    @staticmethod
    def decrypt_key(private_key: rsa.RSAPrivateKey, encrypted_key: bytes) -> bytes:
        """
        Decrypt the encrypted symmetric key using the provided private key.
        Args:
        - private_key: Private key for decryption.
        - encrypted_key (bytes): Encrypted symmetric key.
        Returns:
        - bytes: Decrypted symmetric key.
        """
        return private_key.decrypt(
            encrypted_key,
            padding.OAEP(
                mgf = padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )