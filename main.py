from fastapi import FastAPI, HTTPException, Request, status
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from pydantic import BaseModel, Field
from typing import Literal
import logging
import pandas as pd
import pickle


# Initialize FastAPI app

app = FastAPI(title="Penguins Species Prediction API")


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={"error": "validation_error", "detail": exc.errors(), "body": exc.body},
    )


@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"error": "http_error", "detail": exc.detail},
    )


@app.exception_handler(Exception)
async def generic_exception_handler(request: Request, exc: Exception):
    logging.exception("Unhandled exception: %s", exc)
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"error": "internal_server_error", "detail": "An internal error occurred."},
    )


# Load trained model artifacts

try:
    with open("model.pkl", "rb") as f:
        artifacts = pickle.load(f)
        model = artifacts["model"]
        label_encoder = artifacts["label_encoder"]
        model_columns = artifacts["columns"]
except Exception as e:
    raise RuntimeError(f"Failed to load model artifacts: {e}")


# Input Schema (matches instructions format)

class PredictionInput(BaseModel):
    island: Literal["Biscoe", "Dream", "Torgersen"] = Field(..., example="Biscoe", description="Island where the penguin was observed")
    bill_length_mm: float = Field(..., gt=0, example=45.1, description="Bill length in millimetres; must be positive")
    bill_depth_mm: float = Field(..., gt=0, example=14.5, description="Bill depth in millimetres; must be positive")
    flipper_length_mm: int = Field(..., gt=0, example=210, description="Flipper length in millimetres; must be positive integer")
    body_mass_g: int = Field(..., gt=0, example=4500, description="Body mass in grams; must be positive integer")
    sex: Literal["male", "female"] = Field(..., example="male", description="Sex of the penguin (male/female)")


# Output Schema (matches instructions format)

class PredictionOutput(BaseModel):
    prediction: str   # predicted penguin species


# Prediction Endpoint

@app.post("/predict", response_model=PredictionOutput)
async def predict(input_data: PredictionInput):
    try:
        # Convert input to DataFrame
        input_df = pd.DataFrame([input_data.dict()])

        # One-hot encode categorical variables
        input_df = pd.get_dummies(input_df)

        # Align with training columns
        input_df = input_df.reindex(columns=model_columns, fill_value=0)

        # Model prediction
        pred_numeric = model.predict(input_df)[0]

        # Decode numeric label to species name
        pred_label = label_encoder.inverse_transform([pred_numeric])[0]

        return PredictionOutput(prediction=pred_label)

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
