import streamlit as st
import requests
import urllib.parse

# 네이버 API 키 설정
CLIENT_ID = "Lcd5PPaRdVcTrawgRyUz"
CLIENT_SECRET = "nHRmT_1qTp"

def get_news(keyword, display_count):
    clean_keyword = keyword.strip()
    
    # 🌟 [핵심 개선] 검색어 최적화 시스템
    # 사용자가 'BC카드'나 '비씨카드'를 검색하면, 띄어쓰기 및 혼용 단어까지 포함하여 
    # 네이버 API가 기사를 누락 없이 다 가져오도록 'OR' 연산 검색어로 자동 변환합니다.
    if clean_keyword.replace(" ", "").upper() in ["BC카드", "비씨카드"]:
        query_text = "BC카드 | BC 카드 | 비씨카드"
    else:
        query_text = clean_keyword
        
    enc_text = urllib.parse.quote(query_text)
    url = f"https://openapi.naver.com/v1/search/news.json?query={enc_text}&display={display_count}&sort=date"
    
    headers = {
        "X-Naver-Client-Id": CLIENT_ID,
        "X-Naver-Client-Secret": CLIENT_SECRET
    }
    
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response.json().get('items', [])
    except Exception:
        return []
    return []

# --- 웹 화면 구성 ---
st.set_page_config(page_title="실시간 뉴스 모니터링", layout="wide")

st.title("📰 멀티 키워드 실시간 뉴스 모니터링")
st.caption("여러 키워드를 동시에 추적하고 팀원들과 공유하는 대시보드입니다.")

# 사이드바 설정
st.sidebar.header("🔍 모니터링 설정")
raw_keywords = st.sidebar.text_input("추적할 키워드들 (쉼표로 구분)", value="BC카드, 비씨카드, KT")
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
                    
                    with st.container():
                        st.markdown(f"#### {a_idx}. {title}")
                        st.caption(f"📅 {pub_date}")
                        st.write(f":small[{description}]")
                        st.markdown(f"[🔗 기사 원문 보러가기]({link})")
                        st.write("---")
            else:
                st.info(f"💡 '{keyword}'에 대한 최근 뉴스가 없거나, 검색어 형식을 확인해 주세요.")
else:
    st.info("왼쪽 사이드바에 키워드를 입력해 주세요.")