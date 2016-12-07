from bs4 import BeautifulSoup as bsoup
import requests
import csv


# Team abbreviations to help with url building
TEAMS = {
    'Anaheim'      : 'ana',
    'Arizona'      : 'ari',
    'Boston'       : 'bos',
    'Buffalo'      : 'buf',
    'Calgary'      : 'cgy',
    'Carolina'     : 'car',
    'Chicago'      : 'chi',
    'Colorado'     : 'col',
    'Columbus'     : 'cbj',
    'Dallas'       : 'dal',
    'Detroit'      : 'det',
    'Edmonton'     : 'edm',
    'Florida'      : 'fla',
    'Los Angeles'  : 'la',
    'Minnesota'    : 'min',
    'Montreal'     : 'mtl',
    'Nashville'    : 'nsh',
    'New Jersey'   : 'nj',
    'NY Islanders' : 'nyi',
    'NY Rangers'   : 'nyr',
    'Ottawa'       : 'ott',
    'Philadelphia' : 'phi',
    'Pittsburgh'   : 'pit',
    'San Jose'     : 'sj',
    'St. Louis'    : 'stl',
    'Tampa Bay'    : 'tb',
    'Toronto'      : 'tor',
    'Vancouver'    : 'van',
    'Washington'   : 'wsh',
    'Winnipeg'     : 'wpg'
}


def scrape_season(url, team_name, year):
    
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
        if len(cells) != 9:
            continue

        # get the date of the event
        game_date = cells[0].text

        # determine the home and away teams
        home_team = ''
        away_team = ''
		
        # ignore games against teams that no longer exist
        try:
            lis = cells[1].find_all('li')
            if lis[0].text == 'vs' and len(lis) == 3:
                away_team = lis[2].text
                home_team = team_name 
            elif lis[0].text == '@' and len(lis) == 3:
                home_team = lis[2].text
                away_team = team_name
            elif lis[0].text == 'vs' and len(lis) == 2:
                home_team = team_name
                away_team = lis[1].text
            elif lis[0].text == '@' and len(lis) == 2:
                home_team = lis[1].text
                away_team = team_name 
        except IndexError:
            continue

        # determine the home and away team scores
        try:
            score = cells[2].a.text.split(' ')[0].split('-')
        except AttributeError:
            continue

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

        # determine shots for and against
        try:
            shots = cells[6].text.split('-')
            shots_for = shots[0]
            shots_against = shots[1]
        except AttributeError:
            continue

        # determine powerplay success and attempts
        try:
            powerplay = cells[7].text.split('-')
            powerplay_success = powerplay[0]
            powerplay_attempts = powerplay[1]
        except AttributeError:
            continue

        # determine penalty kill success and attempts
        try:
            penalty_kill = cells[8].text.split('-')
            penalty_kill_success = penalty_kill[0]
            penalty_kill_attempts = penalty_kill[1]
        except AttributeError:
            continue

        game_list.append([
            year, game_date, home_team, away_team, 
            home_team_score, away_team_score,
            shots_for, shots_against, powerplay_success,
            powerplay_attempts, penalty_kill_success,
            penalty_kill_attempts
        ])

    return game_list


def compare(x, y):
    if x[0] == y[0] and x[1] == y[1] and x[2] == y[2]:
        return True
    else:
        return False


def write_to_csv(data):
    with open('data.csv', 'a') as csvfile:
        csvwriter = csv.writer(csvfile, delimiter=',')
        for x in data:
            csvwriter.writerow(x)


def main():
    
    sorted_teams = sorted(TEAMS.items())
    year = input("Please enter a year: ")
    season = list()
    for team in sorted_teams:
        url = 'http://www.espn.com/nhl/team/schedule/_/name/' + team[1] + '/year/' + year
        # scrape all games of a particular season for a team
        game_list = scrape_season(url, team[0], year)
        season.append(game_list)
    
    compressed_season = [game for x in season for game in x]
    """final_season = list()
    for i in range(len(compressed_season)):
        for j in range(i + 1, len(compressed_season)):
            flag = compare(compressed_season[i], compressed_season[j])
            if flag:
                final_season.append(compressed_season[i])
                break"""

    #write_to_csv(compressed_season)


if __name__ == '__main__':
    main()
