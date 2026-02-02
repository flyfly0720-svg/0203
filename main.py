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

