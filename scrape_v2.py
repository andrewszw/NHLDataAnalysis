from bs4 import BeautifulSoup as bsoup
import requests


class Game:
    def __init__(self, h_team, a_team, h_team_score, a_team_score):
        self.home = h_team
        self.away = a_team
        self.h_score = h_team_score
        self.a_score = a_team_score

    def get_winner(self):
        return (self.home if self.h_score > self.a_score else self.away)


def scrape_season(url, team_name):
    
    # get the soup
    r = requests.get(url).text
    soup = bsoup(r, 'lxml')

    # list of game objects
    game_list = list()

    # find the table of games
    table = soup.find('table', 'tablehead')
    for row in table.find_all('tr')[1:]:    

        # skip column headers
        if dict(row.attrs)['class'][0] == 'colhead':
            continue
        if dict(row.attrs)['class'][0] == 'stathead':
            continue

        # get the individual cells
        cells = row.find_all('td')

        # determine the home and away teams
        home_team = ''
        away_team = ''
		
        # ignore games against teams that no longer exist
        try:
            if cells[1].find_all('li')[0].text == 'vs':
                away_team = cells[1].find_all('li')[2].text
                home_team = team_name 
            else:
                home_team = cells[1].find_all('li')[2].text
                away_team = team_name
        except IndexError:
            continue

        # determine the home and away team scores
        score = cells[2].a.text.split(' ')[0].split('-')
        home_team_score = 0;
        away_team_score = 0;
        if cells[2].find_all('li')[0].span.text == 'L' and home_team == team_name:
            home_team_score = int(score[1])
            away_team_score = int(score[0])
        elif cells[2].find_all('li')[0].span.text == 'L' and away_team == team_name:
            home_team_score = int(score[0])
            away_team_score = int(score[1])
        elif cells[2].find_all('li')[0].span.text == 'W' and home_team == team_name:
            home_team_score = int(score[0])
            away_team_score = int(score[1])
        elif cells[2].find_all('li')[0].span.text == 'W' and away_team == team_name:
            home_team_score = int(score[1])
            away_team_score = int(score[0])

        game_list.append(Game(home_team, away_team, home_team_score, away_team_score))

    return game_list


def main():
    
    # get the initial url
    url = 'http://www.espn.com/nhl/team/schedule/_/name/pit/year/2008'
    
    # scrape all games of a particular season for a team
    game_list = scrape_season(url, 'Pittsburgh')
    for game in game_list:
        print("%s" % (game.get_winner()))


if __name__ == '__main__':
    main()
