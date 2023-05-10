import requests
import argparse
from bs4 import BeautifulSoup as bs
from tqdm import tqdm
import ray
import psutil
from datetime import datetime, timedelta

class inven():
    def __init__(self):
        self.title_list = []
        
    @ray.remote
    def inven_post_crawl(self, page_num, recommend, dates):
        '''
        page_num : 메이플 팁 게시판의 페이지 입니다.
        recommend : 전체글, 10추글, 30추글
        '''
        if recommend == 'all':
            url = f"https://www.inven.co.kr/board/maple/5974?p={page_num}"
        elif recommend == 'chu':
            url = f"https://www.inven.co.kr/board/maple/5974?my=chu&p={page_num}"
        elif recommend == 'chuchu':
            url = f"https://www.inven.co.kr/board/maple/5974?my=chuchu&p={page_num}"

        html = requests.get(url)
        html = bs(html.text, "html.parser")
        table = html.find("div", {"class": "board-list"})
        posts = table.find_all("tr")

        for post in posts[1:]: # 커럼명 제거 
            try:
                date = post.find("td", {"class" : "date"}).text
                title = post.find("a").text
                if isinstance(dates, str):
                    if ':' in date:
                        self.title_list.append(title.split(']')[1].strip())
                else:
                    if date in dates:
                        self.title_list.append(title.split(']')[1].strip())
            except Exception as e:
                continue
        return self.title_list

    def set_dates(self, date):
        if date == 'day':
            dates = ':'
        elif date == '7day':
            today = datetime.today()
            dates = [ str((today - timedelta(days=num)).isoformat()).split('-')[1] + f'-{(today - timedelta(days=num)).day}' for num in range(8)]
        return dates

    def inven_title(self, recommend, date):

        dates = self.set_dates(date)

        num_cpu_counts = psutil.cpu_count()

        ray.init(num_cpus=num_cpu_counts)
        obj_id = [
            self.inven_post_crawl.remote(self, page_num, recommend, dates)
            for page_num in tqdm(range(1, 500))
        ]
        results = ray.get(obj_id)
        word_list = []
        for result in results:
            word_list.extend(result)
        ray.shutdown()
        return word_list

if __name__ == "__main__":
    '''
    ray를 사용하여 병렬처리 합니다.
    page_num_start : 시작 페이지 번호 입니다.
    page_num_end : 종료 페이지 번호 입니다.
    시작 페이지 번호 부터 종료 페이지가 나올때 까지 크롤링을 시작 합니다.
    recommend_threshold : 추천 수 제한 입니다.
    '''

