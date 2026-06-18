import streamlit as st
import requests
import urllib.parse

# [필수 변경] 발급받은 네이버 API 키를 입력하세요
CLIENT_ID = "Lcd5PPaRdVcTrawgRyUz"
CLIENT_SECRET = "nHRmT_lqTp"

def get_news(keyword, display_count):
    enc_text = urllib.parse.quote(keyword)
    url = f"https://openapi.naver.com/v1/search/news.json?query={enc_text}&display={display_count}&sort=date"
    headers = {
        "X-Naver-Client-Id": CLIENT_ID,
        "X-Naver-Client-Secret": CLIENT_SECRET
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json().get('items', [])
    return []

# --- 웹 화면 구성 ---
st.set_page_config(page_title="실시간 뉴스 모니터링", layout="wide")

# ✨ [디자인 설정] 글씨 크기를 전체적으로 작게 만드는 비밀 코드
st.markdown("""
    <style>
    /* 전체 본문 글씨 크기 조절 */
    html, body, [data-testid="stWidgetLabel"], .stMarkdown p {
        font-size: 14px !important;
    }
    /* 뉴스 제목 글씨 크기 조절 */
    .news-title {
        font-size: 17px !important;
        font-weight: bold !important;
        margin-bottom: 2px !important;
    }
    /* 날짜 글씨 크기 조절 */
    .news-date {
        font-size: 11px !important;
        color: #888888 !important;
    }
    /* 뉴스 설명 글씨 크기 조절 */
    .news-desc {
        font-size: 13px !important;
        color: #333333 !important;
        line-height: 1.5 !important;
    }
    </style>
    """, unsafe_check_html=True)

st.title("📰 멀티 키워드 실시간 뉴스 모니터링")
st.caption("여러 키워드를 동시에 추적하고 팀원들과 공유하는 대시보드입니다.")

# 사이드바 설정
st.sidebar.header("🔍 모니터링 설정")
raw_keywords = st.sidebar.text_input("추적할 키워드들 (쉼표로 구분)", value="2차전지, 자율주행, 반도체")

# ✨ 기본 가져올 기사 개수를 10개에서 30개로 늘렸습니다! (최대 50개까지 조절 가능)
display_count = st.sidebar.slider("키워드당 기사 개수", min_value=5, max_value=50, value=30)

if st.sidebar.button("🔄 뉴스 실시간 업데이트"):
    st.toast("최신 뉴스를 업데이트했습니다!")

# 입력받은 키워드 쪼개기
keywords = [k.strip() for k in raw_keywords.split(",") if k.strip()]

if keywords:
    tabs = st.tabs(keywords)
    
    for idx, keyword in enumerate(keywords):
        with tabs[idx]:
            st.subheader(f"🔥 '{keyword}' 최신 뉴스")
            articles = get_news(keyword, display_count)
            
            if articles:
                for a_idx, article in enumerate(articles, 1):
                    title = article['title'].replace('<b>', '').replace('</b>', '').replace('&quot;', '"').replace('&amp;', '&')
                    description = article['description'].replace('<b>', '').replace('</b>', '').replace('&quot;', '"').replace('&amp;', '&')
                    link = article['originallink'] or article['link']
                    pub_date = article['pubDate']
                    
                    # ✨ 작아진 폰트 스타일을 적용해서 뉴스 출력
                    with st.container():
                        st.markdown(f"<div class='news-title'>[{a_idx}] {title}</div>", unsafe_check_html=True)
                        st.markdown(f"<div class='news-date'>📅 {pub_date}</div>", unsafe_check_html=True)
                        st.markdown(f"<div class='news-desc'>{description}</div>", unsafe_check_html=True)
                        st.markdown(f"[🔗 기사 원문 보러가기]({link})")
                        st.write("---")
            else:
                st.warning("검색 결과가 없거나 API 키가 올바르지 않습니다.")
else:
    st.info("왼쪽 사이드바에 키워드를 입력해 주세요.")