import requests
from bs4 import BeautifulSoup
import json

class Jogos:
    def __init__(self):
        self.url = "https://www.placardefutebol.com.br"

    def jogo_ao_vivo(self):
        url_completa = self.url + '/jogos-em-andamento'
        resposta = requests.get(url_completa)
        soup = BeautifulSoup(resposta.text, 'html.parser')

        jogos = soup.find_all('a', href=True, class_=False)

        jogos_detalhes = []

        for game in jogos:
            league_tag = game.find_previous('h3', class_='match-list_league-name')
            league_name = league_tag.text.strip() if league_tag else 'Unknown League'

            status_tag = game.find('span', class_='badge')
            status = status_tag.text.strip() if status_tag else 'Unknown Status'

            if status != 'Unknown Status':
                teams = game.find_all('div', class_='team-name')
                if len(teams) >= 2:
                    team1 = teams[0].text.strip()
                    team2 = teams[1].text.strip()
                else:
                    team1 = 'Unknown Team 1'
                    team2 = 'Unknown Team 2'

                scores = game.find_all('span', class_='badge-default')
                if len(scores) >= 2:
                    score1 = scores[0].text.strip()
                    score2 = scores[1].text.strip()
                else:
                    score1 = '0'
                    score2 = '0'

                game_link = game['href'].strip() if 'href' in game.attrs else 'Unknown Link'

                jogos_detalhes.append({
                    'league': league_name,
                    'status': status,
                    'team1': team1,
                    'score1': score1,
                    'team2': team2,
                    'score2': score2,
                    'link': game_link
                })

        with open('ao_vivo.json', 'w', encoding='utf-8') as json_file:
            json.dump(jogos_detalhes, json_file, ensure_ascii=False, indent=4)

        #modo de usar: 'Jogos().jogo_ao_vivo()'
        return jogos_detalhes
    def probabilidade(self):
        pass

    def jogos_de_hoje(self):
        pass

    def jogos_de_amanha(self):
        pass



