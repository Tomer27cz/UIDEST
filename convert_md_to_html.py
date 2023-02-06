import markdown
md = 'README.md'
html = 'Assets/html/README.html'
html_dark = 'Assets/html/README_dark.html'

light_head = """<head>
<style>
    p{color: #24292f}
    a{color: #0969da}
    h1{color: #24292f}
    h2{color: #24292f}
    h3{color: #24292f}
    body{background: #ebebeb}
</style>
</head>"""

dark_head = """<head>
<style>
    p{color: #c9d1d9}
    a{color: #58a6ff}
    h1{color: #c9d1d9}
    h2{color: #c9d1d9}
    h3{color: #c9d1d9}
    body{background: #242424}
</style>
</head>"""


with open(md, 'r') as f:
    text = f.read()

html_txt = markdown.markdown(text)

html_text_light = light_head + '<body>' + html_txt + '</body>'
html_text_dark = dark_head + '<body>' + html_txt + '</body>'

with open(html, 'w') as f:
    f.write(html_text_light)

with open(html_dark, 'w') as f:
    f.write(html_text_dark)
