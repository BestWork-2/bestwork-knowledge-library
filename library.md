---
layout: default
title: Document Library
description: Search and browse every document in the BestWork Knowledge Library.
permalink: /library/
---

<section class="library-hero">
  <div class="shell narrow">
    <p class="eyebrow">Complete collection</p>
    <h1>Document Library</h1>
    <p>Search {{ site.articles.size }} documents or browse the collection by topic.</p>
    <label class="search-box">
      <span class="sr-only">Search the library</span>
      <input id="library-search" type="search" placeholder="Search titles, topics, and descriptions" autocomplete="off">
    </label>
    <p id="search-status" class="search-status" aria-live="polite"></p>
  </div>
</section>

<section class="shell listing-section">
  <div id="search-results" class="article-list" hidden></div>
  <div id="browse-list">
    {% for category in site.data.categories %}
      <section class="library-group">
        <div class="group-heading">
          <h2><a href="{{ '/library/' | append: category.slug | append: '/' | relative_url }}">{{ category.name }}</a></h2>
          <span>{{ category.count }} documents</span>
        </div>
        {% assign category_articles = site.articles | where: "category", category.name | sort: "title" %}
        <div class="article-list">
          {% for article in category_articles %}
            <a class="article-row" href="{{ article.url | relative_url }}">
              <span><strong>{{ article.title }}</strong><small>{{ article.description }}</small></span>
              <span class="arrow" aria-hidden="true">&rarr;</span>
            </a>
          {% endfor %}
        </div>
      </section>
    {% endfor %}
  </div>
</section>

