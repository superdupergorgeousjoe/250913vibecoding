# streamlit_app.py
import streamlit as st
import pandas as pd
import altair as alt
from pathlib import Path

st.set_page_config(page_title="MBTI Top10 by Country", layout="wide")

MBTI_16 = [
    "INTJ","INTP","ENTJ","ENTP","INFJ","INFP","ENFJ","ENFP",
    "ISTJ","ISFJ","ESTJ","ESFJ","ISTP","ISFP","ESTP","ESFP"
]

DEFAULT_FILE = "countriesMBTI_16types.csv"  # 같은 폴더 파일 우선

# ─────────────────────────────────────────────────────────────────────────────
# 정규화: wide(16유형 열) → long(country, type, percentage)
# long 입력도 자동 인식( country / type / value(percentage) )
# ─────────────────────────────────────────────────────────────────────────────
def _is_wide(df: pd.DataFrame) -> bool:
    cols = [c.strip().upper() for c in df.columns]
    return sum(c in MBTI_16 for c in cols) >= 10

def _detect_country_col(df: pd.DataFrame):
    for c in df.columns:
        lc = str(c).strip().lower()
        if lc in ["country", "nation", "지역", "국가", "국가명", "나라"]:
            return c
    return df.columns[0]

def _to_long_from_wide(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df.columns = [c.strip() for c in df.columns]
    country_col = _detect_country_col(df)
    mbti_cols = [c for c in df.columns if c.upper() in MBTI_16]
    melted = df.melt(id_vars=[country_col], value_vars=mbti_cols,
                     var_name="type", value_name="value").rename(columns={country_col:"country"})
    melted["type"] = melted["type"].str.upper().str.strip()
    if pd.api.types.is_numeric_dtype(melted["value"]):
        vals = melted["value"].dropna()
        if len(vals) and vals.max() <= 1.0:
            melted["value"] = melted["value"] * 100.0
    melted["percentage"] = melted["value"]
    out = melted[["country","type","percentage"]].copy()
    out["percentage"] = pd.to_numeric(out["percentage"], errors="coerce")
    out = out[(out["percentage"]>=0) & (out["percentage"]<=100)]
    return out[out["type"].isin(MBTI_16)]

def _to_long_from_longish(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    cols_lower = {c.lower(): c for c in df.columns}
    country_col = cols_lower.get("country", _detect_country_col(df))
    type_col    = cols_lower.get("type", None)

    value_col = None
    for k in ["percentage","value","ratio","share","percent"]:
        if k in cols_lower:
            value_col = cols_lower[k]; break
    if value_col is None:
        num_cols = [c for c in df.columns if pd.api.types.is_numeric_dtype(df[c])]
        value_col = num_cols[0] if num_cols else None

    out = df[[country_col, type_col, value_col]].rename(
        columns={country_col:"country", type_col:"type", value_col:"percentage"}
    )
    out["type"] = out["type"].astype(str).str.upper().str.strip()
    if pd.api.types.is_numeric_dtype(out["percentage"]):
        vals = out["percentage"].dropna()
        if len(vals) and vals.max() <= 1.0:
            out["percentage"] = out["percentage"] * 100.0
    out["percentage"] = pd.to_numeric(out["percentage"], errors="coerce")
    out = out[(out["percentage"]>=0) & (out["percentage"]<=100)]
    return out[out["type"].isin(MBTI_16)].dropna(subset=["country","type","percentage"])

def normalize_to_long(df: pd.DataFrame) -> pd.DataFrame:
    return _to_long_from_wide(df) if _is_wide(df) else _to_long_from_longish(df)

# ─────────────────────────────────────────────────────────────────────────────
# 데이터 로드: 같은 폴더 파일 우선 → 없으면 업로더 사용
# ─────────────────────────────────────────────────────────────────────────────
st.title("MBTI 유형별 비율 Top 10 국가 📊")
status = ""

p = Path(DEFAULT_FILE)
if p.exists():
    raw = pd.read_csv(p)
    df = normalize_to_long(raw)
    status = f"폴더의 기본 파일 사용: ./{DEFAULT_FILE}"
else:
    status = "폴더에서 기본 CSV를 찾지 못했습니다. 아래에서 업로드하세요."
    uploaded = st.file_uploader("CSV 업로드 (wide 또는 long 포맷)", type=["csv"])
    if uploaded is None:
        st.info(status)
        st.stop()
    raw = pd.read_csv(uploaded)
    df = normalize_to_long(raw)
    status = "업로드한 CSV 사용 중"

st.caption(status)

# ─────────────────────────────────────────────────────────────────────────────
# 데이터 품질 점검(국가별 합계≈100%)
# ─────────────────────────────────────────────────────────────────────────────
with st.expander("데이터 품질 점검 보기 (국가별 합계≈100%)", expanded=False):
    sums = df.groupby("country")["percentage"].sum().round(2)
    offenders = sums[(sums < 99.5) | (sums > 100.5)].to_frame("sum_%")
    st.write(f"총 국가 수: **{df['country'].nunique()}**")
    st.write(f"오차(±0.5%) 벗어난 국가 수: **{len(offenders)}**")
    if len(offenders):
        st.dataframe(offenders.sort_values("sum_%"))

# ─────────────────────────────────────────────────────────────────────────────
# UI 컨트롤
# ─────────────────────────────────────────────────────────────────────────────
colA, colB, colC = st.columns([2,1,1])
with colA:
    types_sorted = sorted(df["type"].unique())
    default_idx = types_sorted.index("ENFP") if "ENFP" in types_sorted else 0
    sel_type = st.selectbox("MBTI 유형 선택", types_sorted, index=default_idx)
with colB:
    top_n = st.number_input("Top N", min_value=3, max_value=20, value=10, step=1)
with colC:
    show_labels = st.checkbox("막대 레이블 표시", value=True)

# 선택 유형 Top N
df_top = (
    df[df["type"] == sel_type]
    .dropna(subset=["percentage"])
    .nlargest(int(top_n), "percentage")
    .sort_values("percentage", ascending=True)
)

st.subheader(f"{sel_type} 비율이 높은 국가 Top {int(top_n)}")
if df_top.empty:
    st.warning("해당 유형 데이터가 없습니다.")
else:
    base = alt.Chart(df_top).encode(
        y=alt.Y("country:N", sort=None, title="국가"),
        x=alt.X("percentage:Q", title="비율(%)"),
        tooltip=[
            alt.Tooltip("country:N", title="국가"),
            alt.Tooltip("percentage:Q", title="비율(%)", format=".2f")
        ]
    )
    bars = base.mark_bar().interactive()
    chart = bars
    if show_labels:
        text = base.mark_text(align="left", dx=3).encode(text=alt.Text("percentage:Q", format=".2f"))
        chart = bars + text
    st.altair_chart(chart.properties(height=max(320, 24*len(df_top)), width=720), use_container_width=True)

    with st.expander("표로 보기 / 다운로드"):
        st.dataframe(df_top[["country","type","percentage"]].sort_values("percentage", ascending=False), use_container_width=True)
        st.download_button(
            "이 테이블 CSV 다운로드",
            data=df_top.to_csv(index=False).encode("utf-8"),
            file_name=f"top{int(top_n)}_{sel_type}.csv",
            mime="text/csv"
        )

# 전체 유형별 Top N 미리보기(테이블)
with st.expander("전체 유형별 Top N 미리보기(테이블)"):
    top_all = (
        df.sort_values(["type","percentage"], ascending=[True, False])
        .groupby("type").head(int(top_n)).reset_index(drop=True)
    )
    st.dataframe(top_all, use_container_width=True)
