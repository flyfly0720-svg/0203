import streamlit as st
import re

st.set_page_config(page_title="생활기록부 하이라이트", layout="centered")
st.title("📘 생활기록부 문장 자동 분류 하이라이트")

text = st.text_area(
    "문장을 입력하세요 (줄 구분 없어도 됩니다)",
    height=200,
    placeholder=(
        "[행동] 수업 중 문제를 변형하여 풀이 전략을 설명함. "
        "[동기] 친구들이 이해하기 어려워했기 때문임. "
        "[결론] 개념 이해와 의사소통 능력이 향상됨. "
        "[참고] 교과서 p.132, 추가 자료 "
        "[느낀점] 설명하는 과정에서 나도 더 깊이 이해하게 됨."
    )
)

color_map = {
    "행동": "#cce5ff",    # 파랑
    "동기": "#f8d7da",    # 빨강
    "결론": "#d4edda",    # 초록
    "참고": "#e2d9f3",    # 보라
    "느낀점": "#ffe5b4"   # 주황
}

def highlight_inline(text):
    result = text

    for key, color in color_map.items():
        pattern = rf"\[{key}\](.*?)(?=\[행동\]|\[동기\]|\[결론\]|\[참고\]|\[느낀점\]|$)"
        result = re.sub(
            pattern,
            lambda m: (
                f"<span style='background-color:{color}; "
                f"padding:3px 6px; border-radius:4px;'>"
                f"[{key}] {m.group(1).strip()}</span> "
            ),
            result,
            flags=re.DOTALL
        )
    return result

if text:
    st.subheader("🎨 하이라이트 결과")
    st.markdown(highlight_inline(text), unsafe_allow_html=True)
