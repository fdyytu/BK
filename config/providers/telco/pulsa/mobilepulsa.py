from typing import Dict, Any, Optional
from datetime import datetime
from ....core.base import BaseProviderImpl
from ....core.interfaces import TransactionProvider
from ....core.exceptions import ProviderError, ValidationError
from ....core.validators import ProviderValidator

class MobilePulsaProvider(BaseProviderImpl, TransactionProvider):
    """MobilePulsa provider implementation"""

    def __init__(
        self,
        api_key: str,
        api_secret: str,
        environment: str = "production"
    ):
        base_url = (
            "https://api.mobilepulsa.net/v1"
            if environment == "production"
            else "https://testapi.mobilepulsa.net/v1"
        )
        
        super().__init__(base_url, api_key, api_secret)
        self.validator = ProviderValidator()

    async def check_health(self) -> Dict[str, Any]:
        """Check provider health status"""
        try:
            response = await self._request("GET", "/balance")
            return {
                "status": "healthy",
                "timestamp": datetime.utcnow().isoformat(),
                "details": response
            }
        except Exception as e:
            return {
                "status": "unhealthy",
                "timestamp": datetime.utcnow().isoformat(),
                "error": str(e)
            }

    async def check_balance(self) -> Dict[str, float]:
        """Check provider balance"""
        response = await self._request("GET", "/balance")
        return {
            "balance": float(response.get("balance", 0)),
            "timestamp": datetime.utcnow().isoformat()
        }

    async def check_price(self, product_code: str) -> Dict[str, Any]:
        """Check product price"""
        # Validate product code
        self.validator.validate_product_code(product_code, "PULSE")
        
        response = await self._request(
            "GET",
            "/price",
            params={"code": product_code}
        )
        
        return {
            "product_code": product_code,
            "price": float(response.get("price", 0)),
            "selling_price": float(response.get("selling_price", 0)),
            "status": response.get("status"),
            "timestamp": datetime.utcnow().isoformat()
        }

    async def process_transaction(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Process pulsa transaction"""
        # Validate input
        self.validator.validate_phone(data["phone"])
        self.validator.validate_product_code(data["product_code"], "PULSE")
        
        request_data = {
            "phone": data["phone"],
            "product_code": data["product_code"],
            "ref_id": data["ref_id"],
            "signature": self._generate_signature(data)
        }
        
        response = await self._request(
            "POST",
            "/transaction",
            data=request_data
        )
        
        return {
            "provider_ref": response.get("ref_id"),
            "status": response.get("status"),
            "message": response.get("message"),
            "price": float(response.get("price", 0)),
            "balance": float(response.get("balance", 0)),
            "timestamp": datetime.utcnow().isoformat()
        }

    async def check_status(self, ref_id: str) -> Dict[str, Any]:
        """Check transaction status"""
        response = await self._request(
            "GET",
            "/transaction-status",
            params={"ref_id": ref_id}
        )
        
        return {
            "ref_id": ref_id,
            "status": response.get("status"),
            "message": response.get("message"),
            "timestamp": datetime.utcnow().isoformat()
        }

    async def validate_credentials(self) -> bool:
        """Validate provider credentials"""
        try:
            await self.check_balance()
            return True
        except Exception:
            return False

    def _generate_signature(self, data: Dict[str, Any]) -> str:
        """Generate request signature"""
        signature_data = f"{data['ref_id']}{self.api_secret}"
        return hashlib.md5(signature_data.encode()).hexdigest()