#!/usr/bin/env python3
"""LBA 실적 마스터(data_master/*.csv) 검증.

사용법:  /usr/bin/python3 scripts/validate.py
종료코드: 0=통과, 1=위반(파일·행 번호와 함께 출력).

검사 항목:
  - 필수 필드 누락, 컬럼 헤더 일치
  - id 형식(접두어+숫자)·유일성
  - year 정수·범위(2022~2030)
  - 어휘: papers.category(categories.csv), papers.kind, software_public.type/availability
  - URL 형식(http/https)
  - 중복: papers 제목(정규화 비교), patents 출원(등록)번호
    → 의도적 중복은 해당 행 note에 'dup-ok' 포함 시 허용
  - patents countries/numbers/dates 병렬 목록 길이 일치

의존성: 표준 라이브러리만 (requirements: 없음).
"""
import re
import sys
from collections import defaultdict

import lba_master as M

URL_RE = re.compile(r"^https?://\S+$")

errors = []


def err(name, line, msg):
    errors.append(f"{name}:{line}: {msg}")


def check_common(name, prefix, required, fieldnames, rows):
    expected_ids = set()
    if fieldnames is None:
        err(name, 1, "헤더를 읽을 수 없음")
        return
    missing_cols = [c for c in required if c not in fieldnames]
    if missing_cols:
        err(name, 1, f"필수 컬럼 누락: {missing_cols}")
        return
    id_re = re.compile(rf"^{prefix}\d{{3,}}$") if prefix else None
    for r in rows:
        for c in required:
            if not r.get(c):
                err(name, r["_line"], f"필수 필드 비어 있음: {c}")
        rid = r.get("id", "")
        if id_re:
            if not id_re.match(rid):
                err(name, r["_line"], f"id 형식 오류(예: {prefix}0001): {rid!r}")
            elif rid in expected_ids:
                err(name, r["_line"], f"id 중복: {rid}")
            expected_ids.add(rid)
        if "year" in required and r.get("year"):
            if not r["year"].isdigit():
                err(name, r["_line"], f"year가 정수가 아님: {r['year']!r}")
            elif not (M.YEAR_MIN <= int(r["year"]) <= M.YEAR_MAX):
                err(name, r["_line"],
                    f"year 범위({M.YEAR_MIN}~{M.YEAR_MAX}) 벗어남: {r['year']}")


def check_url(name, row, field, allow_empty=True):
    v = row.get(field, "")
    if not v:
        if not allow_empty:
            err(name, row["_line"], f"필수 URL 비어 있음: {field}")
        return
    if not URL_RE.match(v):
        err(name, row["_line"], f"URL 형식 오류({field}): {v!r}")


def run():
    global errors
    errors = []
    master = M.load_master()

    for name, (prefix, required) in M.FILES.items():
        fieldnames, rows = master[name[:-4]]
        check_common(name, prefix, required, fieldnames, rows)

    # categories: key 유일성
    _, cats = master["categories"]
    seen = set()
    for r in cats:
        if r["key"] in seen:
            err("categories.csv", r["_line"], f"key 중복: {r['key']}")
        seen.add(r["key"])
    cat_keys = {r["key"] for r in cats}

    # papers: 어휘·URL·중복 제목
    _, papers = master["papers"]
    title_groups = defaultdict(list)
    for r in papers:
        if r["category"] and r["category"] not in cat_keys:
            err("papers.csv", r["_line"],
                f"category 어휘 위반: {r['category']!r} (허용: {sorted(cat_keys)})")
        for k in M.split_multi(r["kind"]):
            if k not in M.KINDS:
                err("papers.csv", r["_line"],
                    f"kind 어휘 위반: {k!r} (허용: {M.KINDS})")
        check_url("papers.csv", r, "scholar_url")   # 비면 build가 자동 생성
        check_url("papers.csv", r, "dbpia_url")
        if r["title"]:
            title_groups[M.normalize_title(r["title"])].append(r)
    for rows in title_groups.values():
        if len(rows) > 1 and not any("dup-ok" in x.get("note", "") for x in rows):
            where = ", ".join(f"행 {x['_line']}({x['id']})" for x in rows)
            err("papers.csv", rows[0]["_line"],
                f"중복 제목(정규화 비교): {rows[0]['title'][:40]!r}... → {where} "
                f"(의도적이면 note에 dup-ok 기재)")

    # patents: 병렬 목록 길이·중복 번호
    _, patents = master["patents"]
    num_groups = defaultdict(list)
    for r in patents:
        c, n, d = (M.split_multi(r["countries"]), M.split_multi(r["numbers"]),
                   M.split_multi(r["dates"]))
        if not (len(c) == len(n) == len(d)):
            err("patents.csv", r["_line"],
                f"countries/numbers/dates 개수 불일치: {len(c)}/{len(n)}/{len(d)}")
        for num in n:
            num_groups[num].append(r)
    for num, rows in num_groups.items():
        if len(rows) > 1 and not any("dup-ok" in x.get("note", "") for x in rows):
            where = ", ".join(f"행 {x['_line']}({x['id']})" for x in rows)
            err("patents.csv", rows[0]["_line"],
                f"출원(등록)번호 중복: {num} → {where} (의도적이면 note에 dup-ok 기재)")

    # software_public: 어휘·URL
    _, pub_sw = master["software_public"]
    for r in pub_sw:
        if r["type"] and r["type"] not in M.PUBLIC_SW_TYPES:
            err("software_public.csv", r["_line"],
                f"type 어휘 위반: {r['type']!r} (허용: {M.PUBLIC_SW_TYPES})")
        if r["availability"] and r["availability"] not in M.AVAILABILITIES:
            err("software_public.csv", r["_line"],
                f"availability 어휘 위반: {r['availability']!r} (허용: {M.AVAILABILITIES})")
        check_url("software_public.csv", r, "url", allow_empty=False)

    # featured_repos: URL
    _, feats = master["featured_repos"]
    for r in feats:
        check_url("featured_repos.csv", r, "url", allow_empty=False)

    return errors


def main():
    errs = run()
    if errs:
        print(f"검증 실패: {len(errs)}건")
        for e in errs:
            print("  " + e)
        sys.exit(1)
    master = M.load_master()
    counts = {k: len(v[1]) for k, v in master.items()}
    print("검증 통과:", ", ".join(f"{k} {v}행" for k, v in counts.items()))


if __name__ == "__main__":
    main()
