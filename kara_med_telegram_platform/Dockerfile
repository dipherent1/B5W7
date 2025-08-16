FROM python:3.11-slim

WORKDIR /workspace

# system deps
RUN apt-get update && apt-get install -y build-essential git curl libgl1 && rm -rf /var/lib/apt/lists/*

# python deps
COPY requirements.txt /workspace/requirements.txt
RUN pip install --no-cache-dir -r /workspace/requirements.txt

# app code
COPY . /workspace

# env
ENV PYTHONUNBUFFERED=1     PIP_DISABLE_PIP_VERSION_CHECK=1     DBT_PROFILES_DIR=/workspace/dbt

EXPOSE 8000 3000

CMD ["/bin/bash", "-lc", "uvicorn app.main:app --host 0.0.0.0 --port 8000"]
