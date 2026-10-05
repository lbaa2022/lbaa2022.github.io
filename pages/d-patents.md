---
layout: page
title: 특허
feature-img: "assets/img/pexels/travel.jpeg"
permalink: /patents/
---

{% include deliverables_styles.liquid %}
{% include research_assets.liquid %}
{% assign patents = site.data.deliverables.patents %}

<div class="deliverables-page">
  <p class="research-catalog-link"><a href="{{ '/research/' | relative_url }}">연구개발 성과 지도에서 연구의 맥락 살펴보기 ↗</a></p>
  <p class="deliverables-lead">
    2025년까지의 특허 성과를 정리했습니다.
    동일 발명의 국가별 출원과 등록 이력은 한 카드 안에서 함께 확인할 수 있도록 구성했습니다.
  </p>

  <div class="deliverables-stat-grid">
    {% for pair in patents.counts %}
      <div class="deliverables-stat">
        <strong>{{ pair[1] }}</strong>
        <span>{{ pair[0] }}년 특허</span>
      </div>
    {% endfor %}
  </div>

  {% for year_group in patents.years %}
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
                {% for country in item.countries %}
                  <span class="deliverables-chip deliverables-chip--muted">{{ country }}</span>
                {% endfor %}
              </div>
              <div class="deliverables-meta-block">
                <span class="deliverables-meta-label">권리 번호</span>
                {% for number in item.numbers %}
                  {{ number }}{% unless forloop.last %}<br>{% endunless %}
                {% endfor %}
              </div>
              <div class="deliverables-meta-block">
                <span class="deliverables-meta-label">권리 일자</span>
                {% for date in item.dates %}
                  {{ date }}{% unless forloop.last %}<br>{% endunless %}
                {% endfor %}
              </div>
            {% include research_card_links.liquid kind="patent" item=item %}
                </article>
          {% endfor %}
        </div>
      </div>
    </details>
  {% endfor %}
</div>
