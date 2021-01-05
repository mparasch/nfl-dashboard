# -*- coding: utf-8 -*-
"""
Created on Sat Dec 12 16:16:13 2020

@author: Matt
"""

import pandas as pd
import urllib.request

def gameStats_scrape(team_abbrv):
    column_names = ['Week', 'Day', 'Date', 'Time', 'Boxscore', 'W/L', 'OT', 'Record',
                    '@', 'Opponent', 'Team_score', 'Opp_score', 'off_1stD', 'off_TotYd',
                    'off_PassY', 'off_RushY', 'off_TO', 'def_1stD', 'def_TotYd', 
                    'def_PassY', 'def_RushY', 'def_TO', 'expect_off', 'expect_def', 
                    'expect_specTeam']
    URL = r'https://www.pro-football-reference.com/teams/'
    path = team_abbrv + r'/2020.htm'
    response = urllib.request.urlopen(URL+path)
    dfs = pd.read_html(response)
    df = dfs[1]
    df.rename(columns='_'.join, inplace=True)
    df.columns = df.columns.map('_'.join)
    for i, col in enumerate(df.columns):
        df.rename(columns = {col:column_names[i]}, inplace=True)
    df.drop(['Boxscore', 'expect_off', 'expect_def', 'expect_specTeam'], axis = 1, inplace=True)
    df.insert(0, 'Team_abbrv', team_abbrv)
    df.sort_values(by='Week', inplace=True)
    df['pts_diff'] = df['Team_score'] - df['Opp_score']
    df['r3_team_score'] = df['Team_score'].rolling(window=3, min_periods=1).mean()
    df['r3_opp_score'] = df['Opp_score'].rolling(window=3, min_periods=1).mean()
    df['r3_pts_diff'] = df['pts_diff'].rolling(window=3, min_periods=1).mean()
    df['r3_off_TotYd'] = df['off_TotYd'].rolling(window=3, min_periods=1).mean()
    df['r3_def_TotYd'] = df['def_TotYd'].rolling(window=3, min_periods=1).mean()
    return df

df_appendix = pd.read_excel(r'Data/NFL_Appendix.xlsx', 'Sheet1', index_col = None, engine="openpyxl")

column_names = ['Team_abbrv','Week', 'Day', 'Date', 'Time', 'W/L', 'OT', 'Record', 
                '@', 'Opponent', 'Team_score', 'Opp_score', 'off_1stD', 'off_TotYd',
                'off_PassY', 'off_RushY', 'off_TO', 'def_1stD', 'def_TotYd', 'def_PassY',
                'def_RushY', 'def_TO', 'pts_diff', 'r3_team_score', 'r3_opp_score', 
                'r3_pts_diff', 'r3_off_TotYd', 'r3_def_TotYd']

df_games = pd.DataFrame(columns = column_names)

for i in df_appendix['pro_ref']:
    df_games = pd.concat([df_games, gameStats_scrape(i)])

df_games2 = df_games.merge(df_appendix, how='left', left_on='Team_abbrv', right_on='pro_ref')

df_games2.drop(['Primary', 'Secondary', 'Tertiary', 'pro_ref'], axis=1, inplace=True)

df_games2 = df_games2[['Team','Team_abbrv', 'Week', 'Day', 'Date', 'Time', 
                       'W/L', 'OT', 'Record', '@',
                       'Opponent', 'Team_score', 'Opp_score', 'off_1stD', 'off_TotYd',
                       'off_PassY', 'off_RushY', 'off_TO', 'def_1stD', 'def_TotYd',
                       'def_PassY', 'def_RushY', 'def_TO','pts_diff', 'r3_team_score',
                       'r3_opp_score', 'r3_pts_diff', 'r3_off_TotYd', 'r3_def_TotYd',
                       'Conference', 'Division']]

# 12/14/2020 Updates

df = df_games2.copy()

df.dropna(axis=0, subset=['Team_score'], how='any', inplace=True)

def Update_date(x):
    return str(x) + ', 2020'

df['Date'] = df['Date'].apply(lambda x: Update_date(x))

df['Date'] = pd.to_datetime(df['Date']).dt.date

df.sort_values(by='Date', ascending=True, inplace=True)

def Update_WL(x):
    if x=='W':
        return int(1)
    elif x=='L':
        return int(0)
    
df['W/L'] = df['W/L'].apply(lambda x: Update_WL(x))

df['off_TO'].fillna(0, inplace=True)
df['def_TO'].fillna(0, inplace=True)

def Home_Away(x):
    if x=='@':
        return 'Away'
    else:
        return 'Home'
    
df['Loc'] = df['@'].apply(lambda x: Home_Away(x))

df.drop(['@', 'OT', 'Team_abbrv'], axis=1, inplace=True)

pd.set_option('display.max_columns', None)

# Export new Format
df.to_csv('Data/gameData.csv')

# Export old Format
# df_games2.to_csv('gameData.csv')