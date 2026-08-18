from fastapi import FastAPI

app = FastAPI(title="kajilog")


@app.get("/api/health")
def health():
    return {"status": "ok"}
