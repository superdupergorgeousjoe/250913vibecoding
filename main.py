# streamlit_app.py
import os
import io
import pandas as pd
import streamlit as st
import altair as alt

st.set_page_config(page_title="MBTI Top 10 by Country", layout="wide")

st.title("🌍 MBTI 유형별 비율 Top 10 국가 대시보드")

# --- 파일 읽기 함수 ---
@st.cache_data
def load_data(file_bytes=None):
    filename = "countriesMBTI_16types.csv"
    if os.path.exists(filename):
        st.success(f"로컬 파일을 불러왔습니다: {filename}")
        df = pd.read_csv(filename)
    elif file_bytes is not None:
        st.info("업로드한 파일을 불러왔습니다.")
        df = pd.read_csv(io.BytesIO(file_bytes))
    else:
        st.error("CSV 파일을 찾을 수 없습니다. 로컬에 파일을 두거나 업로드하세요.")
        return None

    # 컬럼 정리
    df.columns = [c.strip() for c in df.columns]
    if "Country" not in df.columns:
        df = df.rename(columns={df.columns[0]: "Country"})
    for c in df.columns:
        if c != "Country":
            df[c] = pd.to_numeric(df[c], errors="coerce")
    return df

# --- 사이드바: 업로드 ---
with st.sidebar:
    st.header("⚙️ 설정")
    file = st.file_uploader("CSV 업로드 (없으면 기본 파일 사용)", type=["csv"])
    default_types = ["INFJ","ISFJ","INTP","ISFP","ENTP","INFP","ENTJ","ISTP",
                     "INTJ","ESFP","ESTJ","ENFP","ESTP","ISTJ","ENFJ","ESFJ"]
    top_n = st.slider("Top N", min_value=5, max_value=20, value=10, step=1)

# --- 데이터 불러오기 ---
df = load_data(file.getvalue() if file else None)
if df is None:
    st.stop()

# --- MBTI 열 자동 탐색 ---
mbti_cols = [c for c in df.columns if c in default_types]
if not mbti_cols:
    st.error("MBTI 유형 열을 찾을 수 없습니다.")
    st.stop()

with st.sidebar:
    mbti_selected = st.selectbox("MBTI 유형 선택", options=sorted(mbti_cols))

# --- Top N 국가 추출 ---
work = df[["Country", mbti_selected]].dropna()
if work[mbti_selected].max() > 1.0:
    work[mbti_selected] = work[mbti_selected] / 100.0

top = work.nlargest(top_n, mbti_selected).reset_index(drop=True)
top["Rank"] = top.index + 1

# --- 표 표시 ---
st.subheader(f"🏆 {mbti_selected} 비율 Top {top_n} 국가")
st.dataframe(
    top.rename(columns={mbti_selected: f"{mbti_selected} (share)"}),
    use_container_width=True
)

# --- Altair 시각화 ---
click = alt.selection_point(fields=["Country"], bind="legend")
hover = alt.selection_point(fields=["Country"], on="mouseover", empty=False)

bar = (
    alt.Chart(top)
    .mark_bar()
    .encode(
        x=alt.X(f"{mbti_selected}:Q", axis=alt.Axis(format=".0%"), title=f"{mbti_selected} 비율"),
        y=alt.Y("Country:N", sort="-x"),
        color=alt.condition(click | hover,
                            alt.Color(f"{mbti_selected}:Q", scale=alt.Scale(scheme="blues")),
                            alt.value("lightgray")),
        tooltip=["Rank", "Country", alt.Tooltip(f"{mbti_selected}:Q", format=".2%")],
        opacity=alt.condition(click | hover, alt.value(1), alt.value(0.6))
    )
    .add_params(click, hover)
    .properties(height=500)
)

st.altair_chart(bar, use_container_width=True)

# --- 다운로드 ---
st.download_button(
    "⬇️ 결과 CSV 다운로드",
    top.to_csv(index=False).encode("utf-8"),
    file_name=f"top{top_n}_{mbti_selected}.csv",
    mime="text/csv"
)
