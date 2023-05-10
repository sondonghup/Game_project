from bs4 import BeautifulSoup as bs
import requests
import ray
import psutil
import argparse

@ray.remote
def crawl_npc_script():
    url = f'https://wcr2.kennysoft.kr/Quest/'

    html = requests.get(url)
    html = bs(html.text, 'html.parser')
    table = html.find('table', {'style' : 'width:500px; '})
    quests = table.find_all('tr')
    for npc in quests[1:]:
        quest_url = url + npc.find_all('a')[0]['href']
        with open('quest_url_list.txt', 'a', encoding='utf-8')as f:
            f.write(f'{quest_url}\n')

@ray.remote
def quest_crawl_script(url):
    
    html = requests.get(url)
    html.encoding='UTF-8'
    html = bs(html.text, 'html.parser')
    quest_box = html.find_all('table')[2]
    tables = quest_box.find_all('div', {'class' : 'dlg c'})
    for table in tables:
        conversation = table.find('pre')

        while True: # 선택지와 캐릭터가 대화를 하는 것을 제거 합니다
            try:
                conversation = conversation.find('div', {'class' : 'label'}).decompose()
            except:
                break
        npc = table.find('div', {'class' : 'bar'}).text

        if '<img' in str(conversation): # 보상이 있는 부분을 제거 합니다
            continue
        try:
            conversation = conversation.text.replace('\n',' ').replace('\r',' ')
        except:
            continue
        with open('npc_data_list.tsv', 'a', encoding='utf-8')as f:
            f.write(f'{npc}\t{conversation}\n')
        

if __name__ == "__main__":
    '''
    npc_data_2 입니다
    npc의 퀘스트 대화를 크롤링합니다.
    '''

    parser = argparse.ArgumentParser()
    parser.add_argument('--mode', type=str, choices=['url', 'data'], default='data')
    args = parser.parse_args()

    if args.mode == 'url': # 퀘스트별 url을 크롤링 합니다.

        num_cpu_counts = psutil.cpu_count()

        ray.init(num_cpus=num_cpu_counts)
        obj_id = [
            crawl_npc_script()
        ]
        results = ray.get(obj_id)
        ray.shutdown()

    elif args.mode == 'data': # 퀘스트별 url을 기준으로 npc와 npc_data를 크롤링 합니다.

        with open('npc_data_list.tsv', 'a', encoding='utf-8')as f:
            f.write(f'npc\tconversation\n')

        url_list = []
        with open('quest_url_list.txt', 'r', encoding='utf-8')as f:
            for text in f:
                url_list.append(text.replace('\n',''))
        
        npc_data_list = []

        num_cpu_counts = psutil.cpu_count()

        ray.init(num_cpus=num_cpu_counts)
        obj_id = [
            quest_crawl_script.remote(url) for url in url_list
        ]
        results = ray.get(obj_id)
        ray.shutdown()
