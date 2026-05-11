import streamlit as st
import base64
from pathlib import Path
import time

# ---------------------------------------------------------
# 설정값
HEADER_HEIGHT = 200  
FOOTER_HEIGHT = 130
SCROLL_CONTENT_HEIGHT = 1640 
# ---------------------------------------------------------

st.set_page_config(page_title="IM세종", layout="centered")

# 1. 상태 저장 및 초기화
if "show_qr" not in st.session_state:
    st.session_state.show_qr = False
if "qr_type" not in st.session_state:
    st.session_state.qr_type = "qr.png"
if "timer_start" not in st.session_state:
    st.session_state.timer_start = 59

# 2. 이미지 로드 함수
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
qr_img_base64 = get_base64(st.session_state.qr_type)

# QR 노출 여부에 따른 블러 처리
blur_style = "filter: blur(10px) brightness(0.5);" if st.session_state.show_qr else ""

# 3. CSS 설정
st.markdown(f"""
<style>
    /* 전체 배경 및 기본 UI 제거 */
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

    .header-fixed {{
        position: absolute;
        top: 0; left: 0; width: 100%;
        height: {HEADER_HEIGHT}px;
        background-image: url("data:image/png;base64,{header_img}");
        background-size: 100% auto;
        background-repeat: no-repeat;
        z-index: 1;
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
        z-index: 1;
        {blur_style}
    }}

    .scroll-area {{
        position: absolute;
        top: {HEADER_HEIGHT}px;
        bottom: {FOOTER_HEIGHT}px;
        left: 0; width: 100%;
        overflow-y: auto;
        z-index: 0;
        {blur_style}
    }}

    .scroll-content {{
        width: 100%;
        height: {SCROLL_CONTENT_HEIGHT}px;
        background-image: url("data:image/png;base64,{scroll_img}");
        background-size: 100% auto;
        background-repeat: no-repeat;
    }}

    .qr-sheet {{
        position: absolute;
        left: 0;
        bottom: {"0" if st.session_state.show_qr else "-100%"};
        width: 100%;
        height: 88%;
        border-radius: 40px 40px 0 0;
        background-image: url("data:image/png;base64,{qr_img_base64}");
        background-size: cover;
        background-position: center top;
        z-index: 100;
        transition: bottom 0.6s cubic-bezier(0.16, 1, 0.3, 1);
    }}

    /* 타이머 디자인 */
    #timer-target::after {{
        content: "{st.session_state.timer_start if st.session_state.show_qr else ''}초 남았습니다.";
        position: absolute;
        top: 50%; left: 42%;
        transform: translate(-50%, -50%);
        color: white; font-size: 18px; font-weight: bold; z-index: 101;
    }}
    
    .refresh-label {{
        position: absolute;
        top: 50%; left: 75%;
        transform: translate(-50%, -50%);
        color: white; font-size: 14px; font-weight: bold;
        background: rgba(255,255,255,0.2);
        padding: 5px 12px; border-radius: 20px;
        z-index: 101; pointer-events: none;
    }}

    /* 버튼 투명화 및 영역 확장 */
    .stButton > button {{
        background: transparent !important;
        color: transparent !important;
        border: none !important;
        width: 100% !important;
        height: 100% !important;
        box-shadow: none !important;
    }}
    .stButton > button:hover {{ color: transparent !important; background: transparent !important; }}
    .stButton > button:active {{ color: transparent !important; background: transparent !important; }}
</style>
""", unsafe_allow_html=True)

# 4. 배경 레이아웃 렌더링
st.markdown(f"""
<div class="phone-container">
    <div class="header-fixed"></div>
    <div class="scroll-area"><div class="scroll-content"></div></div>
    <div class="footer-fixed"></div>
    <div class="qr-sheet">
        <div id="timer-target"></div>
        {"<div class='refresh-label'>새로고침</div>" if st.session_state.show_qr else ""}
    </div>
</div>
""", unsafe_allow_html=True)

# 5. 인터랙션 버튼 레이어 (투명 클릭 영역)
def refresh_action():
    st.session_state.qr_type = "qr2.png" if st.session_state.qr_type == "qr.png" else "qr.png"
    st.session_state.timer_start = 59

if not st.session_state.show_qr:
    # 하단 OPEN 버튼 (푸터 위치에 고정)
    st.markdown(f'<div style="position:fixed; bottom:0; left:50%; transform:translateX(-50%); width:430px; height:{FOOTER_HEIGHT}px; z-index:9999;">', unsafe_allow_html=True)
    if st.button(" ", key="btn_open"):
        st.session_state.show_qr = True
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)
else:
    # 상단 CLOSE 버튼 (헤더 위치에 고정)
    st.markdown(f'<div style="position:fixed; top:0; left:50%; transform:translateX(-50%); width:430px; height:{HEADER_HEIGHT}px; z-index:9999;">', unsafe_allow_html=True)
    if st.button(" ", key="btn_close"):
        st.session_state.show_qr = False
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)
    
    # 중앙 REFRESH 버튼
    st.markdown(f'<div style="position:fixed; top:44%; left:50%; transform:translateX(50px); width:120px; height:60px; z-index:9999;">', unsafe_allow_html=True)
    st.button(" ", key="btn_refresh", on_click=refresh_action)
    st.markdown('</div>', unsafe_allow_html=True)

# 6. 타이머 실시간 루프
if st.session_state.show_qr:
    timer_area = st.empty()
    while st.session_state.timer_start >= 0:
        if not st.session_state.show_qr:
            break
            
        timer_area.markdown(f"""
            <style>
                #timer-target::after {{ content: "{st.session_state.timer_start}초 남았습니다."; }}
            </style>
        """, unsafe_allow_html=True)
        
        time.sleep(1)
        st.session_state.timer_start -= 1
        
        if st.session_state.timer_start < 0:
            st.session_state.timer_start = 0
            break