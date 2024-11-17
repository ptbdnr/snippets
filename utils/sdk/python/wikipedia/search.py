import wikipedia

SEARCH_TERM = 'Python (programming language)'

page_names = wikipedia.search(SEARCH_TERM)
for page_idx, page_name in enumerate(page_names):
    print(page_name)
    try:
        page = wikipedia.page(page_name)
        print(page.content)
    except Exception as ex:
        print(ex)
        continue
