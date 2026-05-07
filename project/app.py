import streamlit as st
import base64
from pathlib import Path

# 1. 페이지 설정
st.set_page_config(
    page_title="IM세종",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# 2. 상태 저장
if "show_qr" not in st.session_state:
    st.session_state.show_qr = False

# 3. 이미지 로드 및 Base64 변환
BASE_DIR = Path(__file__).parent
HOME_PATH = BASE_DIR / "home.png"
QR_PATH = BASE_DIR / "qr.png"

def get_base64(path):
    if path.exists():
        with open(path, "rb") as f:
            return base64.b64encode(f.read()).decode()
    return ""

home_img = get_base64(HOME_PATH)
qr_img = get_base64(QR_PATH)

# 4. CSS (슬라이드 애니메이션 최적화)
st.markdown(f"""
<style>
/* 전체 화면 설정 */
[data-testid="stAppViewContainer"] {{
    background: black;
}}

header, footer {{ display: none !important; }}

.block-container {{
    padding: 0 !important;
    max-width: 430px;
    margin: auto;
}}

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
    transition: all 0.5s cubic-bezier(0.4, 0, 0.2, 1);
}}

.home.blur {{
    filter: blur(15px) brightness(0.6);
    transform: scale(1.05);
}}

/* QR 시트 (항상 존재하지만 위치만 아래에 숨김) */
.qr-sheet {{
    position: absolute;
    left: 0;
    bottom: -100%; /* 처음엔 아래에 숨어있음 */
    width: 100%;
    height: 85%;
    border-radius: 30px 30px 0 0;
    background-image: url("data:image/png;base64,{qr_img}");
    background-size: cover;
    background-position: center top;
    box-shadow: 0 -10px 40px rgba(0,0,0,0.5);
    z-index: 99;
    transition: bottom 0.5s cubic-bezier(0.4, 0, 0.2, 1);
}}

/* 활성화 시 올라오는 클래스 */
.qr-sheet.active {{
    bottom: 0;
}}

/* 버튼들을 HTML 위에 띄우기 위한 설정 */
.stButton {{
    position: fixed;
    bottom: 30px;
    left: 50%;
    transform: translateX(-50%);
    z-index: 1000;
    width: 200px;
}}
</style>
""", unsafe_allow_html=True)

# 5. 메인 화면 구성
# 클래스 조건부 부여
home_class = "home blur" if st.session_state.show_qr else "home"
qr_class = "qr-sheet active" if st.session_state.show_qr else "qr-sheet"

# HTML은 한 번에 렌더링
phone_html = f"""
<div class="phone">
    <div class="{home_class}"></div>
    <div class="{qr_class}"></div>
</div>
"""
st.markdown(phone_html, unsafe_allow_html=True)

# 6. 버튼 (UI 하단 중앙 배치)
if not st.session_state.show_qr:
    if st.button("My QR", key="open_btn"):
        st.session_state.show_qr = True
        st.rerun()
else:
    if st.button("닫기", key="close_btn"):
        st.session_state.show_qr = False
        st.rerun()