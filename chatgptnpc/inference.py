import os
import openai
from dataset import make_dataset
import argparse
import requests
from scipy.spatial import distance
from laserembeddings import Laser
import random

openai.api_key = os.environ["openai_api_key"]

class chat():
    def __init__(self, datas, npc_name):

        self.npc_name = npc_name

        # npc의 기본 정보를 입력 해줍니다.
        self.first_prompt = ''
        self.first_prompt += f'{npc_name}(은/는) 메이플 스토리의 npc 입니다.\n'
        self.first_prompt += f'{npc_name}(은/는) 평소에 다음과 같은 대화를 합니다.\n'

        for data in datas['conversation']:
            self.first_prompt += f'{npc_name}: {data}\n'
            if len(self.first_prompt) > 1900: # 최대 입력 가능 토큰을 넘는것 방지
                self.first_prompt = self.first_prompt.replace(f'{npc_name}: {data}\n', '')
                break
        
    def npc_chat(self, prompt):
        response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
                {"role": "system", "content": self.first_prompt},
                {"role": "user", "content": prompt},
            ]
        )
        return f'{self.npc_name} : '+ response['choices'][0]['message']['content']
    
    def sent(self, text):
        url = "http://localhost:8000/sent"
        data = {"text": f"{text}"}
        response = requests.post(url, json=data)
        
        return response.json()['sentiment']
    
    def cal_similarity(self, source, target):
        return 1 - distance.cosine(source, target)



if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('--npc_data_dir', type=str, default='./data/npc_data_2/preprocessed_npc_data_list.tsv')
    parser.add_argument('--npc_name', type=str, default='나인하트')
    args = parser.parse_args()

    laser = Laser()

    data = make_dataset(args.npc_data_dir)
    npc_data = data.npc_load(args.npc_name)
    chat = chat(npc_data, args.npc_name)
    quest_script = random.choice(list(npc_data[npc_data.answer == 1].conversation))
    
    embedded_quest = laser.embed_sentences([quest_script, "퀘스트를 수행 하겠습니다."], ['ko', 'ko'])

    print(f'현재 퀘스트 : {quest_script}')
    while True:
        
        user_input = input('입력 : ')
        response_input = user_input + f'\n{args.npc_name} : '
        
        user_sent = chat.sent(user_input)        
        response = chat.npc_chat(response_input)

        embedded_input = laser.embed_sentences([user_input], ['ko'])    

        if chat.cal_similarity(embedded_quest[0], embedded_input) >= 0.6 or chat.cal_similarity(embedded_quest[1], embedded_input) >= 0.8:
            print('퀘스트를 수락 하셨습니다.')
            response = chat.npc_chat(f'퀘스트를 수행 하겠습니다 \n{args.npc_name} : ')

        print(user_sent)
        print(response)
