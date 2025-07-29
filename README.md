# Synergym Data Pipeline

Synergym 프로젝트의 데이터 수집, 전처리 및 파이프라인을 관리하는 저장소입니다.

## 📁 프로젝트 구조

```
Synergym-data-pipeline/
├── emotion/                        # 감정 데이터 전처리
│   └── Emotion_Preprocess.ipynb   # 감정 분석 데이터 전처리 노트북
├── naver_data/                     # 네이버 운동 데이터 크롤링
│   ├── naver_crawling_workout.py   # 웨이트 운동 크롤링
│   ├── naver_crawling_yoga.py      # 요가 동작 크롤링
│   ├── naver_crawling_streching.py # 스트레칭 동작 크롤링
│   ├── naver_preprocess.ipynb      # 네이버 데이터 전처리
│   ├── naver_terms_workout.csv     # 웨이트 운동 데이터
│   ├── naver_terms_yoga.csv        # 요가 동작 데이터
│   └── naver_terms_stretching.csv  # 스트레칭 동작 데이터
├── naver_img/                      # 운동 이미지 다운로드
│   └── app.py                      # 이미지 다운로드 및 DB 저장 스크립트
└── README.md
```

## 🚀 주요 기능

### 1. 감정 데이터 전처리 (`emotion/`)

#### `Emotion_Preprocess.ipynb`
- **목적**: 감정 분석 모델 훈련을 위한 데이터 전처리
- **주요 기능**:
  - 감정 라벨이 있는 Excel 파일 로드
  - 불필요한 감정 카테고리 제거 (놀람, 공포, 당황)
  - 감정 라벨 정규화 (행복 → 기쁨)
  - 대화형 데이터와 단일 문장 데이터 통합
  - JSONL 형식으로 훈련/검증 데이터 생성

### 2. 네이버 운동 데이터 크롤링 (`naver_data/`)

#### 크롤링 스크립트
- **`naver_crawling_workout.py`**: 웨이트 트레이닝 운동 정보 크롤링
- **`naver_crawling_yoga.py`**: 요가 동작 정보 크롤링
- **`naver_crawling_streching.py`**: 스트레칭 동작 정보 크롤링

**수집 데이터**:
- 운동명/동작명
- 운동 개요 및 설명
- 운동 효과
- 썸네일 이미지 URL
- 난이도 (초급/중급/상급)
- 자세 분류
- 운동 부위

#### `naver_preprocess.ipynb`
- **목적**: 크롤링된 데이터의 전처리 및 정제
- **주요 기능**:
  - 중복 데이터 제거
  - 데이터 형식 정규화
  - 누락 데이터 처리
  - 데이터베이스 저장 형식으로 변환

### 3. 이미지 데이터 관리 (`naver_img/`)

#### `app.py`
- **목적**: 운동 썸네일 이미지 다운로드 및 데이터베이스 저장
- **주요 기능**:
  - PostgreSQL 데이터베이스 연결
  - 운동 데이터에서 이미지 URL 추출
  - 이미지 파일 다운로드 및 로컬 저장
  - 데이터베이스 이미지 경로 업데이트

## 🛠️ 사용 환경

### 필요 라이브러리

```bash
# 기본 데이터 처리
pip install pandas numpy openpyxl

# 웹 크롤링
pip install requests beautifulsoup4

# 데이터베이스 연결
pip install psycopg2-binary

# 머신러닝 데이터 처리
pip install datasets transformers

# 시각화 (선택사항)
pip install matplotlib seaborn
```

### 데이터베이스 설정

```sql
-- PostgreSQL 데이터베이스 설정
CREATE TABLE exercises (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    effect TEXT,
    thumbnail_url VARCHAR(500),
    difficulty VARCHAR(50),
    category VARCHAR(100),
    target_muscle VARCHAR(100),
    image_path VARCHAR(500)
);
```

## 📊 데이터 통계

### 네이버 운동 데이터
- **웨이트 트레이닝**: ~500개 운동
- **요가**: ~200개 동작  
- **스트레칭**: ~150개 동작
- **총 이미지**: ~850개

### 감정 데이터
- **지원 감정**: 기쁨, 슬픔, 분노, 중성 등
- **훈련 데이터**: 문장별 감정 라벨
- **대화 데이터**: 대화 맥락의 감정 분석

## 🔧 사용 방법

### 1. 네이버 운동 데이터 크롤링

```bash
# 웨이트 트레이닝 데이터 크롤링
python naver_data/naver_crawling_workout.py

# 요가 데이터 크롤링
python naver_data/naver_crawling_yoga.py

# 스트레칭 데이터 크롤링
python naver_data/naver_crawling_streching.py
```

### 2. 이미지 다운로드 및 DB 저장

```bash
# 데이터베이스 설정 후
python naver_img/app.py
```

### 3. 감정 데이터 전처리

```bash
# Jupyter Notebook 실행
jupyter notebook emotion/Emotion_Preprocess.ipynb
```

## 📋 데이터 스키마

### 운동 데이터 (CSV)
```csv
제목,개요,효과,썸네일,난이도,자세분류,부위
크런치,복직근 중 상부를 강화하는 운동...,복부 근력 강화,https://...,초급,근력,복부
```

### 감정 데이터 (JSONL)
```json
{"text": "다음 문장을 읽고 감정을 추론하세요. \n문장 : 오늘 정말 기분이 좋다\n감정 : ", "label": "기쁨", "label_id": 0}
```

## ⚠️ 주의사항

1. **크롤링 정책 준수**:
   - robots.txt 확인
   - 적절한 요청 간격 설정
   - 네이버 이용약관 준수

2. **데이터베이스 연결**:
   - 데이터베이스 접속 정보 보안 관리
   - 연결 풀 설정 권장

3. **이미지 저장**:
   - 충분한 디스크 공간 확보
   - 이미지 파일 권한 설정

4. **데이터 품질**:
   - 정기적인 데이터 검증
   - 중복 데이터 모니터링

## 🔄 데이터 파이프라인 흐름

```
1. 웹 크롤링 (naver_data/)
   ↓
2. 데이터 전처리 (naver_preprocess.ipynb)
   ↓
3. 이미지 다운로드 (naver_img/app.py)
   ↓
4. 데이터베이스 저장
   ↓
5. 모델 훈련용 데이터 준비
```

## 🤝 기여 방법

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/new-crawling`)
3. Commit your changes (`git commit -am 'Add new crawling feature'`)
4. Push to the branch (`git push origin feature/new-crawling`)
5. Create a Pull Request

## 📄 라이선스

이 프로젝트는 MIT 라이선스 하에 배포됩니다.

---

**Synergym Data Team**  
데이터 수집 및 전처리 파이프라인
