from typing import Dict, Type
from .game_service_base import GameServiceBase
from .topup import GameTopup

class GameServiceFactory:
    """Factory for creating game service instances."""
    
    _services: Dict[str, Type[GameServiceBase]] = {
        'topup': GameTopup
    }
    
    @classmethod
    def create(cls,
               service_type: str,
               api_key: str,
               merchant_id: str,
               sandbox: bool = False) -> GameServiceBase:
        """Create game service instance."""
        service_class = cls._services.get(service_type.lower())
        
        if not service_class:
            raise ValueError(f"Unsupported service type: {service_type}")
            
        return service_class(api_key, merchant_id, sandbox)
        
    @classmethod
    def register_service(cls,
                        service_type: str,
                        service_class: Type[GameServiceBase]) -> None:
        """Register new game service."""
        cls._services[service_type.lower()] = service_class