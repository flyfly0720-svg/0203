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

