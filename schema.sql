-- 보평고 비품관리 시스템 v1.1
-- 신규 설치용. 기존 supply.db 는 db.py 의 init_db() 가 누락 컬럼만 추가한다.

CREATE TABLE IF NOT EXISTS supplies (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    category TEXT NOT NULL,
    description TEXT NOT NULL DEFAULT '',
    location TEXT NOT NULL,
    cabinet_number INTEGER NOT NULL,
    quantity TEXT NOT NULL,
    status TEXT NOT NULL DEFAULT '사용 가능',
    qr_code TEXT,
    rfid_epc TEXT,
    cas_number TEXT,
    concentration TEXT,
    volume TEXT,
    opened_at TEXT,
    expires_at TEXT,
    hazard_class TEXT
);
