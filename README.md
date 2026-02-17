`.env` file example (replace with local model or with model running in the cloud)
```env
BASE_URL=<openai.com>
API_KEY=<your-api-key>
MODEL_ID=<gpt-4o>
EMMODEL_ID=<text-embedding>
```

Put source code inside `code/` directory (can put multiple C files).

Run with
```sh
make run
```
