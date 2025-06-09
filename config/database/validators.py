from typing import Any, Dict
from .exceptions import ValidationError
from .constants import COLUMN_TYPES

class DatabaseValidator:
    @staticmethod
    def validate_table_name(table_name: str) -> bool:
        """Validasi nama tabel
        
        Args:
            table_name (str): Nama tabel untuk divalidasi
            
        Returns:
            bool: True jika valid
            
        Raises:
            ValidationError: Jika nama tabel tidak valid
        """
        if not isinstance(table_name, str):
            raise ValidationError("Table name must be string")
        if not table_name.isidentifier():
            raise ValidationError("Invalid table name")
        return True

    @staticmethod
    def validate_column_type(column_type: str) -> bool:
        """Validasi tipe kolom
        
        Args:
            column_type (str): Tipe kolom untuk divalidasi
            
        Returns:
            bool: True jika valid
            
        Raises:
            ValidationError: Jika tipe kolom tidak valid
        """
        if column_type.upper() not in COLUMN_TYPES:
            raise ValidationError(f"Invalid column type: {column_type}")
        return True

    @staticmethod
    def validate_data_type(value: Any, expected_type: str) -> bool:
        """Validasi tipe data
        
        Args:
            value: Nilai untuk divalidasi
            expected_type (str): Tipe yang diharapkan
            
        Returns:
            bool: True jika valid
            
        Raises:
            ValidationError: Jika tipe data tidak valid
        """
        type_mapping = {
            "TEXT": str,
            "INTEGER": int,
            "REAL": float,
            "BOOLEAN": bool,
            "NULL": type(None)
        }
        
        if expected_type in type_mapping:
            if not isinstance(value, type_mapping[expected_type]):
                raise ValidationError(f"Expected {expected_type}, got {type(value)}")
        return True

    @staticmethod
    def validate_record(data: Dict[str, Any], schema: Dict[str, str]) -> bool:
        """Validasi record berdasarkan schema
        
        Args:
            data (Dict[str, Any]): Data untuk divalidasi
            schema (Dict[str, str]): Schema untuk validasi
            
        Returns:
            bool: True jika valid
            
        Raises:
            ValidationError: Jika data tidak valid
        """
        for field, value in data.items():
            if field not in schema:
                raise ValidationError(f"Unknown field: {field}")
            if value is not None:  # Skip validation for NULL values
                DatabaseValidator.validate_data_type(value, schema[field])
        return True