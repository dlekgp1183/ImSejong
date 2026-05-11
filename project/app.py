import streamlit as st
import base64
from pathlib import Path
import time

# ---------------------------------------------------------
# [설정 값] 이미지 비율에 맞춰 이 숫자를 수정하세요 (단위: px)
# 계산법: (이미지 세로 높이 / 이미지 가로 너비) * 430
HEADER_HEIGHT = 200  
FOOTER_HEIGHT = 130
SCROLL_CONTENT_HEIGHT = 1640 # homescroll.png의 전체 세로 길이
# ---------------------------------------------------------

# 1. 페이지 설정
st.set_page_config(page_title="IM세종", layout="centered")

# 2. 상태 저장
if "show_qr" not in st.session_state:
    st.session_state.show_qr = False

# 3. 이미지 로드
BASE_DIR = Path(__file__).parent
def get_base64(path):
    p = BASE_DIR / path
    if p.exists():
        with open(p, "rb") as f:
            return base64.b64encode(f.read()).decode()
    return ""

header_img = get_base64("header.jpg")
footer_img = get_base64("footer.jpg")
scroll_img = get_base64("homescroll.jpg")
qr_img = get_base64("qr.png")

# 4. CSS 설정
blur_style = "filter: blur(10px) brightness(0.5);" if st.session_state.show_qr else ""

st.markdown(f"""
<style>
    [data-testid="stAppViewContainer"] {{ background: black; }}
    header, footer {{ display: none !important; }}
    .block-container {{ padding: 0 !important; max-width: 430px; margin: auto; }}

    /* 전체 컨테이너 */
    .phone-container {{
        position: relative;
        width: 100%;
        height: 100vh;
        overflow: hidden;
        background: black;
    }}

    /* 고정 헤더 */
    .header-fixed {{
        position: absolute;
        top: 0; left: 0; width: 100%;
        height: {HEADER_HEIGHT}px;
        background-image: url("data:image/png;base64,{header_img}");
        background-size: 100% auto;
        background-repeat: no-repeat;
        z-index: 10;
        {blur_style}
    }}

    /* 고정 푸터 */
    .footer-fixed {{
        position: absolute;
        bottom: 0; left: 0; width: 100%;
        height: {FOOTER_HEIGHT}px;
        background-image: url("data:image/png;base64,{footer_img}");
        background-size: 100% auto;
        background-repeat: no-repeat;
        background-position: bottom;
        z-index: 10;
        {blur_style}
    }}

    /* 스크롤 영역 */
    .scroll-area {{
        position: absolute;
        top: {HEADER_HEIGHT}px;
        bottom: {FOOTER_HEIGHT}px;
        left: 0; width: 100%;
        overflow-y: auto;
        overflow-x: hidden;
        {blur_style}
    }}

    /* 스크롤바 숨기기 */
    .scroll-area::-webkit-scrollbar {{ display: none; }}
    .scroll-area {{ -ms-overflow-style: none; scrollbar-width: none; }}

    .scroll-content {{
        width: 100%;
        height: {SCROLL_CONTENT_HEIGHT}px;
        background-image: url("data:image/png;base64,{scroll_img}");
        background-size: 100% auto;
        background-repeat: no-repeat;
    }}

    /* QR 시트 */
    .qr-sheet {{
        position: absolute;
        left: 0;
        bottom: {"0" if st.session_state.show_qr else "-100%"};
        width: 100%;
        height: 88%;
        border-radius: 40px 40px 0 0;
        background-image: url("data:image/png;base64,{qr_img}");
        background-size: cover;
        background-position: center top;
        z-index: 99;
        transition: bottom 0.6s cubic-bezier(0.16, 1, 0.3, 1);
    }}

    /* 타이머 */
    .timer-fixed {{
        position: fixed;
        top: 55%; left: 50%;
        transform: translate(-50%, -50%);
        z-index: 1001;
        color: white; font-size: 18px; font-weight: bold;
        text-align: center; width: 100%;
        pointer-events: none;
    }}

    /* 버튼 스타일 */
    .stButton {{ position: fixed; left: 0; width: 100%; z-index: 1000; }}
    .stButton > button {{
        background: transparent !important;
        color: transparent !important;
        border: none !important;
        width: 100% !important;
        height: {"35vh" if st.session_state.show_qr else "100px"} !important;
    }}
</style>
""", unsafe_allow_html=True)

# 5. 레이아웃 출력
st.markdown(f"""
<div class="phone-container">
    <div class="header-fixed"></div>
    <div class="scroll-area">
        <div class="scroll-content"></div>
    </div>
    <div class="footer-fixed"></div>
    <div class="qr-sheet"></div>
</div>
""", unsafe_allow_html=True)

# 6. 타이머 로직
if st.session_state.show_qr:
    timer_placeholder = st.empty()
    for t in range(59, -1, -1):
        if not st.session_state.show_qr:
            break
        timer_placeholder.markdown(f'<div class="timer-fixed">{t}초 남았습니다.</div>', unsafe_allow_html=True)
        time.sleep(1)

# 7. 투명 버튼
if not st.session_state.show_qr:
    st.markdown(f'<style>.stButton {{ bottom: {FOOTER_HEIGHT}px; }}</style>', unsafe_allow_html=True)
    st.button("OPEN", key="btn_open", on_click=lambda: st.session_state.update({"show_qr": True}))
else:
    st.markdown('<style>.stButton { top: 0; }</style>', unsafe_allow_html=True)
    st.button("CLOSE", key="btn_close", on_click=lambda: st.session_state.update({"show_qr": False}))