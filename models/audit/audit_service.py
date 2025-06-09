from typing import List, Optional
from datetime import datetime
from models.audit.audit_log import AuditLog
from models.common.enums import Status

class AuditService:
    """Service for managing audit logs."""
    
    def __init__(self, database_connection):
        self._db = database_connection
    
    async def create_log(self, audit_log: AuditLog) -> AuditLog:
        """Create new audit log entry."""
        query = """
            INSERT INTO audit_logs (
                action, user_id, resource_type, resource_id,
                details, status, timestamp, metadata,
                ip_address, user_agent
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """
        values = (
            audit_log.action,
            audit_log.user_id,
            audit_log.resource_type,
            audit_log.resource_id,
            audit_log.details,
            audit_log.status.value,
            audit_log.timestamp,
            audit_log.metadata,
            audit_log.ip_address,
            audit_log.user_agent
        )
        
        result = await self._db.execute(query, values)
        audit_log.id = result.lastrowid
        return audit_log
    
    async def get_logs(self,
                      user_id: Optional[int] = None,
                      resource_type: Optional[str] = None,
                      start_date: Optional[datetime] = None,
                      end_date: Optional[datetime] = None,
                      limit: int = 100) -> List[AuditLog]:
        """Get audit logs with filtering."""
        query = "SELECT * FROM audit_logs WHERE 1=1"
        params = []
        
        if user_id:
            query += " AND user_id = ?"
            params.append(user_id)
        
        if resource_type:
            query += " AND resource_type = ?"
            params.append(resource_type)
        
        if start_date:
            query += " AND timestamp >= ?"
            params.append(start_date)
        
        if end_date:
            query += " AND timestamp <= ?"
            params.append(end_date)
        
        query += " ORDER BY timestamp DESC LIMIT ?"
        params.append(limit)
        
        results = await self._db.execute(query, params)
        return [AuditLog.from_dict(row) for row in results]