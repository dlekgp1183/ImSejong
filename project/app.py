import streamlit as st
import base64
from pathlib import Path

# 현재 app.py 기준 경로
BASE_DIR = Path(__file__).parent

# 이미지 경로
HOME_PATH = BASE_DIR / "home.png"

# 페이지 설정
st.set_page_config(
    layout="centered",
    initial_sidebar_state="collapsed"
)

# 이미지 base64 변환
def get_base64(image_path):
    with open(image_path, "rb") as img:
        return base64.b64encode(img.read()).decode()

home_img = get_base64(HOME_PATH)

# HTML + CSS
st.markdown(f"""
<style>

html, body, [data-testid="stAppViewContainer"] {{
    margin: 0;
    padding: 0;
    overflow: hidden;
    background: black;
}}

header {{
    display: none;
}}

.block-container {{
    padding: 0 !important;
    max-width: 430px;
    margin: auto;
}}

.phone {{
    width: 100%;
    height: 100vh;

    background-image: url("data:image/png;base64,{home_img}");
    background-size: cover;
    background-position: center;
}}

</style>

<div class="phone"></div>

""", unsafe_allow_html=True)