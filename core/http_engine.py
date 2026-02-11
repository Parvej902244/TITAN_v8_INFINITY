import aiohttp
import asyncio
from typing import Dict, Any

class AsyncHttpEngine:
    def __init__(self, config):
        self.config = config
        self.semaphore = asyncio.Semaphore(config['system']['max_concurrency'])
        self.headers = {'User-Agent': config['system']['user_agent']}
        self.sessions = {}
        self.contexts = config.get('auth', {}).get('contexts', [{'name': 'anon'}])

    async def start(self):
        for ctx in self.contexts:
            self.sessions[ctx['name']] = aiohttp.ClientSession(headers=self.headers)

    async def stop(self):
        for session in self.sessions.values():
            await session.close()

    async def request(self, method: str, url: str, context: str = "anon", **kwargs) -> Dict[str, Any]:
        async with self.semaphore:
            try:
                session = self.sessions.get(context, self.sessions.get('anon'))
                async with session.request(
                    method, url, 
                    timeout=self.config['system']['request_timeout'],
                    ssl=False,
                    **kwargs
                ) as response:
                    text = await response.text(errors='ignore')
                    return {
                        'status': response.status,
                        'url': str(response.url),
                        'headers': dict(response.headers),
                        'body': text,
                        'length': len(text),
                        'context': context,
                        'time': 0.1
                    }
            except Exception as e:
                return {'status': 0, 'error': str(e)}
              
