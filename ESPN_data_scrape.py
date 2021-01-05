'''
Script is used to reformat data from ESPN NFL stats website in the scenario where there are multi-tier column headers.
On direct table pull, 1st team name is considered a header, not value.

***THERE ARE JOINS - ONLY USE FOR URL STATED BELOW OR ELSE NEEDS TO BE MODIFIED***
'''

import urllib.request
import pandas as pd

def fix_ESPN_data(URL):
    response = urllib.request.urlopen(URL)
    df = pd.read_html(response)
    df_teams = df[0]
    df_stats = df[1]   
    
    while max(df_teams.index)<31: # loop shifts the indecies of first data set so matches df_stats
        df_teams.index += 1
    
    df_teams.loc[0] = [df_teams.columns[0]] #Sets first row team name = column header
    df_teams.rename(columns = {df_teams.columns[0]:'Team'}, inplace=True) #updates column header
    df_teams.sort_index(inplace=True)
    df = df_teams.join(df_stats,how='left') #joins on index with df_stats
    
    if 'standings' in URL:
        column_names = ['Team','Win','Loss','Tie','PCT','Home_rec','Away_rec',
                        'Div_rec','Conf_rec','PF', 'PA','DIFF','STRK']
        df.columns = column_names
        df['Team'] = df['Team'].str.extract('[A-Z]{2,}([A-Z].+)', expand=False).str.strip()
        
    else:
        column_names = ['Team','GP','Total_yds','Yds_PG','Pass_Total_Yds',
                        'Pass_Yds_PG','Rush_Total_Yds','Rush_Yds_PG',
                        'Total_pts','pts_PG']   
        df.columns = column_names
    
    df.set_index('Team', inplace=True)
    return df

off_URL = 'https://www.espn.in/nfl/stats/team/_/stat/total'
def_URL = 'https://www.espn.com/nfl/stats/team/_/view/defense'
stand_URL = 'https://www.espn.com/nfl/standings/_/group/league'

df_appendix = pd.read_excel(r'Data/NFL_Appendix.xlsx', index_col=0, engine="openpyxl")

df_offense = fix_ESPN_data(off_URL)
df_defense = fix_ESPN_data(def_URL)
df_standings = fix_ESPN_data(stand_URL)

df = df_offense.join(df_defense, lsuffix='_off', rsuffix='_def')
df = df.join(df_standings)
df = df.join(df_appendix).reset_index()

df.to_csv(r'Data/ESPN_Data.csv')