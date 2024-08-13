import streamlit as st
import openai
from dotenv import load_dotenv
import os
from metadata import metadata
import streamlit as st
from PIL import Image

# 이미지 파일 로드
favicon = Image.open('images/favicon.png')

# Load environment variables
load_dotenv()

# Set up OpenAI API key
#openai.api_key = os.getenv("OPENAI_API_KEY")
openai.api_key = st.secrets["openai"]

# 20명의 유명 시인 리스트
POETS = ["김소월", "윤동주", "한용운", "정지용", "백석", "이상", "김춘수", "서정주", "유치환", "김수영",
         "박목월", "조지훈", "이육사", "신동엽", "김영랑", "황동규", "정호승", "기형도", "나희덕", "문정희"]

# 11가지 시 장르
GENRES = ["서정시", "서사시", "풍자시", "자유시", "소네트", "발라드", "민요시", "상징시", "실험시", "구체시", "한국시조"]

def generate_poem(prompt, model="gpt-4o"):
    response = openai.ChatCompletion.create(
        model=model,
        messages=[
            {"role": "system", "content": "당신은 뛰어난 시인입니다. 주어진 지시에 따라 40자 이내 짧은 시를 작성해주세요."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=100
    )
    return response.choices[0].message['content'].strip()

def analyze_poem(poem, prompt, model="gpt-4o"):
    response = openai.ChatCompletion.create(
        model=model,
        messages=[
            {"role": "system", "content": "당신은 문학 평론가입니다. 주어진 40자 이내 짧은 시를 분석하고 분류해주세요."},
            {"role": "user", "content": prompt + "\n\n시: " + poem}
        ],
        max_tokens=150
    )
    return response.choices[0].message['content'].strip()

st.title("짧은 시 생성 및 분석 앱")

# 사이드바에 프롬프트 엔지니어링 옵션 추가
st.sidebar.title("프롬프트 엔지니어링 옵션")
show_prompts = st.sidebar.checkbox("프롬프트 보기/수정")

# 기능 1: 특정 시인의 문체로 짧은 시 작성
st.header("1. 특정 시인의 문체로 짧은 시 작성")
theme = st.text_input("시의 주제나 글감을 입력하세요:")
selected_poets = st.multiselect("시인을 선택하세요 (최대 4명):", POETS, max_selections=4)

if st.button("시 생성하기") and theme and selected_poets:
    for poet in selected_poets:
        prompt = f"{poet}의 문체로 '{theme}'에 대한 50자 이내의 짧은 시를 작성해주세요."
        if show_prompts:
            st.text_area(f"{poet}의 프롬프트:", prompt, key=f"prompt_{poet}")
        poem = generate_poem(prompt)
        st.write(f"**{poet}의 문체로 작성된 시:**")
        st.write(poem)
        st.write("---")

# 기능 2: 특정 시인의 문체로 댓글 및 좋아요 반응 시뮬레이션
st.header("2. 시에 대한 반응 시뮬레이션")
user_poem = st.text_area("당신의 짧은 시를 입력하세요 (50자 이내):")
reaction_poet = st.selectbox("반응을 생성할 시인을 선택하세요:", POETS)

if st.button("반응 생성하기") and user_poem and reaction_poet:
    prompt = f"""
    다음은 한 사용자가 작성한 50자 이내의 짧은 시입니다:
    
    {user_poem}
    
    {reaction_poet}의 문체로 이 시에 대한 짧은 댓글(30자 이내)과 1부터 5까지의 별점을 매겨주세요. 
    출력 형식:
    댓글: [댓글 내용]
    별점: [1-5 사이의 숫자]
    """
    if show_prompts:
        st.text_area("반응 생성 프롬프트:", prompt)
    reaction = generate_poem(prompt)
    st.write(f"**{reaction_poet}의 반응:**")
    st.write(reaction)

# 기능 3: 시 장르 분류
st.header("3. 시 장르 분류")
genre_poem = st.text_area("장르를 분류할 짧은 시를 입력하세요 (50자 이내):", key="genre_poem")

if st.button("장르 분류하기") and genre_poem:
    prompt = f"""
    다음은 50자 이내의 짧은 시입니다:
    
    {genre_poem}
    
    이 시를 다음 장르 중 하나로 분류해주세요: {', '.join(GENRES)}
    분류 결과와 그 이유를 간단히 설명해주세요.
    출력 형식:
    장르: [선택한 장르]
    이유: [분류 이유 간단 설명]
    """
    if show_prompts:
        st.text_area("장르 분류 프롬프트:", prompt)
    analysis = analyze_poem(genre_poem, prompt)
    st.write("**장르 분류 결과:**")
    st.write(analysis)

# 프롬프트 엔지니어링 팁
st.sidebar.title("프롬프트 엔지니어링 팁")
st.sidebar.write("""
1. 구체적이고 명확한 지시를 제공하세요.
2. 원하는 출력 형식을 명시하세요.
3. 예시를 제공하면 더 좋은 결과를 얻을 수 있습니다.
4. 시스템 메시지를 활용하여 AI의 역할을 정의하세요.
5. 프롬프트를 반복적으로 개선하며 최적의 결과를 찾으세요.
""")

st.sidebar.title("프로젝트 정보")
st.sidebar.info("""
이 앱은 GPT-4를 활용하여 짧은 시를 생성하고 분석합니다. 
프롬프트 엔지니어링을 직접 체험해보세요!
""")
