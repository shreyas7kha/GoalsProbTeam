import requests
from bs4 import BeautifulSoup as soup
import json
import pandas as pd
import numpy as np
import random
from collections import Counter

# COMPLEMENTARY COLOR
def complementaryColor(my_hex):
    if my_hex[0] == '#':
        my_hex = my_hex[1:]
    rgb = (my_hex[0:2], my_hex[2:4], my_hex[4:6])
    comp = ['%02X' % (255 - int(a, 16)) for a in rgb]
    return '#'+''.join(comp)

# DATA SCRAPING
cols = ['match_id', 'x', 'y', 'minute', 'player', 'player_id', 'result', 'xg', 'team', 'h_a',
       'situation', 'season', 'player_assist', 'last_action', 'shot_type']
cookies = {"beget" : "begetok"}

def scrap_understat_match(idx, home_away='h'):
    base_url = 'https://understat.com/match/'
    url = base_url+str(idx)
    
    req = requests.get(url, cookies=cookies)
    parse_soup = soup(req.content, 'lxml')
    scripts = parse_soup.find_all('script')
    strings = scripts[1].string
    ind_start = strings.index("('")+2
    ind_end = strings.index("')")

    json_data = strings[ind_start:ind_end]
    json_data = json_data.encode('utf8').decode('unicode_escape')

    data = json.loads(json_data)
    
    data = data[home_away]
        
    match_id = []
    x = []
    y = []
    xg = []
    team = []
    minute = []
    result = []
    player = []
    player_id = []
    situation = []
    season = []
    player_assist = []
    last_action = []
    shot_type = []
    h_a = []
    
    for index in range(len(data)):
        for key in data[index]:
            if key=='match_id':
                match_id.append(data[index][key])
            if key=='X':
                x.append(data[index][key])
            if key=='Y':
                y.append(data[index][key])
            if key=='xG':
                xg.append(data[index][key])
            if key==home_away+'_team':
                team.append(data[index][key])
            if key=='minute':
                minute.append(data[index][key])
            if key=='result':
                result.append(data[index][key])
            if key=='player':
                player.append(data[index][key])
            if key=='player_id':
                player_id.append(data[index][key])
            if key=='situation':
                situation.append(data[index][key])
            if key=='season':
                season.append(data[index][key])
            if key=='player_assisted':
                player_assist.append(data[index][key])
            if key=='lastAction':
                last_action.append(data[index][key])
            if key=='shotType':
                shot_type.append(data[index][key])
                h_a.append(home_away)
                
    df = pd.DataFrame([match_id, x, y, minute, player, player_id, result, xg, team, h_a, situation,
                       season, player_assist, last_action, shot_type], index=cols)
    df = df.T
    df = df.apply(pd.to_numeric, errors='ignore')
    
    return df

def scrap_main_func(team, season, opp_data = True):
    if len(team.split())==1: 
        url = 'https://understat.com/team/'+team+'/'+str(season)
    else:
        url = 'https://understat.com/team/'+'_'.join(team.split())+'/'+str(season)
        
    req = requests.get(url, cookies=cookies)
    parse_soup = soup(req.content, 'lxml')
    league = parse_soup.find_all('a')[-8].string
    scripts = parse_soup.find_all('script')
        
    strings = scripts[1].string
    ind_start = strings.index("('")+2
    ind_end = strings.index("')")

    json_data = strings[ind_start:ind_end]
    json_data = json_data.encode('utf8').decode('unicode_escape')

    data = json.loads(json_data)
    
    df = pd.DataFrame(columns=cols)
    
    for i, match in enumerate(data):
        match_id = match['id']
        home_away = match['side']
        opposition = ['h','a']
        opposition.remove(home_away)
        df_opp = pd.DataFrame(columns=cols)
        
        print('Match no: {}, match id: {} is loading'.format(i+1, match_id))
        print('--------------------')
        
        try:
            df_match = scrap_understat_match(match_id, home_away)
            if opp_data:
                df_opp = scrap_understat_match(match_id, opposition[0])
            df = pd.concat([df, df_match, df_opp])
        except: 
            pass
    
    return league, df.reset_index()

def xG_data_team(team, season):
    if len(team.split())==1: 
        url = 'https://understat.com/team/'+team+'/'+str(season)
    else:
        url = 'https://understat.com/team/'+'_'.join(team.split())+'/'+str(season)
        
    req = requests.get(url)
    parse_soup = soup(req.content, "lxml")
    scripts = parse_soup.find_all('script')
        
    strings = scripts[2].string
    ind_start = strings.index("('")+2
    ind_end = strings.index("')")

    json_data = strings[ind_start:ind_end]
    json_data = json_data.encode('utf8').decode('unicode_escape')
    data = json.loads(json_data)
    
    shots_for, xG_for, shots_against, xG_against = 0,0,0,0
    for sit in data['situation']:
        if sit != 'Penalty':
            shots_for += data['situation'][sit]['shots']
            xG_for += data['situation'][sit]['xG']
            shots_against += data['situation'][sit]['against']['shots']
            xG_against += data['situation'][sit]['against']['xG']

    return shots_for, xG_for, shots_against, xG_against

def league_team_data(league, season):
    base_url = 'https://understat.com/league/'
    url = base_url+str('_'.join(league.split()))+'/'+str(season)
    
    req = requests.get(url)
    parse_soup = soup(req.content, "lxml")
    scripts = parse_soup.find_all('script')
    strings = scripts[2].string

    ind_start = strings.index("('")+2
    ind_end = strings.index("')")

    json_data = strings[ind_start:ind_end]
    json_data = json_data.encode('utf8').decode('unicode_escape')

    data = json.loads(json_data)
    
    teams = []
    team_90s = []
    for x in data:
        teams.append(data[x]['title'])
        team_90s.append(len(data[x]['history']))
        
    cols = ['Team', 'Shots For', 'xG For', 'Shots Against', 'xG Against']
    df = pd.DataFrame(columns = cols)

    for team in teams:
        shots_for, xG_for, shots_against, xG_against = xG_data_team(team, season)
        df = pd.concat([df, pd.DataFrame(np.array([[team, shots_for, xG_for, shots_against, xG_against]]),
                                        columns=cols)])
    
    df = df.reset_index(drop=True)
    df['90s'] = team_90s
    df = df.apply(pd.to_numeric, errors='ignore')
    
    return df

# OTHER FUNCS
def goals_prob(arr):
    goals = 0
    for xg in arr:
        if random.random() < xg:
            goals+=1
    return goals

# FILTER THE DICTS BASED ON SIGNIFICANCE
def check_limit(goals, tot_goals_scored, most_goals_scored, tot_goals_conceded, most_goals_conceded, own_team=True):
    if own_team:
        if tot_goals_scored < most_goals_scored and goals < most_goals_scored:   
            return (goals >= tot_goals_scored) 
        elif tot_goals_scored > most_goals_scored and goals > most_goals_scored:
            return goals <= tot_goals_scored
        return False
    else:
        if tot_goals_conceded < most_goals_conceded and goals < most_goals_conceded:
            return goals >= tot_goals_conceded
        elif tot_goals_conceded > most_goals_conceded and goals > most_goals_conceded:
            return goals <= tot_goals_conceded
        return False

def process_data(df, team_name):
    tot_goals_scored = sum(df[df['team']==team_name]['result']=='Goal') + sum(df[df['team']!=team_name]['result']=='OwnGoal')
    tot_goals_conceded = sum(df[df['team']!=team_name]['result']=='Goal') + sum(df[df['team']==team_name]['result']=='OwnGoal')
    matches = df['match_id'].nunique()
    df_fil = df[df['result']!='OwnGoal']

    # RUNNING THE SHOT SIMULATIONS
    shots_team = df_fil[df_fil['team']==team_name]['xg'].tolist()
    shots_opp = df_fil[df_fil['team']!=team_name]['xg'].tolist()
    no_simulations = 100000
    team_goals = []
    opp_goals = []

    for i in range(no_simulations):
        goals_team = goals_prob(shots_team)
        team_goals.append(goals_team)
        goals_opp = goals_prob(shots_opp)
        opp_goals.append(goals_opp)
    
    dic_team = dict(Counter(team_goals))
    dic_opp = dict(Counter(opp_goals))

    total_prob_scored = 0
    total_prob_conceded = 0
    for i in range(tot_goals_scored, max(dic_team.keys())+1):
        try:
            total_prob_scored += dic_team[i]*100/no_simulations
        except: pass
    for i in range(min(dic_opp.keys()), tot_goals_conceded+1):
        try:
            total_prob_conceded += dic_opp[i]*100/no_simulations
        except: pass

    # MAX OCCURENCE oF GOALS SCORED AND CONCEDED
    most_goals_scored = list(dict(sorted(dic_team.items(),key=lambda x:x[1], reverse=True)).keys())[0] 
    most_goals_conceded = list(dict(sorted(dic_opp.items(),key=lambda x:x[1], reverse=True)).keys())[0]

    # SELECTING THRESHOLD AND FILTERING DICTIONARIES
    THRESHOLD = 0.001

    dic_team = {d:x for d,x in dic_team.items() if (x>no_simulations*THRESHOLD) | check_limit(d, tot_goals_scored, 
                                                                                            most_goals_scored, tot_goals_conceded, 
                                                                                            most_goals_conceded)}
    dic_team = dict(sorted(dic_team.items(), key=lambda x:x[0]))
    dic_opp = {d:x for d,x in dic_opp.items() if (x>no_simulations*THRESHOLD) | check_limit(d, tot_goals_scored,
                                                                                            most_goals_scored, tot_goals_conceded, 
                                                                                            most_goals_conceded, False)}
    dic_opp = dict(sorted(dic_opp.items(), key=lambda x:x[0]))

    # FINDING VARIOUS PARAMETERS
    least_goals_scored = min(dic_team.keys()) # LEAST GOALS SCORED ACCORDING TO SIM
    max_goals_scored = max(dic_team.keys()) # MOST GOALS SCORED ACCORDING TO SIM

    least_goals_conceded = min(dic_opp.keys())
    max_goals_conceded = max(dic_opp.keys())

    max_prob_scored = dic_team[most_goals_scored]*100/no_simulations # MAX PROBABILITY OF GOALS SCORED
    max_prob_conceded = dic_opp[most_goals_conceded]*100/no_simulations # MAX PROBABILITY OF GOALS CONCEDED

    # DEFINING VIZ VARIABLES
    shots_team_p90 = len(shots_team)/matches
    shots_opp_p90 = len(shots_opp)/matches
    xg_pshot_for = sum(shots_team)/len(shots_team)
    xg_pshot_against = sum(shots_opp)/len(shots_opp)
    xg_for_p90 = sum(shots_team)/matches
    xg_against_p90 = sum(shots_opp)/matches

    return (tot_goals_scored, tot_goals_conceded, matches, dic_team, dic_opp, total_prob_scored, total_prob_conceded, most_goals_scored,
            most_goals_conceded, least_goals_scored, least_goals_conceded, max_goals_scored, max_goals_conceded, max_prob_scored, 
            max_prob_conceded, shots_team_p90, shots_opp_p90, xg_pshot_for, xg_pshot_against, xg_for_p90, xg_against_p90, no_simulations,
            shots_team, shots_opp)

def process_league_data(df_leagues, team):
    # FINDING LEAGUE RANKS - DESCENDING IN FOR VALUES, ASCENDING IN AGAINST VALUES
    df_leagues['Shots For Rank'] = (df_leagues['Shots For']/df_leagues['90s']).rank(ascending=False)
    df_leagues['xG For Rank'] = (df_leagues['xG For']/df_leagues['90s']).rank(ascending=False)
    df_leagues['xG Per Shot Rank'] = (df_leagues['xG For']/df_leagues['Shots For']).rank(ascending=False)
    df_leagues['Shots Against Rank'] = (df_leagues['Shots Against']/df_leagues['90s']).rank()
    df_leagues['xG Against Rank'] = (df_leagues['xG Against']/df_leagues['90s']).rank()
    df_leagues['xG Per Shot Against Rank'] = (df_leagues['xG Against']/df_leagues['Shots Against']).rank()

    # FINDING EXACT TEAM RANKS
    team_idx = df_leagues[df_leagues['Team']==team].index

    team_ranks = np.array(df_leagues.loc[team_idx, :])[0][-6:].tolist() # TAKING LAST 6 ROWs FOR DATA 
    team_ranks = list(map(int, team_ranks))

    return team_ranks

def suffix_def(i):
    return 'th' if 11<=i<=13 else {1:'st',2:'nd',3:'rd'}.get(i%10, 'th')