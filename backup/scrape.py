from bs4 import BeautifulSoup as bsoup
import requests


START_URL = 'http://www.espn.com/nhl/team/schedule/_/name/pit/year/2016'
TEAM = 'Pittsburgh'


def main():
    r = requests.get(START_URL).text
    soup = bsoup(r, 'lxml')

    game_list = list()

    table = soup.find("table", "tablehead")
    for tr in table.find_all("tr")[1:]:
        if dict(tr.attrs)['class'][0] == 'colhead':
            continue
        if dict(tr.attrs)['class'][0] == 'stathead':
            break
        cells = tr.find_all('td')
        
        # determine the home team and away teams
        home_team = TEAM
        away_team = ''

        if cells[1].find_all('li')[0].text == 'vs':
            away_team = cells[1].find_all('li')[2].text
        else:
            home_team = cells[1].find_all('li')[2].text
            away_team = TEAM

        
        # determine the home and away team scores
        score = cells[2].a.text.split(' ')[0].split('-')
        home_team_score = 0;
        away_team_score = 0;
        if cells[2].find_all('li')[0].span.text == 'L' and home_team == TEAM:
            home_team_score = int(score[1])
            away_team_score = int(score[0])
        elif cells[2].find_all('li')[0].span.text == 'L' and away_team == TEAM:
            home_team_score = int(score[0])
            away_team_score = int(score[1])
        elif cells[2].find_all('li')[0].span.text == 'W' and home_team == TEAM:
            home_team_score = int(score[0])
            away_team_score = int(score[1])
        elif cells[2].find_all('li')[0].span.text == 'W' and away_team == TEAM:
            home_team_score = int(score[1])
            away_team_score = int(score[0])

        game_list.append([home_team, home_team_score, away_team, away_team_score])


    for game in game_list:
        print("%d %s @ %s %d" % (game[3], game[2], game[0], game[1]))
        


if __name__ == '__main__':
    main()
