---
layout: page
title: 논문
feature-img: "assets/img/pexels/travel.jpeg"
permalink: /publications/
---

{% include deliverables_styles.liquid %}
{% include research_assets.liquid %}
<link rel="stylesheet" href="{{ '/assets/css/outcomes.css' | relative_url }}">
{% assign publications = site.data.deliverables.papers %}

<div class="deliverables-page">
  <p class="research-catalog-link"><a href="{{ '/research/' | relative_url }}">연구개발 성과 지도에서 연구의 맥락 살펴보기 ↗</a></p>
  <p class="deliverables-lead">
    2025년까지의 논문 및 학술대회 성과를 정리했습니다.
    보고서와 기존 사이트 목록을 대조해 <strong>논문 제목 그룹 {{ publications.stats_by_kind.totals.total }}건</strong>으로 통합했습니다. 같은 제목의 학회 발표와 저널 게재는 한 그룹으로 집계하며, 각 발표·게재 이력은 목록에 보존합니다.
  </p>

  <p class="deliverables-lead">
    집계 기준: 최초 보고연도를 우선 적용하고, 보고연도가 없는 논문은 확인된 출판연도로 보완합니다. CAMA 논문은 ICLR 2024 출판기록에 따라 2024년에 배정했습니다.
    유형이 겹치는 제목은 저널을 우선해 한 번만 집계합니다. 이 수치는 서로 다른 출판물 수나 외부 검증 완료 논문 수를 뜻하지 않습니다.
    <a href="{{ '/outcomes/' | relative_url }}?kind=paper">검증 DB에서 근거 확인 ↗</a>
  </p>
  <details class="deliverables-year">
    <summary>167건과 190건의 차이 · 2026-10-07 검증</summary>
    <div class="deliverables-year-body">
      <p>기존 목록 {{ site.data.publication_reconciliation.previous_entries }}건에서 같은 제목의 발표·게재 이력 1건을 통합한 {{ site.data.publication_reconciliation.site_title_groups }}개 제목에, 보고서에서 추가 확인한 {{ site.data.publication_reconciliation.report_only_title_groups }}개 제목을 더했습니다. 최종 {{ publications.stats_by_kind.totals.total }}개 제목 그룹입니다.</p>
      <p>통합한 제목: 「이동형 조작 로봇의 강건한 물체 파지를 위한 RGB-D 이미지 기반 3차원 비학습 물체 탐지」 (2023년 학회 발표, 2025년 저널 게재).</p>
      <p>보고서에서 추가한 제목은 보고서 기재 실적이며, 외부 서지 확인 상태는 검증 DB에서 별도로 표시합니다.</p>
    </div>
  </details>

  <div class="deliverables-stat-grid">
    {% for pair in publications.counts %}
      <div class="deliverables-stat">
        <strong>{{ pair[1] }}</strong>
        <span>{% if pair[0] == "미확인" %}보고연도 미확인{% else %}{{ pair[0] }}년{% endif %}</span>
      </div>
    {% endfor %}
  </div>

  {% assign stats = publications.stats_by_kind %}
  <div class="deliverables-table-wrap">
    <table class="deliverables-table">
      <thead>
        <tr>
          <th>구분</th>
          {% for year in stats.years %}
            <th>{% if year == "미확인" %}연도 미확인{% else %}{{ year }}년{% endif %}</th>
          {% endfor %}
          <th>합계</th>
        </tr>
      </thead>
      <tbody>
        {% for row in stats.rows %}
          <tr>
            <th>{{ row.kind }}</th>
            {% for n in row.counts %}
              <td>{{ n }}</td>
            {% endfor %}
            <td><strong>{{ row.total }}</strong></td>
          </tr>
        {% endfor %}
      </tbody>
      <tfoot>
        <tr>
          <th>합계</th>
          {% for n in stats.totals.counts %}
            <td><strong>{{ n }}</strong></td>
          {% endfor %}
          <td><strong>{{ stats.totals.total }}</strong></td>
        </tr>
      </tfoot>
    </table>
  </div>

  <p class="deliverables-lead">논문은 주된 연구 기여에 따라 UMC·UQG·OCL2의 세 수평 핵심 기술 분야로 분류했습니다. 분야별 목록에는 해당 기술을 지원하는 기반 연구와 평가·벤치마크도 포함합니다.</p>

  <div class="deliverables-category-grid">
    {% for category in publications.categories %}
      <div class="deliverables-category-card">
        <div class="deliverables-eyebrow">Core Area</div>
        <h3>{{ category.title }}</h3>
        <p>{{ category.description }}</p>
        <span class="deliverables-count">총 {{ category.count }}건</span>
      </div>
    {% endfor %}
  </div>

  {% for category in publications.categories %}
    <section class="deliverables-section">
      <div class="deliverables-section-header">
        <div class="deliverables-eyebrow">Category {{ forloop.index }}</div>
        <h2>{{ category.title }}</h2>
        <p>{{ category.description }}</p>
      </div>

      {% for year_group in category.years %}
        <details class="deliverables-year" {% if forloop.first %}open{% endif %}>
          <summary>
            <span class="deliverables-year-label">{% if year_group.year == "미확인" %}보고연도 미확인{% else %}{{ year_group.year }}년{% endif %}</span>
            <span class="deliverables-year-count">{{ year_group.items | size }}건</span>
          </summary>
          <div class="deliverables-year-body">
            <div class="deliverables-grid">
              {% for item in year_group.items %}
                <article class="deliverables-card" id="{{ item.id }}">
                  <h3>{{ item.title }}</h3>
                  <div class="deliverables-chip-row">
                    {% for org in item.orgs %}
                      <span class="deliverables-chip">{{ org }}</span>
                    {% endfor %}
                    {% for kind in item.kinds %}
                      <span class="deliverables-chip deliverables-chip--muted">{{ kind }}</span>
                    {% endfor %}
                  </div>
                  <div class="deliverables-meta-block">
                    <span class="deliverables-meta-label">보고 이력 / 검증 상태</span>
                    {% if item.statistics_year_basis == 'publication_year' %}<a href="{{ item.statistics_year_source }}" target="_blank" rel="noopener noreferrer">{{ item.statistics_year }}년 출판연도 기준</a>{% elsif item.reported_years.size > 0 %}{{ item.reported_years | join: ', ' }}{% else %}보고연도 미확인{% endif %} · {{ item.verification_label }}
                  </div>
                  {% if item.authors %}
                    <div class="deliverables-meta-block">
                      <span class="deliverables-meta-label">저자</span>
                      {{ item.authors | join: ', ' }}
                    </div>
                  {% endif %}
                  <div class="deliverables-meta-block">
                    <span class="deliverables-meta-label">학술지 / 학술대회</span>
                    {% for venue in item.venues %}
                      {{ venue }}{% unless forloop.last %}<br>{% endunless %}
                    {% endfor %}
                  </div>
                  {% if item.scholar_url or item.dbpia_url %}
                    <div class="deliverables-link-row">
                      {% if item.scholar_url %}
                        <a class="deliverables-link" href="{{ item.scholar_url }}" target="_blank" rel="noopener noreferrer">Google Scholar</a>
                      {% endif %}
                      {% if item.dbpia_url %}
                        <a class="deliverables-link" href="{{ item.dbpia_url }}" target="_blank" rel="noopener noreferrer">DBpia</a>
                      {% endif %}
                    </div>
                  {% endif %}
                {% include research_card_links.liquid kind="paper" item=item %}
                {% assign existing_outcome_link = site.data.outcome_links.paper[item.title] %}
                {% unless existing_outcome_link.size > 0 %}
                  <div class="outcome-card-links"><a href="{{ '/outcomes/' | relative_url }}?id={{ item.id }}#{{ item.id }}">검증 DB와 보고서 근거 ↗</a></div>
                {% endunless %}
                </article>
              {% endfor %}
            </div>
          </div>
        </details>
      {% endfor %}
    </section>

    {% unless forloop.last %}
      <div class="deliverables-divider"></div>
    {% endunless %}
  {% endfor %}
</div>
