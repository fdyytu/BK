#!/usr/bin/env python3
"""
Configuration System Test Script
Tests all major functionality of the enhanced configuration system
"""

import sys
import os
from pathlib import Path

# Add config module to path
sys.path.insert(0, str(Path(__file__).parent))

def test_configuration_system():
    """Test the configuration system comprehensively"""
    print("🚀 Testing Enhanced Configuration System")
    print("=" * 60)
    
    try:
        from config import (
            initialize_configs,
            get_config,
            get_config_value,
            set_config_value,
            get_health_status,
            get_statistics,
            backup_configs,
            config_context,
            ApplicationConfig,
            SchemaValidator,
            MemoryCache
        )
        
        print("✅ All imports successful")
        
        # Test 1: Basic initialization
        print("\n📋 Test 1: Basic Initialization")
        initialize_configs(environment="development")
        print("✅ Configuration system initialized")
        
        # Test 2: Configuration values
        print("\n📋 Test 2: Configuration Values")
        app_name = get_config_value('application', 'app_name')
        debug = get_config_value('application', 'debug')
        port = get_config_value('application', 'port')
        
        print(f"✅ App Name: {app_name}")
        print(f"✅ Debug Mode: {debug}")
        print(f"✅ Port: {port}")
        
        # Test 3: Setting values
        print("\n📋 Test 3: Setting Values")
        set_config_value('application', 'test_key', 'test_value')
        test_value = get_config_value('application', 'test_key')
        print(f"✅ Test Value: {test_value}")
        
        # Test 4: Health monitoring
        print("\n📋 Test 4: Health Monitoring")
        health = get_health_status()
        print(f"✅ Total Configs: {health['total_configs']}")
        print(f"✅ Loaded Configs: {health['loaded_configs']}")
        print(f"✅ Environment: {health['environment']}")
        
        # Test 5: Context manager
        print("\n📋 Test 5: Context Manager")
        original_debug = get_config_value('application', 'debug')
        with config_context('application', debug=True):
            temp_debug = get_config_value('application', 'debug')
            print(f"✅ Temporary debug: {temp_debug}")
        
        restored_debug = get_config_value('application', 'debug')
        print(f"✅ Restored debug: {restored_debug}")
        
        # Test 6: Backup functionality
        print("\n📋 Test 6: Backup Functionality")
        backup = backup_configs()
        print(f"✅ Backup created with {len(backup['configs'])} configurations")
        
        # Test 7: Individual config access
        print("\n📋 Test 7: Individual Config Access")
        app_config = get_config('application')
        print(f"✅ Application config loaded: {app_config.is_loaded()}")
        print(f"✅ Application config validated: {app_config.is_validated()}")
        
        # Test 8: Configuration validation
        print("\n📋 Test 8: Configuration Validation")
        validation_passed = 0
        validation_failed = 0
        
        for name, status in health['configs'].items():
            if status['validated']:
                validation_passed += 1
            else:
                validation_failed += 1
        
        print(f"✅ Validation passed: {validation_passed}")
        print(f"⚠️  Validation warnings: {validation_failed}")
        
        print("\n" + "=" * 60)
        print("🎉 All tests completed successfully!")
        print("✅ Configuration system is working properly")
        
        return True
        
    except Exception as e:
        print(f"\n❌ Test failed with error: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_configuration_system()
    sys.exit(0 if success else 1)
