import os
import sqlite3

import db

# 예시 비품: (이름, 분류, 설명, 시약장 번호, 잔량, 상태)
SAMPLE_SUPPLIES = [
    ("비커 250mL", "유리기구", "액체를 담거나 섞을 때 쓰는 유리 비커입니다.", 1, "많음", "사용 가능"),
    ("삼각플라스크 500mL", "유리기구", "가열과 흔들기 실험에 쓰는 삼각플라스크입니다.", 1, "보통", "사용 가능"),
    ("메스실린더 100mL", "측정기구", "액체의 부피를 눈금으로 재는 실린더입니다.", 2, "보통", "사용 가능"),
    ("스포이트", "측정기구", "소량의 액체를 옮길 때 쓰는 도구입니다.", 2, "적음", "사용 가능"),
    ("에탄올 500mL", "시약", "소독과 세척에 쓰는 에탄올입니다.", 3, "보통", "사용 가능"),
    ("페놀프탈레인 용액", "시약", "산과 염기를 구분하는 지시약입니다.", 3, "적음", "사용 가능"),
    ("여과지", "소모품", "거름 장치에 쓰는 원형 여과지입니다.", 4, "많음", "사용 가능"),
    ("라텍스 장갑 (M)", "소모품", "실험 중 손을 보호하는 일회용 장갑입니다.", 4, "없음", "사용 가능"),
    ("전자저울", "기기", "고체 시료의 무게를 재는 전자저울입니다.", 5, "적음", "사용 가능"),
    ("알코올 온도계", "측정기구", "액체의 온도를 재는 온도계입니다.", 5, "보통", "사용 가능"),
    ("보안경", "안전용품", "실험할 때 눈을 보호하는 보안경입니다.", 6, "많음", "사용 가능"),
    ("분말 소화기", "안전용품", "실험실 화재에 대비한 소형 소화기입니다.", 6, "보통", "사용 가능"),
]


def main():
    # 기존 데이터를 지우지 않도록, DB 파일이 있으면 아무것도 하지 않고 중단한다.
    # 연결(connect)이나 테이블 생성보다 먼저 검사해야 파일이 바뀌지 않는다.
    if os.path.exists(db.DATABASE):
        print(f"이미 supply.db 가 있어 실행을 중단했습니다: {db.DATABASE}")
        print("새로 만들려면 기존 파일을 직접 옮기거나 삭제한 뒤 다시 실행하세요.")
        return

    db.init_db()
    conn = sqlite3.connect(db.DATABASE)
    conn.row_factory = sqlite3.Row

    try:
        for name, category, description, cabinet_number, quantity, status in SAMPLE_SUPPLIES:
            cursor = conn.execute(
                """
                INSERT INTO supplies
                    (name, category, description, location, cabinet_number, quantity, status)
                VALUES (?, ?, ?, ?, ?, ?, ?)
                """,
                (name, category, description, "보일랩", cabinet_number, quantity, status),
            )
            db.assign_qr_code(conn, cursor.lastrowid)
        conn.commit()
    finally:
        conn.close()

    print(f"예시 비품 {len(SAMPLE_SUPPLIES)}개를 {db.DATABASE} 에 저장했습니다.")


if __name__ == "__main__":
    main()
