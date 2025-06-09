from typing import List, Dict, Any
from .connection import DatabaseConnection

def dict_factory(cursor: Any, row: tuple) -> Dict:
    """Convert database row to dictionary
    
    Args:
        cursor: Database cursor
        row: Database row
        
    Returns:
        Dict: Row as dictionary
    """
    fields = [column[0] for column in cursor.description]
    return {key: value for key, value in zip(fields, row)}

def execute_script(filename: str) -> None:
    """Execute SQL script file
    
    Args:
        filename (str): Path to SQL script file
    """
    db = DatabaseConnection()
    with open(filename, 'r') as sql_file:
        sql_script = sql_file.read()
        db.execute_query(sql_script)

def check_database_exists() -> bool:
    """Check if database file exists
    
    Returns:
        bool: True if exists, False otherwise
    """
    from .settings import DB_PATH
    return os.path.exists(DB_PATH)