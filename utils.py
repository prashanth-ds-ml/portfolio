
from __future__ import annotations
import re, pathlib
import frontmatter

ROOT = pathlib.Path(__file__).parent
BLOG_DIR = ROOT / "blog"

def read_markdown_posts():
    posts = []
    if not BLOG_DIR.exists():
        return posts
    for md_path in sorted(BLOG_DIR.glob("*.md"), reverse=True):
        try:
            post = frontmatter.load(md_path)
            meta = post.metadata
            content = post.content
            posts.append({
                "slug": md_path.stem,
                "title": meta.get("title", md_path.stem.replace('-', ' ').title()),
                "date": meta.get("date", ""),
                "summary": meta.get("summary", ""),
                "tags": meta.get("tags", []),
                "content": content,
            })
        except Exception as e:
            continue
    return posts

def get_post_by_slug(slug: str):
    """Return a single post dict by slug, or None if not found."""
    md_path = BLOG_DIR / f"{slug}.md"
    if not md_path.exists():
        return None
    try:
        post = frontmatter.load(md_path)
        meta = post.metadata
        content = post.content
        return {
            "slug": md_path.stem,
            "title": meta.get("title", md_path.stem.replace('-', ' ').title()),
            "date": meta.get("date", ""),
            "summary": meta.get("summary", ""),
            "tags": meta.get("tags", []),
            "content": content,
        }
    except Exception:
        return None

_YT_PATTERNS = [
    r"https?://www\.youtube\.com/watch\?v=([\w-]{6,})",
    r"https?://youtu\.be/([\w-]{6,})",
]

def youtube_id(url: str) -> str | None:
    for pat in _YT_PATTERNS:
        m = re.match(pat, url)
        if m:
            return m.group(1)
    return None
