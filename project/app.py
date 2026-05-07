import streamlit as st
import base64
from pathlib import Path

# -----------------------------------
# 페이지 설정
# -----------------------------------
st.set_page_config(
    page_title="IM세종",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# -----------------------------------
# 현재 경로
# -----------------------------------
BASE_DIR = Path(__file__).parent

# 이미지 경로
HOME_PATH = BASE_DIR / "home.png"

# -----------------------------------
# 이미지 -> base64 변환
# -----------------------------------
def get_base64(image_path):
    with open(image_path, "rb") as img:
        return base64.b64encode(img.read()).decode()

home_img = get_base64(HOME_PATH)

# -----------------------------------
# 화면 출력
# -----------------------------------
st.markdown(f"""
<style>

/* ---------------------------
   전체 기본 설정
---------------------------- */
html, body, [data-testid="stAppViewContainer"] {{
    margin: 0;
    padding: 0;
    overflow: hidden;
    background: black;

    overscroll-behavior: none;
    touch-action: manipulation;
}}

/* ---------------------------
   Streamlit UI 제거
---------------------------- */

/* 상단 헤더 제거 */
header {{
    display: none !important;
}}

/* 우측 상단 메뉴 제거 */
[data-testid="stToolbar"] {{
    display: none !important;
}}

/* 우하단 streamlit 버튼 제거 */
[data-testid="stStatusWidget"] {{
    display: none !important;
}}

/* deploy 버튼 제거 */
.stDeployButton {{
    display: none !important;
}}

/* footer 제거 */
footer {{
    display: none !important;
}}

/* 기본 패딩 제거 */
.block-container {{
    padding: 0 !important;
    max-width: 430px;
    margin: auto;
}}

/* ---------------------------
   핸드폰 화면
---------------------------- */
.phone {{
    position: relative;

    width: 100%;
    height: 100vh;

    overflow: hidden;

    background-image: url("data:image/png;base64,{home_img}");
    background-size: cover;
    background-position: center top;
    background-repeat: no-repeat;
}}

</style>

<div class="phone"></div>

""", unsafe_allow_html=True)