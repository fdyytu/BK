class DatabaseError(Exception):
    """Base class untuk semua error database"""
    pass

class ConnectionError(DatabaseError):
    """Error saat koneksi database"""
    pass

class QueryError(DatabaseError):
    """Error saat eksekusi query"""
    pass

class ValidationError(DatabaseError):
    """Error untuk validasi data"""
    pass

class MigrationError(DatabaseError):
    """Error saat migrasi database"""
    pass

class IntegrityError(DatabaseError):
    """Error untuk integrity constraint"""
    pass