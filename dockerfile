FROM python:3.13-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy your app files (py + html)
COPY . .

# Cloud Run listens on 8080
ENV PORT=8080

# Start FastAPI
CMD ["uvicorn", "scrap_data:app", "--host", "0.0.0.0", "--port", "8080"]
