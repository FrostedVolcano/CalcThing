# build.py
import os

html_content = """
<!DOCTYPE html>
<html>
<head>
    <meta name="google-site-verification" content="UpK4x268-JAVGifEIIa0LG7x9OFnEFgoBqvRvdxio-E" />
</head>
<body>
    <div id="root"></div>
</body>
</html>
"""

with open("index.html", "w") as f:
    f.write(html_content)