import streamlit as st
import re

st.set_page_config(page_title="생활기록부 자가 점검", layout="centered")
st.title("📘 생활기록부 자가 점검 도구")

# ======================
# 입력
# ======================
text = st.text_area(
    "생활기록부 문장을 입력하세요 (줄글 가능)",
    height=200,
    placeholder=(
        "[행동] 수업 중 문제를 변형하여 풀이 전략을 설명함. "
        "[동기] 친구들이 이해하기 어려워했기 때문임. "
        "[결론] 개념 이해와 의사소통 능력이 향상됨. "
        "[참고] 교과서 p.132, 추가 자료 "
        "[느낀점] 설명하는 과정에서 나도 더 깊이 이해하게 됨."
    )
)

# ======================
# 분류 기준
# ======================
sections = {
    "행동": "🔵 [행동]",
    "동기": "🔴 [동기]",
    "결론": "🟢 [결론]",
    "참고": "🟣 [참고]",
    "느낀점": "🟠 [느낀점]"
}

# ======================
# 바이트 계산 함수
# ======================
def calc_bytes(s):
    return len(s.encode("utf-8"))

# ======================
# 처리
# ======================
if text:
    st.divider()
    st.subheader("📌 문장 분류 결과")

    total_bytes = calc_bytes(text)
    st.info(f"📏 **전체 바이트 수:** {total_bytes} byte")

    st.divider()

    for key, label in sections.items():
        pattern = rf"\[{key}\](.*?)(?=\[행동\]|\[동기\]|\[결론\]|\[참고\]|\[느낀점\]|$)"
        match = re.search(pattern, text, re.DOTALL)

        if match:
            content = match.group(1).strip()
            byte_count = calc_bytes(content)

            st.markdown(f"**{label}** {content}")
            st.caption(f"➡️ 바이트 수: {byte_count} byte")

    st.divider()

    # ======================
    # 바이트 기준 안내
    # ======================
    if total_bytes > 1500:
        st.error("⚠️ 생활기록부 권장 바이트 수를 초과했습니다.")
    else:
        st.success("✅ 생활기록부 바이트 기준에 적절합니다.")
