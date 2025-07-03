import os
import pandas as pd
import requests
import psycopg2
from urllib.parse import urlparse

# DB 연결 정보
DB_CONFIG = {
    "host": "192.168.2.6",
    "port": "5432",
    "dbname": "postgres",
    "user": "synergym",
    "password": "1234"
}

# 테이블 이름 지정
TABLE_NAME = "exercises"  

def download_image(url, save_path):
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        with open(save_path, 'wb') as f:
            f.write(response.content)
        print(f"저장 완료: {save_path}")
    except Exception as e:
        print(f"실패: {url} -> {e}")

def main():
    save_dir = "imgs"
    os.makedirs(save_dir, exist_ok=True)

    # CSV 파일 읽기
    csv_df = pd.read_csv("naver_exercise_cleaned.csv")
    if not {"name", "thumbnail_url"}.issubset(csv_df.columns):
        print("CSV에 'name', 'thumbnail_url' 컬럼이 필요합니다.")
        return

    # DB에서 name과 id 조회
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cursor = conn.cursor()
        cursor.execute(f"SELECT exercise_id, name FROM {TABLE_NAME};")
        db_data = cursor.fetchall()
        db_df = pd.DataFrame(db_data, columns=["exercise_id", "name"])
    except Exception as e:
        print("DB 연결 실패:", e)
        return

    # name 기준으로 merge
    merged_df = pd.merge(csv_df, db_df, on="name", how="inner")

    print(f"{len(merged_df)}개의 이미지 다운로드 시작...")

    # 이미지 다운로드
    for _, row in merged_df.iterrows():
        url = row["thumbnail_url"]
        img_id = row["exercise_id"]
        if pd.isna(url) or pd.isna(img_id):
            continue
        save_path = os.path.join(save_dir, f"{img_id}.jpg")
        download_image(url, save_path)

    cursor.close()
    conn.close()
    print("모든 작업 완료!")

if __name__ == "__main__":
    main()
