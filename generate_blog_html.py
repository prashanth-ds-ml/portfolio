import os
import markdown
import frontmatter

BLOG_DIR = "blog"
STATIC_DIR = "static_blog"
TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>{title}</title>
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="description" content="{summary}">
  <style>
    body {{ max-width: 700px; margin: 2rem auto; font-family: sans-serif; line-height: 1.7; padding: 0 1rem; }}
    h1, h2, h3 {{ color: #1a4fa0; }}
    pre {{ background: #f4f4f4; padding: 1em; overflow-x: auto; }}
    code {{ background: #f4f4f4; padding: 2px 4px; border-radius: 3px; }}
    .meta {{ color: #888; font-size: 0.95em; margin-bottom: 2em; }}
    a {{ color: #1a4fa0; text-decoration: none; }}
    a:hover {{ text-decoration: underline; }}
    .back {{ display: inline-block; margin-bottom: 2em; }}
  </style>
</head>
<body>
  <a href="../" class="back">&larr; Back to Portfolio</a>
  <h1>{title}</h1>
  <div class="meta">
    <strong>Date:</strong> {date} <br>
    <strong>Tags:</strong> {tags}
  </div>
  <div>
    {content}
  </div>
</body>
</html>
"""

def slugify(filename):
    return os.path.splitext(filename)[0]

def main():
    if not os.path.exists(STATIC_DIR):
        os.makedirs(STATIC_DIR)

    for fname in os.listdir(BLOG_DIR):
        if fname.endswith(".md"):
            path = os.path.join(BLOG_DIR, fname)
            post = frontmatter.load(path)
            html_content = markdown.markdown(
                post.content,
                extensions=["fenced_code", "codehilite", "tables", "nl2br"]
            )
            slug = slugify(fname)
            tags = ", ".join(post.get("tags", []))
            html = TEMPLATE.format(
                title=post.get("title", slug),
                date=post.get("date", ""),
                tags=tags,
                summary=post.get("summary", ""),
                content=html_content
            )
            out_path = os.path.join(STATIC_DIR, f"{slug}.html")
            with open(out_path, "w", encoding="utf-8") as f:
                f.write(html)
            print(f"Generated {out_path}")



if __name__ == "__main__":
    main()