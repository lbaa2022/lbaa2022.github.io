#!/usr/bin/env python3
"""LBA 실적 마스터(data_master/*.csv) 공용 로더·어휘 정의.

validate.py / build_site_data.py / export_xlsx.py 가 공유하는 모듈.
의존성: /usr/bin/python3 표준 라이브러리만.
"""
import csv
import os
import re
import unicodedata
from urllib.parse import quote_plus

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_MASTER = os.path.join(ROOT, "data_master")
SITE_JSON = os.path.join(ROOT, "_data", "deliverables.json")

# ── 통제 어휘 ────────────────────────────────────────────────
KINDS = ["SCI(E) 저널", "비SCI(E) 저널", "국제학술대회", "국내학술대회"]
PUBLIC_SW_TYPES = ["공개 SW", "데이터셋"]  # 통계표 키는 '데이터셋'→'공개 데이터셋'
AVAILABILITIES = ["공개", "비공개"]
YEAR_MIN, YEAR_MAX = 2022, 2030

# 파일별 (ID 접두어, 필수 컬럼) — note는 항상 선택
FILES = {
    "categories.csv":     (None,  ["key", "title", "description"]),
    "papers.csv":         ("P",   ["id", "year", "category", "kind", "title",
                                   "authors", "orgs", "venue"]),
    "patents.csv":        ("PT",  ["id", "year", "title", "orgs", "countries",
                                   "numbers", "dates"]),
    "software.csv":       ("SW",  ["id", "year", "title", "org", "author", "date"]),
    "software_public.csv": ("OS", ["id", "title", "type", "availability", "org",
                                   "url", "metric_label", "metric"]),
    "featured_repos.csv": ("FR",  ["id", "name", "category", "url"]),
    "publicity.csv":      ("PB",  ["id", "year", "title", "type", "mode",
                                   "org", "outlet", "date"]),
}


def split_multi(value):
    """세미콜론 구분 다중값 → 리스트 (공백 정돈, 빈 값 제거)."""
    return [p.strip() for p in value.split(";") if p.strip()] if value else []


def normalize_title(title):
    """중복 비교용 제목 정규화: NFKC + 소문자 + 공백/문장부호 제거."""
    t = unicodedata.normalize("NFKC", title).lower()
    return re.sub(r"[\s\W_]+", "", t)


def scholar_url_for(title):
    return "https://scholar.google.com/scholar?q=%22" + quote_plus(title) + "%22"


def dbpia_url_for(title):
    return "https://www.dbpia.co.kr/search/topSearch?query=" + quote_plus(title)


def load_csv(name):
    """CSV → [dict]. 각 행에 '_line'(파일 내 행 번호, 헤더=1) 부여."""
    path = os.path.join(DATA_MASTER, name)
    with open(path, newline="", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        rows = []
        for lineno, row in enumerate(reader, start=2):
            row = {k: (v or "").strip() for k, v in row.items() if k is not None}
            row["_line"] = lineno
            rows.append(row)
        return reader.fieldnames, rows


def load_master():
    """마스터 전체 로드 → {파일명(확장자 제외): (fieldnames, rows)}."""
    out = {}
    for name in FILES:
        out[name[:-4]] = load_csv(name)
    return out


def category_order(master):
    """categories.csv 행 순서 = 사이트 카테고리 표시 순서."""
    return [r["key"] for r in master["categories"][1]]
