import streamlit as st
import base64
from pathlib import Path

# 1. 페이지 설정
st.set_page_config(page_title="IM세종", layout="centered")

# 2. 상태 저장
if "show_qr" not in st.session_state:
    st.session_state.show_qr = False

# 3. 이미지 로드
BASE_DIR = Path(__file__).parent
def get_base64(path):
    if Path(path).exists():
        with open(path, "rb") as f:
            return base64.b64encode(f.read()).decode()
    return ""

home_img = get_base64(BASE_DIR / "home.png")
qr_img = get_base64(BASE_DIR / "qr.png")

# 4. CSS 및 스타일 설정
blur_style = f"""
    filter: blur(10px) brightness(0.5) saturate(0.8);
    transform: scale(1.1);
""" if st.session_state.show_qr else ""

st.markdown(f"""
<style>
    [data-testid="stAppViewContainer"] {{ background: black; }}
    header, footer {{ display: none !important; }}
    .block-container {{ padding: 0 !important; max-width: 430px; margin: auto; }}

    .phone {{
        position: relative;
        width: 100%;
        height: 100vh;
        overflow: hidden;
        background: black;
    }}

    .home {{
        position: absolute;
        inset: 0;
        background-image: url("data:image/png;base64,{home_img}");
        background-size: cover;
        background-position: center top;
        transition: all 0.6s ease;
        {blur_style}
    }}

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
        box-shadow: 0 -15px 50px rgba(0,0,0,0.8);
        z-index: 99;
        transition: bottom 0.6s cubic-bezier(0.16, 1, 0.3, 1);
    }}

    .timer-overlay {{
        position: absolute;
        top: 52.5%; 
        left: 50%;
        transform: translate(-50%, -50%);
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 10px;
        width: 100%;
        z-index: 101;
        pointer-events: none;
    }}

    .timer-text {{
        color: white;
        font-size: 18px;
        font-family: sans-serif;
    }}

    .refresh-btn {{
        pointer-events: auto;
        cursor: pointer;
        width: 22px;
        height: 22px;
        fill: white;
    }}

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

# 5. HTML 및 타이머 자바스크립트
phone_content = f"""
<div class="phone">
    <div class="home"></div>
    <div class="qr-sheet">
        <div class="timer-overlay">
            <span id="countdown_text" class="timer-text">59초 남았습니다.</span>
            <svg class="refresh-btn" id="refresh_svg" viewBox="0 0 24 24">
                <path d="M17.65 6.35C16.2 4.9 14.21 4 12 4c-4.42 0-7.99 3.58-7.99 8s3.57 8 7.99 8c3.73 0 6.84-2.55 7.73-6h-2.08c-.82 2.33-3.04 4-5.65 4-3.31 0-6-2.69-6-6s2.69-6 6-6c1.66 0 3.14.69 4.22 1.78L13 11h7V4l-2.35 2.35z"/>
            </svg>
        </div>
    </div>
</div>

<script>
    (function() {{
        let timeLeft = 59;
        const textEl = document.getElementById('countdown_text');
        const refreshEl = document.getElementById('refresh_svg');

        // 타이머 로직
        const timerInterval = setInterval(() => {{
            if (timeLeft > 0) {{
                timeLeft--;
            }} else {{
                timeLeft = 59;
            }}
            
            if (textEl) {{
                textEl.innerText = timeLeft + "초 남았습니다.";
            }} else {{
                clearInterval(timerInterval);
            }}
        }}, 1000);

        // 리셋 버튼 로직
        if (refreshEl) {{
            refreshEl.onclick = () => {{
                timeLeft = 59;
                if (textEl) textEl.innerText = "59초 남았습니다.";
            }};
        }}
    }})();
</script>
"""

st.markdown(phone_content, unsafe_allow_html=True)

# 6. 투명 버튼 (오픈/닫기)
if not st.session_state.show_qr:
    st.markdown('<style>.stButton { bottom: 80px; }</style>', unsafe_allow_html=True)
    st.button("OPEN", key="btn_open", on_click=lambda: st.session_state.update({"show_qr": True}))
else:
    st.markdown('<style>.stButton { top: 0; }</style>', unsafe_allow_html=True)
    st.button("CLOSE", key="btn_close", on_click=lambda: st.session_state.update({"show_qr": False}))