FROM python:3.11-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt

COPY . /app

EXPOSE 8000

# NOTE: MT5 integration typically requires a Wine bridge; for containerized dev/CI
# set MT5_DISABLE=true to skip MT5 connect on startup.
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]

