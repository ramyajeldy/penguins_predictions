def main():
    print("Hello from final-prj-folder!")

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
import pickle
import pandas as pd

app = FastAPI(title="Penguins Species Classifier API")

# Load model once at startup
with open("model.pkl", "rb") as f:
    artifacts = pickle.load(f)

model = artifacts["model"]
label_encoder = artifacts["label_encoder"]
model_columns = artifacts["columns"]
class PenguinFeatures(BaseModel):
    bill_length_mm: float = Field(..., example=43.2)
    bill_depth_mm: float = Field(..., example=17.1)
    flipper_length_mm: float = Field(..., example=201)
    body_mass_g: float = Field(..., example=4200)
    sex: str = Field(..., example="male")
    
class PredictionOutput(BaseModel):
    predicted_species: str
   
@app.post("/predict", response_model=PredictionOutput)
def predict_species(data: PenguinFeatures):
    try:
        # Convert input to DataFrame
        input_df = pd.DataFrame([data.dict()])

        # One-hot encode categorical variables
        input_df = pd.get_dummies(input_df)

        # Align columns with training data
        input_df = input_df.reindex(columns=model_columns, fill_value=0)

        # Predict
        prediction = model.predict(input_df)[0]

        # Decode label
        species = label_encoder.inverse_transform([prediction])[0]

        return PredictionOutput(predicted_species=species)

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    main()
