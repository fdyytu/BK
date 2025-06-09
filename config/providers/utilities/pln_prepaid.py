from typing import Dict, Any, Optional
from datetime import datetime
from ....core.base import BaseProviderImpl
from ....core.interfaces import InquiryProvider, TransactionProvider
from ....core.exceptions import ProviderError, ValidationError
from ....core.validators import ProviderValidator

class PLNPrepaidProvider(BaseProviderImpl, InquiryProvider, TransactionProvider):
    """PLN Prepaid provider implementation"""

    def __init__(
        self,
        api_key: str,
        api_secret: str,
        environment: str = "production"
    ):
        base_url = (
            "https://api.pln.co.id/v2"
            if environment == "production"
            else "https://sandbox.pln.co.id/v2"
        )
        
        super().__init__(base_url, api_key, api_secret)
        self.validator = ProviderValidator()

    async def inquiry(self, customer_id: str) -> Dict[str, Any]:
        """Inquiry PLN customer"""
        # Validate customer ID
        self.validator.validate_customer_id(customer_id, "pln")
        
        response = await self._request(
            "GET",
            "/inquiry",
            params={"customer_id": customer_id}
        )
        
        return {
            "customer_id": customer_id,
            "name": response.get("name"),
            "segment": response.get("segment"),
            "power": response.get("power"),
            "timestamp": datetime.utcnow().isoformat()
        }

    async def validate_customer(self, customer_id: str) -> bool:
        """Validate PLN customer"""
        try:
            await self.inquiry(customer_id)
            return True
        except Exception:
            return False

    async def process_transaction(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Process PLN token purchase"""
        # Validate input
        self.validator.validate_customer_id(data["customer_id"], "pln")
        self.validator.validate_amount(
            data["amount"],
            min_amount=20000,
            max_amount=1000000
        )
        
        request_data = {
            "customer_id": data["customer_id"],
            "amount": data["amount"],
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
            "token": response.get("token"),
            "amount": float(response.get("amount", 0)),
            "admin_fee": float(response.get("admin_fee", 0)),
            "status": response.get("status"),
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
            "token": response.get("token"),
            "timestamp": datetime.utcnow().isoformat()
        }