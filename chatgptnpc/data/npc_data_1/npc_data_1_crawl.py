from bs4 import BeautifulSoup as bs
import requests

def crawl_npc_script():
    url = f'https://gamedori.xyz/magongtip/1305410'

    html = requests.get(url)
    html = bs(html.text, 'html.parser')
    table = html.find('div', {'class' : 'document_1305410_1305042 rhymix_content xe_content'})
    npcs = table.find_all('p')
    for npc in npcs:
        print(npc.get_text())
        input()

if __name__ == "__main__":
    crawl_npc_script()