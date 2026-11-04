"""Build the Charter pages: embed fonts and photos into one offline HTML file each.

usage: python3 build.py            (from this folder)
Photos: put a JPG or PNG in images/ named after its slot (see README). Missing photos leave a designed placeholder.
Also writes artifact/ copies without the document wrapper, for publishing as a claude.ai Artifact.
"""
import base64, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.dirname(HERE)
FONTS = [
    ("Cinzel", "normal", "400 700", "cinzel-latin-wght.woff2"),
    ("Montserrat", "normal", "300 700", "montserrat-latin-wght.woff2"),
    ("Montserrat", "italic", "400", "montserrat-latin-italic-400.woff2"),
    ("Source Sans 3", "normal", "400 700", "sourcesans3-latin-wght.woff2"),
]


def b64(path):
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode()


def font_css():
    out = []
    for fam, style, weight, fn in FONTS:
        out.append(
            "@font-face{font-family:'%s';font-style:%s;font-weight:%s;font-display:swap;"
            "src:url(data:font/woff2;base64,%s) format('woff2')}" % (fam, style, weight, b64(os.path.join(HERE, "fonts", fn)))
        )
    return "\n".join(out)


def image_uri(slot):
    for ext, mime in ((".jpg", "image/jpeg"), (".jpeg", "image/jpeg"), (".png", "image/png"), (".webp", "image/webp")):
        p = os.path.join(HERE, "images", slot + ext)
        if os.path.exists(p):
            return "data:%s;base64,%s" % (mime, b64(p))
    return ""


def build(template, outname):
    src = open(os.path.join(HERE, template), encoding="utf-8").read()
    src = src.replace("/*__FONTS__*/", font_css())
    used, missing = [], []

    def sub(m):
        uri = image_uri(m.group(1))
        (used if uri else missing).append(m.group(1))
        return uri

    src = re.sub(r"\{\{IMG:([a-z0-9-]+)\}\}", sub, src)
    full = os.path.join(OUT, outname)
    open(full, "w", encoding="utf-8").write(src)

    # Artifact copy: the publisher adds its own document wrapper.
    title = re.search(r"<title>.*?</title>", src, re.S).group(0)
    style = re.search(r"<style>.*?</style>", src, re.S).group(0)
    body = re.search(r"<body>(.*)</body>", src, re.S).group(1)
    art = title + '\n<meta name="claude:viewport-fit-sides" content="cover">\n' + style + "\n" + body.strip() + "\n"
    os.makedirs(os.path.join(HERE, "artifact"), exist_ok=True)
    open(os.path.join(HERE, "artifact", outname), "w", encoding="utf-8").write(art)
    print("wrote %s (%d KB) photos: %s; empty slots: %s" % (outname, len(src) // 1024, ", ".join(used) or "none", ", ".join(missing) or "none"))


if __name__ == "__main__":
    build("template.html", "Chethan-N-for-The-Charter.html")
    build("brief.html", "Charter-Send-Checklist.html")
