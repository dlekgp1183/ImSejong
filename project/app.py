import streamlit as st
import base64

# 페이지 설정
st.set_page_config(
    layout="centered",
    initial_sidebar_state="collapsed"
)

# 이미지 base64 변환
def get_base64(image_path):
    with open(image_path, "rb") as img:
        return base64.b64encode(img.read()).decode()

home_img = get_base64("home.png")

# HTML + CSS
st.markdown(f"""
<style>

/* 전체 기본 설정 */
html, body, [data-testid="stAppViewContainer"] {{
    margin: 0;
    padding: 0;
    overflow: hidden;
    background: black;
}}

/* 상단 스트림릿 헤더 제거 */
header {{
    display: none;
}}

/* 기본 여백 제거 */
.block-container {{
    padding: 0 !important;
    max-width: 430px;
    margin: auto;
}}

/* 핸드폰 화면 */
.phone {{
    position: relative;

    width: 100%;
    height: 100vh;

    overflow: hidden;

    background-image: url("data:image/png;base64,{home_img}");
    background-size: cover;
    background-position: center;
}}

</style>

<div class="phone"></div>

""", unsafe_allow_html=True)