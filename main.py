import streamlit as st
import re

# -----------------------------
# 페이지 설정
# -----------------------------
st.set_page_config(page_title="생활기록부 자가 점검", layout="centered")
st.title("🧑‍🎓 생활기록부 구조 · 바이트 자가 점검")

st.caption("색으로 구조를 확인하고, 바이트를 함께 점검하세요")

MAX_BYTES = 1500
st.info("📌 기준: 항목당 1500 byte")

# -----------------------------
# 입력
# -----------------------------
text = st.text_area(
    "✏️ 문장 앞에 태그를 붙여 입력하세요",
    height=280,
    placeholder="[행동] 수업 중 질문을 통해 개념을 확장함."
)

# -----------------------------
# 바이트 계산
# -----------------------------
def calculate_bytes(text):
    total = 0
    for ch in text:
        total += 1 if ord(ch) <= 127 else 3
    return total

current_bytes = calculate_bytes(text)

# -----------------------------
# 하이라이트 규칙
# -----------------------------
highlight_rules = {
    r"\[행동\](.*)": ("#cce5ff", "🔵 구체적 행동"),
    r"\[동기\](.*)": ("#f8d7da", "🔴 동기"),
    r"\[결론\](.*)": ("#d4edda", "🟢 결론"),
    r"\[참고\](.*)": ("#e2d9f3", "🟣 참고 문헌"),
    r"\[느낀점\](.*)": ("#ffe5b4", "🟠 느낀점"),
}

# -----------------------------
# 하이라이트 처리
# -----------------------------
def highlight_text(text):
    lines = text.split("\n")
    result = []

    for line in lines:
        applied = False
        for pattern, (color, _) in highlight_rules.items():
            match = re.match(pattern, line)
            if match:
                content = match.group(1)
                result.append(
                    f"<div style='background-color:{color}; padding:6px; border-radius:6px; margin-bottom:4px;'>"
                    f"{content}</div>"
                )
                applied = True
                break
        if not applied:
            result.append(f"<div style='margin-bottom:4px;'>{line}</div>")

    return "".join(result)

# -----------------------------
# 결과 출력
# -----------------------------
st.subheader("🎨 구조 하이라이트 결과")
st.markdown(highlight_text(text), unsafe_allow_html=True)

# -----------------------------
# 바이트 상태
# -----------------------------
st.subheader("📊 바이트 상태")

progress = min(current_bytes / MAX_BYTES, 1.0)
st.progress(progress)

col1, col2 = st.columns(2)
col1.metric("현재 바이트", current_bytes)
col2.metric("남은 바이트", MAX_BYTES - current_bytes)

if current_bytes > MAX_BYTES:
    st.error("❌ 바이트 초과! 표현을 줄이세요.")
elif current_bytes > MAX_BYTES * 0.8:
    st.warning("⚠️ 거의 찼어요. 불필요한 수식어 점검!")
else:
    st.success("✅ 바이트 여유 있음")

# -----------------------------
# 안내
# -----------------------------
with st.expander("ℹ️ 태그 안내"):
    st.markdown("""
- 🔵 `[행동]` : 실제로 한 구체적 활동  
- 🔴 `[동기]` : 왜 그렇게 했는지  
- 🟢 `[결론]` : 변화·성과·의미  
- 🟣 `[참고]` : 자료·탐구 출처  
- 🟠 `[느낀점]` : 배운 점·성찰  
""")

st.caption("※ 이 도구는 **자가 점검용**입니다.")
