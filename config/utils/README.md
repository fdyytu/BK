# Advanced Configuration Utils

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Python](https://img.shields.io/badge/python-3.9+-blue.svg)
![Version](https://img.shields.io/badge/version-1.0.0-green.svg)
![Last Updated](https://img.shields.io/badge/last%20updated-2025--06--06-brightgreen.svg)

A comprehensive Python configuration management library with advanced features for enterprise applications.

## Features

### 🔐 Security
- Encryption and decryption of sensitive values
- Value masking for logs and outputs
- Input sanitization
- SSL/TLS configuration validation
- Security policy enforcement

### 🔍 Validation
- Schema validation
- Type checking and coercion
- Network configuration validation
- Custom validation rules
- Pattern matching

### 🔄 Loading & Parsing
- Multiple format support (YAML, JSON, TOML, ENV)
- Async loading capabilities
- Variable interpolation
- Type inference
- Cross-platform compatibility

### 🛠 Configuration Management
- Override management
- Fallback strategies
- Dependency resolution
- Path resolution
- Environment variable handling

### 🎯 Error Handling
- Detailed error tracking
- Custom error handlers
- Fallback mechanisms
- Error reporting
- Retry strategies

config/utils/
├── __init__.py
├── abstracts/
│   ├── __init__.py
│   ├── base_loader.py
│   ├── base_validator.py
│   └── base_parser.py
├── loaders/
│   ├── __init__.py
│   ├── yaml_loader.py
│   ├── json_loader.py
│   ├── env_loader.py
│   └── toml_loader.py
├── validators/
│   ├── __init__.py
│   ├── schema_validator.py
│   ├── type_validator.py
│   ├── network_validator.py
│   └── security_validator.py
├── parsers/
│   ├── __init__.py
│   ├── env_parser.py
│   ├── path_parser.py
│   └── value_parser.py
├── resolvers/
│   ├── __init__.py
│   ├── path_resolver.py
│   ├── env_resolver.py
│   └── dependency_resolver.py
├── security/
│   ├── __init__.py
│   ├── encryption.py
│   ├── masking.py
│   └── sanitizer.py
├── handlers/
│   ├── __init__.py
│   ├── error_handler.py
│   ├── fallback_handler.py
│   └── override_handler.py
├── constants/
│   ├── __init__.py
│   ├── messages.py
│   ├── patterns.py
│   └── defaults.py
└── exceptions/
    ├── __init__.py
    ├── validation_errors.py
    ├── loading_errors.py
    └── security_errors.py

## Installation

```bash
pip install git+https://github.com/fdyytu/kun.git#subdirectory=config/utils

Quick Start
Python
from config.utils import YAMLLoader, SchemaValidator, ConfigEncryption
from config.utils.handlers import ErrorHandlingService

# Initialize components
loader = YAMLLoader()
validator = SchemaValidator()
encryption = ConfigEncryption()
error_handler = ErrorHandlingService()

# Load and validate configuration
async def load_config():
    try:
        # Load configuration
        config = await loader.load('config.yml')
        
        # Validate
        if await validator.validate(config):
            print("Configuration valid!")
            
        # Encrypt sensitive values
        encrypted_config = encryption.encrypt_values(config)
        
        return encrypted_config
        
    except Exception as e:
        await error_handler.handle_error(e, "config_loading")
Architecture
The library follows SOLID principles and implements several design patterns:

1. Abstract Base Classes
BaseConfigLoader: Template for configuration loaders
BaseParser: Template for value parsers
BaseValidator: Template for validation implementations
2. Core Components
Loaders: YAML, JSON, TOML, ENV
Validators: Schema, Type, Network, Security
Parsers: Environment, Path, Value
Resolvers: Path, Environment, Dependency
Security: Encryption, Masking, Sanitization
Handlers: Error, Fallback, Override
3. Constants and Defaults
Message definitions
Regex patterns
Default configurations
Validation rules
Advanced Usage
Custom Validation Rules
Python
from config.utils.validators import TypeValidator

validator = TypeValidator()

# Add custom type
validator.add_custom_type(
    'port_number',
    lambda x: isinstance(x, int) and 0 <= x <= 65535
)

# Validate
result = await validator.validate({
    'port': {'_type': 'port_number', 'value': 8080}
})
Encrypted Configuration
Python
from config.utils.security import ConfigEncryption

encryption = ConfigEncryption()

# Encrypt sensitive values
encrypted_config = encryption.encrypt_value("api_key_123")

# Decrypt when needed
decrypted_value = encryption.decrypt_value(encrypted_config)
Environment Resolution
Python
from config.utils.resolvers import EnvResolver

resolver = EnvResolver(prefix='APP_')

# Resolve with type conversion
db_port = await resolver.resolve(
    'DB_PORT',
    default=5432,
    var_type=int
)
Best Practices
Security

Always encrypt sensitive values
Use proper access controls
Validate input thoroughly
Performance

Enable caching for frequent operations
Use async loading when possible
Implement proper error handling
Maintenance

Keep configuration DRY
Use clear naming conventions
Document custom implementations
Contributing
Fork the repository
Create your feature branch (git checkout -b feature/AmazingFeature)
Commit your changes (git commit -m 'Add some AmazingFeature')
Push to the branch (git push origin feature/AmazingFeature)
Open a Pull Request
License
This project is licensed under the MIT License - see the LICENSE file for details.

Author
fdyytu

GitHub: @fdyytu
Created: 2025-06-06
Last Updated: 2025-06-06 16:11:10 UTC
Acknowledgments
Python community for inspiration
Contributors and maintainers
Everyone who has provided feedback and suggestions
Code

Ini adalah README.md yang mencakup semua aspek penting dari project, termasuk:
- Fitur utama
- Panduan instalasi
- Contoh penggunaan
- Arsitektur
- Best practices
- Panduan kontribusi
- Informasi lisensi
- Detail author dan timestamp

README ini juga mengikuti best practices dokumentasi dengan:
1. Badge untuk informasi penting
2. Contoh kode yang jelas
3. Struktur yang terorganisir
4. Emoji untuk meningkatkan keterbacaan
5. Informasi kontribusi yang jelas
6. Detail teknis yang relevan

Apakah ada bagian yang perlu saya tambahkan atau perbarui?
How can I help you?
