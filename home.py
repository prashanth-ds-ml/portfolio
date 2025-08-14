import streamlit as st
import json
import textwrap
from pathlib import Path
from components.link_preview import create_preview_link, show_link_preview

# Try to import utils, create empty functions if not available
try:
    from utils import read_markdown_posts, youtube_id, get_post_by_slug
except ImportError:
    def read_markdown_posts():
        return []
    def youtube_id(url):
        return None
    def get_post_by_slug(slug):
        return None

# --- PAGE CONFIG ---
st.set_page_config(
    page_title="Katakam Prashanth – Portfolio",
    layout="centered",
)

# --- STYLES ---
CENTER_STYLE = """
<style>
main .block-container {max-width: 880px;}
h1, h2, h3 {font-weight: 700;}
p {line-height: 1.6;}
hr {margin: 1.25rem 0;}
.small {opacity: 0.8; font-size: 0.9rem;}
.badge {display:inline-block; padding:2px 8px; border-radius:999px; background:#f1f5f9; margin-right:6px;}
.links a {margin-right: 12px;}
.bio-text {
    font-size: 16px;
    line-height: 1.6;
    color: #333;
    margin-bottom: 20px;
    text-align: justify;
}
</style>
"""
st.markdown(CENTER_STYLE, unsafe_allow_html=True)

# --- HERO ---
st.title("Katakam Prashanth")
st.caption("Python Developer · Backend Development · Database Management")
st.markdown(
    '<p class="links">\n'
    '<a href="https://github.com/yourname" target="_blank">GitHub</a>'
    '<a href="https://linkedin.com/in/yourname" target="_blank">LinkedIn</a>'
    '<a href="resume.pdf" target="_blank">Resume</a>'
    '<a href="mailto:prashanth@example.com" target="_blank">Email</a>'
    '</p>',
    unsafe_allow_html=True,
)

st.divider()

# --- ABOUT ---
st.header("About")
st.write(textwrap.dedent("""
Hi! I'm Prashanth, a Python developer focused on building robust backend applications and working with databases. 
I enjoy solving problems through code and am particularly interested in data processing, web application development, 
and creating efficient, scalable solutions.

My work primarily involves Python development, MongoDB database management, and building web applications with 
frameworks like Streamlit. I believe in writing clean, maintainable code and continuously learning new technologies 
to improve my craft.
"""))

st.divider()

# --- PROJECTS ---
st.header("Projects")
projects = []
try:
    with open("data/projects.json", "r", encoding="utf-8") as f:
        projects = json.load(f)
except FileNotFoundError:
    st.info("Add your project entries in data/projects.json")

for p in projects:
    st.subheader(p["title"])
    st.write(p.get("desc", ""))

    links = []
    if p.get("github"): links.append(f"[💻 GitHub]({p['github']})")
    if p.get("live"):   links.append(f"[🚀 Live Demo]({p['live']})")
    if links:
        st.markdown(" | ".join(links))

    yt_url = p.get("youtube")
    if yt_url:
        st.video(yt_url)

    tags = p.get("tags", [])
    if tags:
        st.markdown(" ".join([f"<span class='badge'>{t}</span>" for t in tags]), unsafe_allow_html=True)
    st.markdown("---")


# --- BLOG ---

# --- BLOG ---
st.header("Blog")
posts = read_markdown_posts()
if not posts:
    st.info("No blog posts yet. Add Markdown files to the blog/ folder.")
else:
    for post in posts:
        blog_url = f"/static_blog/{post['slug']}.html"
        st.markdown(f"### {post['title']}")
        if post.get("date"):
            st.caption(post["date"])
        if post.get("summary"):
            st.write(post["summary"])
        tags = post.get("tags", [])
        if tags:
            st.markdown(" ".join([f"<span class='badge'>{t}</span>" for t in tags]), unsafe_allow_html=True)
        st.markdown(f"<a href='{blog_url}' target='_blank' style='display:inline-block;margin-top:8px;margin-bottom:8px;font-weight:600;color:#2563eb;'>Read more &rarr;</a>", unsafe_allow_html=True)
        st.markdown("---")

# --- EXTERNAL LINKS WITH PREVIEW ---
st.header("Articles & External Links")
st.markdown("**Professional Articles & Posts:**")

col1, col2 = st.columns(2)

with col1:
    if st.button("📝 LinkedIn Articles", key="linkedin_articles"):
        show_link_preview("https://www.linkedin.com/in/yourname/recent-activity/posts/", "My LinkedIn Articles")

with col2:
    if st.button("📚 Medium Articles", key="medium_articles"):
        show_link_preview("https://medium.com/@yourname", "Medium Profile")

st.divider()

# --- CURRENTLY ---
st.header("Currently")
st.write(textwrap.dedent("""
I'm working on improving my skills in backend development and exploring machine learning integration 
with web applications. Always learning new ways to optimize database performance and write better Python code.

Current focus areas:
- Advanced MongoDB optimization techniques
- Building scalable REST APIs
- Streamlit application development
- Code quality and testing practices
"""))

st.divider()

# --- RESUME & CONTACT ---
st.header("Resume & Contact")
st.markdown("""
📄 [Download Resume](resume.pdf)  
📧 prashanth@example.com  
🐙 [GitHub](https://github.com/yourname) · 💼 [LinkedIn](https://linkedin.com/in/yourname)
""")

st.caption("© 2025 Katakam Prashanth. Built with Streamlit.")