import streamlit as st
import base64
from pathlib import Path
import time

# ---------------------------------------------------------
# 설정 및 상수
# ---------------------------------------------------------
HEADER_HEIGHT = 200  
FOOTER_HEIGHT = 130
SCROLL_CONTENT_HEIGHT = 1640 

st.set_page_config(page_title="IM세종", layout="centered")

if "show_qr" not in st.session_state:
    st.session_state.show_qr = False

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

# ---------------------------------------------------------
# CSS 스타일링
# ---------------------------------------------------------
blur_style = "filter: blur(10px) brightness(0.5);" if st.session_state.show_qr else ""

st.markdown(f"""
<style>
    [data-testid="stAppViewContainer"] {{ background: black; }}
    header, footer {{ display: none !important; }}
    .block-container {{ padding: 0 !important; max-width: 430px; margin: auto; }}

    .phone-container {{
        position: relative;
        width: 100%;
        height: 100vh;
        overflow: hidden;
        background: black;
    }}

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

    .scroll-area {{
        position: absolute;
        top: {HEADER_HEIGHT}px;
        bottom: {FOOTER_HEIGHT}px;
        left: 0; width: 100%;
        overflow-y: auto;
        overflow-x: hidden;
        {blur_style}
    }}

    .scroll-area::-webkit-scrollbar {{ display: none; }}

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

    /* 투명 버튼 스타일 */
    .stButton > button {{
        background: transparent !important;
        color: transparent !important;
        border: none !important;
        width: 100% !important;
        cursor: pointer;
    }}
</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# 기본 레이아웃 렌더링
# ---------------------------------------------------------
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

# ---------------------------------------------------------
# 버튼 및 타이머 로직 (핵심 수정 구간)
# ---------------------------------------------------------

# 1. 닫기/열기 버튼을 타이머보다 먼저 배치 (즉시 나타나게 함)
if not st.session_state.show_qr:
    # 홈 화면: 하단 footer 클릭 시 열기
    st.markdown(f'<style>.stButton {{ position: fixed; bottom: 0; height: {FOOTER_HEIGHT}px; z-index: 1000; }}</style>', unsafe_allow_html=True)
    st.button("OPEN", key="btn_open", on_click=lambda: st.session_state.update({"show_qr": True}))
else:
    # QR 화면: 상단 header 클릭 시 닫기
    st.markdown(f'<style>.stButton {{ position: fixed; top: 0; height: {HEADER_HEIGHT}px; z-index: 10000; }}</style>', unsafe_allow_html=True)
    st.button("CLOSE", key="btn_close", on_click=lambda: st.session_state.update({"show_qr": False}))

    # 2. 타이머 텍스트 및 새로고침 아이콘 표시
    timer_placeholder = st.empty()
    
    # SVG 새로고침 아이콘
    refresh_svg = """
    <svg width="20" height="20" viewBox="0 0 24 24" fill="white" style="margin-left:8px;">
        <path d="M17.65 6.35A7.958 7.958 0 0012 4c-4.42 0-7.99 3.58-7.99 8s3.57 8 7.99 8c3.73 0 6.84-2.55 7.73-6h-2.08c-.82 2.33-3.04 4-5.65 4-3.31 0-6-2.69-6-6s2.69-6 6-6c1.66 0 3.14.69 4.22 1.78L13 11h7V4l-2.35 2.35z"/>
    </svg>
    """

    # 3. 타이머 루프
    for t in range(59, -1, -1):
        if not st.session_state.show_qr:
            break
        
        timer_placeholder.markdown(f"""
            <div style="
                position: fixed;
                top: 51%; 
                left: 50%;
                transform: translate(-50%, -50%);
                z-index: 1001;
                width: 100%;
                display: flex;
                justify-content: center;
                align-items: center;
                pointer-events: none;
            ">
                <span style="
                    color: white;
                    font-size: 19px;
                    font-weight: bold;
                    text-shadow: 2px 2px 4px rgba(0,0,0,0.5);
                ">
                    {t:02d}초 남았습니다.
                </span>
                {refresh_svg}
            </div>
        """, unsafe_allow_html=True)
        time.sleep(1)

    # 타이머 종료 후 처리
    if st.session_state.show_qr:
        st.session_state.show_qr = False
        st.rerun()