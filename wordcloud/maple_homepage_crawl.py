import requests
import argparse
from bs4 import BeautifulSoup as bs
from tqdm import tqdm
import ray
import psutil
from datetime import datetime, timedelta

class maple():
    def __init__(self):
        self.title_list = []
        
    @ray.remote
    def maple_post_crawl(self, page_num, dates):
        '''
        page_num : 메이플 팁 게시판의 페이지 입니다.
        recommend : 전체글, 10추글, 30추글
        '''
        url = f'https://maplestory.nexon.com/Community/N23Free?page={page_num}'

        html = requests.get(url)
        html = bs(html.text, "html.parser")
        table = html.find("div", {"class": "notice"})
        post_list = table.find_all("span", {"class" : "title"})
        date_list = table.find_all("li", {"class" : "date_cnt"})

        for post, date in zip(post_list, date_list):
            date = date.text
            if '.' in date:
                date = '-'.join(date.split('.')[1:3]).strip()
            if isinstance(dates, str):
                if ':' in date:
                    self.title_list.append(post.text)
            else:
                if date in dates:
                    self.title_list.append(post.text)

        return self.title_list

    def set_dates(self, date):
        if date == 'day':
            dates = ':'
        elif date == '7day':
            today = datetime.today()
            dates = [ str((today - timedelta(days=num)).isoformat()).split('-')[1] + f'-{(today - timedelta(days=num)).day}' for num in range(8)]
        return dates

    def maple_title(self, date):

        dates = self.set_dates(date)

        num_cpu_counts = psutil.cpu_count()

        ray.init(num_cpus=num_cpu_counts)
        obj_id = [
            self.maple_post_crawl.remote(self, page_num, dates)
            for page_num in tqdm(range(1, 10))
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
