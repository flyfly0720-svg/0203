import streamlit as st

# -----------------------------
# 페이지 설정
# -----------------------------
st.set_page_config(
    page_title="생활기록부 바이트 자가 점검",
    layout="centered"
)

st.title("🧑‍🎓 생활기록부 바이트 자가 점검")
st.caption("학생이 직접 확인하는 간단 점검용 도구")

# -----------------------------
# 바이트 기준 (고정)
# -----------------------------
MAX_BYTES = 1500

st.info("📌 기준: 생활기록부 한 항목당 **1500 byte**")

# -----------------------------
# 입력 영역
# -----------------------------
text = st.text_area(
    "✏️ 작성한 내용을 그대로 붙여 넣으세요",
    height=260,
    placeholder="예) 수업 시간에 질문을 통해 개념을 확장하려는 태도를 보였으며..."
)

# -----------------------------
# 바이트 계산 함수
# -----------------------------
def calculate_bytes(text):
    total = 0
    for ch in text:
        if ord(ch) <= 127:
            total += 1   # 영문, 숫자, 기본 기호
        else:
            total += 3   # 한글, 한자, 기타
    return total

current_bytes = calculate_bytes(text)

# -----------------------------
# 결과 표시
# -----------------------------
st.subheader("📊 현재 상태")

progress = min(current_bytes / MAX_BYTES, 1.0)
st.progress(progress)

col1, col2 = st.columns(2)
col1.metric("현재 바이트", f"{current_bytes}")
col2.metric("남은 바이트", f"{MAX_BYTES - current_bytes}")

# -----------------------------
# 상태 피드백 (학생용 문장)
# -----------------------------
if current_bytes == 0:
    st.warning("아직 입력된 내용이 없어요.")
elif current_bytes < MAX_BYTES * 0.8:
    st.success("👍 여유 있어요. 구체적인 활동을 더 써도 돼요.")
elif current_bytes < MAX_BYTES:
    st.info("🙂 거의 다 찼어요. 표현을 다듬으면서 마무리해요.")
elif current_bytes == MAX_BYTES:
    st.warning("⚠️ 딱 맞아요. 이 상태로 제출하면 좋아요.")
else:
    st.error("❌ 바이트 초과! 불필요한 표현을 줄여야 해요.")

# -----------------------------
# 자가 점검 체크리스트
# -----------------------------
st.subheader("✅ 자가 점검 체크")

st.checkbox("과목명 또는 활동 맥락이 드러나는가?")
st.checkbox("단순 태도보다 **구체적 행동**이 쓰였는가?")
st.checkbox("‘열심히’, ‘성실히’ 같은 반복 표현을 줄였는가?")
st.checkbox("결과보다 **과정·사고**가 드러나는가?")

# -----------------------------
# 도움말
# -----------------------------
with st.expander("💡 바이트 줄이는 팁"):
    st.markdown("""
- 의미 없는 수식어 제거  
  → *매우*, *항상*, *꾸준히*  
- 같은 뜻 반복 제거  
- 문장 끝 표현 통일  
  → `~함`, `~보임`
- 접속어 과다 사용 주의  
  → 그리고, 또한, 또한
""")

# -----------------------------
# 마무리 메시지
# -----------------------------
st.caption("이 도구는 **자가 점검용**입니다. 최종 판단은 교사가 합니다.")
