# app.py
import time
import random
import streamlit as st

# ------------------------- 기본 설정 -------------------------
st.set_page_config(
    page_title="MBTI × 역사 공부 추천",
    page_icon="📚",
    layout="wide"
)

# ------------------------- 스타일 & 효과 -------------------------
EMOJI_POOL = ["📚","🗺️","🏯","🏛️","🧭","🧠","🧩","✨","🌟","🎯","⚔️","🏺","📝","🔎","📜","🗿","🚀","🌍","🇰🇷","🎮"]

def rainbow_title(text):
    st.markdown(
        f"""
        <h1 style="
            font-family: 'Pretendard', 'Noto Sans KR', sans-serif;
            font-size: 46px;
            background: linear-gradient(90deg,#ff7a7a,#ffd36e,#7affb5,#6ecbff,#c89cff);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin: 0 0 8px 0;
        ">{text}</h1>
        """,
        unsafe_allow_html=True
    )

def floating_emoji_layer():
    # 단순 CSS로 둥둥 떠다니는 이모지들
    emojis = random.sample(EMOJI_POOL, k=8)
    items = "".join(
        [
            f"""<span class="float-emoji" style="left:{i*10+5}%; animation-delay:{i*0.6}s">{e}</span>"""
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
            animation: rise 10s linear infinite;
            z-index: 0;
        }}
        @keyframes rise {{
            0%   {{ transform: translateY(0);     opacity: 0.0; }}
            10%  {{ opacity: 0.9; }}
            90%  {{ opacity: 0.9; }}
            100% {{ transform: translateY(-120vh); opacity: 0.0; }}
        }}
        /* 컨텐츠 위 클릭 방지 */
        .block-container, .main, [data-testid="stAppViewContainer"] * {{ position: relative; z-index: 1; }}
        </style>
        {items}
        """,
        unsafe_allow_html=True
    )

floating_emoji_layer()

# ------------------------- 데이터 -------------------------
GROUPS = {
    "NT": {"name":"분석형(Analysts)", "emoji":"🧠", "vibe":"논리 · 시스템 · 전략"},
    "NF": {"name":"외교형(Diplomats)", "emoji":"🌱", "vibe":"의미 · 공감 · 스토리"},
    "SJ": {"name":"수호형(Sentinels)", "emoji":"🛡️", "vibe":"체계 · 성실 · 기록"},
    "SP": {"name":"탐험형(Explorers)", "emoji":"🧭", "vibe":"경험 · 실습 · 게임"}
}

MBTI_GROUP = {
    "INTJ":"NT","INTP":"NT","ENTJ":"NT","ENTP":"NT",
    "INFJ":"NF","INFP":"NF","ENFJ":"NF","ENFP":"NF",
    "ISTJ":"SJ","ISFJ":"SJ","ESTJ":"SJ","ESFJ":"SJ",
    "ISTP":"SP","ISFP":"SP","ESTP":"SP","ESFP":"SP",
}

# 공통 가이드(그룹별 베이스) — 한국사/세계사 공통 뼈대
BASE_STRATEGY = {
    "NT": {
        "core": ["개념 맵핑 🧩","인과관계 화살표 ➡️","비교표 📊","타임라인 ⏳","가설-검증 🔬"],
        "k_activities": [
            "조선~대한제국 경제·제도 변천 인과 그래프 만들기 📈",
            "개항기 조약 비교표(조약 조항→영향→사회 변화) 정리 📋",
            "3·1운동과 임시정부 노선 차이 ‘주장–근거’ 카드 소팅 🃏"
        ],
        "w_activities": [
            "제국주의 원인-결과 매트릭스(정치·경제·기술·사상) 🗺️",
            "세계대전 전간기(1919~39) 정책 시뮬레이션 미니 토론 🎤",
            "산업혁명 기술 발전 → 노동·도시 변화 ‘시스템 다이어그램’ ⚙️"
        ],
        "tips": ["증거–주장–추론(Claim–Evidence–Reasoning) 구조로 답안 쓰기 🧱",
                 "통계·지도·사료에서 ‘패턴’ 먼저 찾기 🔍",
                 "오답노트는 ‘왜 틀렸는가’ 로직 중심 메모 📝"]
    },
    "NF": {
        "core": ["서사 만들기 📖","인물 관점 전환 👓","가치·윤리 토론 💬","감정·맥락 연결 💡"],
        "k_activities": [
            "의병·계몽운동 ‘가상 신문 인터뷰’ 작성 🗞️",
            "일제강점기 인물 일기(그날의 선택과 고민) ✍️",
            "대한민국 수립 전후 찬반 토론 팟캐스트 🎙️"
        ],
        "w_activities": [
            "르네상스 예술가 vs 종교개혁가 대화극 🎭",
            "대항해시대 원주민 시점 카드스토리 📇",
            "냉전시대 시민의 하루: 동서독 청소년 편지 교환 ✉️"
        ],
        "tips": ["사료를 ‘사람의 목소리’로 읽기(의도·감정·상황) 🗣️",
                 "논쟁적 질문에 찬·반 각 2근거씩 균형맞추기 ⚖️",
                 "암기는 ‘스토리 북마크(사건-인물-장소-상징)’로 🌟"]
    },
    "SJ": {
        "core": ["루틴·체크리스트 ✅","연표·용어 카드 📇","기출 유형별 폴더링 🗂️","오답 루프 ♻️"],
        "k_activities": [
            "삼국~통일신라→고려→조선 핵심 제도 연표 완성 ⏱️",
            "조세·군역·신분제 핵심용어 카드 100장 만들기 🪪",
            "근현대사 연도-사건-키워드 3단 암기표 🧾"
        ],
        "w_activities": [
            "고대→중세→근대 전환 포인트 도식화 🧭",
            "프랑스혁명~빈체제~민족주의 흐름 표로 정리 📑",
            "세계대전 연합·추축 전선 지도 퀴즈 🗺️"
        ],
        "tips": ["‘아침 20분 복습+주말 60분 총정리’ 고정 루틴 ⏰",
                 "틀린 문제는 원인 태그(개념/연도/사료) 붙이기 🏷️",
                 "문제집은 회차별 목표(범위·시간·정확도) 명시 🎯"]
    },
    "SP": {
        "core": ["체험·게임화 🎮","짧고 굵은 스프린트 ⏱️","시각화·모형 🧱","현장·지도로 연결 🗺️"],
        "k_activities": [
            "창덕궁·경복궁 가상 투어 후 미션형 퀴즈 🏯",
            "훈민정음 창제 카드 뒤집기 게임(원리 매칭) 🃏",
            "독립운동 거점 지도 찍고 ‘탈출 룰렛 퀘스트’ 🧭"
        ],
        "w_activities": [
            "고대 문명 생존키트 만들기(강·기후·작물 선택) 🏕️",
            "대항해 항로 퍼즐(풍향·해류·교역품 매칭) 🌬️",
            "콜드워 스파이 보드게임(정보 카드로 협상) 🕵️"
        ],
        "tips": ["25분 집중·5분 리셋 ‘포모도로’로 탄력 있게 🍅",
                 "이미지·영상 요약 3줄 → 말풍선 카드로 정리 💬",
                 "퀘스트형 체크리스트로 달성감 업 📈"]
    }
}

# 타입별 소소한 맞춤 메시지(개성)
PERSONA = {
    "INTJ":"전략가 모드 ON ♟️ 복잡한 흐름을 구조화하면 당신이 1등 전략가!",
    "INTP":"호기심 폭발 연구자 🔍 가설 세우고 근거로 논파하자!",
    "ENTJ":"사령관 리더십 💼 목표-절차-성과, 깔끔한 드라이브!",
    "ENTP":"토론의 폭격기 💥 관점을 바꿔보며 논쟁형 질문에 강해요!",
    "INFJ":"의미 탐색가 🌌 역사 속 ‘왜’를 발견해 가치를 잇자!",
    "INFP":"스토리 메이커 📖 인물 감정선·윤리적 선택에 강점!",
    "ENFJ":"팀 빌더 🤝 역할 분담·협업 프레임으로 배움 확장!",
    "ENFP":"아이디어 폭죽 🎆 창의적 프로젝트·콘텐츠 제작이 찰떡!",
    "ISTJ":"성실의 정석 📏 루틴과 표준 절차로 완성도 UP!",
    "ISFJ":"세심한 돌봄 🌿 정리·정돈·노트테이킹의 장인!",
    "ESTJ":"운영의 달인 🗂️ 계획→실행→검토 루프가 무기!",
    "ESFJ":"분위기 메이커 🎉 협동·발표·서포트에서 빛나요!",
    "ISTP":"실험가 공돌이 🛠️ 모형·지도·게임으로 Hands-on!",
    "ISFP":"감각형 아티스트 🎨 시각화·카드·콜라주로 기억 고정!",
    "ESTP":"액션 플레이어 🏃 즉시 시도→피드백→개선!",
    "ESFP":"스테이지 장인 🎤 퍼포먼스형 발표·브이로그로 심화!"
}

# MBTI 검증 리스트
MBTIS = list(MBTI_GROUP.keys())

# ------------------------- UI 상단 -------------------------
rainbow_title("MBTI × 역사 공부 추천 🧭📚")
st.caption("중학생 취향저격 😎 이모지 팡팡 + 인터랙션 가득! (한국사·세계사 맞춤)")

col1, col2 = st.columns([1,3])
with col1:
    mbti = st.selectbox("MBTI를 골라요 ✨", MBTIS, index=MBTIS.index("ENFP"))
    go = st.button("추천 보기 🔮")
with col2:
    st.info("Tip) 본인/친구 MBTI로 바꿔보며 ‘나랑 맞는 공부법’을 비교해 보세요! 👯")

# 로딩 연출
def loading_bar(txt="나만의 추천을 준비중..."):
    with st.spinner(txt):
        prog = st.progress(0)
        for i in range(0,101,8):
            time.sleep(0.03)
            prog.progress(i)
    st.balloons()
    st.toast("완료! 스크롤을 내려보세요 🤩", icon="✅")

# ------------------------- 컨텐츠 생성 함수 -------------------------
def make_week_plan(group_key):
    # 간단 주간 루틴: 한국사/세계사 번갈아가며 핵심역량
    g = BASE_STRATEGY[group_key]
    core = " · ".join(g["core"][:4])
    return [
        ("월", f"핵심 개념 미니 강의 요약(10분) + {core} 정리(20분) + 퀴즈(10분)"),
        ("화", "한국사 — 활동 과제 1 진행(30분) + 오답 태깅(10분)"),
        ("수", "세계사 — 활동 과제 1 진행(30분) + 이미지 요약(10분)"),
        ("목", "기출 유형 20문 항해 ⛵ (연표/사료 중심)"),
        ("금", "토론/발표/콘텐츠 제작 🎤 (팀/개인 선택)"),
        ("토", "현장·지도·영상으로 확장 🔎 (가볍게 30~40분)"),
        ("일", "주간 리셋: 오답 루프 ♻️ + 다음 주 목표 3줄 🎯")
    ]

def section_block(title, bullets, icon="📌"):
    st.markdown(f"### {icon} {title}")
    for b in bullets:
        st.markdown(f"- {b}")

def activity_block(title, items, icon="🧪"):
    st.markdown(f"#### {icon} {title}")
    for i in items:
        st.markdown(f"- {i}")

def edtech_block():
    st.markdown("### 🛠️ 에듀테크 도구 (중학생 찰떡)")
    st.markdown(
        """
        - **퀴즈**: Kahoot/Quizizz/Wordwall — 게임처럼 복습 🎮  
        - **보드/정리**: Canva/Google Jamboard(또는 FigJam) — 개념 카드·타임라인 🧩  
        - **지도/현장감**: Google Earth/Street View — 사료+지도로 맥락 연결 🗺️  
        - **토론/녹음**: Vocaroo/Padlet — 1분 주장 녹음 & 서로 피드백 🎙️
        """
    )

def tips_block(tips):
    st.markdown("### 💡 고득점 꿀팁")
    for t in tips:
        st.markdown(f"- {t}")

# ------------------------- 메인 로직 -------------------------
if go:
    loading_bar()

    gkey = MBTI_GROUP[mbti]
    ginfo = GROUPS[gkey]
    base = BASE_STRATEGY[gkey]

    st.markdown("---")
    st.subheader(f"{mbti} | {ginfo['name']} {ginfo['emoji']}")
    st.success(PERSONA.get(mbti,"너만의 강점으로 공부해봐요! ✨"))
    st.caption(f"핵심 학습 기질: **{ginfo['vibe']}**")

    # 탭: 한국사 / 세계사 / 루틴 & 체크리스트
    tab_k, tab_w, tab_r = st.tabs(["🇰🇷 한국사", "🌍 세계사", "🗓️ 루틴·체크리스트"])

    with tab_k:
        section_block("이 유형에 찰떡인 공부법", base["core"], icon="🎯")
        activity_block("추천 활동 (수업·자율학습 겸용)", base["k_activities"], icon="🏯")
        edtech_block()
        tips_block(base["tips"])
        with st.expander("📎 미니 체크리스트"):
            st.write("□ 오늘 배운 핵심개념 3개 요약하기")
            st.write("□ 사료 1개를 ‘누가/언제/왜/무엇을’로 분석")
            st.write("□ 오답 3개 원인 태그 달기(개념/연표/사료)")

    with tab_w:
        section_block("이 유형에 찰떡인 공부법", base["core"], icon="🎯")
        activity_block("추천 활동 (수업·자율학습 겸용)", base["w_activities"], icon="🏛️")
        edtech_block()
        tips_block(base["tips"])
        with st.expander("🌐 미니 체크리스트"):
            st.write("□ 사건 1개를 세계지도에 핀 찍고 주변국 반응 메모")
            st.write("□ 동시기 한국사와 연결 고리 1개 찾기")
            st.write("□ 논쟁적 질문에 찬반 근거 1개씩 쓰기")

    with tab_r:
        plan = make_week_plan(gkey)
        st.markdown("### 🗓️ 1주 루틴(샘플)")
        for day, line in plan:
            st.markdown(f"- **{day}**: {line}")
        st.markdown("### ✅ 성취 루프")
        st.markdown("**목표 설정 → 실천(스프린트) → 피드백 → 오답루프 → 다음 목표 갱신**")
        st.info("Tip) ‘25분 집중 + 5분 휴식’ 포모도로로 탄력 유지! 🍅")

    # 작은 보상 연출
    st.success("미션 언락! 오늘 20분만 투자해서 ‘핵심 개념 3개’ 카드 만들어 보기 📇")
    st.toast(random.choice(["대단해요! 🤩","좋은 출발! 🚀","성장 중! 🌱","집중력 만점! 💯"]), icon="🎉")

else:
    st.markdown(
        f"#### 아래에서 MBTI를 고르고 **추천 보기 🔮** 버튼을 눌러보세요! {' '.join(random.sample(EMOJI_POOL, k=12))}"
    )
    st.markdown("> 한국사·세계사 각각 **탭**으로 맞춤 전략이 펼쳐집니다 ✨")
