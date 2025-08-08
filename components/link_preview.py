import streamlit as st
import requests
from bs4 import BeautifulSoup
import re
from urllib.parse import urljoin, urlparse

def get_link_preview(url):
    """Extract preview data from a URL"""
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()

        soup = BeautifulSoup(response.content, 'html.parser')

        # Extract title
        title = ""
        if soup.find('meta', property='og:title'):
            title = soup.find('meta', property='og:title')['content']
        elif soup.find('title'):
            title = soup.find('title').text.strip()
        else:
            title = "No title available"

        # Extract description
        description = ""
        if soup.find('meta', property='og:description'):
            description = soup.find('meta', property='og:description')['content']
        elif soup.find('meta', attrs={'name': 'description'}):
            description = soup.find('meta', attrs={'name': 'description'})['content']
        else:
            description = "No description available"

        # Extract image
        image_url = ""
        if soup.find('meta', property='og:image'):
            image_url = soup.find('meta', property='og:image')['content']
            if image_url.startswith('/'):
                image_url = urljoin(url, image_url)

        # Extract site name
        site_name = ""
        if soup.find('meta', property='og:site_name'):
            site_name = soup.find('meta', property='og:site_name')['content']
        else:
            parsed_url = urlparse(url)
            site_name = parsed_url.netloc

        return {
            'title': title,
            'description': description,
            'image': image_url,
            'site_name': site_name,
            'url': url
        }

    except Exception as e:
        return {
            'title': 'Preview unavailable',
            'description': f'Could not load preview: {str(e)}',
            'image': '',
            'site_name': urlparse(url).netloc,
            'url': url
        }

def show_link_preview(url, link_text=None):
    """Display link with preview functionality"""
    if not link_text:
        link_text = url

    # Create unique key for each link
    link_key = f"preview_{hash(url) % 10000}"

    # Button to show preview
    if st.button(f"🔗 {link_text}", key=link_key, help="Click to preview"):
        st.session_state[f"show_preview_{link_key}"] = True

    # Show preview modal if button was clicked
    if st.session_state.get(f"show_preview_{link_key}", False):
        with st.spinner("Loading preview..."):
            preview_data = get_link_preview(url)

        # Create preview modal
        st.markdown("---")
        st.markdown(f"### Preview: {preview_data['site_name']}")

        col1, col2 = st.columns([2, 1])

        with col1:
            st.markdown(f"**{preview_data['title']}**")
            st.markdown(preview_data['description'])

            col_btns1, col_btns2 = st.columns(2)
            with col_btns1:
                if st.button("🚀 Visit Link", key=f"visit_{link_key}"):
                    st.markdown(f'<a href="{url}" target="_blank">Click here if not redirected</a>', unsafe_allow_html=True)
                    st.success(f"Opening {preview_data['site_name']}...")

            with col_btns2:
                if st.button("❌ Close Preview", key=f"close_{link_key}"):
                    st.session_state[f"show_preview_{link_key}"] = False
                    st.rerun()

        with col2:
            if preview_data['image']:
                try:
                    st.image(preview_data['image'], width=200)
                except:
                    st.info("📷 Image preview unavailable")
            else:
                st.info("📷 No preview image")

        st.markdown("---")

def create_preview_link(url, text=None, description=None):
    """Create a styled link with preview capability"""
    display_text = text or url

    # Generate unique key
    link_key = f"link_{hash(url) % 10000}"

    # Custom CSS for link styling
    st.markdown("""
        <style>
        .preview-link {
            display: inline-block;
            padding: 8px 12px;
            background: #f0f2f6;
            border: 1px solid #ddd;
            border-radius: 6px;
            margin: 5px 0;
            cursor: pointer;
            transition: all 0.2s ease;
        }
        .preview-link:hover {
            background: #e8eaf0;
            border-color: #0066cc;
        }
        .preview-link-title {
            font-weight: 600;
            color: #0066cc;
            margin-bottom: 2px;
        }
        .preview-link-desc {
            font-size: 12px;
            color: #666;
        }
        </style>
    """, unsafe_allow_html=True)

    # Create clickable preview card
    if st.button(
        f"🔗 {display_text}", 
        key=link_key,
        help=f"Click to preview: {url}"
    ):
        st.session_state[f"preview_active_{link_key}"] = True

    # Show preview if activated
    if st.session_state.get(f"preview_active_{link_key}", False):
        show_link_preview(url, display_text)