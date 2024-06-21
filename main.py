import requests
from bs4 import BeautifulSoup
import json

class Jogos:
    def __init__(self):
        self.url = "https://www.placardefutebol.com.br"
        url_jogos = self.url + '/jogos-em-andamento'
        resposta = requests.get(url_jogos)
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

                # Extract game statistics
                stats = self.extract_game_statistics(game_link)

                jogos_detalhes.append({
                    'league': league_name,
                    'status': status,
                    'team1': team1,
                    'score1': score1,
                    'team2': team2,
                    'score2': score2,
                    'link': game_link,
                    'stats': stats
                })

        with open('ao_vivo.json', 'w', encoding='utf-8') as json_file:
            json.dump(jogos_detalhes, json_file, ensure_ascii=False, indent=4)

    def extract_game_statistics(self, game_link):
        url_estatistica = self.url + game_link
        resposta2 = requests.get(url_estatistica)
        soup2 = BeautifulSoup(resposta2.text, 'html.parser')
        tes = soup2.get_text()
        print(tes)

        # Example extraction based on observed HTML structure
        stats_section = soup2.find('div', class_='stats-section')
        if stats_section:
            statistics = []
            stats_items = stats_section.find_all('div', class_='stat-item')
            for stat_item in stats_items:
                label = stat_item.find('div', class_='label').text.strip()
                value = stat_item.find('div', class_='value').text.strip()
                statistics.append({
                    'label': label,
                    'value': value
                })
            return statistics
        else:
            return [{'label': 'Stats Not Available', 'value': 'N/A'}]

if __name__ == "__main__":
    Jogos().extract_game_statistics('/brasileirao-serie-a/20-06-2024-vitoria-x-atletico-mg.html')
