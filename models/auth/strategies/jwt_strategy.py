from datetime import datetime, timedelta
from typing import Optional, Dict, Any
from uuid import UUID
import jwt
from ..interfaces import AuthStrategy
from ..schemas import TokenData, AuthenticatedUser
from ..exceptions import InvalidTokenError, AuthenticationError

class JWTStrategy(AuthStrategy):
    """JWT authentication strategy."""
    
    def __init__(self, 
                 secret_key: str,
                 token_expire_minutes: int = 30,
                 algorithm: str = "HS256"):
        self.secret_key = secret_key
        self.token_expire_minutes = token_expire_minutes
        self.algorithm = algorithm
        
    async def authenticate(self, credentials: Dict[str, Any]) -> AuthenticatedUser:
        """Authenticate user with username/password."""
        # Authentication logic here
        pass
        
    async def create_token(self, user_id: UUID) -> TokenData:
        """Create JWT token."""
        expires_delta = timedelta(minutes=self.token_expire_minutes)
        expire = datetime.utcnow() + expires_delta
        
        to_encode = {
            "sub": str(user_id),
            "exp": expire
        }
        
        access_token = jwt.encode(
            to_encode,
            self.secret_key,
            algorithm=self.algorithm
        )
        
        return TokenData(
            access_token=access_token,
            token_type="bearer",
            expires_at=expire
        )
        
    async def validate_token(self, token: str) -> Optional[AuthenticatedUser]:
        """Validate JWT token."""
        try:
            payload = jwt.decode(
                token,
                self.secret_key,
                algorithms=[self.algorithm]
            )
            
            user_id = UUID(payload["sub"])
            if datetime.fromtimestamp(payload["exp"]) < datetime.utcnow():
                raise InvalidTokenError("Token has expired")
                
            return AuthenticatedUser(id=user_id)
            
        except jwt.JWTError as e:
            raise InvalidTokenError(f"Invalid token: {str(e)}")