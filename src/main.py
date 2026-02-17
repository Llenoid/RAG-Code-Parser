import os
import httpx
import numpy as np
import pandas as pd
from pathlib import Path
from typing import cast
from dotenv import load_dotenv

from src.embedder import Embedder
from src.massager import DataMassager
from src.parser import CParser
from src.searcher import Searcher
load_dotenv()

API_KEY: str | None = os.environ.get('API_KEY')
BASE_URL: str | None = os.environ.get('BASE_URL')
MODEL_ID: str | None = os.environ.get('MODEL_ID')

def load_files_from_directory(directory_path, extension="*"):
    source_dir = Path(directory_path)
    pattern = "*" if extension == "*" else f"*.{extension}"
    files_to_load = source_dir.glob(pattern)

    loaded_data = []
    for file_path in files_to_load:
        with file_path.open('r') as f:
            content = f.read()
            loaded_data.append((file_path.name, content))
    return loaded_data

async def main():
    EM_MODEL_ID: str = os.environ.get('EMMODEL_ID', 'text-embedding-3-small')

    files = load_files_from_directory('/app/code')
    # print(f"Loaded {len(files)} files.")

    all_data = [] # Store tuples of (file_name, chunk)
    for file_name, content in files:
        parser = CParser()
        chunks = parser.parse_string(content)
        # print(f"Parsed {len(chunks)} chunks from {file_name}")
        for chunk in chunks:
            all_data.append({"file_name": file_name, "text": chunk})

    if not all_data:
        print("Warning: No chunks found by the parser.")
        return

    # Use pd.DataFrame(all_data) directly to keep file_name!
    df = pd.DataFrame(all_data)
    massager = DataMassager([]) # Dummy chunks, we'll set df manually
    massager.df = df
    massager.clean()
    massager.add_metadata()
    df = cast(pd.DataFrame, massager.df)
    
    # print(f"Dataframe after cleaning has {len(df)} rows.")
    if df.empty:
        print("Error: All chunks were filtered out. Check threshold in massager.py")
        return

    texts = cast(list[str], df["text"].to_list())

    if not API_KEY or not BASE_URL:
        print("Error: API_KEY or BASE_URL environment variables are not set.")
        print("Please check your .env file or host environment.")
        return

    embedder = Embedder(API_KEY, BASE_URL, model_id=EM_MODEL_ID)
    # print(f"Requesting embeddings for {len(texts)} chunks using model {EM_MODEL_ID}...")
    vectors = await embedder.embed_all(texts)
    df["embedding"] = vectors

    df_clean = df.dropna(subset=["embedding"]).reset_index(drop=True)
    if df_clean.empty:
        print("Error: No valid embeddings were generated. Check your code chunks and API connectivity.")
        return

    embeddings_list = cast(list[list[float]], df_clean["embedding"].to_list())
    matrix = np.stack(embeddings_list)
    searcher = Searcher(matrix)

    print("\n Code Analysis System Ready ")

    async with httpx.AsyncClient(timeout=120.0) as client:
        print("System Ready. Ask about your C Codebase")

        while True:
            print("\nAsk about your code (or 'quit' to exit):", flush=True)
            query = input("> ")
            if query.lower() in ["exit", "quit", "q"]: break

            query_list = await embedder.fetch_embeddings(client, query)

            idx = searcher.search(np.array(query_list))
            if idx == -1: continue

            row = df_clean.iloc[idx]

            answer = await ask_llm(client, row["text"], query)

            print(f"\n[{row['file_name']}]")
            print(f"--------------------")
            print(answer)

async def ask_llm(client: httpx.AsyncClient, context: str, query: str) -> str:
    system_prompt = (
        "You are a C Code Expert. "
        "Your task is to explain the provided code context. "
        "Always include the line numbers and file names when citing the code."
        "Rules:\n"
        "1. Answer only using the provided context.\n"
        "2. If the code provided does not contain the answer, respond with 'The provided context does not contain enough information to answer this question.\n"
        "3. Keep explanations technical and concise."
    )

    user_content = f"Context from Codebase: {context}\n\nQuestion: {query}"

    response = await client.post(
        f"{BASE_URL}/chat/completions",
        headers={"Authorization": f"Bearer {API_KEY}"},
        json={
            "model": MODEL_ID,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_content}
            ],
            "temperature": 0.0
        }
    )

    data = response.json()
    return str(data["choices"][0]["message"]["content"])

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
