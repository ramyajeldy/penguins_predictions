Run the code using "uv run fastapi dev main.py" or http://localhost:8000/docs#/default/predict_predict_post to see the predictions on FastAPI
I have built a docker image and containerized the dependencies and deployed as a service on a free cloud platform render.com where you can check the predictions.
I have used uv for dependency management and environment consistency as instructed 

I have used the "penguins" dataset as provided
stratify=y is applied to match the train data and test data with the original dataset.

XGBoost classifier model was chosen as it works well with multi-classification problems
Evaluation metrics - f1-score is chosen over accuracy as it is harmonic mean of precision and recall values 

Exceptions have been handled gracefully with a default 422 error so that there is a response whenever the input given is not in a right

Overfitting assessment: The model is not overfitting but generalizes well as it performs well with both training data and test data.
I have plotted train data set and test data F1-score using bar plot and assessed and I observed that both are same, it suggests that the model is not overfitting.