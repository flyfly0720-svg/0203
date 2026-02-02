import streamlit as st
import re
import streamlit.components.v1 as components

st.set_page_config(page_title="생활기록부 색상 분류", layout="centered")
st.title("📘 생활기록부 문장 색상 분류 (글씨 색 기준)")

text = st.text_area(
    "문장을 입력하세요 (연결된 문장도 가능)",
    height=200,
    placeholder=(
        "[행동] 수업 중 문제를 변형하여 풀이 전략을 설명함. "
        "[동기] 친구들이 이해하기 어려워했기 때문임. "
        "[결론] 개념 이해와 의사소통 능력이 향상됨. "
        "[참고] 교과서 p.132, 추가 자료 "
        "[느낀점] 설명하는 과정에서 나도 더 깊이 이해하게 됨."
    )
)

# 글씨 색상 정의
color_map = {
    "행동": "#0066cc",   # 파랑
    "동기": "#cc0000",   # 빨강
    "결론": "#2e7d32",   # 초록
    "참고": "#6a1b9a",   # 보라
    "느낀점": "#ef6c00"  # 주황
}

def color_text(text):
    result = text
    for key, color in color_map.items():
        pattern = rf"\[{key}\](.*?)(?=\[행동\]|\[동기\]|\[결론\]|\[참고\]|\[느낀점\]|$)"
        result = re.sub(
            pattern,
            lambda m: (
                f"<span style='color:{color}; font-weight:600;'>"
                f"[{key}] {m.group(1).strip()}</span> "
            ),
            result,
            flags=re.DOTALL
        )
    return result

if text:
    html = f"""
    <div style="font-size:17px; line-height:1.9;">
        {color_text(text)}
    </div>
    """
    components.html(html, height=300)
