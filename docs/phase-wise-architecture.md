# Phase-Wise Architecture

## Blueprint

| Phase | Goal | Core Components | Input | Output |
|---|---|---|---|---|
| 0. Scope and foundations | Lock boundaries and setup | repo setup, env config, dataset contract, non-goals | project idea + constraints | clear scope and runnable skeleton |
| 1. Data ingestion | Build clean data layer | dataset loader, normalizer, schema mapper | raw Hugging Face dataset | canonical `Restaurant` records |
| 2. Preferences and validation | Capture user intent safely | preference model, validators, parser | user input from UI/API/CLI | validated `UserPreferences` |
| 3. Retrieval and prompt assembly | Prepare high-quality LLM context | deterministic filters, candidate ranking hint, prompt builder | restaurant records + preferences | `candidates[]` and `prompt_payload` |
| 4. LLM recommendation engine | Produce grounded recommendations | LLM client, parser, retries, fallback | prompt payload + candidate list | ranked recommendations + explanations |
| 5. Output and experience | Present useful results | renderer, empty/error states, light observability | ranked recommendations | user-facing response |
| 6. Hardening and handoff | Improve reliability and maintainability | tests, docs, performance tuning | completed pipeline | release-ready milestone |

## Runtime Layers

```text
UI/CLI
  -> Preference Validation Layer
  -> Deterministic Retrieval Layer
  -> Prompt Builder + LLM Layer
  -> Response Parser + Fallback Layer
  -> Presentation Layer
```

## Deliverables by Phase
- Phase 0: setup docs, `.env.example`, dataset contract
- Phase 1: ingestion module and normalization tests
- Phase 2: validated preferences model and clear error messages
- Phase 3: filter pipeline and prompt builder
- Phase 4: LLM integration with structured output parsing
- Phase 5: output formatting and basic logging
- Phase 6: expanded tests, runbook, and optimization notes
