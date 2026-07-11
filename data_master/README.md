# LBA 과제 실적 마스터 데이터 (SSOT)

과제 실적(논문·특허·SW·홍보)의 **단일 진실 공급원(Single Source of Truth)**.
이 폴더의 CSV가 원본이며, 사이트 데이터(`_data/deliverables.json`)는 여기서
**자동 생성**된다. 제출용 엑셀 성과표도 여기서 출력한다.
`_data/deliverables.json`을 직접 수정하지 말 것 (build 시 덮어써짐).

## 워크플로우

```
새 실적 발생
  → 해당 CSV에 행 추가 (data_master/*.csv)
  → /usr/bin/python3 scripts/validate.py          # 검증 (실패 시 행 번호 출력)
  → /usr/bin/python3 scripts/build_site_data.py   # _data/deliverables.json 재생성
  → git add -A && git commit && git push          # GitHub Pages 자동 반영 (~2분)
```

제출용 성과표: `/usr/bin/python3 scripts/export_xlsx.py 2025` (연도 또는 `all`).
마스터에 없는 항목(초록·ISSN·기여율·IF 등)은 `-`로 출력되므로 제출 전 보완 필요.
의존성: 표준 라이브러리만. `export_xlsx.py`만 `openpyxl` 필요.

## 파일·컬럼 정의

여러 값을 갖는 컬럼은 **세미콜론(`;`)** 으로 구분한다 (예: `authors`).
`id`는 파일별 접두어 + 일련번호이며 재사용·변경하지 않는다. `note`는 자유
메모(사이트에 출력되지 않음).

### papers.csv — 논문·학술대회 (사이트 Publications)
| 컬럼 | 설명 |
|---|---|
| id | `P0001`… |
| year | 성과 연도 (2022~2030) |
| category | `umc` \| `uqg` \| `ocl2` \| `planning` (categories.csv의 key) |
| kind | `SCI(E) 저널` \| `비SCI(E) 저널` \| `국제학술대회` \| `국내학술대회` — 복수 시 `;` 구분, **첫 값 기준으로 통계 집계** |
| title | 논문 제목 |
| authors | 저자 (`;` 구분, 첫 저자 = 주저자) |
| orgs | 성과 발생 기관 (`;` 구분) |
| venue | 학술지명/학술대회명 (`;` 구분 가능) |
| scholar_url / dbpia_url | 검색 링크. **비워두면 build가 제목으로 자동 생성** |
| note | 메모. 의도적 중복 제목이면 `dup-ok` 포함 기재 |

### patents.csv — 특허
| 컬럼 | 설명 |
|---|---|
| id | `PT0001`… |
| year / title / orgs | 연도 / 발명 명칭 / 출원(등록) 기관 |
| countries | 예: `대한민국 출원`, `대한민국 등록`, `미국 출원`, `PCT` — `;` 구분 |
| numbers / dates | 출원(등록)번호 / 일자 — countries와 **개수·순서 일치 필수** (병렬 목록) |
| note | 동일 번호가 다른 행에도 있으면(출원→등록 진행 등) `dup-ok` 포함 기재 |

### software.csv — SW 저작권 등록
`id`(`SW0001`…), `year`, `title`, `org`, `author`, `date`,
`number`(등록번호, 선택), `status`(예: `등록 진행중`, 선택), `note`.

### software_public.csv — 공개 SW·데이터셋 (연도 무관 목록)
`id`(`OS0001`…), `title`, `type`(`공개 SW` \| `데이터셋`),
`availability`(`공개` \| `비공개`), `org`, `url`(필수),
`metric_label`, `metric`, `description`, `note`.

### featured_repos.csv — 사이트 상단 대표 저장소
`id`(`FR001`…), `name`, `category`(표시용 자유 텍스트), `url`(필수).

### publicity.csv — 홍보
`id`(`PB0001`…), `year`, `title`, `type`(언론/SNS/전시회 등), `mode`(기사 홍보 등),
`org`, `outlet`(매체명), `date`, `note`.

### categories.csv — 논문 카테고리 정의
`key`, `title`, `description`. **행 순서 = 사이트 표시 순서.** 함부로 수정 금지.

## 자동 집계·정렬 규칙 (build_site_data.py)

- 연도별 건수(counts), 카테고리별 count, 종별 통계표(stats_by_kind),
  공개 SW/데이터셋 집계(public_counts)는 전부 **자동 산출** — 손으로 세지 말 것.
- 정렬: 카테고리(categories.csv 순서) → 연도 내림차순 → **CSV 행 순서 유지**.
  새 행은 파일 끝에 추가해도 올바른 위치에 배치된다.
- 종별 통계는 각 논문을 첫 번째 kind 기준으로 1회만 집계 (총합 = 논문 건수).

## 자주 하는 실수 (성과표 오기 사례)

1. **중복 등재** — 같은 논문을 두 카테고리/연도에 넣는 실수. validate가 정규화
   비교(공백·문장부호·대소문자 무시)로 잡아낸다. 실제 별건이면 `note`에 `dup-ok`.
   ※ 초기 적재 데이터에 1건 존재(P0002/P0140 동일 제목, umc 2025 / planning
   2023) — 원본 사이트 그대로 보존했으며 사실 확인 필요.
2. **kind 오기** — `SCIE 저널`, `국제 학술대회`(띄어쓰기) 등 어휘 밖 표기는
   통계표가 어긋난다. validate가 차단.
3. **특허 병렬 목록 불일치** — countries 2개인데 numbers 1개 등. validate가 차단.
4. **연도 불일치** — 출원은 출원연도, 등록은 등록연도 성과로 별도 행 기재
   (번호 중복은 `dup-ok`로 명시).
5. **counts 수동 수정** — JSON의 통계를 직접 고치면 다음 build에서 사라진다.
   반드시 CSV를 고칠 것.
