import pandas as pd 
from tqdm import tqdm
import numpy as np
import plotly
import plotly.graph_objs as go
import plotly.plotly as py

## Creating a new column if the team won or not:

def map_win(x):
    #print(x)
    if x['H_V'] == 'H' and x['LABEL'] == 1:
        
        return 1
    
    elif x['H_V'] == 'V' and x['LABEL'] == 0:
        return 1
    
    else:
        return 0



def get_team_data(df, home_team, visitor_team):

	df = df[df['YEAR'] == 2019]

	## Home team:
	df_home_team = df[(df['HOME'] == home_team) | (df['VISITOR'] == home_team)]
	df_home_team = df_home_team.reset_index()

	always_cols = ['DATE', 'START', 'VISITOR', 'HOME', 'ATTEND','DAY_OF_WEEK', 'YEAR', 'LABEL']

	home_cols = ['HOME_FG%', 'HOME_3P%',
	       'HOME_FT%', 'HOME_ORB', 'HOME_DRB', 'HOME_TRB', 'HOME_AST', 'HOME_STL',
	       'HOME_BLK', 'HOME_TOV', 'HOME_PTS', 'HOME_TS%', 'HOME_eFG%',
	       'HOME_3PAr', 'HOME_FTr', 'HOME_ORB%', 'HOME_DRB%', 'HOME_TRB%',
	       'HOME_AST%', 'HOME_STL%', 'HOME_BLK%', 'HOME_TOV%', 'HOME_ORtg',
	       'HOME_DRtg']


	visitor_cols = ['VISITOR_FG%',
	       'VISITOR_3P%', 'VISITOR_FT%', 'VISITOR_ORB', 'VISITOR_DRB',
	       'VISITOR_TRB', 'VISITOR_AST', 'VISITOR_STL', 'VISITOR_BLK',
	       'VISITOR_TOV', 'VISITOR_PTS', 'VISITOR_TS%', 'VISITOR_eFG%',
	       'VISITOR_3PAr', 'VISITOR_FTr', 'VISITOR_ORB%', 'VISITOR_DRB%',
	       'VISITOR_TRB%', 'VISITOR_AST%', 'VISITOR_STL%', 'VISITOR_BLK%',
	       'VISITOR_TOV%', 'VISITOR_ORtg', 'VISITOR_DRtg']

	colums_team = ['FG%', '3P%',
       'FT%', 'ORB', 'DRB', 'TRB', 'AST', 'STL',
       'BLK', 'TOV', 'PTS', 'TS%', 'eFG%',
       '3PAr', 'FTr', 'ORB%', 'DRB%', 'TRB%',
       'AST%', 'STL%', 'BLK%', 'TOV%', 'ORtg',
       'DRtg', 'H_V']


	df_h = pd.DataFrame()
	h_v_list = []
	for i in range(len(df_home_team)):
	    if df_home_team['HOME'][i] == home_team:
	        
	        df_h = df_h.append([list(df_home_team.iloc[i][home_cols].values)])
	        h_v_list.append('H')
	    if df_home_team['VISITOR'][i] == home_team:
	        
	        df_h = df_h.append([list(df_home_team.iloc[i][visitor_cols].values)])
	        h_v_list.append('V')

	# Renaming cols:
	for i, col in enumerate(df_h.columns):
	    df_h = df_h.rename(columns={col: colums_team[i]})


	df_h.reset_index(drop=True, inplace=True)
	for col in always_cols:
   		df_h[col] = df_home_team[col]

	df_h['H_V'] = h_v_list

	df_h['WIN'] = df_h.apply(map_win, axis=1)

	df_h['NRtg'] = df_h['ORtg'] - df_h['DRtg']


   	## VISITOR team:
	df_visitor_team = df[(df['HOME'] == visitor_team) | (df['VISITOR'] == visitor_team)]
	df_visitor_team = df_visitor_team.reset_index()

	always_cols = ['DATE', 'START', 'VISITOR', 'HOME', 'ATTEND','DAY_OF_WEEK', 'YEAR', 'LABEL']

	home_cols = ['HOME_FG%', 'HOME_3P%',
	       'HOME_FT%', 'HOME_ORB', 'HOME_DRB', 'HOME_TRB', 'HOME_AST', 'HOME_STL',
	       'HOME_BLK', 'HOME_TOV', 'HOME_PTS', 'HOME_TS%', 'HOME_eFG%',
	       'HOME_3PAr', 'HOME_FTr', 'HOME_ORB%', 'HOME_DRB%', 'HOME_TRB%',
	       'HOME_AST%', 'HOME_STL%', 'HOME_BLK%', 'HOME_TOV%', 'HOME_ORtg',
	       'HOME_DRtg']


	visitor_cols = ['VISITOR_FG%',
	       'VISITOR_3P%', 'VISITOR_FT%', 'VISITOR_ORB', 'VISITOR_DRB',
	       'VISITOR_TRB', 'VISITOR_AST', 'VISITOR_STL', 'VISITOR_BLK',
	       'VISITOR_TOV', 'VISITOR_PTS', 'VISITOR_TS%', 'VISITOR_eFG%',
	       'VISITOR_3PAr', 'VISITOR_FTr', 'VISITOR_ORB%', 'VISITOR_DRB%',
	       'VISITOR_TRB%', 'VISITOR_AST%', 'VISITOR_STL%', 'VISITOR_BLK%',
	       'VISITOR_TOV%', 'VISITOR_ORtg', 'VISITOR_DRtg']

	colums_team = ['FG%', '3P%',
       'FT%', 'ORB', 'DRB', 'TRB', 'AST', 'STL',
       'BLK', 'TOV', 'PTS', 'TS%', 'eFG%',
       '3PAr', 'FTr', 'ORB%', 'DRB%', 'TRB%',
       'AST%', 'STL%', 'BLK%', 'TOV%', 'ORtg',
       'DRtg', 'H_V']


	df_v = pd.DataFrame()
	h_v_list = []
	for i in range(len(df_visitor_team)):
	    if df_visitor_team['HOME'][i] == visitor_team:
	        
	        df_v = df_v.append([list(df_visitor_team.iloc[i][home_cols].values)])
	        h_v_list.append('H')
	    if df_visitor_team['VISITOR'][i] == visitor_team:
	        
	        df_v = df_v.append([list(df_visitor_team.iloc[i][visitor_cols].values)])
	        h_v_list.append('V')

	# Renaming cols:
	for i, col in enumerate(df_v.columns):
	    df_v = df_v.rename(columns={col: colums_team[i]})


	df_v.reset_index(drop=True, inplace=True)
	for col in always_cols:
   		df_v[col] = df_visitor_team[col]

	df_v['H_V'] = h_v_list

	df_v['WIN'] = df_v.apply(map_win, axis=1)
	df_v['NRtg'] = df_v['ORtg'] - df_v['DRtg']  

	df_v['NRtgm'] = df_v['NRtg'].rolling(10).mean()

	df_v = df_v.dropna()
	df_v = df_v.drop_duplicates(subset=['DATE', 'HOME', 'VISITOR'])
   	 
	df_h['NRtgm'] = df_h['NRtg'].rolling(10).mean()

	df_h = df_h.dropna()
	df_h = df_h.drop_duplicates(subset=['DATE', 'HOME', 'VISITOR'])

   	# Create traces
	trace_home = go.Scatter(
	    x = list(df_h['DATE']),
	    y = list(df_h['NRtgm']),
	    mode = 'lines+markers',
	    name = home_team + ' NRtg'
	)
	trace_visitor = go.Scatter(
	    x = list(df_v['DATE']),
	    y = list(df_v['NRtgm']),
	    mode = 'lines+markers',
	    name = visitor_team + ' NRtg'
	)

	data = [trace_home, trace_visitor]


	layout=dict()

	fig = dict( data=data, layout=layout )
	

	fig['layout'].update(title='NET RATINGS COMPARISON:')

	return fig


def computing_home_advantage(df,window=20):
    
    df = df.reset_index()
    df['HOME_ADVANTAGE'] = 0
    
    for i in range(len(df)):
        if i<window:
            pass
        else:
            print(i)
            data = df[i-window:i]
            data_home = data[data['H_V'] == 'H' ]
            print('TOTAL GAMES PLAYED AT HOME:', len(data_home))
            
            data_visitor = data[data['H_V'] == 'V' ]
            print('TOTAL GAMES PLAYED AT VISITOR:', len(data_visitor))
            
            home_wins = Counter(data_home['WIN'])
            
            visitor_wins = Counter(data_visitor['WIN'])
            
            len_df = len(data_home)
            #print('HOME PCT WINS')
            h_w = round(home_wins[1]/len_df, 3)*100
            #print(round(home_wins[1]/len_df, 3)*100, '%')
            
            len_df = len(data_visitor)
            #print('VISITOR PCT WINS')
            v_w = round(visitor_wins[1]/len_df, 3)*100
            #print(round(visitor_wins[1]/len_df, 3)*100, '%')
            
            print('HOME ADVANTAGE:', (h_w - v_w))
            df['HOME_ADVANTAGE'][i] = (h_w - v_w)
           
            print('#####################')
        
    
    return df



def home_court_advantage(df, team):

	year = 2019


	df = df[df['YEAR'] == year]

	## Home team:
	df_home_team = df[(df['HOME'] == team )|(df['VISITOR'] == team )]
	df_home_team = df_home_team.reset_index()

	always_cols = ['DATE', 'START', 'VISITOR', 'HOME', 'ATTEND','DAY_OF_WEEK', 'YEAR', 'LABEL']

	home_cols = ['HOME_FG%', 'HOME_3P%',
	       'HOME_FT%', 'HOME_ORB', 'HOME_DRB', 'HOME_TRB', 'HOME_AST', 'HOME_STL',
	       'HOME_BLK', 'HOME_TOV', 'HOME_PTS', 'HOME_TS%', 'HOME_eFG%',
	       'HOME_3PAr', 'HOME_FTr', 'HOME_ORB%', 'HOME_DRB%', 'HOME_TRB%',
	       'HOME_AST%', 'HOME_STL%', 'HOME_BLK%', 'HOME_TOV%', 'HOME_ORtg',
	       'HOME_DRtg']


	visitor_cols = ['VISITOR_FG%',
	       'VISITOR_3P%', 'VISITOR_FT%', 'VISITOR_ORB', 'VISITOR_DRB',
	       'VISITOR_TRB', 'VISITOR_AST', 'VISITOR_STL', 'VISITOR_BLK',
	       'VISITOR_TOV', 'VISITOR_PTS', 'VISITOR_TS%', 'VISITOR_eFG%',
	       'VISITOR_3PAr', 'VISITOR_FTr', 'VISITOR_ORB%', 'VISITOR_DRB%',
	       'VISITOR_TRB%', 'VISITOR_AST%', 'VISITOR_STL%', 'VISITOR_BLK%',
	       'VISITOR_TOV%', 'VISITOR_ORtg', 'VISITOR_DRtg']

	colums_team = ['FG%', '3P%',
       'FT%', 'ORB', 'DRB', 'TRB', 'AST', 'STL',
       'BLK', 'TOV', 'PTS', 'TS%', 'eFG%',
       '3PAr', 'FTr', 'ORB%', 'DRB%', 'TRB%',
       'AST%', 'STL%', 'BLK%', 'TOV%', 'ORtg',
       'DRtg', 'H_V']


	df_h = pd.DataFrame()
	h_v_list = []
	for i in range(len(df_home_team)):
	    if df_home_team['HOME'][i] == home_team:
	        
	        df_h = df_h.append([list(df_home_team.iloc[i][home_cols].values)])
	        h_v_list.append('H')
	    if df_home_team['VISITOR'][i] == home_team:
	        
	        df_h = df_h.append([list(df_home_team.iloc[i][visitor_cols].values)])
	        h_v_list.append('V')

	# Renaming cols:
	for i, col in enumerate(df_h.columns):
	    df_h = df_h.rename(columns={col: colums_team[i]})


	df_h.reset_index(drop=True, inplace=True)
	for col in always_cols:
   		df_h[col] = df_home_team[col]

	df_h['H_V'] = h_v_list

	df_h['WIN'] = df_h.apply(map_win, axis=1)

	df_h['NRtg'] = df_h['ORtg'] - df_h['DRtg']


	data= computing_home_advantage(df_h)
	

	return data


