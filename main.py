import streamlit as st
import re

st.set_page_config(page_title="생활기록부 자가 점검", layout="centered")
st.title("🧑‍🎓 생활기록부 구조 하이라이트 점검")

MAX_BYTES = 1500
st.info("📌 기준: 1500 byte")

text = st.text_area(
    "✏️ 태그를 붙여 입력하세요",
    height=280,
    placeholder="[행동] 수업 중 문제를 변형하여 풀이 과정을 설명함."
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
    "행동": "#cce5ff",   # 파랑
    "동기": "#f8d7da",   # 빨강
    "결론": "#d4edda",   # 초록
    "참고": "#e2d9f3",   # 보라
    "느낀점": "#ffe5b4", # 주황
}

# -----------------------------
# 하이라이트 처리
# -----------------------------
def highlight_text(text):
    lines = text.split("\n")
    html_lines = []

    for line in lines:
        stripped = line.strip()
        applied = False

        for tag, color in highlight_rules.items():
            pattern = rf"\[{tag}\]"
            if re.search(pattern, stripped):
                content = re.sub(pattern, "", stripped)
                html_lines.append(
                    f"""
                    <div style="
                        background-color:{color};
                        padding:8px;
                        border-radius:6px;
                        margin-bottom:6px;
                    ">
                    {content}
                    </div>
                    """
                )
                applied = True
                break

        if not applied:
            html_lines.append(f"<div style='margin-bottom:6px;'>{stripped}</div>")

    return "".join(html_lines)

# -----------------------------
# 출력
# -----------------------------
st.subheader("🎨 구조 하이라이트 결과")
st.markdown(highlight_text(text), unsafe_allow_html=True)

# -----------------------------
# 바이트 상태
# -----------------------------
st.subheader("📊 바이트 상태")

st.progress(min(current_bytes / MAX_BYTES, 1.0))

col1, col2 = st.columns(2)
col1.metric("현재 바이트", current_bytes)
col2.metric("남은 바이트", MAX_BYTES - current_bytes)

if current_bytes > MAX_BYTES:
    st.error("❌ 바이트 초과")
elif current_bytes > MAX_BYTES * 0.8:
    st.warning("⚠️ 거의 가득 찼어요")
else:
    st.success("✅ 여유 있음")

# -----------------------------
# 안내
# -----------------------------
with st.expander("ℹ️ 태그 안내"):
    st.markdown("""
- 🔵 `[행동]` 구체적 활동  
- 🔴 `[동기]` 왜 했는지  
- 🟢 `[결론]` 결과·의미  
- 🟣 `[참고]` 참고 문헌  
- 🟠 `[느낀점]` 성찰  
""")




