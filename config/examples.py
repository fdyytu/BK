"""
Configuration System Usage Examples
Demonstrates how to use the enhanced configuration system
"""

import os
import sys
from pathlib import Path

# Add config module to path
sys.path.insert(0, str(Path(__file__).parent))

from config import (
    initialize_configs,
    get_config,
    get_config_value,
    set_config_value,
    create_config_builder,
    config_context,
    config_required,
    with_config,
    get_health_status,
    backup_configs,
    ApplicationConfig,
    SchemaValidator,
    FileLoader,
    MemoryCache
)

def basic_usage_example():
    """Basic configuration usage example"""
    print("=== Basic Usage Example ===")
    
    # Initialize configurations
    initialize_configs(environment="development")
    
    # Get configuration values
    app_name = get_config_value('application', 'app_name')
    debug_mode = get_config_value('application', 'debug', False)
    db_host = get_config_value('database', 'host', 'localhost')
    
    print(f"App Name: {app_name}")
    print(f"Debug Mode: {debug_mode}")
    print(f"Database Host: {db_host}")
    
    # Set configuration values
    set_config_value('application', 'custom_setting', 'custom_value')
    custom_value = get_config_value('application', 'custom_setting')
    print(f"Custom Setting: {custom_value}")

def advanced_usage_example():
    """Advanced configuration usage with builder pattern"""
    print("\n=== Advanced Usage Example ===")
    
    # Create custom configuration using builder pattern
    validator = SchemaValidator({
        'api_key': {'type': str, 'required': True},
        'timeout': {'type': int, 'min': 1, 'max': 300}
    })
    
    loader = FileLoader()
    cache = MemoryCache()
    
    builder = create_config_builder(ApplicationConfig)
    custom_config = (builder
                    .with_validator(validator)
                    .with_loader(loader)
                    .with_cache(cache)
                    .build())
    
    # Set some values
    custom_config.set('api_key', 'test-api-key-123')
    custom_config.set('timeout', 30)
    
    print(f"API Key: {custom_config.get('api_key')}")
    print(f"Timeout: {custom_config.get('timeout')}")
    print(f"Config loaded: {custom_config.is_loaded()}")
    print(f"Config validated: {custom_config.is_validated()}")

def context_manager_example():
    """Configuration context manager example"""
    print("\n=== Context Manager Example ===")
    
    # Get original debug value
    original_debug = get_config_value('application', 'debug')
    print(f"Original debug value: {original_debug}")
    
    # Use context manager to temporarily change configuration
    with config_context('application', debug=False, test_mode=True):
        temp_debug = get_config_value('application', 'debug')
        test_mode = get_config_value('application', 'test_mode')
        print(f"Temporary debug value: {temp_debug}")
        print(f"Temporary test mode: {test_mode}")
    
    # Values should be restored
    restored_debug = get_config_value('application', 'debug')
    test_mode_after = get_config_value('application', 'test_mode')
    print(f"Restored debug value: {restored_debug}")
    print(f"Test mode after context: {test_mode_after}")

def decorator_examples():
    """Configuration decorator examples"""
    print("\n=== Decorator Examples ===")
    
    @config_required('application', 'app_name')
    def function_requiring_config():
        app_name = get_config_value('application', 'app_name')
        return f"Function executed with app: {app_name}"
    
    @with_config('database')
    def function_with_injected_config(config=None):
        if config:
            host = config.get('host')
            port = config.get('port')
            return f"Database connection: {host}:{port}"
        return "No config injected"
    
    try:
        result1 = function_requiring_config()
        print(f"Required config result: {result1}")
        
        result2 = function_with_injected_config()
        print(f"Injected config result: {result2}")
    except Exception as e:
        print(f"Decorator error: {e}")

def monitoring_example():
    """Configuration monitoring example"""
    print("\n=== Monitoring Example ===")
    
    # Get health status
    health = get_health_status()
    print(f"Total configs: {health['total_configs']}")
    print(f"Loaded configs: {health['loaded_configs']}")
    print(f"Environment: {health['environment']}")
    
    # Show individual config status
    for name, status in health['configs'].items():
        print(f"  {name}: loaded={status['loaded']}, validated={status['validated']}, keys={status['keys_count']}")

def backup_restore_example():
    """Configuration backup and restore example"""
    print("\n=== Backup & Restore Example ===")
    
    # Create backup
    backup = backup_configs()
    print(f"Backup created at: {backup['timestamp']}")
    print(f"Backup environment: {backup['environment']}")
    print(f"Configs in backup: {len(backup['configs'])}")
    
    # Modify a configuration
    original_port = get_config_value('application', 'port')
    set_config_value('application', 'port', 9999)
    modified_port = get_config_value('application', 'port')
    
    print(f"Original port: {original_port}")
    print(f"Modified port: {modified_port}")
    
    # Note: In a real scenario, you would restore from backup
    # restore_configs(backup)
    # restored_port = get_config_value('application', 'port')
    # print(f"Restored port: {restored_port}")

def error_handling_example():
    """Configuration error handling example"""
    print("\n=== Error Handling Example ===")
    
    try:
        # Try to get non-existent configuration
        non_existent = get_config('non_existent_config')
    except Exception as e:
        print(f"Expected error for non-existent config: {e}")
    
    try:
        # Try to get non-existent value with default
        value = get_config_value('application', 'non_existent_key', 'default_value')
        print(f"Non-existent key with default: {value}")
    except Exception as e:
        print(f"Unexpected error: {e}")
    
    try:
        # Try to set invalid value (if validator is present)
        app_config = get_config('application')
        app_config.set('port', 'invalid_port')  # Should be integer
    except Exception as e:
        print(f"Expected validation error: {e}")

def environment_specific_example():
    """Environment-specific configuration example"""
    print("\n=== Environment-Specific Example ===")
    
    environments = ['development', 'testing', 'production']
    
    for env in environments:
        print(f"\n--- {env.upper()} Environment ---")
        try:
            # Reinitialize with different environment
            initialize_configs(environment=env)
            
            debug = get_config_value('application', 'debug', False)
            host = get_config_value('application', 'host', 'localhost')
            db_ssl = get_config_value('database', 'ssl_mode', 'disable')
            
            print(f"Debug: {debug}")
            print(f"Host: {host}")
            print(f"DB SSL: {db_ssl}")
            
        except Exception as e:
            print(f"Error loading {env} config: {e}")

def performance_example():
    """Configuration performance example"""
    print("\n=== Performance Example ===")
    
    import time
    
    # Test configuration access performance
    start_time = time.time()
    
    for i in range(1000):
        app_name = get_config_value('application', 'app_name')
        debug = get_config_value('application', 'debug')
        port = get_config_value('application', 'port')
    
    end_time = time.time()
    duration = end_time - start_time
    
    print(f"1000 config accesses took: {duration:.4f} seconds")
    print(f"Average per access: {(duration/1000)*1000:.4f} ms")

def main():
    """Run all examples"""
    print("Configuration System Examples")
    print("=" * 50)
    
    try:
        basic_usage_example()
        advanced_usage_example()
        context_manager_example()
        decorator_examples()
        monitoring_example()
        backup_restore_example()
        error_handling_example()
        environment_specific_example()
        performance_example()
        
        print("\n" + "=" * 50)
        print("All examples completed successfully!")
        
    except Exception as e:
        print(f"\nExample failed with error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
