# Home.py (Block 1)

import streamlit as st
from pathlib import Path

# --- PAGE CONFIG ---
st.set_page_config(page_title="My Portfolio", layout="wide")

# --- CUSTOM CSS ---
st.markdown("""
    <style>
    .hero-text {
        font-size: 36px;
        font-weight: 700;
        margin-bottom: 0.5rem;
    }
    .sub-text {
        font-size: 20px;
        color: #6c757d;
    }
    .content-block {
        margin-top: 20px;
        font-size: 18px;
        line-height: 1.6;
    }
    </style>
""", unsafe_allow_html=True)

# --- HERO SECTION ---
# st.image("assets/profile.jpg", width=150)  # You can change the image path

st.markdown('<div class="hero-text">Hi, I\'m Katakam Prashanth</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-text">Python Developer | MongoDB | Streamlit | SEO Learner</div>', unsafe_allow_html=True)

st.markdown('<div class="content-block">Welcome to my portfolio! I love solving real-world problems using simple, elegant tools. </div>', unsafe_allow_html=True)
