"""ローカル開発用の初期データ投入スクリプト。`uv run python seed.py`で実行する。"""

from database import Base, SessionLocal, engine
from models import Chore, Household, Member, Tag

Base.metadata.create_all(bind=engine)

session = SessionLocal()

household = Household(name="佐藤家")
session.add(household)
session.flush()

kenta = Member(household_id=household.id, name="健太", icon="🧑", color="#2a78d6")
misaki = Member(household_id=household.id, name="美咲", icon="👩", color="#eb6834")
session.add_all([kenta, misaki])

chores = [
    Chore(household_id=household.id, name="トイレ掃除", weight=2.0, location="トイレ"),
    Chore(household_id=household.id, name="皿洗い", weight=1.5, location="キッチン"),
    Chore(household_id=household.id, name="洗濯物たたみ", weight=1.0, location="リビング"),
]
session.add_all(chores)
session.flush()

tags = [Tag(chore_id=chore.id) for chore in chores]
session.add_all(tags)

session.commit()

print(f"household: {household.id} ({household.name})")
print(f"members: {kenta.name}={kenta.id}, {misaki.name}={misaki.id}")
for chore, tag in zip(chores, tags):
    print(f"chore: {chore.name} (weight={chore.weight}) -> tag_id={tag.id}")

session.close()
