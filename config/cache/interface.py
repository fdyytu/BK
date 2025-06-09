from abc import ABC, abstractmethod
from typing import Any, Optional, Union
from datetime import timedelta

class CacheInterface(ABC):
    """Interface dasar untuk implementasi cache"""
    
    @abstractmethod
    def get(self, key: str, default: Any = None) -> Any:
        """Mengambil data dari cache"""
        pass
    
    @abstractmethod
    def set(
        self, 
        key: str, 
        value: Any, 
        timeout: Optional[Union[int, timedelta]] = None
    ) -> bool:
        """Menyimpan data ke cache"""
        pass
    
    @abstractmethod
    def delete(self, key: str) -> bool:
        """Menghapus data dari cache"""
        pass
    
    @abstractmethod
    def clear(self) -> bool:
        """Menghapus semua data cache"""
        pass
    
    @abstractmethod
    def get_many(self, keys: list) -> dict:
        """Mengambil multiple data dari cache"""
        pass
    
    @abstractmethod
    def set_many(self, mapping: dict, timeout: Optional[Union[int, timedelta]] = None) -> bool:
        """Menyimpan multiple data ke cache"""
        pass
    
    @abstractmethod
    def delete_many(self, keys: list) -> bool:
        """Menghapus multiple data dari cache"""
        pass

    @abstractmethod
    def incr(self, key: str, delta: int = 1) -> int:
        """Increment nilai cache"""
        pass

    @abstractmethod
    def decr(self, key: str, delta: int = 1) -> int:
        """Decrement nilai cache"""
        pass