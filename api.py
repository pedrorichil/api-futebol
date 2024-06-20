import requests
from bs4 import BeautifulSoup
import json


class Jogos:
    def __init__(self):
        self.url = "https://www.placardefutebol.com.br/"


    def jogo_ao_vivo(self):
        url_completa = self.url + 'jogos-em-andamento'
        response = requests.get(url_completa)
        soup = BeautifulSoup(response.text, 'html.parser')

        # Encontrar todos os jogos em andamento
        games = soup.find_all('a', href=True, class_=False)

        # Para armazenar os detalhes dos jogos
        game_details = []

        for game in games:
            league_tag = game.find_previous('h3', class_='match-list_league-name')
            league_name = league_tag.text.strip() if league_tag else 'Unknown League'

            status_tag = game.find('span', class_='badge')
            status = status_tag.text.strip() if status_tag else 'Unknown Status'

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

            game_details.append({
                'league': league_name,
                'status': status,
                'team1': team1,
                'score1': score1,
                'team2': team2,
                'score2': score2
            })

        with open('jogos_ao_vivo.json', 'w', encoding='utf-8') as json_file:
            json.dump(game_details, json_file, ensure_ascii=False, indent=4)
        return game_details

    def jogos_de_hoje(self):
        pass

    def jogos_de_amanha(self):
        pass




jogos = Jogos()  # Criar uma instância da classe Jogos
games = jogos.jogo_ao_vivo()  # Chamar o método da instância jogos
