# My Project

AI-powered restaurant recommendation system (Zomato use case).

## Project Structure

```text
My_Project/
├── docs/
│   ├── projectquery.md
│   ├── phase-wise-architecture.md
│   ├── phase0-scope.md
│   ├── dataset-contract.md
│   └── edge-cases.md
├── src/
│   ├── phases/
│   │   ├── phase0/
│   │   │   └── foundation.py
│   │   └── phase1/
│   │       └── ingestion/
│   └── main.py
├── tests/
├── scripts/
├── .env.example
└── README.md
```

## Notes
- Keep product/problem documents in `docs/`.
- Keep implementation code grouped by phase in `src/phases/`.
- Keep tests in `tests/` and helper automation in `scripts/`.

## Phase 0 Commands

- Show setup info:
  - `python src/main.py info`
- Run foundation checks:
  - `python src/main.py doctor`

## Phase 1 Command

- Run ingestion smoke check with local sample data:
  - `python src/main.py phase1-ingest-smoke --source sample --limit 5`
- Run ingestion smoke check with Hugging Face dataset (requires `datasets` package):
  - `python src/main.py phase1-ingest-smoke --source hf --split train --limit 20`
