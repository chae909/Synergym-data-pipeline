import requests
from bs4 import BeautifulSoup
import pandas as pd
import time

base_url = "https://terms.naver.com"
list_base_url = "https://terms.naver.com/list.naver?cid=51030&categoryId=51030&page={}"
headers = {"User-Agent": "Mozilla/5.0"}

results = []

# 1~17 페이지 반복
for page in range(1, 18):
    print(f"📄 페이지 {page} 처리 중...")
    list_url = list_base_url.format(page)
    res = requests.get(list_url, headers=headers)
    soup = BeautifulSoup(res.text, "html.parser")
    links = soup.select("ul.content_list > li > div.info_area > div.subject > strong > a")
    if not links:
        print(f"페이지 {page}에 항목이 없습니다.")
        continue

    for link in links:
        item_url = base_url + link['href']
        try:
            item_res = requests.get(item_url, headers=headers)
            item_soup = BeautifulSoup(item_res.text, "html.parser")

            # 제목
            title_elem = item_soup.select_one("h2.headword")
            title = title_elem.text.strip() if title_elem else ""

            # 개요
            overview_elem = item_soup.select_one("h3#TABLE_OF_CONTENT1 + p")
            overview = overview_elem.text.strip() if overview_elem else ""

            # 효과
            effect = ""
            for tag in item_soup.select("h3, strong"):
                if "효과" in tag.text:
                    sibling = tag.find_next_sibling()
                    if sibling:
                        effect = sibling.get_text(separator=" ").strip()
                    break

            # 썸네일
            thumb_elem = item_soup.select_one('h3#TABLE_OF_CONTENT2 ~ div.thmb img')
            thumbnail = thumb_elem['src'] if thumb_elem else ""

            # 테이블 정보
            difficulty = posture_type = body_part = ""
            for row in item_soup.select("table.tmp_profile_tb tbody tr"):
                label_elem = row.select_one("th > span.title")
                value_elem = row.select_one("td")
                if not label_elem or not value_elem:
                    continue
                label = label_elem.text.strip()
                value = value_elem.get_text(separator=", ").strip()
                if label == "난이도":
                    difficulty = value
                elif label == "자세분류":
                    posture_type = value
                elif label == "운동 부위":   # 여기만 정확히 '운동 부위' 체크
                    body_part = value


            results.append({
                "제목": title,
                "개요": overview,
                "효과": effect,
                "썸네일": thumbnail,
                "난이도": difficulty,
                "자세분류": posture_type,
                "부위": body_part
            })

        except Exception as e:
            print(f"에러: {item_url} - {e}")

        time.sleep(1)

    time.sleep(2)

# DataFrame 저장
df = pd.DataFrame(results)
df.to_csv("naver_terms_workout.csv", index=False, encoding="utf-8-sig")
print("'workout' 카테고리 크롤링 완료! 총", len(df), "개 항목 저장됨.")
