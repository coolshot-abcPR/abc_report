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
st.title("📰 멀티 키워드 실시간 뉴스 모니터링")
st.caption("여러 키워드를 동시에 추적하고 팀원들과 공유하는 대시보드입니다.")

# 사이드바 설정
st.sidebar.header("🔍 모니터링 설정")
# 쉼표로 구분하여 여러 키워드를 입력받음
raw_keywords = st.sidebar.text_input("추적할 키워드들 (쉼표로 구분)", value="bc카드, 비씨카드, kt")
display_count = st.sidebar.slider("키워드당 기사 개수", min_value=5, max_value=30, value=10)

if st.sidebar.button("🔄 뉴스 실시간 업데이트"):
    st.toast("최신 뉴스를 업데이트했습니다!")

# 입력받은 키워드를 쉼표 기준으로 쪼개고 공백 제거
keywords = [k.strip() for k in raw_keywords.split(",") if k.strip()]

if keywords:
    # 🌟 입력한 키워드 개수만큼 상단에 탭(가로 메뉴)을 자동으로 만들어 줌!
    tabs = st.tabs(keywords)
    
    # 각 탭별로 매칭되는 뉴스를 채워넣음
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
                    
                    with st.container():
                        st.markdown(f"### [{a_idx}] {title}")
                        st.caption(f"📅 {pub_date}")
                        st.write(description)
                        st.markdown(f"[🔗 기사 원문 보러가기]({link})")
                        st.write("---")
            else:
                st.warning("검색 결과가 없거나 API 키가 올바르지 않습니다.")
else:
    st.info("왼쪽 사이드바에 키워드를 입력해 주세요 (예: 삼성전자, 애플, 현대차)")