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
│   │   ├── phase1/
│   │   │   └── ingestion/
│   │   ├── phase2/
│   │       └── preferences/
│   │   └── phase3/
│   │       └── retrieval/
│   │   └── phase4/
│   │       └── recommendation/
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

## Phase 2 Command

- Validate and parse preferences:
  - `python src/main.py phase2-prefs-parse --location Delhi --budget medium --cuisines "North Indian, Chinese" --minimum-rating 4.0`
- Validate city against loaded dataset cities:
  - `python src/main.py phase2-prefs-parse --location Bangalore --budget low --cuisines "Chinese" --minimum-rating 3.5 --validate-city --city-source sample`

## Phase 3 Command

- Run deterministic retrieval + prompt assembly:
  - `python src/main.py phase3-retrieve-smoke --location Delhi --budget medium --cuisines "North Indian" --minimum-rating 4.0 --source sample --candidate-cap 10 --top-k 5`

## Phase 4 Command (Groq LLM)

- Set environment key first:
  - `set GROQ_API_KEY=your_key_here`
- Run LLM recommendation with fallback:
  - `python src/main.py phase4-recommend-smoke --location Delhi --budget medium --cuisines "North Indian" --minimum-rating 4.0 --source sample --candidate-cap 10 --top-k 5`
