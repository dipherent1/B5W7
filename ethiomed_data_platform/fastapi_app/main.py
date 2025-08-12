from fastapi import FastAPI

app = FastAPI(title="Ethiomed Analytical API")

@app.get("/")
def root():
    return {"message": "Ethiomed API is running"}
