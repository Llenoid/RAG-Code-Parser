from typing import Any, cast
import httpx
import asyncio

class Embedder:
    def __init__(self, api_key: str, base_url: str) -> None:
        self.api_key = api_key
        self.base_url = base_url

    async def fetch_embeddings(self, client: httpx.AsyncClient, text: str) -> list[float]:
        response = await client.post(
            f"{self.base_url}/embeddings",
            headers={"Authorization": f"Bearer {self.api_key}"},
            json={"input": text, "model": "text-embedding-3-small"}
        )
        data = cast(dict[str, Any], response.json())
        embedding = data["data"][0]["embedding"]
        return cast(list[float], embedding)

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

