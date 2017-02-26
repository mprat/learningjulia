---
layout: default
---

# All Posts

If you want to go through my entire journey through Julia, here are all the posts, first to last (there are a total of {{ site.posts.size }}):

<ul class="post-list">
	{% for post in site.posts reversed %}
	  <li>
	    <span class="post-meta">{{ post.date | date: "%b %-d, %Y" }}</span>: <a href="{{ post.url | relative_url }}">{{ post.title | escape }}</a>
	  </li>
	{% endfor %}
</ul>

Hope you enjoyed it!
