import streamlit as st

# -----------------------------
# 페이지 설정
# -----------------------------
st.set_page_config(page_title="생활기록부 바이트 계산기", layout="centered")
st.title("🧾 생활기록부 바이트 계산기")

st.markdown("""
생활기록부 입력 내용을 **바이트 기준**으로 계산합니다.  
(교육청 시스템과 동일한 방식)
""")

# -----------------------------
# 기준 설정
# -----------------------------
MAX_BYTES = st.selectbox(
    "📌 항목별 바이트 기준 선택",
    [500, 1000, 1500, 2000],
    index=2
)

# -----------------------------
# 텍스트 입력
# -----------------------------
text = st.text_area(
    "✏️ 생활기록부 내용을 입력하세요",
    height=250,
    placeholder="예) 수업에 성실히 참여하며 개념 이해도가 높고..."
)

# -----------------------------
# 바이트 계산 함수
# -----------------------------
def calculate_bytes(text):
    total = 0
    for ch in text:
        if ord(ch) <= 127:
            total += 1      # 영문, 숫자, 특수문자
        else:
            total += 3      # 한글, 한자, 기타 유니코드
    return total

current_bytes = calculate_bytes(text)

# -----------------------------
# 결과 출력
# -----------------------------
st.subheader("📊 바이트 계산 결과")

col1, col2 = st.columns(2)

col1.metric("현재 바이트", f"{current_bytes} byte")
col2.metric("기준 바이트", f"{MAX_BYTES} byte")

progress = min(current_bytes / MAX_BYTES, 1.0)
st.progress(progress)

# -----------------------------
# 상태 메시지
# -----------------------------
if current_bytes < MAX_BYTES:
    st.success(f"✅ {MAX_BYTES - current_bytes} byte 남았습니다.")
elif current_bytes == MAX_BYTES:
    st.warning("⚠️ 정확히 기준 바이트에 도달했습니다.")
else:
    st.error(f"❌ {current_bytes - MAX_BYTES} byte 초과했습니다.")

# -----------------------------
# 추가 정보
# -----------------------------
with st.expander("ℹ️ 바이트 계산 기준 안내"):
    st.markdown("""
- 한글 / 한자 / 대부분의 특수문자: **3 byte**
- 영문 / 숫자 / 기본 특수문자: **1 byte**
- 실제 교육행정정보시스템(NEIS) 기준과 동일
""")







import streamlit as st
import re

st.set_page_config(page_title="생활기록부 맥락 분류", layout="centered")
st.title("📘 생활기록부 맥락 기반 자동 분류 (동기·행동·평가·느낀점)")

text = st.text_area(
    "줄글로 입력하세요",
    height=200,
    placeholder=(
        "수업 중 문제를 변형하여 풀이 전략을 설명함."
        "친구들이 이해하기 어려워했기 때문임."
        "개념 이해와 의사소통 능력이 향상됨."
        "설명하는 과정에서 나도 더 깊이 이해하게 됨."
    )
)

def split_sentences(text):
    return [s.strip() for s in re.split(r"[.!?]", text) if s.strip()]

def classify_context(text):
    sentences = split_sentences(text)

    result = {
        "동기": [],
        "행동": [],
        "평가": [],
        "느낀점": []
    }

    for s in sentences:
        # 🔴 동기
        if any(k in s for k in ["때문", "어려워", "필요", "문제", "부족"]):
            result["동기"].append(s)

        # 🟠 느낀점
        elif any(k in s for k in ["깨닫", "느끼", "이해하게", "생각하게", "의미"]):
            result["느낀점"].append(s)

        # 🟢 평가
        elif any(k in s for k in ["향상", "신장", "강화", "돋보", "성장", "능력"]):
            result["평가"].append(s)

        # 🔵 행동
        else:
            result["행동"].append(s)

    return result

if text:
    st.divider()
    st.subheader("📌 분류 결과")

    icons = {
        "동기": "🔴 [동기]",
        "행동": "🔵 [행동]",
        "평가": "🟢 [평가]",
        "느낀점": "🟠 [느낀점]"
    }

    classified = classify_context(text)

    for key in ["동기", "행동", "평가", "느낀점"]:
        if classified[key]:
            st.markdown(f"**{icons[key]}** {' '.join(classified[key])}")

