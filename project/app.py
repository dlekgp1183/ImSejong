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
# 상태 저장
# -----------------------------------
if "show_qr" not in st.session_state:
    st.session_state.show_qr = False

# -----------------------------------
# 이미지 경로
# -----------------------------------
BASE_DIR = Path(__file__).parent

HOME_PATH = BASE_DIR / "home.png"
QR_PATH = BASE_DIR / "qr.png"

# -----------------------------------
# base64 변환
# -----------------------------------
def get_base64(path):
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode()

home_img = get_base64(HOME_PATH)
qr_img = get_base64(QR_PATH)

# -----------------------------------
# 버튼 이벤트
# -----------------------------------
def open_qr():
    st.session_state.show_qr = True

def close_qr():
    st.session_state.show_qr = False

# -----------------------------------
# CSS
# -----------------------------------
st.markdown(f"""
<style>

/* 전체 */
html, body, [data-testid="stAppViewContainer"] {{
    margin: 0;
    padding: 0;
    overflow: hidden;
    background: black;
}}

header, footer {{
    display: none !important;
}}

[data-testid="stToolbar"],
[data-testid="stStatusWidget"] {{
    display: none !important;
}}

.block-container {{
    padding: 0 !important;
    max-width: 430px;
    margin: auto;
}}

/* 폰 영역 */
.phone {{
    position: relative;
    width: 100%;
    height: 100vh;
    overflow: hidden;
    background: black;
}}

/* 홈 화면 */
.home {{
    position: absolute;
    inset: 0;

    background-image: url("data:image/png;base64,{home_img}");
    background-size: cover;
    background-position: center top;

    transition: all 0.4s ease;
}}

/* blur */
.home.blur {{
    filter: blur(10px) brightness(0.7);
    transform: scale(1.03);
}}

/* QR 시트 */
.qr {{
    position: absolute;

    left: 0;
    bottom: 0;

    width: 100%;
    height: 88%;

    border-radius: 30px 30px 0 0;

    background-image: url("data:image/png;base64,{qr_img}");
    background-size: cover;
    background-position: center top;

    box-shadow: 0 -10px 30px rgba(0,0,0,0.35);

    z-index: 10;
}}

</style>
""", unsafe_allow_html=True)

# -----------------------------------
# 메인 화면
# -----------------------------------
phone_html = f"""
<div class="phone">
    <div class="home {'blur' if st.session_state.show_qr else ''}"></div>
"""

# QR 표시 여부
if st.session_state.show_qr:
    phone_html += """
    <div class="qr"></div>
    """

phone_html += "</div>"

st.markdown(phone_html, unsafe_allow_html=True)

# -----------------------------------
# 버튼
# -----------------------------------
btn_col1, btn_col2, btn_col3 = st.columns([1,1,1])

with btn_col2:

    if not st.session_state.show_qr:
        st.button(
            "My QR",
            use_container_width=True,
            on_click=open_qr
        )

    else:
        st.button(
            "닫기",
            use_container_width=True,
            on_click=close_qr
        )