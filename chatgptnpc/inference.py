import os
import openai
from dataset import make_dataset
import argparse
import requests

openai.api_key = os.environ["openai_api_key"]

class chat():
    def __init__(self, datas, npc_name):

        self.npc_name = npc_name

        # npc의 기본 정보를 입력 해줍니다.
        self.first_prompt = ''
        self.first_prompt += f'{npc_name}(은/는) 메이플 스토리의 npc 입니다.\n'
        self.first_prompt += f'{npc_name}(은/는) 평소에 다음과 같은 대화를 합니다.\n'

        for data in datas:
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
        data = {"text": f"{user_input}"}
        response = requests.post(url, json=data)
        
        return response.json()['sentiment']


if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('--npc_data_dir', type=str, default='./data/npc_data_2/npc_data_list.tsv')
    parser.add_argument('--npc_name', type=str, default='나인하트')
    args = parser.parse_args()

    data = make_dataset(args.npc_data_dir)
    npc_data = data.npc_load(args.npc_name)
    chat = chat(npc_data['conversation'], args.npc_name)
    while True:
        user_input = input('입력 :') + f'\n{args.npc_name} : '

        print(chat.sent(user_input))
        print(chat.npc_chat(user_input))
