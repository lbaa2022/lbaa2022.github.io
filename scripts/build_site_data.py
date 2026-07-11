#!/usr/bin/env python3
"""마스터 CSV(data_master/) → 사이트 데이터(_data/deliverables.json) 생성.

사용법:
  /usr/bin/python3 scripts/build_site_data.py           # 검증 후 JSON 생성·저장
  /usr/bin/python3 scripts/build_site_data.py --check   # 저장하지 않고 현행 JSON과 대조

정렬 규칙(안정 정렬, 라운드트립 보장):
  - papers: 카테고리(categories.csv 행 순서) → 연도 내림차순 → CSV 행 순서
  - patents/software/publicity: 연도 내림차순 → CSV 행 순서
  - counts 키: 연도 내림차순 / stats_by_kind.years: 오름차순
집계(counts, 카테고리 count, stats_by_kind, public_counts)는 전부 자동 산출.
papers의 scholar_url/dbpia_url이 비어 있으면 제목으로 자동 생성.

의존성: 표준 라이브러리만 (requirements: 없음).
"""
import json
import sys
from collections import Counter, defaultdict

import lba_master as M
import validate


def group_by_year(rows):
    """연도 내림차순 그룹, 그룹 내 CSV 행 순서 유지."""
    by_year = defaultdict(list)
    for r in rows:
        by_year[int(r["year"])].append(r)
    return sorted(by_year.items(), key=lambda kv: -kv[0])


def year_counts(rows):
    c = Counter(int(r["year"]) for r in rows)
    return {str(y): c[y] for y in sorted(c, reverse=True)}


def build_papers(master):
    _, cats = master["categories"]
    _, papers = master["papers"]
    by_cat = defaultdict(list)
    for r in papers:
        by_cat[r["category"]].append(r)

    categories = []
    for cat in cats:
        rows = by_cat.get(cat["key"], [])
        years = []
        for year, yrows in group_by_year(rows):
            items = []
            for r in yrows:
                items.append({
                    "title": r["title"],
                    "orgs": M.split_multi(r["orgs"]),
                    "kinds": M.split_multi(r["kind"]),
                    "venues": M.split_multi(r["venue"]),
                    "authors": M.split_multi(r["authors"]),
                    "scholar_url": r["scholar_url"] or M.scholar_url_for(r["title"]),
                    "dbpia_url": r["dbpia_url"] or M.dbpia_url_for(r["title"]),
                })
            years.append({"year": year, "items": items})
        categories.append({
            "key": cat["key"],
            "title": cat["title"],
            "description": cat["description"],
            "count": len(rows),
            "years": years,
        })

    # 종별 통계: 첫 번째 kind 기준 1회 집계 (연도 오름차순 축)
    stat_years = sorted({int(r["year"]) for r in papers})
    kind_counts = {k: [0] * len(stat_years) for k in M.KINDS}
    for r in papers:
        first_kind = M.split_multi(r["kind"])[0]
        kind_counts[first_kind][stat_years.index(int(r["year"]))] += 1
    rows_stat = [{"kind": k, "counts": kind_counts[k], "total": sum(kind_counts[k])}
                 for k in M.KINDS]
    totals = [sum(kind_counts[k][i] for k in M.KINDS) for i in range(len(stat_years))]

    return {
        "counts": year_counts(papers),
        "categories": categories,
        "stats_by_kind": {
            "years": stat_years,
            "rows": rows_stat,
            "totals": {"counts": totals, "total": sum(totals)},
        },
    }


def build_patents(master):
    _, patents = master["patents"]
    years = []
    for year, yrows in group_by_year(patents):
        items = [{
            "title": r["title"],
            "orgs": M.split_multi(r["orgs"]),
            "countries": M.split_multi(r["countries"]),
            "numbers": M.split_multi(r["numbers"]),
            "dates": M.split_multi(r["dates"]),
        } for r in yrows]
        years.append({"year": year, "items": items})
    return {"counts": year_counts(patents), "years": years}


def build_software(master):
    _, sw = master["software"]
    _, pub = master["software_public"]
    _, feats = master["featured_repos"]

    years = []
    for year, yrows in group_by_year(sw):
        items = []
        for r in yrows:
            item = {"title": r["title"], "org": r["org"],
                    "author": r["author"], "date": r["date"]}
            if r.get("number"):
                item["number"] = r["number"]
            if r.get("status"):
                item["status"] = r["status"]
            items.append(item)
        years.append({"year": year, "items": items})

    public_items = [{
        "title": r["title"], "type": r["type"], "availability": r["availability"],
        "org": r["org"], "url": r["url"], "metric_label": r["metric_label"],
        "metric": r["metric"], "description": r["description"],
    } for r in pub]
    n_sw = sum(1 for r in pub if r["type"] == "공개 SW")
    n_ds = sum(1 for r in pub if r["type"] == "데이터셋")

    return {
        "counts": year_counts(sw),
        "featured_repos": [{"name": r["name"], "category": r["category"],
                            "url": r["url"]} for r in feats],
        "years": years,
        "public_years": [],
        "public_counts": {"공개 SW": n_sw, "공개 데이터셋": n_ds, "전체": n_sw + n_ds},
        "public_items": public_items,
    }


def build_publicity(master):
    _, rows = master["publicity"]
    years = []
    for year, yrows in group_by_year(rows):
        items = [{"title": r["title"], "type": r["type"], "mode": r["mode"],
                  "org": r["org"], "outlet": r["outlet"], "date": r["date"]}
                 for r in yrows]
        years.append({"year": year, "items": items})
    return {"counts": year_counts(rows), "years": years}


def build():
    master = M.load_master()
    return {
        "papers": build_papers(master),
        "patents": build_patents(master),
        "software": build_software(master),
        "publicity": build_publicity(master),
    }


def main():
    errs = validate.run()
    if errs:
        print(f"마스터 검증 실패 {len(errs)}건 — 생성 중단. scripts/validate.py 실행 후 수정 요망.")
        for e in errs[:20]:
            print("  " + e)
        sys.exit(1)

    data = build()
    # 현행 사이트 JSON과 동일 포맷 (indent=2, 비ASCII 원문, 후행 개행 없음)
    text = json.dumps(data, ensure_ascii=False, indent=2)

    if "--check" in sys.argv:
        try:
            with open(M.SITE_JSON, encoding="utf-8") as f:
                current_text = f.read()
        except FileNotFoundError:
            print("현행 JSON 없음 — 대조 불가")
            sys.exit(1)
        semantic = json.loads(current_text) == data
        print(f"의미 동일(구조·건수·값): {'예' if semantic else '아니오'}")
        print(f"바이트 동일: {'예' if current_text == text else '아니오'}")
        sys.exit(0 if semantic else 1)

    with open(M.SITE_JSON, "w", encoding="utf-8") as f:
        f.write(text)
    n_papers = sum(c["count"] for c in data["papers"]["categories"])
    print(f"생성 완료: {M.SITE_JSON}")
    print(f"  논문 {n_papers} / 특허 {sum(data['patents']['counts'].values())}"
          f" / SW등록 {sum(data['software']['counts'].values())}"
          f" / 공개SW·데이터셋 {data['software']['public_counts']['전체']}"
          f" / 홍보 {sum(data['publicity']['counts'].values())}")


if __name__ == "__main__":
    main()
