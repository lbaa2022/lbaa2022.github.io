---
layout: page
title: SW+Data
feature-img: "assets/img/pexels/travel.jpeg"
permalink: /sw-data/
---

{% include deliverables_styles.liquid %}
{% include research_assets.liquid %}
{% assign software = site.data.deliverables.software %}

<div class="deliverables-page">
  <p class="research-catalog-link"><a href="{{ '/research/' | relative_url }}">연구개발 성과 지도에서 연구의 맥락 살펴보기 ↗</a></p>
  <p class="deliverables-lead">
    공개 SW와 데이터셋, 등록 SW 성과를 함께 정리했습니다.
    공개 SW+Data는 연도 구분 없이 중복을 제거해 한 번에 살펴볼 수 있도록 구성했습니다.
  </p>

  <section class="deliverables-section">
    <div class="deliverables-section-header">
      <div class="deliverables-eyebrow">Open Releases</div>
      <h2>공개 SW+Data</h2>
      <p>2024년과 2025년 공개 저장소 및 데이터셋을 통합해, 동일 자산은 중복 없이 정리했습니다.</p>
    </div>

    <div class="deliverables-stat-grid">
      {% for pair in software.public_counts %}
        <div class="deliverables-stat">
          <strong>{{ pair[1] }}</strong>
          <span>{{ pair[0] }}</span>
        </div>
      {% endfor %}
    </div>

    <div class="deliverables-grid">
      {% for item in software.public_items %}
        <article class="deliverables-card">
          <h3>{{ item.title }}</h3>
          <div class="deliverables-chip-row">
            <span class="deliverables-chip">{{ item.type }}</span>
            <span class="deliverables-chip">{{ item.org }}</span>
            <span class="deliverables-chip deliverables-chip--muted">{{ item.availability }}</span>
          </div>
          {% if item.metric %}
            <div class="deliverables-meta-block">
              <span class="deliverables-meta-label">{{ item.metric_label }}</span>
              {{ item.metric }}
            </div>
          {% endif %}
          {% if item.description %}
            <div class="deliverables-meta-block">
              <span class="deliverables-meta-label">설명</span>
              {{ item.description }}
            </div>
          {% endif %}
          {% if item.url %}
            <div class="deliverables-link-row">
              <a class="deliverables-link" href="{{ item.url }}" target="_blank" rel="noopener noreferrer">바로가기</a>
            </div>
          {% endif %}
        {% include research_card_links.liquid kind="software" item=item %}
                </article>
      {% endfor %}
    </div>
  </section>

  <section class="deliverables-section">
    <div class="deliverables-section-header">
      <div class="deliverables-eyebrow">Registered Software</div>
      <h2>등록 SW 성과</h2>
      <p>연도별 SW 등록 성과를 기관, 저작자, 등록일과 등록번호 기준으로 정리했습니다.</p>
    </div>

    <div class="deliverables-stat-grid">
      {% for pair in software.counts %}
        <div class="deliverables-stat">
          <strong>{{ pair[1] }}</strong>
          <span>{{ pair[0] }}년 등록 SW</span>
        </div>
      {% endfor %}
    </div>

    {% for year_group in software.years %}
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
                  <span class="deliverables-chip">{{ item.org }}</span>
                  <span class="deliverables-chip deliverables-chip--muted">{{ item.date }}</span>
                  {% if item.status %}
                    <span class="deliverables-chip deliverables-chip--muted">{{ item.status }}</span>
                  {% endif %}
                </div>
                <div class="deliverables-meta-block">
                  <span class="deliverables-meta-label">저작자</span>
                  {{ item.author }}
                </div>
                {% if item.number %}
                  <div class="deliverables-meta-block">
                    <span class="deliverables-meta-label">등록번호</span>
                    {{ item.number }}
                  </div>
                {% endif %}
              {% include research_card_links.liquid kind="registered" item=item %}
                </article>
            {% endfor %}
          </div>
        </div>
      </details>
    {% endfor %}
  </section>
</div>
