
import httpx
from fastapi import Request

from src.common import constants


class ProxyAuthService:
    auth_service_host = f"http://{constants.AUTH_SERVICE_HOST}:8001"
    async def proxy_request(self, proxy_path: str, request: Request):
        service_url = f"{self.auth_service_host}/auth/{proxy_path}"
        print(service_url)
        async with httpx.AsyncClient() as client:
            response = await client.request(
                method=request.method,
                url=service_url,
                headers=request.headers,
                params=request.query_params,
                json=await request.json() if request.method in ("POST", "PUT") else None,
            )
            return response.json()