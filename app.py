import streamlit as st
import requests
import xml.etree.ElementTree as ET
import urllib.parse

def get_news_rss(keyword, display_count):
    # 🌟 [엔진 전면 교체] 네이버 공식 RSS 피드를 활용하여 API 키 없이 무제한 수집
    clean_keyword = keyword.strip()
    enc_text = urllib.parse.quote(clean_keyword)
    
    # 네이버 뉴스 RSS 주소 구성
    url = f"https://news.naver.com/rss?rss=news&query={enc_text}"
    
    try:
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            # XML 데이터 파싱
            root = ET.fromstring(response.content)
            items = root.findall('.//item')
            
            articles = []
            for item in items[:display_count]:
                title = item.find('title').text if item.find('title') is not None else ''
                description = item.find('description').text if item.find('description') is not None else ''
                link = item.find('link').text if item.find('link') is not None else ''
                pub_date = item.find('pubDate').text if item.find('pubDate') is not None else ''
                
                # HTML 태그 제거 및 텍스트 정제
                title = title.replace('<b>', '').replace('</b>', '').replace('&quot;', '"').replace('&amp;', '&')
                description = description.replace('<b>', '').replace('</b>', '').replace('&quot;', '"').replace('&amp;', '&')
                
                articles.append({
                    'title': title,
                    'description': description,
                    'link': link,
                    'pubDate': pub_date
                })
            return articles
    except Exception:
        return []
    return []

# --- 웹 화면 구성 ---
st.set_page_config(page_title="실시간 뉴스 모니터링", layout="wide")

st.title("📰 멀티 키워드 실시간 뉴스 모니터링")
st.caption("API 키 제한 없이 365일 언제나 실시간 뉴스를 추적하는 팀 대시보드입니다.")

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
            articles = get_news_rss(keyword, display_count)
            
            if articles:
                for a_idx, article in enumerate(articles, 1):
                    with st.container():
                        st.markdown(f"#### {a_idx}. {article['title']}")
                        st.caption(f"📅 {article['pubDate']}")
                        st.write(f":small[{article['description']}]")
                        st.markdown(f"[🔗 기사 원문 보러가기]({article['link']})")
                        st.write("---")
            else:
                st.info(f"💡 '{keyword}'에 대한 최신 뉴스를 불러오는 중이거나 현재 조건에 맞는 기사가 없습니다. 사이드바의 업데이트 버튼을 눌러보세요.")
else:
    st.info("왼쪽 사이드바에 키워드를 입력해 주세요.")