import aiohttp
import asyncio
from typing import Dict, Optional


class DexToolsAPI:
    BASE_URL = "https://core-api.dextools.io"
    
    def __init__(self):
        self.headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json', 
            'Sec-Fetch-Site': 'same-site',
            'Accept-Language': 'en-GB,en;q=0.9',
            'Sec-Fetch-Mode': 'cors',
            'Origin': 'https://www.dextools.io',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.5 Safari/605.1.15',
            'Referer': 'https://www.dextools.io/',
            'Connection': 'keep-alive',
            'Host': 'core-api.dextools.io',
            'Sec-Fetch-Dest': 'empty',
            'Priority': 'u=3, i',
            'X-API-Version': '1'
        }
        self.session: Optional[aiohttp.ClientSession] = None

    async def __aenter__(self):
        self.session = aiohttp.ClientSession(headers=self.headers)
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.session:
            await self.session.close()

    async def _make_request(self, endpoint: str, params: Dict = None) -> Dict:
        """Make an async HTTP request to the DexTools API"""
        if not self.session:
            raise RuntimeError("API client not initialized. Use 'async with' context manager.")
            
        async with self.session.get(
            f"{self.BASE_URL}{endpoint}",
            params=params
        ) as response:
            response.raise_for_status()
            return await response.json()

    async def get_token_race(self, lite: bool = False) -> Dict:
        """
        Get token race data from DexTools API
        
        Args:
            lite (bool): Whether to return lite version of data
            
        Returns:
            Dict: Token race data
        """
        params = {"lite": str(lite).lower()}
        return await self._make_request("/pool/listing/token-race", params)


async def get_token_race(lite: bool = False) -> Dict:
    """
    Convenience function to get token race data without managing context
    
    Args:
        lite (bool): Whether to return lite version of data
        
    Returns:
        Dict: Token race data
    """
    async with DexToolsAPI() as api:
        return await api.get_token_race(lite)
