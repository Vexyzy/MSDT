import json

from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives.serialization import load_pem_public_key, load_pem_private_key


class FileWorking:
    """
    Class for work with files and keys.
    """
    
    @staticmethod
    def read_file(file_path: str) -> str:
        """
        Read the file.
        Args:
        - file_path (str): The path to the file to be read.
        Returns:
        - str: The content of the file.
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                return file.read()
        except FileNotFoundError as e:
            raise FileNotFoundError(f"The file {file_path} does not exist") from e
        except Exception as e:
            raise e

    @staticmethod
    def write_file(file_path: str, file_content: str) -> None:
        """
        Write to file.
        Args:
        - file_path (str): The path to the file to be written.
        - file_content (str): The content to write to the file.
        Returns:
        - None
        """
        try:
            with open(file_path, 'w', encoding='utf-8') as file:
                file.write(file_content)
        except FileNotFoundError as e:
            raise FileNotFoundError(f"The file {file_path} does not exist") from e
        except Exception as e:
            raise e

    @staticmethod 
    def read_json(file_path: str) -> dict:
        """
        Read JSON from file.
        Args:
        - file_path (str): The path to the JSON file to be read.
        Returns:
        - dict: The JSON data.
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                return json.load(file)
        except FileNotFoundError as e:
            raise FileNotFoundError(f"The file {file_path} does not exist") from e
        except Exception as e:
            raise e
        
    @staticmethod  
    def write_json(file_path: str, file_content: dict) -> None:
        """
        Write a dictionary to a JSON file.
        Args:
        - file_path (str): The path to the file to be written.
        - file_content (dict): The dictionary to write to the file.
        Returns:
        - None
        """
        try:
            with open(file_path, 'w', encoding='utf-8') as file:
                json.dump(file_content, file, indent=4, ensure_ascii=False)
        except FileNotFoundError as e:
            raise FileNotFoundError(f"The file {file_path} does not exist") from e
        except Exception as e:
            raise e
        
    @staticmethod
    def read_bytes_file(file_path: str) -> bytes:
        """
        Reads the bytes file.
        Args:
        - file_path (str): The path to the file to be read.
        Returns:
        - bytes: The bytes read from the file.
        """
        try:
            with open(file_path, "rb") as file:
                file_content = file.read()
            return file_content
        except FileNotFoundError as e:
            raise FileNotFoundError(f"The file {file_path} does not exist") from e
        except Exception as e:
            raise e

    @staticmethod
    def write_bytes_file(file_path: str, file_content: bytes) -> None:
        """
        Writes the bytes file.
        Args:
        - file_path (str): The path to the file to be written.
        - file_content (bytes): The bytes to write to the file.
        Returns:
        - None
        """
        try:
            with open(file_path, "wb") as file:
                file.write(file_content)
        except FileNotFoundError as e:
            raise FileNotFoundError(f"The file {file_path} does not exist") from e
        except Exception as e:
            raise e
            
    @staticmethod
    def serealization_public_key (public_key_path: str, public_key: rsa.RSAPublicKey) -> None:
        """
        Serealize the public key to a file.
        Args:
        - public_key_path (str): The path to the key's file.
        - public_key (rsa.RSAPublicKey) : The public key to serialize.
        Returns:
        - None
        """
        try:
            FileWorking.write_bytes_file(public_key_path, public_key.public_bytes(encoding=serialization.Encoding.PEM,
                    format=serialization.PublicFormat.SubjectPublicKeyInfo))
        except FileNotFoundError as e:
            raise FileNotFoundError(f"The file {public_key_path} does not exist") from e
        except Exception as e:
            raise e
            
    @staticmethod       
    def serealization_private_key (private_key_path: str, private_key: rsa.RSAPrivateKey) -> None:
        """
        Serealize the private key to a file.
        Args:
        - private_key_path (str): The path to the key's file.
        - private_key (rsa.RSAPrivateKey) : The private key to serialize.
        Returns:
        - None
        """
        try:
            FileWorking.write_bytes_file(private_key_path, private_key.private_bytes(encoding=serialization.Encoding.PEM,
                    format=serialization.PrivateFormat.TraditionalOpenSSL,
                    encryption_algorithm=serialization.NoEncryption()))
        except FileNotFoundError as e:
            raise FileNotFoundError(f"The file {private_key_path} does not exist") from e
        except Exception as e:
            raise e
            
    @staticmethod     
    def deserealization_public_key (public_key_path: str) -> rsa.RSAPublicKey: 
        """
        Deserealize the public key.
        Args:
        - public_key_path (str) : The path to the key's file.
        Returns:
        - rsa.RSAPublicKey : Returns the public key.
        """
        try:
            return serialization.load_pem_public_key(FileWorking.read_bytes_file(public_key_path), password=None)
        except FileNotFoundError as e:
            raise FileNotFoundError(f"The file {public_key_path} does not exist") from e
        except Exception as e:
            raise e
        
    @staticmethod
    def deserealization_private_key (private_key_path: str) -> rsa.RSAPrivateKey:
        """
        Deserealize the private key.
        Args:
        - private_key_path (str) : The path to the key's file.
        Returns:
        - rsa.RSAPrivateKey : Returns the private key.
        """
        try:
            return serialization.load_pem_private_key(FileWorking.read_bytes_file(private_key_path), password=None)
        except FileNotFoundError as e:
            raise FileNotFoundError(f"The file {private_key_path} does not exist") from e
        except Exception as e:
            raise e
        
    @staticmethod
    def serialization_nonce(file_path: str, file_nonce: bytes) -> None:
        """
        Serialize the nonce to a file.
        Args:
        - file_nonce (bytes): Nonce to be serialized.
        - file_path (str): File path to save the nonce.
        Returns:
        - None.
        """
        try:
            FileWorking.write_bytes_file(file_path, file_nonce)
        except FileNotFoundError as e:
            raise FileNotFoundError(f"The file {file_path} does not exist") from e
        except Exception as e:
            raise e
        
    @staticmethod      
    def deserealization_nonce(file_path: str) -> bytes:
        """
        Deserialize the nonce
        Args:
        - file_path (str): File path to serealize the nonce.
        Returns:
        - bytes : The bytes read from the file.
        """
        try:
            return FileWorking.read_bytes_file(file_path)
        except FileNotFoundError as e:
            raise FileNotFoundError(f"The file {file_path} does not exist") from e
        except Exception as e:
            raise e