# Assignment: ML Model Deployment with FastAPI

## Overview
Building off your previous assignment, you will train a simple classification model and deploy it as a REST API endpoint using FastAPI. This assignment focuses on the deployment pipeline rather than modeling techniques.

You are expected to use `uv` as your virtual environemnt manager and python package manager. Do not use `venv` and do not use `pip` nor a `requirements.txt`. You should have a `pyproject.toml` file. 

## Learning Objectives
- Train and serialize a machine learning model
- Create a production-ready API endpoint with proper data validation
- Implement error handling and graceful failure patterns
- Use Pydantic for data contract definition

## Prerequisites
- Completion of previous FastAPI project
- Familiarity with scikit-learn or similar ML libraries
- Basic understanding of classification problems

---

## Part 1: Model Training

### 1.1 Data Preparation
- Load your dataset. It is the penguins dataset 

```python
import seaborn as sns
penguins = sns.load_dataset("penguins")
```


- Split data into features (X) and target (y)
- Create train/test split using **stratified sampling** (use `stratify` parameter)

### 1.2 Exploratory Data Analysis (Minimal)
Perform **only** the following basic checks:
- **Visualizations:**
  - Histogram of the target variable
  - Histograms of 2-3 key features
- **Data inspection:**
  - Check data types (`.dtypes`)
  - Run `.describe()`, `.info()`, and check for missing values (`.isna().sum()`)
  - Identify if categorical encoding is needed

### 1.3 Model Training
- **Select ONE model:** XGBoost, CatBoost, or any sklearn classification model
- **Use default hyperparameters** (no tuning required)
- **Use all features** (no feature selection/engineering required)
- Train on X_train and y_train

### 1.4 Model Evaluation
- Evaluate on **both** training and test sets
- **Do NOT use accuracy** — choose an appropriate metric (e.g., F1-score, ROC-AUC, precision/recall)
- **Determine if the model is overfitting** and document your reasoning
  - ⚠️ **Important:** Incorrect overfitting assessment will result in grade deductions

### 1.5 Model Serialization
- Save your trained model as a `.pkl` (pickle) or `.json` file to your project directory

---

## Part 2: FastAPI Endpoint Development

### 2.1 Required Components

**Pydantic Data Contract:**
- Define input schema using Pydantic models
- Include appropriate data types and validation rules

**Model Loading:**
- Load your serialized model at application startup

**Prediction Endpoint:**
- Create a POST endpoint that accepts feature data and returns predictions
- Load the model and generate predictions

**Error Handling:**
- Handle invalid payloads gracefully
- Return appropriate HTTP error codes (e.g., 400, 422, 500)
- Provide meaningful error messages

### 2.2 Example Structure
```python
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

class PredictionInput(BaseModel):
    # Define your features here
    feature1: float
    feature2: str
    # ...

class PredictionOutput(BaseModel):
    prediction: int  # or float
    # Optional: probability, confidence, etc.

@app.post("/predict", response_model=PredictionOutput)
async def predict(input_data: PredictionInput):
    try:
        # Your prediction logic
        pass
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
```

---

## Deliverables

Submit the following:
1. **Jupyter Notebook or Python script** containing:
   - Data loading and splitting
   - EDA (histograms, data inspection)
   - Model training and evaluation
   - Overfitting analysis
   
2. **FastAPI application** (`main.py` or similar) with:
   - Pydantic models
   - Prediction endpoint
   - Error handling

3. **Serialized model file** (`.pkl` or `.json`)

4. **README.md** documenting:
   - How to run your code
   - Dataset used
   - Model chosen and evaluation metrics
   - Overfitting assessment

---

## Recommended Project Structure
├── train.py or train.ipynb 
├── main.py                  # FastAPI app
├── model.pkl or model.json  # Saved model
├── pyproject.toml
└── README.md

---

## Grading Criteria

| Component | Points |
|-----------|--------|
| Proper data splitting (with stratification) | 10% |
| Basic EDA completed | 10% |
| Model training and serialization | 20% |
| Correct evaluation metrics used | 15% |
| **Correct overfitting assessment** | 10% |
| Pydantic data validation | 15% |
| Error handling implementation | 10% |
| Using `uv` for your project | 10% |


**You are also expected to submit a 5 minute demo, walking me through your project**. Use the `docs` endpoint to show me how to make a prediction. 

If you read from a script word by word you will be **heavily penalized**. Speak naturally, tell me what you learned, it's only to trip over your words, this is **not** a Ted Talk.

---

## Tips
- Start with Part 1 (model training) before building the API
- Swagger UI at http://127.0.0.1:8000/docs
- Consider what happens if someone sends the wrong data type or missing features

## Resources
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Pydantic Documentation](https://docs.pydantic.dev/)


