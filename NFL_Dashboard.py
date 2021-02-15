import pandas as pd
import plotly.express as px
import dash
import dash_core_components as dcc
import dash_html_components as html
from ESPN_data_scrape import fix_ESPN_data
from dash.dependencies import Input, Output
from plotly.subplots import make_subplots
import plotly.graph_objects as go

app = dash.Dash(__name__)

colors = {'background': '#292d36',
          'text': '#7FDBFF',
          'title': '#dfe7f7',
          'white':'#ffffff'
         }

font = {'title':'Franklin Gothic',
        'text':'Arial'
        }

scores_style = {'font-family':'Arial', 
          'fontSize':'20pt',
          'color':colors['title'],
          'display':'inline-block',
          'width':'30.75vw',
          'textAlign':'center',
          'margin':'10px',
          'padding':'0px',
          'left-padding':'10vw'
        }

stats_style = {'vertical-align':'top',
          'font-family':'Arial', 
          'font-style':'italic',
          'fontSize':'18pt',
          'color':colors['title'],
          'display':'inline-block',
          'width':'32vw',
          'textAlign':'center',
          'margin-top':'3vw',
          'padding':'0px',
          'left-padding':'10vw'
          }

dropdown_style = {'fontSize':'12pt',
          'color':'black',
          'display':'inline-block',
          'width':'30.75vw',
          'textAlign':'center',
          'padding-top':'0px',
          'top-margin':'0px',
          'margin':'10px',
          'font-family':font['text'],
          'align-items':'center'
          }

label_style = {'fontSize':'14pt',
          'color':colors['white'],
          'display':'inline-block',
          'width':'22.5vw',
          'textAlign':'center',
          'padding-top':'0px',
          'top-margin':'0px',
          'margin':'10px',
          'font-family':font['text'],
          'align-items':'center'
          }

dropdown_style2 = {'fontSize':'12pt',
          'color':'black',
          'display':'inline-block',
          'width':'22.5vw',
          'textAlign':'center',
          'padding-top':'0px',
          'top-margin':'0px',
          'margin':'10px',
          'font-family':font['text'],
          'align-items':'center'
          }

off_URL = 'https://www.espn.in/nfl/stats/team/_/stat/total'
def_URL = 'https://www.espn.com/nfl/stats/team/_/view/defense'
stand_URL = 'https://www.espn.com/nfl/standings/_/group/league'

df_appendix = pd.read_excel(r'Data/NFL_Appendix.xlsx', index_col=0, engine="openpyxl")

df_offense = fix_ESPN_data(off_URL)
df_defense = fix_ESPN_data(def_URL)
df_standings = fix_ESPN_data(stand_URL)

df_1 = df_offense.join(df_defense, lsuffix='_off', rsuffix='_def')
df_1 = df_1.join(df_standings)
df_1 = df_1.join(df_appendix).reset_index()
df_1['pts_diff'] = df_1['pts_PG_off']  - df_1['pts_PG_def']
df_1.sort_values(by='Team', inplace=True)

df_gameData = pd.read_csv(r'Data/gameData.csv', index_col = 0)

df_gameData = df_gameData[df_gameData['Team_score'].notna()]

df_gameData.sort_values(by='Week', inplace=True)

games_num_col = [x for x in df_gameData.columns if df_gameData[x].dtypes in ['int64', 'float64']]

app.layout = html.Div(id='uppderDiv', style={'backgroundColor':colors['background']},children=[
        html.H1(children='NFL Dashboard',
                style={
                    'textAlign':'center',
                    'color':colors['title'],
                    'font-family':font['title'],
                    'fontSize':'30pt'
                        }),
        
        html.Div([html.H3(children='Matchup Compairson Tool',
                 style={
                    'textAlign':'center',
                    'color':colors['title'],
                    'font-family':font['text'],
                    'font-style':'italic',
                    'padding-bottom':'0px',
                    'bottom-margin':'0px'
                    })
                 ]),

        dcc.Dropdown(id='Team_1', options=[{'label':x, 'value' :x} for x in df_1['Team'].unique()],
                                           style= dropdown_style, value='Green Bay Packers', multi=False
                    ),
                        
        html.P(style= dropdown_style),
        
        dcc.Dropdown(id='Team_2', options=[{'label':x, 'value' :x} for x in df_1['Team'].unique()],
                                           style= dropdown_style, value='Chicago Bears', multi=False
                    ),
        
        html.Div(children=[html.P(style={'display':'inline-block','width':'5px'}),
                           html.P(id='t1Score',style=scores_style),
                           html.P(id='totalScore',style=scores_style),
                           html.P(id='t2Score',style=scores_style)]
                ),
        
        html.P(id='t1Stats',
                  style = stats_style),
        
        dcc.Graph(id='Total_Points',
                  style={'width':'30vw', 'display':'inline-block'}),
            
        html.P(id='t2Stats',
                  style= stats_style),
        
        html.P('Y axis', style = label_style
                    ),
                                             
        dcc.Dropdown(id='line_y_axis', options=[{'label':x, 'value':x} for x in games_num_col if x[:2]=='r3'],
                            style = dropdown_style2, value = 'r3_pts_diff'
                    ),
        
        dcc.Graph(id='rolling_line'),
        
        html.H2('Dynamic Scatter Plot',
                style={
                    'textAlign':'center',
                    'color':colors['title'],
                    'font-family':font['title'],
                    'fontSize':'30pt'
                        }),

        html.P('Conference Filter',style = label_style
                    ),
                                              
        html.P('Division Filter', style = label_style
                    ),
                                             
        html.P('X axis', style = label_style
                    ),
        
        html.P('Y axis', style = label_style
                    ),
               
        dcc.Dropdown(id='conference',options=[{'label':x, 'value':x} for x in df_gameData['Conference'].unique()],
                            style = dropdown_style2, placeholder='Select a Conference...', multi=True
                    ),
                                              
        dcc.Dropdown(id='division',options=[{'label':x, 'value':x} for x in df_gameData['Division'].unique()],
                            style = dropdown_style2, placeholder='Select a Division...', multi=True
                    ),
                                             
        dcc.Dropdown(id='x_axis', options=[{'label':x, 'value':x} for x in games_num_col],
                             style = dropdown_style2, value = 'Opp_score'        
                    ),
        
        dcc.Dropdown(id='y_axis', options=[{'label':x, 'value':x} for x in games_num_col],
                            style = dropdown_style2, value = 'Team_score'
                    ),
                     
        dcc.Graph(id='scatter')
])

@app.callback(
        Output('Total_Points', 'figure'),
        [Input('Team_1', 'value'),
         Input('Team_2', 'value')]
        )
def update_graph(Team_1, Team_2):
    l = [Team_1, Team_2]
    df = df_1[df_1['Team'].isin(l)]
    if l[0] != l[1]:
        df['Team'] = pd.Categorical(df['Team'], [Team_1, Team_2])
        df.sort_values(by='Team', inplace=True)
    fig = make_subplots(rows=1, cols=1, shared_xaxes=True)
    fig.add_trace(
        go.Bar(x=df['Team'],y=df['pts_PG_off'], marker={'color':df['Primary']},name='Pts per game',
               textfont={'color':colors['text']}), row=1, col=1)
        
    fig.add_trace(
        go.Scatter(x=df['Team'],y=df['pts_PG_def'], name='Pts allowed per game',
                   textfont={'color':colors['text']}), row=1, col=1)
    
    fig.add_trace(
        go.Bar(x=df['Team'], y=df['pts_diff'], marker={'color':df['Secondary']},name='Point Differential',
                   textfont={'color':colors['text']}), row=1, col=1)
    
    fig.update_layout(title_text="Points For vs. Points Allowed", hovermode='x unified', barmode='relative', showlegend=False,
                      font_color = colors['white'], title_font_color = colors['white'], legend_title_font_color=colors['white'])
    fig.layout.plot_bgcolor = colors['background']
    fig.layout.paper_bgcolor = colors['background']
    return fig

@app.callback(
        [Output('t1Score', 'children'),
         Output('t2Score', 'children'),
         Output('totalScore','children')],
        [Input('Team_1', 'value'),
         Input('Team_2', 'value')]
        )
def updateText(Team_1, Team_2):
    l = [Team_1, Team_2]
    df = df_gameData[df_gameData['Team'].isin(l)]
    t1_df = df[df['Team']==Team_1]
    t1_df = t1_df[t1_df['Week']==t1_df['Week'].max()]
    t2_df = df[df['Team']==Team_2]
    t2_df = t2_df[t2_df['Week']==t2_df['Week'].max()]
    t1_pts = int(round(((t1_df.iloc[0]['r3_team_score'] + t2_df.iloc[0]['r3_opp_score'])/2)))
    t2_pts = int(round(((t2_df.iloc[0]['r3_team_score'] + t1_df.iloc[0]['r3_opp_score'])/2)))
    total_pts = t1_pts + t2_pts
    t1_txt = [str(Team_1), html.Br(), str(t1_pts)]
    t2_txt = [str(Team_2), html.Br(), str(t2_pts)]
    total_txt = ['Total Points', html.Br(), str(total_pts)]
    return [t1_txt, t2_txt, total_txt]

@app.callback(
        [Output('t1Stats','children'),
         Output('t2Stats','children')],
         [Input('Team_1', 'value'),
          Input('Team_2', 'value')]
         )
def update_stats(Team_1, Team_2):
    l = [Team_1, Team_2]
    df = df_1[df_1['Team'].isin(l)]
    df['pts_diff'] = df['pts_PG_off']  - df['pts_PG_def']
    t1_df = df[df['Team']==Team_1]
    t2_df = df[df['Team']==Team_2]
    t1_record = '{}-{}-{}'.format(str(t1_df.iloc[0]['Win']), str(t1_df.iloc[0]['Loss']), str(t1_df.iloc[0]['Tie']))
    t2_record = '{}-{}-{}'.format(str(t2_df.iloc[0]['Win']), str(t2_df.iloc[0]['Loss']), str(t2_df.iloc[0]['Tie']))
    t1_streak = str(t1_df.iloc[0]['STRK'])
    t2_streak = str(t2_df.iloc[0]['STRK'])
    return [[html.Br(), html.Br(), 'Record: ' + t1_record, html.Br(), html.Br() , 'Streak: ' + t1_streak],
            [html.Br(), html.Br(), 'Record: ' + t2_record, html.Br(), html.Br()
             , 'Streak: ' + t2_streak]]

@app.callback(
        Output('scatter', 'figure'),
        [Input('conference', 'value'),
         Input('division', 'value'),
         Input('x_axis', 'value'),
         Input('y_axis', 'value')])
def update_scatter(conference, division, x_axis, y_axis):
    if conference:
        if type(conference)!=list:
            conference = list(conference)
        df = df_gameData[df_gameData['Conference'].isin(conference)]
    else:
        df = df_gameData
    if division:
        if type(division)!=list:
            division = list(division)
        df = df[df['Division'].isin(division)]
    fig = px.scatter(df, x=x_axis, y=y_axis, color=df['Team'], size='Team_score', hover_name='Team',
                     animation_frame='Week', animation_group='Team')
    fig.update_layout(title_text=str(x_axis) + ' vs ' + str(y_axis), hovermode='closest', showlegend=True,
                      font_color = colors['white'], title_font_color = colors['white'], legend_title_font_color=colors['white'],
                      xaxis_range=[df[x_axis].min(axis=0), df[x_axis].max(axis=0)*1.1], yaxis_range=[df[y_axis].min(axis=0), df[y_axis].max(axis=0)*1.1])
    fig.update_layout(transition = {'duration': 1000})
    fig.layout.plot_bgcolor = colors['background']
    fig.layout.paper_bgcolor = colors['background']
    return fig

@app.callback(
        Output('rolling_line', 'figure'),
        [Input('line_y_axis', 'value'),
         Input('Team_1', 'value'),
         Input('Team_2', 'value')])
def update_linegraph(line_y_axis, Team_1, Team_2):
    l = [Team_1, Team_2]
    df = df_gameData[df_gameData['Team'].isin(l)].sort_values(by='Date', ascending=True)
    label = str(line_y_axis)
    fig = px.line(df, x='Week', y=line_y_axis, color=df['Team'],
                  custom_data=['Week','Team','Team_score','Opponent','Opp_score',line_y_axis])
    fig.update_layout(title_text=str(line_y_axis), hovermode='x unified', showlegend=True,
                      font_color = colors['white'], title_font_color = colors['white'], legend_title_font_color=colors['white'])
    fig.layout.plot_bgcolor = colors['background']
    fig.layout.paper_bgcolor = colors['background']
    fig.update_traces(mode='lines+markers', hovertemplate="<br>".join([
        " %{customdata[2]}",
        "%{customdata[3]}: %{customdata[4]}",
        "Value: %{customdata[5]}"
    ]))
    return fig

if __name__ == '__main__':
    app.run_server(debug=True)