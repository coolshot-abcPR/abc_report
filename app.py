import streamlit as st
import requests
import urllib.parse

# 네이버 API 키 설정 (정확하게 입력 완료)
CLIENT_ID = "Lcd5PPaRdVcTrawgRyUz"
CLIENT_SECRET = "nHRmT_1qTp"

def get_news(keyword, display_count):
    # 🌟 앞뒤 불필요한 공백을 완전히 제거하여 API 에러 방지
    clean_keyword = keyword.strip()
    enc_text = urllib.parse.quote(clean_keyword)
    
    url = f"https://openapi.naver.com/v1/search/news.json?query={enc_text}&display={display_count}&sort=date"
    headers = {
        "X-Naver-Client-Id": CLIENT_ID,
        "X-Naver-Client-Secret": CLIENT_SECRET
    }
    
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response.json().get('items', [])
    except Exception as e:
        return []
    return []

# --- 웹 화면 구성 ---
st.set_page_config(page_title="실시간 뉴스 모니터링", layout="wide")

st.title("📰 멀티 키워드 실시간 뉴스 모니터링")
st.caption("여러 키워드를 동시에 추적하고 팀원들과 공유하는 대시보드입니다.")

# 사이드바 설정
st.sidebar.header("🔍 모니터링 설정")
# 🌟 기본 세팅 키워드를 원하시는 'BC카드, 비씨카드, KT'로 변경해 두었습니다!
raw_keywords = st.sidebar.text_input("추적할 키워드들 (쉼표로 구분)", value="BC카드, 비씨카드, KT")

# 기본 출력 개수 30개 설정
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
                    
                    # 폰트 축소 스타일 적용
                    with st.container():
                        st.markdown(f"#### {a_idx}. {title}")
                        st.caption(f"📅 {pub_date}")
                        st.write(f":small[{description}]")
                        st.markdown(f"[🔗 기사 원문 보러가기]({link})")
                        st.write("---")
            else:
                # 🌟 무조건 API 오류라고 출력하는 대신, 진짜 검색 결과가 없는 경우를 고려해 문구 수정
                st.info(f"💡 '{keyword}'에 대한 최근 24시간 내 뉴스가 없거나, 검색어 형식을 확인해 주세요. (잠시 후 다시 업데이트 버튼을 눌러보세요)")
else:
    st.info("왼쪽 사이드바에 키워드를 입력해 주세요.")