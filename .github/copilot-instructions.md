<!-- Copilot / AI agent instructions for this repository -->
# Copilot instructions — Final Prj folder

This repo contains a small ML + FastAPI assignment (penguins classifier). The goal of this file is to give AI coding agents the concrete, project-specific knowledge needed to make useful code changes quickly.

- **Big picture**: training (notebooks / scripts) -> serialize model (`model.pkl` or `model.json`) -> serve predictions via a FastAPI app in `main.py` with a POST `/predict` endpoint and Pydantic input schema. The interactive docs should be at `/docs` when the app runs.

- **Key files**:
  - `instructions.md` — authoritative assignment requirements (use this first).
  - `main.py` — current placeholder app entry; replace or extend with a FastAPI `app` instance (e.g. `app = FastAPI()`).
  - `train.ipynb` or `train.py` — training, evaluation and model serialization belong here.
  - `pyproject.toml` — dependency manifest to be used by the environment manager required by the assignment.

- **Project conventions / gotchas discovered**:
  - The assignment explicitly requires using `uv` as the Python environment / package manager (do NOT use `venv`, `pip`, or `requirements.txt`). If `uv` is not available in your environment, ask the repo owner before substituting another tool.
  - `pyproject.toml` in the repo lists packages but the file currently appears non-standard; validate it before running installs.
  - Model file should live at project root (e.g. `model.pkl`); code expects to load it at startup rather than re-training on each request.

- **API patterns to follow (examples)**:
  - FastAPI app must expose a JSON POST `/predict` endpoint that accepts a Pydantic model and returns a prediction payload.
  - Load model once at startup (module-level or via `@app.on_event("startup")`) and reuse it for requests.

- **Minimal Pydantic input example (penguins features)**:
```python
class PredictionInput(BaseModel):
    bill_length_mm: float
    bill_depth_mm: float
    flipper_length_mm: float
    body_mass_g: float
    sex: Optional[str]
    island: Optional[str]
```

- **Example predict handler**:
```python
@app.post('/predict')
def predict(payload: PredictionInput):
    # convert to feature vector, call model.predict, return {"prediction": ...}
```

- **Local dev / debug commands**:
  - Start the API (when `main.py` defines `app`):
```
uvicorn main:app --reload
```
  - Use `/docs` (Swagger UI) for manual checks.
  - Example curl POST (replace numeric fields):
```
curl -X POST "http://127.0.0.1:8000/predict" -H "Content-Type: application/json" -d '{"bill_length_mm":39.1,"bill_depth_mm":18.7,"flipper_length_mm":181,"body_mass_g":3750}'
```

- **Model & train guidance (from `instructions.md`)**:
  - Use the penguins dataset, perform stratified train/test split (`stratify=`) and evaluate with a proper metric (F1, ROC-AUC, precision/recall) — accuracy is not acceptable.
  - Serialize the final trained model to a file in the project root (`.pkl` or `.json`).

- **What to look for when editing**:
  - Ensure `main.py` exposes `app` variable (FastAPI) so `uvicorn` can import it (e.g. `main:app`).
  - Don't re-train at request time — load serialized model once.
  - Validate JSON inputs with Pydantic and return appropriate HTTP codes (400/422/500).
  - Keep deliverables consistent with `instructions.md` (EDA, train, serialized model, README usage instructions).

- **When uncertain**:
  - If you need to change the environment setup (e.g., the expected `uv` workflow or `pyproject.toml` formatting), ask the repo owner — the assignment enforces `uv` usage.

If any part of these instructions is unclear or you want me to expand examples (e.g., full FastAPI `main.py` scaffold or a minimal `train.py`), tell me which file you'd like me to create or update next.
