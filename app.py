import streamlit as st
import requests
import urllib.parse

# 네이버 API 키 설정
CLIENT_ID = "Lcd5PPaRdVcTrawgRyUz"
CLIENT_SECRET = "nHRmT_1qTp"

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
raw_keywords = st.sidebar.text_input("추적할 키워드들 (쉼표로 구분)", value="BC카드, 비씨카드, KT")

# 기본 출력 개수를 30개로 상향 조정 완료!
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
                    # 검색어 하이라이트 태그 제거 및 텍스트 정제
                    title = article['title'].replace('<b>', '').replace('</b>', '').replace('&quot;', '"').replace('&amp;', '&')
                    description = article['description'].replace('<b>', '').replace('</b>', '').replace('&quot;', '"').replace('&amp;', '&')
                    link = article['originallink'] or article['link']
                    pub_date = article['pubDate']
                    
                    # 🌟 [에러 해결 및 폰트 축소] 
                    # 에러를 유발하던 HTML 대신 Streamlit 공식 스몰 폰트(small) 및 캡션 기능 활용
                    with st.container():
                        st.markdown(f"#### {a_idx}. {title}") # 제목 크기 한 단계 축소
                        st.caption(f"📅 {pub_date}") # 날짜 아주 작게 표시
                        st.write(f":small[{description}]") # 본문 글씨 크기 축소 적용
                        st.markdown(f"[🔗 기사 원문 보러가기]({link})")
                        st.write("---")
            else:
                st.warning("검색 결과가 없거나 API 키가 올바르지 않습니다.")
else:
    st.info("왼쪽 사이드바에 키워드를 입력해 주세요.")