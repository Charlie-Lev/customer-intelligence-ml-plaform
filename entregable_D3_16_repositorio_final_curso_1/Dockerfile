FROM python:3.12-slim
WORKDIR /app
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
COPY requirements-api.txt .
RUN pip install --no-cache-dir \
    -r requirements-api.txt
COPY api ./api
COPY src ./src
COPY artifacts ./artifacts
COPY config ./config
COPY params.yaml .
EXPOSE 8000
CMD ["uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "8000"]
