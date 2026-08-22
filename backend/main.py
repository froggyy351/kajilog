from datetime import datetime, timezone

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from database import SessionLocal
from models import Chore, Member, Record, Tag

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


@app.get("/api/tags/{tag_id}")
def get_tag(tag_id: str):
    session = SessionLocal()
    try:
        tag = session.get(Tag, tag_id)
        if tag is None:
            raise HTTPException(status_code=404, detail="tag not found")
        chore = tag.chore
        members = (
            session.query(Member)
            .filter(Member.household_id == chore.household_id)
            .all()
        )
        return {
            "tag_id": tag.id,
            "chore": {
                "id": chore.id,
                "name": chore.name,
                "weight": chore.weight,
                "location": chore.location,
            },
            "members": [
                {"id": m.id, "name": m.name, "icon": m.icon, "color": m.color}
                for m in members
            ],
        }
    finally:
        session.close()


class CreateRecordRequest(BaseModel):
    tag_id: str
    member_id: str


@app.post("/api/records")
def create_record(body: CreateRecordRequest):
    session = SessionLocal()
    try:
        tag = session.get(Tag, body.tag_id)
        if tag is None:
            raise HTTPException(status_code=404, detail="tag not found")
        member = session.get(Member, body.member_id)
        if member is None:
            raise HTTPException(status_code=404, detail="member not found")

        chore = tag.chore
        record = Record(
            chore_id=chore.id,
            member_id=member.id,
            weight_snapshot=chore.weight,
        )
        session.add(record)
        session.commit()
        session.refresh(record)

        return {
            "record_id": record.id,
            "chore_name": chore.name,
            "member_name": member.name,
            "recorded_at": record.recorded_at.isoformat(),
        }
    finally:
        session.close()


@app.post("/api/records/{record_id}/undo")
def undo_record(record_id: str):
    session = SessionLocal()
    try:
        record = session.get(Record, record_id)
        if record is None:
            raise HTTPException(status_code=404, detail="record not found")
        record.undone_at = datetime.now(timezone.utc)
        session.commit()
        return {"record_id": record.id, "undone_at": record.undone_at.isoformat()}
    finally:
        session.close()


@app.get("/api/dashboard")
def dashboard():
    """世帯ごとのメンバー別ポイント集計。世帯は1つのみ運用する前提の現段階ではhousehold_idの絞り込みは省略している。"""
    session = SessionLocal()
    try:
        members = session.query(Member).all()
        summary = []
        for m in members:
            records = (
                session.query(Record)
                .filter(Record.member_id == m.id, Record.undone_at.is_(None))
                .all()
            )
            summary.append(
                {
                    "id": m.id,
                    "name": m.name,
                    "icon": m.icon,
                    "color": m.color,
                    "total_points": sum(r.weight_snapshot for r in records),
                    "record_count": len(records),
                }
            )
        return {"members": summary}
    finally:
        session.close()
