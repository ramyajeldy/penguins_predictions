# Use official Python image
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Copy dependency files
# Copy dependency files
COPY pyproject.toml uv.lock ./

# Install dependencies directly with pip (avoid using an unavailable/misused `uv` command)
# Using explicit package list ensures Docker build doesn't rely on an external 'uv' tool.
RUN pip install --no-cache-dir \
	scikit-learn pandas numpy matplotlib seaborn \
	fastapi[standard] uvicorn[standard] pydantic xgboost

# Copy application files
COPY main.py model.pkl ./

# Expose FastAPI port
EXPOSE 8000

# Run the FastAPI app
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
