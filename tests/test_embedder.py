import pytest
import respx
import httpx
from httpx import Response
from src.embedder import Embedder

@pytest.mark.asyncio
@respx.mock
async def test_embedder_concurrency():
    base_url = "http://api.openai.com/v1"
    respx.post(f"{base_url}/embeddings").mock(return_value=Response(200, json={
        "data": [{"embedding": [0.1, 0.2, 0.3]}]
    }))
    texts = ["void func() {}", "void func2() {}"]

    embedder = Embedder(api_key="fake", base_url=base_url)

    embeddings = await embedder.embed_all(texts)

    assert len(embeddings) == 2
    assert isinstance(embeddings[0], list)
    assert embeddings[0][0] == 0.1

@pytest.mark.asyncio
@respx.mock
async def test_embedder_handles_timeout():
    base_url = "http://api.openai.com/v1"
    respx.post(f"{base_url}/embeddings").mock(side_effect=httpx.ConnectTimeout("Connection timed out"))

    texts = ["func1", "func2"]

    embedder = Embedder(api_key="fake", base_url=base_url)

    results = await embedder.embed_all(texts)

    assert len(results) == 2
    assert results[0] is None
    assert results[1] is None
