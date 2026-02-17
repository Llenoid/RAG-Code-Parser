import os
from typing import Any, cast
import httpx
import asyncio

EMMODEL_ID: str | None = os.environ.get('EMMODEL_ID')

class Embedder:
    def __init__(self, api_key: str, base_url: str, model_id: str = "text-embedding-3-small") -> None:
        self.api_key = api_key
        self.base_url = base_url
        self.model_id = model_id

    async def fetch_embeddings(self, client: httpx.AsyncClient, text: str) -> list[float]:
        response = await client.post(
            f"{self.base_url}/embeddings",
            headers={"Authorization": f"Bearer {self.api_key}"},
            json={"input": text, "model": self.model_id}
        )
        if response.status_code != 200:
            print(f"API Error: {response.status_code} - {response.text}")
            return []
            
        data = cast(dict[str, Any], response.json())
        embedding = data["data"][0]["embedding"]
        return embedding

    async def embed_all(self, texts: list[str]) -> list[list[float] | None]:
        async with httpx.AsyncClient() as client:
            tasks = [self.fetch_embeddings(client, text) for text in texts]
            results = await asyncio.gather(*tasks, return_exceptions=True)
            final_embeddings: list[list[float] | None] = []
            for res in results:
                if isinstance(res, BaseException):
                    print(f"Embedding failed: {res}")
                    final_embeddings.append(None)
                else:
                    final_embeddings.append(res)

            return final_embeddings

