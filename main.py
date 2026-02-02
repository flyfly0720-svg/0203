import streamlit as st
import re

st.set_page_config(page_title="생활기록부 맥락 기반 분류", layout="centered")
st.title("📘 생활기록부 맥락 기반 자동 분류")

text = st.text_area(
    "줄글로 입력하세요 (태그 필요 없음)",
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

def classify_by_context(text):
    sentences = split_sentences(text)

    result = {
        "행동": [],
        "동기": [],
        "결론": [],
        "느낀점": []
    }

    for s in sentences:
        # 동기: 원인, 문제 상황
        if any(x in s for x in ["때문", "어려워", "필요", "문제"]):
            result["동기"].append(s)

        # 느낀점: 1인칭 성찰
        elif any(x in s for x in ["깨닫", "느끼", "이해하게", "생각하게"]):
            result["느낀점"].append(s)

        # 결론: 능력 변화·성과
        elif any(x in s for x in ["향상", "신장", "강화", "성장", "기를 수 있었"]):
            result["결론"].append(s)

        # 행동: 관찰 가능한 활동
        else:
            result["행동"].append(s)

    return result

if text:
    st.divider()
    st.subheader("📌 맥락 기반 분류 결과")

    icons = {
        "행동": "🔵 [행동]",
        "동기": "🔴 [동기]",
        "결론": "🟢 [결론]",
        "느낀점": "🟠 [느낀점]"
    }

    classified = classify_by_context(text)

    for key in ["행동", "동기", "결론", "느낀점"]:
        if classified[key]:
            st.markdown(f"**{icons[key]}** {' '.join(classified[key])}")

