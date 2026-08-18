from fastapi import FastAPI

from database import SessionLocal
from models import Chore

app = FastAPI(title="kajilog")


@app.get("/api/health")
def health():
    return {"status": "ok"}


@app.get("/api/chores")
def list_chores():
    session = SessionLocal()
    try:
        chores = session.query(Chore).all()
        return [
            {"id": c.id, "name": c.name, "weight": c.weight, "location": c.location}
            for c in chores
        ]
    finally:
        session.close()
