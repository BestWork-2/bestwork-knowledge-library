---
layout: default
title: BestWork Knowledge Library
description: Explore research and practical perspectives on behavioral data, cognitive abilities, talent, teams, leadership, and work.
permalink: /
---

<section class="hero">
  <div class="shell hero-grid">
    <div>
      <p class="eyebrow">Behavioral intelligence for better decisions</p>
      <h1>Understand people.<br>Improve work.</h1>
      <p class="hero-copy">A growing library of BestWork DATA research, essays, and practical guidance for selecting, developing, and organizing people.</p>
      <a class="button" href="{{ '/library/' | relative_url }}">Explore the library <span aria-hidden="true">&rarr;</span></a>
    </div>
    <div class="hero-stat" aria-label="Library summary">
      <strong>{{ site.articles.size }}</strong>
      <span>documents across</span>
      <strong>{{ site.data.categories.size }}</strong>
      <span>topic collections</span>
    </div>
  </div>
</section>

<section class="shell section">
  <div class="section-heading">
    <div><p class="eyebrow">Browse by subject</p><h2>Knowledge organized for discovery</h2></div>
    <a href="{{ '/library/' | relative_url }}">View all documents</a>
  </div>
  <div class="category-grid">
    {% for category in site.data.categories %}
      <a class="category-card" href="{{ '/library/' | append: category.slug | append: '/' | relative_url }}">
        <span class="category-count">{{ category.count | prepend: '00' | slice: -2, 2 }}</span>
        <h3>{{ category.name }}</h3>
        <p>{{ category.description }}</p>
        <span class="card-link">Browse collection <span aria-hidden="true">&rarr;</span></span>
      </a>
    {% endfor %}
  </div>
</section>

