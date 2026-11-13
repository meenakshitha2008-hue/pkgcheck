FROM python:3.14-slim
WORKDIR /code
COPY requirements-api.txt .
RUN pip install --no-cache-dir -r requirements-api.txt
COPY app.py db.py ./
COPY models ./models
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]