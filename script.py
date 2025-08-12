import os

# Project root folder
PROJECT_NAME = "ethiomed_data_platform"

# Folder structure definition
structure = [
    f"{PROJECT_NAME}/data/raw/telegram_messages",  # Data Lake raw zone
    f"{PROJECT_NAME}/data/processed",              # Processed data
    f"{PROJECT_NAME}/dbt_project/models/staging",  # DBT staging models
    f"{PROJECT_NAME}/dbt_project/models/marts",    # DBT mart models
    f"{PROJECT_NAME}/dbt_project/tests",           # DBT tests
    f"{PROJECT_NAME}/fastapi_app",                 # FastAPI app root
    f"{PROJECT_NAME}/fastapi_app/routers",         # API routers
    f"{PROJECT_NAME}/fastapi_app/schemas",         # Pydantic schemas
    f"{PROJECT_NAME}/fastapi_app/crud",            # CRUD/query logic
    f"{PROJECT_NAME}/pipeline/orchestration",      # Dagster pipelines
    f"{PROJECT_NAME}/pipeline/scripts",            # Individual scripts
    f"{PROJECT_NAME}/yolo",                        # YOLO scripts/models
    f"{PROJECT_NAME}/docker",                      # Docker configs
    f"{PROJECT_NAME}/docs",                        # Documentation
]

# Files to create with default content
files = {
    f"{PROJECT_NAME}/.gitignore": """# Python
__pycache__/
*.pyc
*.pyo
*.pyd

# Env
.env

# Data
data/

# Docker
*.log
""",
    f"{PROJECT_NAME}/requirements.txt": """telethon
python-dotenv
psycopg2-binary
dbt-postgres
ultralytics
fastapi
uvicorn
dagster
dagster-webserver
pydantic
""",
    f"{PROJECT_NAME}/Dockerfile": """FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["uvicorn", "fastapi_app.main:app", "--host", "0.0.0.0", "--port", "8000"]
""",
    f"{PROJECT_NAME}/docker-compose.yml": """version: '3.8'

services:
  app:
    build: .
    env_file: .env
    ports:
      - "8000:8000"
    depends_on:
      - db
  db:
    image: postgres:15
    environment:
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: postgres
      POSTGRES_DB: ethiomed
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data

volumes:
  postgres_data:
""",
    f"{PROJECT_NAME}/.env.example": """# Rename to .env and set actual values
TELEGRAM_API_ID=your_api_id
TELEGRAM_API_HASH=your_api_hash
DATABASE_URL=postgresql://postgres:postgres@db:5432/ethiomed
""",
    f"{PROJECT_NAME}/fastapi_app/main.py": """from fastapi import FastAPI

app = FastAPI(title="Ethiomed Analytical API")

@app.get("/")
def root():
    return {"message": "Ethiomed API is running"}
""",
    f"{PROJECT_NAME}/README.md": f"# {PROJECT_NAME}\n\nData platform for Ethiopian medical business insights."
}

def create_structure():
    for folder in structure:
        os.makedirs(folder, exist_ok=True)
        # Add __init__.py for Python packages
        if "fastapi_app" in folder or "pipeline" in folder or "yolo" in folder:
            init_file = os.path.join(folder, "__init__.py")
            open(init_file, "a").close()

    for filepath, content in files.items():
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        with open(filepath, "w") as f:
            f.write(content)

    print(f"✅ Project structure for '{PROJECT_NAME}' created successfully!")

if __name__ == "__main__":
    create_structure()
