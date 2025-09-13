# app.py
import time
import random
import textwrap
import streamlit as st

# ------------------------- 기본 설정 -------------------------
st.set_page_config(
    page_title="MBTI × 한국사 공부 설계기",
    page_icon="🇰🇷",
    layout="wide"
)

# ------------------------- 이모지 & 효과 -------------------------
EMOJI_POOL = ["📚","🏯","🧭","🧠","🧩","✨","🌟","🎯","⚔️","🏺","📝","🔎","📜","🚀","🇰🇷","🎮","🧪","🗂️","🗺️","💡"]

def rainbow_title(text):
    st.markdown(
        f"""
        <h1 style="
            font-family: 'Noto Sans KR', sans-serif;
            font-size: 42px;
            background: linear-gradient(90deg,#ff7a7a,#ffd36e,#7affb5,#6ecbff,#c89cff);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin: 0 0 6px 0;
        ">{text}</h1>
        """,
        unsafe_allow_html=True
    )

def floating_emoji_layer():
    emojis = random.sample(EMOJI_POOL, k=8)
    items = "".join(
        [
            f"""<span class="float-emoji" style="left:{i*10+5}%; animation-delay:{i*0.5}s">{e}</span>"""
            for i, e in enumerate(emojis)
        ]
    )
    st.markdown(
        f"""
        <style>
        .float-emoji {{
            position: fixed;
            bottom: -30px;
            font-size: 28px;
            opacity: 0.85;
            animation: rise 9s linear infinite;
            z-index: 0;
            pointer-events: none;
        }}
        @keyframes rise {{
            0%   {{ transform: translateY(0);     opacity: 0.0; }}
            10%  {{ opacity: 0.9; }}
            90%  {{ opacity: 0.9; }}
            100% {{ transform: translateY(-120vh); opacity: 0.0; }}
        }}
        .block-container, .main, [data-testid="stAppViewContainer"] * {{ position: relative; z-index: 1; }}
        </style>
        {items}
        """,
        unsafe_allow_html=True
    )

floating_emoji_layer()

# ------------------------- MBTI 그룹 정의 -------------------------
GROUPS = {
    "NT": {"name":"분석형", "emoji":"🧠", "vibe":"논리·시스템·전략"},
    "NF": {"name":"외교형", "emoji":"🌱", "vibe":"의미·공감·스토리"},
    "SJ": {"name":"수호형", "emoji":"🛡️", "vibe":"체계·루틴·기록"},
    "SP": {"name":"탐험형", "emoji":"🧭", "vibe":"경험·게임·시각화"}
}

MBTI_GROUP = {
    "INTJ":"NT","INTP":"NT","ENTJ":"NT","ENTP":"NT",
    "INFJ":"NF","INFP":"NF","ENFJ":"NF","ENFP":"NF",
    "ISTJ":"SJ","ISFJ":"SJ","ESTJ":"SJ","ESFJ":"SJ",
    "ISTP":"SP","ISFP":"SP","ESTP":"SP","ESFP":"SP",
}
PERSONA = {
    "INTJ":"전략가 모드 ♟️ 복잡한 흐름을 구조화!",
    "INTP":"호기심 연구자 🔍 가설→증거로 검증!",
    "ENTJ":"사령관 💼 목표-절차-성과 드라이브!",
    "ENTP":"토론 폭격기 💥 관점 전환으로 논파!",
    "INFJ":"의미 탐색가 🌌 역사 속 ‘왜’를 찾자!",
    "INFP":"스토리 메이커 📖 인물 감정선에 강점!",
    "ENFJ":"팀 빌더 🤝 협업·피드백의 장!",
    "ENFP":"아이디어 폭죽 🎆 창의 프로젝트 적합!",
    "ISTJ":"성실의 정석 📏 표준 절차·정확도!",
    "ISFJ":"세심한 돌봄 🌿 노트·정리 장인!",
    "ESTJ":"운영의 달인 🗂️ 계획→실행→검토!",
    "ESFJ":"분위기 메이커 🎉 발표·지원 강점!",
    "ISTP":"실험가 🛠️ 모형·지도·게임 Hands-on!",
    "ISFP":"아티스트 🎨 시각화·카드·콜라주!",
    "ESTP":"액션 플레이어 🏃 즉시 시도·개선!",
    "ESFP":"스테이지 장인 🎤 퍼포먼스형 발표!"
}

MBTIS = list(MBTI_GROUP.keys())

# ------------------------- 한국사 단원 사전 -------------------------
# (중학교 3학년 중심 흐름+연결 학습)
UNITS = [
    {
        "id":"kh-01",
        "title":"삼국과 통일신라·발해",
        "focus":"국가 통합과 문화 교류",
        "key_terms":["관등제","골품제","신라 민정문서","발해 5경","통일 전후 변화"],
    },
    {
        "id":"kh-02",
        "title":"고려의 성립과 발전",
        "focus":"중앙집권과 문벌·무신·원 간섭",
        "key_terms":["과거제","전시과","무신정변","삼별초","권문세족","쌍성총관부"],
    },
    {
        "id":"kh-03",
        "title":"조선 전기",
        "focus":"유교질서 확립과 제도 정비",
        "key_terms":["경국대전","사림의 대두","훈구와 사림","토지·군역","향약","집현전"],
    },
    {
        "id":"kh-04",
        "title":"조선 후기",
        "focus":"신분·경제 변화와 실학",
        "key_terms":["대동법","균역법","환곡","공인","실학","신분제 동요","서얼허통"],
    },
    {
        "id":"kh-05",
        "title":"근대 태동기와 개항",
        "focus":"개항·개화와 위기 대응",
        "key_terms":["강화도조약","임오군란","갑신정변","동학농민운동","을미개혁","독립협회"],
    },
    {
        "id":"kh-06",
        "title":"일제 식민지 지배와 민족운동",
        "focus":"무단·문화·민족말살 통치와 항일",
        "key_terms":["토지조사사업","회사령","3·1운동","임시정부","의열단","한글학회","민족말살"],
    },
    {
        "id":"kh-07",
        "title":"광복·분단과 대한민국 정부 수립",
        "focus":"해방 정국과 체제 수립",
        "key_terms":["미소공동위원회","좌우합작","제헌국회","6·25전쟁","정전협정","한미상호방위조약"],
    }
]

# ------------------------- MBTI별 ‘만들 것’ 프리셋 -------------------------
PRESETS = {
    "NT": {
        "artifacts":[
            "인과관계 다이어그램(사건→원인/배경→결과) 📈",
            "비교표(제도/세력/정책의 공통·차이) 📊",
            "주장-근거-추론(CER) 답안 템플릿 🧱"
        ],
        "worksheet_blocks":[
            "용어·연표 체크(사실)", "인과·구조 질문(개념)", "쟁점 토론 프롬프트(논쟁)", "CER 서술칸"
        ],
        "method":"가설 설정→사료 검증→반례 점검 루프 🔁"
    },
    "NF": {
        "artifacts":[
            "인물 일기/인터뷰 카드(선택의 윤리) ✍️",
            "서사 타임라인(감정·상징 북마크) 📖",
            "팟캐스트/역할극 토론 대본 🎙️"
        ],
        "worksheet_blocks":[
            "핵심 사건 요약(사실)", "가치·의미 연결(개념)", "찬반 균형 논증(논쟁)", "스토리 리플렉션"
        ],
        "method":"사람의 목소리로 사료 읽기→가치 충돌 지도 그리기 🗺️"
    },
    "SJ": {
        "artifacts":[
            "연표→용어 카드 100 🪪",
            "기출 유형 폴더(사료/도표/지도) 🗂️",
            "오답 루프 시트(원인 태그) ♻️"
        ],
        "worksheet_blocks":[
            "연표·용어 확인(사실)", "원리·제도 구조화(개념)", "정책 비교 평가(논쟁)", "오답노트 섹션"
        ],
        "method":"루틴(아침 15′ 복습/주말 45′ 총정리) ⏰"
    },
    "SP": {
        "artifacts":[
            "퀘스트형 미션 보드 🎮",
            "장소·지도 기반 활동 🗺️",
            "카드/보드게임 프로토타입 🧩"
        ],
        "worksheet_blocks":[
            "이미지·지도 퍼즐(사실)", "모형·시뮬(개념)", "역할 협상 시나리오(논쟁)", "스프린트 체크리스트"
        ],
        "method":"25′ 집중 스프린트→5′ 리셋 포모도로 🍅"
    }
}

# ------------------------- UI -------------------------
rainbow_title("MBTI × 한국사 공부 설계기 🇰🇷")
st.caption("중학생 취향저격 😎 이모지 팡팡 + 한 파일로 수업 제작 가이드 자동 생성!")

c1, c2 = st.columns([1,3])
with c1:
    mbti = st.selectbox("MBTI 선택 ✨", MBTIS, index=MBTIS.index("ENFP"))
with c2:
    st.info("Tip) 학생 MBTI/팀 MBTI에 맞춰 단원 산출물을 차별화해 보세요! 👯‍♀️")

# 추천 단원(유형별 시너지) 매핑
RECO_BY_GROUP = {
    "NT": ["kh-02","kh-05","kh-06"],  # 구조·인과 많은 단원
    "NF": ["kh-04","kh-06","kh-07"],  # 서사·가치·인물 풍부
    "SJ": ["kh-03","kh-04","kh-06"],  # 제도·용어·연표 정리 적합
    "SP": ["kh-01","kh-05","kh-06"],  # 현장감·게임화 쉬움
}

def unit_by_id(uid):
    return next(u for u in UNITS if u["id"] == uid)

gkey = MBTI_GROUP[mbti]
ginfo = GROUPS[gkey]
preset = PRESETS[gkey]

st.markdown("---")
st.subheader(f"{mbti} | {ginfo['name']} {ginfo['emoji']}")
st.success(PERSONA.get(mbti, "너만의 강점으로 공부해봐요! ✨"))
st.caption(f"핵심 학습 기질: **{ginfo['vibe']}** · 권장 방법: **{preset['method']}**")

# ------------------------- 추천 단원 카드 -------------------------
st.markdown("### 🔎 이 MBTI에 잘 맞는 추천 단원 3")
rc_ids = RECO_BY_GROUP[gkey]
rc_cols = st.columns(3)
for col, uid in zip(rc_cols, rc_ids):
    u = unit_by_id(uid)
    with col:
        st.markdown(
            f"""
            <div style="border:1px solid #eee;border-radius:16px;padding:14px">
                <div style="font-size:18px"><b>{u['title']}</b> {random.choice(['🌟','🎯','✨','📌'])}</div>
                <div style="color:#666">핵심: {u['focus']}</div>
                <div style="margin-top:6px;font-size:14px;">키워드: {" · ".join(u['key_terms'][:5])}…</div>
            </div>
            """,
            unsafe_allow_html=True
        )

# ------------------------- 단원 선택 & 난이도/형식 -------------------------
st.markdown("### 🧭 제작할 단원 선택")
unit_titles = [f"{u['title']} — {u['focus']}" for u in UNITS]
selected = st.multiselect("여러 단원을 한 번에 가이드로 묶을 수 있어요.", unit_titles, default=[f"{unit_by_id(rc_ids[0])['title']} — {unit_by_id(rc_ids[0])['focus']}"])

c3, c4, c5 = st.columns(3)
with c3:
    level = st.select_slider("난이도", options=["기초","표준","심화"], value="표준")
with c4:
    ws_len = st.select_slider("학습지 길이(쪽)", options=[1,2,3,4], value=2)
with c5:
    add_quiz = st.checkbox("미니 퀴즈 10문 추가(4지선다)", value=True)

# ------------------------- 생성 로직 -------------------------
def build_questions(u, mode):
    """단원별 사실/개념/논쟁 질문 예시 3종"""
    t = u["title"]
    if mode=="기초":
        factual = [f"{t} 핵심 용어의 뜻을 연결하시오.", f"{t} 관련 연표에서 빈칸을 채우시오.", f"{t} 지도/그림에 해당 사건을 표시하시오."]
        conceptual = [f"{t} 변화의 공통 원인을 2가지로 묶어 설명하시오.", f"{t} 제도/사상의 구조를 도식화하시오."]
        debatable = [f"{t}의 변화가 ‘개인의 삶’에 더 큰 영향을 주었는지 ‘국가 구조’에 더 큰 영향을 주었는지 논증하시오."]
    elif mode=="심화":
        factual = [f"{t} 사료 A/B를 비교해 출처·관점을 판별하시오.", f"{t} 도표를 해석해 정책의 의도를 추론하시오."]
        conceptual = [f"{t}의 장기 인과(단기↔장기)를 화살표로 제시하시오.", f"{t} 동시기 세계사/한국사 연결고리 2가지를 제시하시오."]
        debatable = [f"{t}의 개혁/운동이 대안적 경로를 가졌다면 어떤 결과가 가능했는지(What if) 근거를 들어 논증하시오."]
    else:  # 표준
        factual = [f"{t} 핵심 연도–사건–인물을 매칭하시오.", f"{t} 용어 5개를 정의–사례로 연결하시오."]
        conceptual = [f"{t} 원인–전개–결과를 구조도로 작성하시오.", f"{t} 주요 세력의 목표·수단을 비교표로 정리하시오."]
        debatable = [f"{t}의 사건/정책이 당시 최선이었는지 찬반 근거를 2개씩 제시하시오."]
    return factual, conceptual, debatable

def build_artifacts_by_mbti(u, preset, ws_len, add_quiz):
    """MBTI별 산출물/학습지 틀"""
    blocks = "\n".join([f"- {b}" for b in preset["worksheet_blocks"]])
    arts = "\n".join([f"- {a}" for a in preset["artifacts"]])
    quiz_hint = "포함(4지선다 10문)" if add_quiz else "미포함"
    return f"""
### 🧩 학습지 구조(권장 {ws_len}쪽)
{blocks}

### 🛠️ 만들 산출물(수업·과제 겸용)
{arts}

### 🧪 운영 방법(이 MBTI 추천)
- {preset["method"]}
- 팀/개인 선택 운영, 발표는 60초 스피드 톡 추천 ⏱️
- 피드백: ‘증거→개선점→한 줄 칭찬’ 3단 구조 💬

### 🎯 퀴즈 구성
- {quiz_hint}
"""

def build_quiz(u):
    # 단순 예시 10문 생성기(4지선다), 교사용 편집 전제로 템플릿만 생성
    items = []
    bases = u["key_terms"][:10] if len(u["key_terms"])>=10 else (u["key_terms"]*2)[:10]
    for i, k in enumerate(bases, 1):
        items.append(f"{i}. 다음 중 ‘{k}’와 가장 관련이 깊은 것은?\n   ① 용어A  ② 용어B  ③ 용어C  ④ 용어D  ⟹ [정답/근거 입력]")
    return "\n".join(items)

def build_md(mbti, level, ws_len, add_quiz, selected_units):
    gkey = MBTI_GROUP[mbti]
    ginfo = GROUPS[gkey]
    preset = PRESETS[gkey]
    head = f"# MBTI × 한국사 제작 가이드 ({mbti} | {ginfo['name']} {ginfo['emoji']})\n\n" \
           f"- 난이도: **{level}** · 권장 루틴: **{preset['method']}**\n" \
           f"- 학습지 길이: **{ws_len}쪽** · 퀴즈: **{'포함' if add_quiz else '미포함'}**\n\n" \
           f"---\n"
    body = []
    for idx, title in enumerate(selected_units, 1):
        u = next(u for u in UNITS if title.startswith(u["title"]))
        factual, conceptual, debatable = build_questions(u, level)
        arti = build_artifacts_by_mbti(u, preset, ws_len, add_quiz)
        section = textwrap.dedent(f"""
        ## {idx}. {u['title']} — {u['focus']} {random.choice(['🏯','📜','🧭','⚔️'])}
        **키워드:** {", ".join(u['key_terms'])}

        ### 📘 질문 세트
        - **사실(F):** {factual[0]}
        - **사실(F):** {factual[1]}
        - **개념(C):** {conceptual[0]}
        - **개념(C):** {conceptual[1]}
        - **논쟁(D):** {debatable[0]}

        {arti}

        ### 🧱 빈칸 학습지(복사용 템플릿: 예시)
        1) 핵심 개념: (__1__) · (__2__) · (__3__)
        2) 연표: (__연도__) — (__사건__) — (__결과__)
        3) 사료: “(______)” → 누가/언제/왜/무엇을?
        4) 비교표: [세력/정책/목표/수단/영향]
        5) CER: 주장(___), 근거1(___), 근거2(___), 추론(___)

        ### 🧭 활동 운영(한 시간 45′ 예시)
        - 10′ 인트로/키워드 퀵리뷰 {random.choice(['✨','🌟','🎯'])}
        - 20′ 제작(학습지 블록 2~3개) + 팀 피드백
        - 10′ 60초 발표(스피드 톡)
        - 5′ 오답·개선 포인트 태깅(개념/연표/사료)

        """)
        if add_quiz:
            section += f"### 📝 미니 퀴즈(템플릿 10문)\n{build_quiz(u)}\n\n"
        body.append(section)
    tail = "---\n**제작 팁**\n- Canva 카드/타임라인, Google Earth/Street View로 장소·지도를 함께 제시 🗺️\n" \
           "- Kahoot/Quizizz로 퀵 퀴즈, Padlet/Vocaroo로 60초 발표 녹음 🎙️\n" \
           "- 평가: 체크리스트(근거 충실/용어 정확/구조 명료/반례 검토)\n"
    return head + "\n".join(body) + tail

# ------------------------- 생성 & 미리보기/다운로드 -------------------------
if st.button("📦 제작 가이드 생성하기"):
    with st.spinner("나만의 한국사 제작 가이드를 조립 중… 🔧"):
        time.sleep(0.7)
    md = build_md(mbti, level, ws_len, add_quiz, selected)
    st.balloons()
    st.success("완료! 아래 미리보기와 다운로드를 확인하세요 🤩")

    st.markdown("### 🔍 미리보기")
    st.code(md, language="markdown")

    st.download_button(
        label="⬇️ 교사용 제작 가이드(.md) 다운로드",
        data=md.encode("utf-8"),
        file_name=f"MBTI_KoreanHistory_Guide_{mbti}.md",
        mime="text/markdown"
    )
else:
    st.markdown(
        f"#### 아래에서 **단원**을 고르고 **제작 가이드 생성하기** 버튼을 눌러보세요! {' '.join(random.sample(EMOJI_POOL, k=10))}"
    )
    st.markdown("> 클릭 한 번으로 **질문 세트·빈칸 학습지 구조·퀴즈 템플릿**까지 완성됩니다 ✨")
