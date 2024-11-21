from jinja2 import (
    Environment,
    FileSystemLoader,
)

# create template from string
environment = Environment()
template = environment.from_string("Hello, {{ name }}!")
compiled_template = template.render(name="World")
with open('out.txt', mode="w", encoding="utf-8") as results:
    results.write(compiled_template)

# load template from file
environment = Environment(loader=FileSystemLoader("./"))
template = environment.get_template("template.txt")
item = {"product": "foo", "price": 100}
compiled_template = template.render(
    item,
    user='Joe Doe',
    vendor='Company.com'
)
with open('template.out.txt', mode="w", encoding="utf-8") as results:
    results.write(compiled_template)

# load template from file with list
items = [
    {"product": "foo", "price": 200},
    {"product": "bar", "price": 100},
    {"product": "baz", "price": 300},
]
environment = Environment(loader=FileSystemLoader("./"))
template = environment.get_template("template.html")
compiled_template = template.render(
    items=items,
    user='Joe Doe',
    vendor='Company.com'
)
with open('template.out.html', mode="w", encoding="utf-8") as results:
    results.write(compiled_template)
