---
layout: page
title: 논문
feature-img: "assets/img/pexels/travel.jpeg"
permalink: /publications/
---

{% include deliverables_styles.liquid %}
{% assign publications = site.data.deliverables.papers %}

<div class="deliverables-page">
  <p class="deliverables-lead">
    2025년까지의 논문 및 학술대회 성과를 정리했습니다.
    동일 제목의 성과는 중복 없이 통합했고, 과제의 핵심 기술 분야 관점에서 다시 분류해 연도순으로 살펴볼 수 있도록 구성했습니다.
  </p>

  <div class="deliverables-stat-grid">
    {% for pair in publications.counts %}
      <div class="deliverables-stat">
        <strong>{{ pair[1] }}</strong>
        <span>{{ pair[0] }}년 성과</span>
      </div>
    {% endfor %}
  </div>

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
            <span class="deliverables-year-label">{{ year_group.year }}년</span>
            <span class="deliverables-year-count">{{ year_group.items | size }}건</span>
          </summary>
          <div class="deliverables-year-body">
            <div class="deliverables-grid">
              {% for item in year_group.items %}
                <article class="deliverables-card">
                  <h3>{{ item.title }}</h3>
                  <div class="deliverables-chip-row">
                    {% for org in item.orgs %}
                      <span class="deliverables-chip">{{ org }}</span>
                    {% endfor %}
                    {% for kind in item.kinds %}
                      <span class="deliverables-chip deliverables-chip--muted">{{ kind }}</span>
                    {% endfor %}
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
