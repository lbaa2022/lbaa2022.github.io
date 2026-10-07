"""Project the paper catalog and every count from the canonical outcome registry."""
import json, collections
from pathlib import Path
from urllib.parse import quote
ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / '_data'
db = json.loads((DATA / 'outcomes.json').read_text())
old = json.loads((DATA / 'deliverables.json').read_text())
legacy_items = {i['title']: i for c in old['papers']['categories'] for y in c['years'] for i in y['items']}
claims = {c['id']: c for c in db['source_claims']}
papers = [r for r in db['records'] if r['kind'] == 'paper']
categories = [{k: c[k] for k in ('key', 'title', 'description')} for c in old['papers']['categories']]
# Functional grouping for report-only records; retained site group otherwise.
tech_category = {'T01':'umc','T02':'umc','T04':'uqg','T06':'planning','T07':'umc','T09':'ocl2','T10':'ocl2','T13':'ocl2','T16':'uqg','T17':'ocl2','T18':'umc'}
kind_order = ['SCI(E) 저널','비SCI(E) 저널','국제학술대회','국내학술대회','유형 미확인']
items = []; added = []; repeated = []
def unique(values):
    return list(dict.fromkeys(v for v in values if v))
for r in papers:
    sources = [claims[i] for i in r['source_claim_ids']]
    site = [c for c in sources if c['source_type'] == 'project_site']
    year = min(r['reported_years']) if r['reported_years'] else '미확인'
    kinds = unique(k for c in site for k in c['details'].get('kinds', []))
    if site:
        category = categories[int(site[0]['id'].split('-')[2])]['key']
    else:
        keys = unique(tech_category[t] for t in r['technology_ids'] if t in tech_category)
        assert len(keys) == 1, (r['id'], keys)
        category = keys[0]
        venues = ' '.join(r['venues'])
        kinds = ['국내학술대회' if '한국' in venues else '국제학술대회']
        assert all(c['details'].get('publication_type') == 'conference' for c in sources)
        added.append({'id':r['id'],'title':r['title'],'references':r['report_references']})
    primary = next((k for k in kind_order if k in kinds), '유형 미확인')
    item = dict(id=r['id'], title=r['title'], orgs=r['organizations'], kinds=kinds,
                venues=r['venues'], authors=unique(a for c in site for a in c['details'].get('authors', [])) or r['authors'],
                scholar_url='https://scholar.google.com/scholar?q='+quote('"'+r['title']+'"'),
                statistics_year=year, statistics_kind=primary, category_key=category,
                reported_years=r['reported_years'], report_references=r['report_references'],
                verification_label=r['verification']['status_label'])
    dbpia = next((legacy_items[t].get('dbpia_url') for t in r['aliases'] if t in legacy_items and legacy_items[t].get('dbpia_url')), None)
    if dbpia: item['dbpia_url'] = dbpia
    if len(site)>1:
        repeated.append({'id':r['id'],'title':r['title'],'source_entries':len(site),'years':[c['year'] for c in site]})
    items.append(item)
years = sorted({r['statistics_year'] for r in items if isinstance(r['statistics_year'],int)})
if any(r['statistics_year']=='미확인' for r in items): years.append('미확인')
for c in categories:
    selected = [i for i in items if i['category_key']==c['key']]
    c['count']=len(selected)
    c['years']=[{'year':y,'items':sorted([i for i in selected if i['statistics_year']==y],key=lambda i:i['title'])} for y in reversed(years) if any(i['statistics_year']==y for i in selected)]
rows=[]
for k in kind_order:
    counts=[sum(i['statistics_kind']==k and i['statistics_year']==y for i in items) for y in years]
    if sum(counts): rows.append({'kind':k,'counts':counts,'total':sum(counts)})
totals=[sum(i['statistics_year']==y for i in items) for y in years]
old['papers']={'counts':{str(y):n for y,n in zip(years,totals)},'categories':categories,'stats_by_kind':{'years':years,'rows':rows,'totals':{'counts':totals,'total':len(items)}},'counting_policy':{'unit':'논문 제목 그룹','year':'DB의 최초 보고연도. 연도 미확인은 별도 집계.','kind':'한 제목에 여러 유형이 있으면 SCI(E) 저널, 비SCI(E) 저널, 국제학술대회, 국내학술대회 순으로 한 번 집계. 원 발표·게재 유형은 목록에 모두 보존.','source':'outcomes.json의 paper 레코드와 source_claims에서 생성','checked_at':'2026-10-07'}}
reconciliation={'checked_at':'2026-10-07','previous_entries':sum(c['source_type']=='project_site' and c['outcome_id'] in {r['id'] for r in papers} for c in db['source_claims']),'site_title_groups':sum('project_site' in r['source_presence'] for r in papers),'report_only_title_groups':len(added),'total_title_groups':len(items),'repeated_site_titles':repeated,'added_report_titles':added,'year_counts':old['papers']['counts']}
assert len(items)==len({i['id'] for i in items})==sum(totals)==sum(c['count'] for c in categories)==sum(r['total'] for r in rows)
assert reconciliation['site_title_groups']+len(added)==len(items)
for name,value in [('deliverables.json',old),('publication_reconciliation.json',reconciliation)]:
    (DATA/name).write_text(json.dumps(value,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({k:v for k,v in reconciliation.items() if not isinstance(v,list)},ensure_ascii=False))
