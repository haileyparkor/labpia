import os
import re
import secrets
import sqlite3

from flask import g

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATABASE = os.environ.get("LABPIA_DB", os.path.join(BASE_DIR, "supply.db"))

LOCATIONS = ["보일랩"]
QUANTITIES = ["많음", "보통", "적음", "없음"]

NEW_COLUMNS = {
    "qr_code": "TEXT",
    "rfid_epc": "TEXT",
    "cas_number": "TEXT",
    "concentration": "TEXT",
    "volume": "TEXT",
    "opened_at": "TEXT",
    "expires_at": "TEXT",
    "hazard_class": "TEXT",
}

INDEXES = [
    "CREATE UNIQUE INDEX IF NOT EXISTS idx_supplies_qr_code ON supplies(qr_code)",
    "CREATE UNIQUE INDEX IF NOT EXISTS idx_supplies_rfid_epc ON supplies(rfid_epc)",
]

QR_ALPHABET = "ABCDEFGHJKLMNPQRSTUVWXYZ23456789"
EPC_PATTERN = re.compile(r"[0-9A-F]{16,64}")


def get_db():
    if "db" not in g:
        g.db = sqlite3.connect(DATABASE)
        g.db.row_factory = sqlite3.Row
    return g.db


def close_db(exception=None):
    db = g.pop("db", None)
    if db is not None:
        db.close()


def init_db(path=None):
    path = path or DATABASE
    with open(os.path.join(BASE_DIR, "schema.sql"), encoding="utf-8") as schema_file:
        schema = schema_file.read()

    db = sqlite3.connect(path)
    try:
        db.executescript(schema)
        existing = {row[1] for row in db.execute("PRAGMA table_info(supplies)")}
        for name, column_type in NEW_COLUMNS.items():
            if name not in existing:
                db.execute(f"ALTER TABLE supplies ADD COLUMN {name} {column_type}")
        for statement in INDEXES:
            db.execute(statement)
        db.commit()
    finally:
        db.close()


def new_qr_token():
    return "Q" + "".join(secrets.choice(QR_ALPHABET) for _ in range(10))


def assign_qr_code(db, supply_id):
    for _ in range(5):
        token = new_qr_token()
        exists = db.execute(
            "SELECT 1 FROM supplies WHERE qr_code = ?", (token,)
        ).fetchone()
        if exists is None:
            db.execute(
                "UPDATE supplies SET qr_code = ? WHERE id = ?", (token, supply_id)
            )
            return token
    raise RuntimeError("QR 코드를 생성하지 못했습니다.")


def normalize_code(raw):
    value = (raw or "").strip()
    if not value:
        return None, None
    if "/q/" in value:
        value = value.rsplit("/q/", 1)[1].strip("/")
    compact = re.sub(r"[\s:-]", "", value).upper()
    if EPC_PATTERN.fullmatch(compact):
        return "rfid", compact
    return "qr", value


def find_by_code(code):
    kind, value = normalize_code(code)
    if value is None:
        return None, None
    column = "rfid_epc" if kind == "rfid" else "qr_code"
    row = get_db().execute(
        f"SELECT * FROM supplies WHERE {column} = ?", (value,)
    ).fetchone()
    return kind, row


if __name__ == "__main__":
    init_db()
    print(f"DB를 초기화했습니다: {DATABASE}")
