from bs4 import BeautifulSoup
from markdownify import markdownify as md
import trafilatura

html_doc = """<html>
<head><title>The Dormouse's story</title></head>
<body>
<p class="title"><b>The Dormouse's story</b></p>

<p class="story">Once upon a time there were three little sisters; and their names were
<a href="http://example.com/elsie" class="sister" id="link1">Elsie</a>,
<a href="http://example.com/lacie" class="sister" id="link2">Lacie</a> and
<a href="http://example.com/tillie" class="sister" id="link3">Tillie</a>;
and they lived at the bottom of a well.</p>

<p class="story">...</p>
"""

soup = BeautifulSoup(html_doc, 'html.parser')
print(soup.prettify())

ps = soup.find_all(name="p")
# p = soup.find(name="p", attrs={"id": "link1", 'class':'sister'})
print(ps)

# extract content to string with markdown (incl links)
print(md(soup))

# extract content to string
print(trafilatura.extract(soup))
