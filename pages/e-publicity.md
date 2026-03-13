---
layout: page
title: 홍보
feature-img: "assets/img/pexels/travel.jpeg"
permalink: /publicity/
---

{% include deliverables_styles.liquid %}
{% assign publicity = site.data.deliverables.publicity %}

<div class="deliverables-page">
  <p class="deliverables-lead">
    언론 보도, 전시, 세미나, 커뮤니티 활동 등 2025년까지의 대외 확산 성과를 정리했습니다.
  </p>

  <div class="deliverables-stat-grid">
    {% for pair in publicity.counts %}
      <div class="deliverables-stat">
        <strong>{{ pair[1] }}</strong>
        <span>{{ pair[0] }}년 홍보 성과</span>
      </div>
    {% endfor %}
  </div>

  {% for year_group in publicity.years %}
    <details class="deliverables-year" {% if forloop.first %}open{% endif %}>
      <summary>
        <span class="deliverables-year-label">{{ year_group.year }}년</span>
        <span class="deliverables-year-count">{{ year_group.items | size }}건</span>
      </summary>
      <div class="deliverables-year-body">
        <div class="deliverables-grid">
          {% for item in year_group.items %}
            <article class="deliverables-card">
              <h3>{{ item.title }}</h3>
              <div class="deliverables-chip-row">
                <span class="deliverables-chip">{{ item.type }}</span>
                <span class="deliverables-chip deliverables-chip--muted">{{ item.mode }}</span>
              </div>
              <div class="deliverables-meta-block">
                <span class="deliverables-meta-label">기관</span>
                {{ item.org }}
              </div>
              <div class="deliverables-meta-block">
                <span class="deliverables-meta-label">언론사 / 행사</span>
                {{ item.outlet }}
              </div>
              <div class="deliverables-meta-block">
                <span class="deliverables-meta-label">일자</span>
                {{ item.date }}
              </div>
            </article>
          {% endfor %}
        </div>
      </div>
    </details>
  {% endfor %}
</div>
