import requests
from bs4 import BeautifulSoup

def get_cgv_movies():
    url = "http://www.cgv.co.kr/movies/"
    headers = {
        "User-Agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36"
    }
    # 서버에 요청
    resp = requests.get(url, headers=headers)

    # 응답이 에러면 예외 발생
    resp.raise_for_status()

    # HTML 텍스트를 객체로 변환
    soup = BeautifulSoup(resp.text, "html.parser")

    # 원하는 요소 선택
    chart_box = soup.select("div.sect-movie-chart ol li") 
# 먼저 웹페이지에 접속 -> 응답이 정상인지 확인 -> html을 파싱 -> 필요한 정보를 선택

    result = []
    for movie in chart_box:
        title_tag = movie.select_one("strong.title")
        percent_tag = movie.select_one("strong.percent span")
        release_tag = movie.select_one("span.txt-info")

        # result.append({
        #     "title" : title_tag.text.strip() if title_tag else None,
        #     "percent": percent_tag.text.strip() if percent_tag else None,
        #     "release": release_tag.text.strip() if release_tag else None,
        # })

        if title_tag:
            result.append({
            "title" : title_tag.text.strip(),
            "percent": percent_tag.text.strip() if percent_tag else None,
            "release": release_tag.text.strip() if release_tag else None,
        })

    return result   

        # if percent_tag:
        #     span_tag = percent_tag.fin("span")

if __name__ == "__main__":
    movie = get_cgv_movies()
    for idx, m in enumerate(movie, 1):
        print(f"{idx}. {m['title']} - 예매율: {m['percent']} {m['release']} ")
    

        # img_tag = movie.select_one("span.thumb-image img")
        # if img_tag:
        #     img_url = img_tag["src"]
        # else:
        #     img_url = None    


# find() : 태그 한개
# find_all(): 여러개
# css선택자일때 여러개: select() 
# 한개 select_one()


# <strong class="title">쥬라기 월드: 새로운 시작</strong>
# <strong class="percent">예매율<span>32.6%</span></strong>
# <span class="txt-info"><strong>2025.07.02 <span>개봉</span></strong></span>
# <span class="thumb-image"><img src="https://img.cgv.co.kr/Movie/Thumbnail/Poster/000089/89462/89462_320.jpg" alt="쥬라기 월드: 새로운 시작 포스터" onerror="errorImage(this)"><!-- 영상물 등급 노출 변경 2022.08.24 --><i class="cgvIcon etc age12">12</i><!-- <span class="ico-grade 12">12</span> --></span>