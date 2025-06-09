"""
Encryption Constants
Author: fdygt
Created: 2025-06-04 16:25:57
"""

# Encryption Algorithms
ALGORITHMS = {
    'AES': 'AES',
    'RSA': 'RSA',
    'BLOWFISH': 'Blowfish',
    'TWOFISH': 'Twofish'
}

# Key Sizes
KEY_SIZES = {
    'AES_128': 128,
    'AES_192': 192,
    'AES_256': 256,
    'RSA_2048': 2048,
    'RSA_4096': 4096
}

# Modes of Operation
MODES = {
    'ECB': 'ECB',
    'CBC': 'CBC',
    'CFB': 'CFB',
    'OFB': 'OFB',
    'CTR': 'CTR',
    'GCM': 'GCM'
}

# Hash Functions
HASH_FUNCTIONS = {
    'MD5': 'md5',
    'SHA1': 'sha1',
    'SHA256': 'sha256',
    'SHA512': 'sha512',
    'BLAKE2': 'blake2b'
}

# Salt Settings
SALT = {
    'MIN_LENGTH': 16,
    'RECOMMENDED_LENGTH': 32,
    'MAX_LENGTH': 64
}