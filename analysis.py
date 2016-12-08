import pymongo
import numpy as np

def team_correlation(db, boolean):

    team_data = list()    
    for item in db.hockey.find({'home': boolean}):
        tmp_list = [
            item['goals_for'], item['goals_against'],
            item['shots_for'], item['shots_against'],
            item['pp_success'], item['pp_attempt'],
            item['pk_success'], item['pk_attempt']
        ]
        team_data.append(tmp_list)
    matrix = np.array(team_data).astype(np.float)
    team_corr = np.corrcoef(matrix.T)
    
    return team_corr


def average_shots_for(db):
    home_shots_win = 0
    home_shots_loss = 0
    away_shots_win = 0
    away_shots_loss = 0
    total_home_games = 0
    total_away_games = 0
    for item in db.hockey.find({'home': 1}):
        if item['goals_for'] > item['goals_against']:
            home_shots_win += item['shots_for']
        elif item['goals_for'] < item['goals_against']:
            home_shots_loss += item['shots_for']
        total_home_games += 1

    for item in db.hockey.find({'home': 0}):
        if item['goals_for'] > item['goals_against']:
            away_shots_win += item['shots_for']
        elif item['goals_for'] < item['goals_against']:
            away_shots_loss += item['shots_for']
        total_away_games += 1

    print("Average Shots by Home Team in Win: %f" % (home_shots_win / (total_home_games / 2)))
    print("Average Shots by Home Team in Loss: %f" % (home_shots_loss / (total_home_games / 2)))
    print("Average Shots by Away Team in Win: %f" % (away_shots_win / (total_away_games / 2)))
    print("Average Shots by Away in Loss: %f" % (away_shots_loss / (total_away_games / 2)))

    total_shots = (home_shots_win + home_shots_loss) + (away_shots_win + away_shots_loss)
    total_games = total_home_games + total_away_games
    print("Average Shots Per Game: %f" % (total_shots / total_games))
    
    

def average_goals_for(db):
    home_goals_win = 0
    home_goals_loss = 0
    away_goals_win = 0
    away_goals_loss = 0
    total_home_games = 0
    total_away_games = 0
    for item in db.hockey.find({'home': 1}):
        if item['goals_for'] > item['goals_against']:
            home_goals_win += item['goals_for']
        elif item['goals_for'] < item['goals_against']:
            home_goals_loss += item['goals_for']
        total_home_games += 1

    for item in db.hockey.find({'home': 0}):
        if item['goals_for'] > item['goals_against']:
            away_goals_win += item['goals_for']
        elif item['goals_for'] < item['goals_against']:
            away_goals_loss += item['goals_for']
        total_away_games += 1

    print("Average Goals by Home Team in Win: %f" % (home_goals_win / (total_home_games / 2)))
    print("Average Goals by Home Team in Loss: %f" % (home_goals_loss / (total_home_games / 2)))
    print("Average Goals by Away Team in Win: %f" % (away_goals_win / (total_away_games / 2)))
    print("Average Goals by Away in Loss: %f" % (away_goals_loss / (total_away_games / 2)))

    total_goals = (home_goals_win + home_goals_loss) + (away_goals_win + away_goals_loss)
    total_games = total_home_games + total_away_games
    print("Average Goals Per Game: %f" % (total_goals / total_games))


def average_powerplay(db):
    home_pp_win = 0
    home_pp_loss = 0
    away_pp_win = 0
    away_pp_loss = 0
    total_home_games = 0
    total_away_games = 0
    for item in db.hockey.find({'home': 1}):
        if item['pp_attempt'] == 0:
            continue
        if item['goals_for'] > item['goals_against']:
            home_pp_win += (item['pp_success'] / item['pp_attempt'])
        elif item['goals_for'] < item['goals_against']:
            home_pp_loss += (item['pp_success'] / item['pp_attempt'])
        total_home_games += 1

    for item in db.hockey.find({'home': 0}):
        if item['pp_attempt'] == 0:
            continue
        if item['goals_for'] > item['goals_against']:
            away_pp_win += (item['pp_success'] / item['pp_attempt'])
        elif item['goals_for'] < item['goals_against']:
            away_pp_loss += (item['pp_success'] / item['pp_attempt'])
        total_away_games += 1

    print("Average PowerPlay Conversion by Home Team in Win: %f" % (home_pp_win / (total_home_games / 2)))
    print("Average PowerPlay Conversion by Home Team in Loss: %f" % (home_pp_loss / (total_home_games / 2)))
    print("Average PowerPlay Conversion by Away Team in Win: %f" % (away_pp_win / (total_away_games / 2)))
    print("Average PowerPlay Conversion by Away in Loss: %f" % (away_pp_loss / (total_away_games / 2)))

    total_pp = (home_pp_win + home_pp_loss) + (away_pp_win + away_pp_loss)
    total_games = total_home_games + total_away_games
    print("Average PowerPlay Conversion Per Game: %f" % (total_pp / total_games))


def main():
    client = pymongo.MongoClient("localhost", 27017)

    db = client.nhl

    hteam_corr = team_correlation(db, 1)
    hteam_rounded = [['%.5f' % round(y, 5) for y in x] for x in hteam_corr]
    ateam_corr = team_correlation(db, 0)
    ateam_rounded = [['%.5f' % round(y, 5) for y in x] for x in ateam_corr]

    average_shots_for(db)
    print()
    average_goals_for(db)
    print()
    average_powerplay(db)


if __name__ == '__main__':
    main()
