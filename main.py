import streamlit as st
import re
import streamlit.components.v1 as components

st.set_page_config(page_title="생활기록부 자가 점검", layout="centered")
st.title("📘 생활기록부 자동 분류 · 글자수 · 바이트 계산")

# ======================
# 입력
# ======================
text = st.text_area(
    "생활기록부 줄글을 입력하세요",
    height=200,
    placeholder=(
        "수업 중 문제를 변형하여 풀이 전략을 설명함."
        "친구들이 이해하기 어려워했기 때문임."
        "개념 이해와 의사소통 능력이 향상됨."
        "교과서 p.132, 추가 자료를 설명하는 과정에서 나도 더 깊이 이해하게 됨."
    )
)

# ======================
# 유틸 함수
# ======================
def calc_bytes(s):
    return len(s.encode("utf-8"))

def split_sentences(text):
    return [s.strip() for s in re.split(r"[.!?]", text) if s.strip()]

# ======================
# 의미 기반 분류
# ======================
def classify(text):
    sentences = split_sentences(text)

    result = {
        "행동": [],
        "동기": [],
        "결론": [],
        "참고": [],
        "느낀점": []
    }

    for s in sentences:
        if any(k in s for k in ["수업", "문제", "풀이", "설명", "활동", "발표"]):
            result["행동"].append(s)
        elif any(k in s for k in ["때문", "이유", "어려워"]):
            result["동기"].append(s)
        elif any(k in s for k in ["향상", "성장", "이해", "능력"]):
            result["결론"].append(s)
        elif any(k in s for k in ["교과서", "자료", "p.", "페이지"]):
            result["참고"].append(s)
        else:
            result["느낀점"].append(s)

    return result

# ======================
# 처리
# ======================
if text:
    st.divider()

    classified = classify(text)

    st.subheader("📌 5가지 항목 분류 결과")

    icon = {
        "행동": "🔵 [행동]",
        "동기": "🔴 [동기]",
        "결론": "🟢 [결론]",
        "참고": "🟣 [참고]",
        "느낀점": "🟠 [느낀점]"
    }

    color = {
        "행동": "#1e88e5",
        "동기": "#e53935",
        "결론": "#43a047",
        "참고": "#8e24aa",
        "느낀점": "#fb8c00"
    }

    reconstructed = ""

    for key in ["행동", "동기", "결론", "참고", "느낀점"]:
        content = " ".join(classified[key])
        if content:
            char_count = len(content)
            byte_count = calc_bytes(content)

            st.markdown(f"**{icon[key]}** {content}")
            st.caption(f"✏️ 글자 수: {char_count}자 ｜ 📦 바이트 수: {byte_count} byte")

            # 하이라이트용 재구성
            reconstructed += (
                f"<span style='color:{color[key]}; font-weight:600;'>"
                f"{icon[key]} {content}</span><br>"
            )

    st.divider()

    # ======================
    # 전체 글자수 / 바이트수
    # ======================
    st.info(
        f"📊 전체 글자 수: **{len(text)}자** ｜ "
        f"전체 바이트 수: **{calc_bytes(text)} byte**"
    )

    # ======================
    # 하이라이트된 줄글 다시 보여주기
    # ======================
    st.subheader("🎨 색상 하이라이트 적용된 전체 문장")

    components.html(
        f"""
        <div style="font-size:16px; line-height:1.8;">
            {reconstructed}
        </div>
        """,
        height=300
    )
