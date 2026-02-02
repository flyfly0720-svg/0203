import streamlit as st
import re

st.set_page_config(page_title="생활기록부 자가 점검", layout="centered")
st.title("📘 생활기록부 자동 분류 & 바이트 계산기")

# ======================
# 입력
# ======================
text = st.text_area(
    "생활기록부 문장을 입력하세요 (태그·줄바꿈 없어도 됩니다)",
    height=200,
    placeholder=(
        "수업 중 문제를 변형하여 풀이 전략을 설명함."
        "친구들이 이해하기 어려워했기 때문임."
        "개념 이해와 의사소통 능력이 향상됨."
        "교과서 p.132, 추가 자료를 설명하는 과정에서 나도 더 깊이 이해하게 됨."
    )
)

# ======================
# 바이트 계산
# ======================
def calc_bytes(s):
    return len(s.encode("utf-8"))

# ======================
# 문장 분해 + 의미 기반 분류
# ======================
def classify_sentences(text):
    sentences = [s.strip() for s in re.split(r"[.!?]", text) if s.strip()]

    result = {
        "행동": "",
        "동기": "",
        "결론": "",
        "참고": "",
        "느낀점": ""
    }

    for s in sentences:
        if any(k in s for k in ["수업", "설명", "풀이", "활동", "발표", "참여"]):
            result["행동"] += s + ". "
        elif any(k in s for k in ["때문", "이유", "어려워", "필요"]):
            result["동기"] += s + ". "
        elif any(k in s for k in ["향상", "성장", "깨달", "이해", "능력"]):
            result["결론"] += s + ". "
        elif any(k in s for k in ["교과서", "자료", "논문", "p.", "페이지"]):
            result["참고"] += s + ". "
        else:
            result["느낀점"] += s + ". "

    return result

# ======================
# 처리
# ======================
if text:
    st.divider()

    classified = classify_sentences(text)
    total_bytes = calc_bytes(text)

    st.info(f"📏 전체 바이트 수: **{total_bytes} byte**")
    st.divider()

    icons = {
        "행동": "🔵 [행동]",
        "동기": "🔴 [동기]",
        "결론": "🟢 [결론]",
        "참고": "🟣 [참고]",
        "느낀점": "🟠 [느낀점]"
    }

    for key in ["행동", "동기", "결론", "참고", "느낀점"]:
        content = classified[key].strip()
        if content:
            st.markdown(f"**{icons[key]}** {content}")
            st.caption(f"➡️ 바이트 수: {calc_bytes(content)} byte")

    st.divider()

    if total_bytes > 1500:
        st.error("⚠️ 생활기록부 권장 바이트 수를 초과했습니다.")
    else:
        st.success("✅ 생활기록부 바이트 기준에 적절합니다.")

