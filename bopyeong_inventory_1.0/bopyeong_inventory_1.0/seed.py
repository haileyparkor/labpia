
import sqlite3, os

DB_PATH = os.path.join("data", "inventory.db")
os.makedirs("data", exist_ok=True)

db = sqlite3.connect(DB_PATH)
db.executescript("""
DROP TABLE IF EXISTS items;
DROP TABLE IF EXISTS locations;

CREATE TABLE locations (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL UNIQUE,
    building TEXT,
    floor TEXT,
    room_name TEXT
);

CREATE TABLE items (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    category TEXT NOT NULL,
    description TEXT,
    location_id INTEGER NOT NULL,
    cabinet_number INTEGER,
    remaining_level TEXT NOT NULL CHECK (remaining_level IN ('많음','보통','적음','없음')),
    status TEXT NOT NULL DEFAULT '사용 가능',
    updated_at TEXT DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (location_id) REFERENCES locations(id)
);
""")

locations = [
    ("보일랩", "본관", "1층", "보일랩"),
]

for name, building, floor, room in locations:
    db.execute(
        "INSERT INTO locations (name, building, floor, room_name) VALUES (?, ?, ?, ?)",
        (name, building, floor, room),
    )

boil_lab_id = db.execute(
    "SELECT id FROM locations WHERE name = ?", ("보일랩",)
).fetchone()[0]

items = [
    ("염산", "산", "실험용 염산. 부식성이 있으므로 보호장비를 착용하고 사용합니다.", boil_lab_id, 1, "보통", "사용 가능"),
    ("황산", "산", "실험용 황산. 물에 천천히 넣어야 합니다.", boil_lab_id, 1, "많음", "사용 가능"),
    ("수산화나트륨", "염기", "실험용 수산화나트륨 용액 및 고체.", boil_lab_id, 2, "적음", "사용 가능"),
    ("페놀프탈레인", "지시약", "산-염기 적정 실험에 사용하는 지시약.", boil_lab_id, 3, "많음", "사용 가능"),
    ("메틸오렌지", "지시약", "산-염기 적정 실험에 사용하는 지시약.", boil_lab_id, 3, "보통", "사용 가능"),
    ("질산은", "염", "빛에 민감하므로 갈색 용기에 보관합니다.", boil_lab_id, 4, "적음", "사용 가능"),
    ("염화바륨", "염", "황산이온 검출 실험에 사용합니다.", boil_lab_id, 5, "많음", "사용 가능"),
    ("과산화수소", "산화제", "3% 과산화수소 용액.", boil_lab_id, 6, "보통", "사용 가능"),
]

for name, category, description, location_id, cabinet, remaining, status in items:
    db.execute(
        """
        INSERT INTO items
        (name, category, description, location_id, cabinet_number, remaining_level, status)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """,
        (name, category, description, location_id, cabinet, remaining, status),
    )

db.commit()
db.close()
print("데이터베이스와 예시 데이터가 생성되었습니다.")
