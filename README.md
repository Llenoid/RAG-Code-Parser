This is an implementation of RAG along with a parser for a C codebase.

Its purpose is to query a C codebase and have an LLM interface to ask about the codebase.

It takes in the C source code files in the `code/` directory, parses them into chunks, puts the chunks into a
dataframe, and sends them into an embedding model. We can then get the user query, parse it, send it to the same
embedding model so that we can "relate" the query with the embedded documents we sent to the embedding model. We then
use an LLM to generate responses based on the results.

Since we can't go by token-length, character-length, or line count without cutting off some chunks of a function. We use
the parser to preserve semantic meaning and make the input we send the embedding model complete and coherent.

To run it:
`.env` file example (replace with local model or with model running in the cloud)
```env
BASE_URL=<openai.com>
API_KEY=<your-api-key>
MODEL_ID=<gpt-4o>
EMMODEL_ID=<text-embedding>
```
Make a `code/` directory
Put source code inside `code/` directory (can put multiple C files).

Run with
```sh
make run
```

Run tests:
```sh
make test
```
