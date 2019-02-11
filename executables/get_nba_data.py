import requests
from bs4 import BeautifulSoup
import pandas as pd
import datetime
import numpy as np
from collections import Counter

def map_dates(x):

	dict_months = {'Oct': 10, 'Nov': 11, 'Dec': 12, 'Jan': 1, 'Feb': 2, 'Mar': 3, \
	               'Apr': 4, 'May': 5, 'Jun': 6}


	year = x.split(', ')[-1]
	month = dict_months[date.split(' ')[1]]
	day = date.split(' ')[2].split(',')[0]
	whole_date = str(year) + '-' + str(month) + '-' + str(day)
	try:
		dt = datetime.datetime.strptime(whole_date, '%Y-%m-%d')
	except:
		dt = ''
	return df

def map_day_of_the_week(x):

	dict_day_of_the_week = {'Mon': 1, 'Tue': 2, 'Wed': 3, 'Thu': 4, 'Fri': 5, 'Sat': 6, 'Sun': 7,}

	day_of_the_week = dict_day_of_the_week[x.split(' ')[0].split(',')[0]]
    
	return day_of_the_week


def map_year(x):
   
    month = x.month
    
    if month in [10, 11, 12]:
        
        year = x.year +1
        
        return year
    if month in [1, 2, 3, 4, 5, 6]:
    
        year = x.year
        
        return year



def get_table_from_url(url):

        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'lxml')
        table = soup.find_all('table')[-1]

        with open('../data/example.html', 'w') as f:
            f.write(str(table))
            f.close()

        df = pd.read_html('../data/example.html',header=0, index_col = 0)[0]

        df = df.reset_index()
        df = df.drop(['Â.1', 'Â'], axis = 1)
        df = df.rename(columns={'Date' : 'DATE', 'PTS.1': 'PTS', 'Visitor/Neutral' : 'VISITOR', 'Home/Neutral' : 'HOME', 'Start (ET)': 'START', 'Attend.': 'ATTEND', 'Notes': 'NOTES'})

        return df

def get_tables_from_url(url):

        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'lxml')
        tables = soup.find_all('table')

        df_list = []

        for table in tables:

	        with open('../data/example.html', 'w') as f:
	            f.write(str(table))
	            f.close()

	        df = pd.read_html('../data/example.html',header=1, index_col = 0)[0]

	        df_list.append(df.iloc[-1])

        return df_list


def get_all_links(url):
	list_links = []
	response = requests.get(url)
	soup = BeautifulSoup(response.text, 'lxml')
	links = soup.find('table').find_all('td', attrs={'data-stat': 'box_score_text'})
	for link in links:
		try:
			new_url = link.find('a')
			#print('https://www.basketball-reference.com' +new_url['href'])
			list_links.append('https://www.basketball-reference.com' +new_url['href'])
		except:
			pass

	return list_links


def get_all_info_match(url):
	## Getting now match data...

	df_list = get_tables_from_url(url)

	#print(df_list)
	df_tot = pd.DataFrame()

	for i, df_item in enumerate(df_list):

		
		#print('I', i)
		#print(df_item.iloc[len(df_item)-1])
		df_row = pd.DataFrame(df_item)
		df_row = df_row.T
		df_row = df_row.reset_index(drop=True)
		#print('DF_ITEM:')
		#print(df_row)

		## renaming cols:
		if i == 0:

			for col in df_row.columns:

				df_row = df_row.rename(columns={col: 'VISITOR_'+col})
			#print('DF_ROW:')
			#print(df_row)
			df_tot = pd.concat([df_tot, df_row], axis=1)

		elif i == 1:

			for col in df_row.columns:

				df_row = df_row.rename(columns={col: 'VISITOR_'+col})
			df_row = df_row.drop('VISITOR_MP', axis =1)
			#print('DF_ROW:')
			#print(df_row)
			df_tot = pd.concat([df_tot, df_row], axis=1)

		elif i == 2:

			for col in df_row.columns:

				df_row = df_row.rename(columns={col: 'HOME_'+col})
			#print('DF_ROW:')
			#print(df_row)
			df_tot = pd.concat([df_tot, df_row], axis=1)

		elif i ==3:

			for col in df_row.columns:

				df_row = df_row.rename(columns={col: 'HOME_'+col})
			df_row = df_row.drop('HOME_MP', axis =1)
			#print('DF_ROW:')
			#print(df_row)
			df_tot = pd.concat([df_tot, df_row], axis=1)


	return df_tot


def get_nba_data(url):

	#df = pd.DataFrame()

	df = get_table_from_url(url)

	list_links = get_all_links(url)

	df_info = pd.DataFrame()

	for link in list_links:
		info = get_all_info_match(link)

		df_info =  df_info.append(info)


	df_info = df_info.reset_index(drop=True)


	df = pd.concat([df, df_info], axis=1)


	return df


def get_months(url, selected_month):

	list_months = []
	response = requests.get(url)
	soup = BeautifulSoup(response.text, 'lxml')
	links = soup.find('div', class_='filter').find_all('a')

	for link in links:

		#print('https://www.basketball-reference.com/'+link['href'])
		list_months.append('https://www.basketball-reference.com/'+link['href'])

	list_final_month = []
	for month in list_months:
		if selected_month in  month:
			list_final_month.append(month)
	return list_final_month


def get_seasons(season_ini,season_end):


	list_seasons = []
	for i in range(season_ini,season_end):

		#print('https://www.basketball-reference.com/leagues/NBA_201'+str(i)+'_games.html')
		list_seasons.append('https://www.basketball-reference.com/leagues/NBA_201'+str(i)+'_games.html')


	return list_seasons


def get_season(season):


	list_seasons = []
	
	list_seasons.append('https://www.basketball-reference.com/leagues/NBA_'+str(season)+'_games.html')


	return list_seasons


def nba(selected_season, selected_month, file_name):

	df = pd.DataFrame()

	list_seasons = get_season(selected_season)

	for season in list_seasons:

		print('SEASON:')
		print(season)

		list_months = get_months(season, selected_month)

		df_season = pd.DataFrame()

		for i, month in enumerate(list_months):
			
			print('MONTH:')
			print(month)

			if i == 0:
				df_month = get_nba_data(month)
				#df_month.to_csv('nba_data_seasons_02_10.csv')
			
			else:
				try:
					df_month = get_nba_data(month)
					#df_month.to_csv('nba_data_seasons_02_10.csv', mode='a', header=False)
				except:
					pass

			try:
				df_season = df_season.append(df_month)
			except:
				pass
			
		print('######################')

		df = df.append(df_season)

	df = df[df['HOME_MP'].notnull()]

	print('A first look at the dataframe:')
	print(df.head())
	print('Total Lenght:')
	print(len(df))
	
	return df

def update_db(selected_season = '2019', selected_month = 'february', file_name = 'nba_all'):

	df = nba(selected_season, selected_month, file_name)
	df.reset_index(drop=True, inplace=True)
	df = df.drop('NOTES', axis=1)
	#print(df.columns)
	df.columns = ['DATE', 'START', 'VISITOR', 'PTS', 'HOME', 'PTS.1', 'ATTEND',
	       'VISITOR_MP', 'VISITOR_FG', 'VISITOR_FGA', 'VISITOR_FG%', 'VISITOR_3P',
	       'VISITOR_3PA', 'VISITOR_3P%', 'VISITOR_FT', 'VISITOR_FTA',
	       'VISITOR_FT%', 'VISITOR_ORB', 'VISITOR_DRB', 'VISITOR_TRB',
	       'VISITOR_AST', 'VISITOR_STL', 'VISITOR_BLK', 'VISITOR_TOV',
	       'VISITOR_PF', 'VISITOR_PTS', 'VISITOR_+/-', 'VISITOR_TS%',
	       'VISITOR_eFG%', 'VISITOR_3PAr', 'VISITOR_FTr', 'VISITOR_ORB%',
	       'VISITOR_DRB%', 'VISITOR_TRB%', 'VISITOR_AST%', 'VISITOR_STL%',
	       'VISITOR_BLK%', 'VISITOR_TOV%', 'VISITOR_USG%', 'VISITOR_ORtg',
	       'VISITOR_DRtg', 'HOME_MP', 'HOME_FG', 'HOME_FGA', 'HOME_FG%', 'HOME_3P',
	       'HOME_3PA', 'HOME_3P%', 'HOME_FT', 'HOME_FTA', 'HOME_FT%', 'HOME_ORB',
	       'HOME_DRB', 'HOME_TRB', 'HOME_AST', 'HOME_STL', 'HOME_BLK', 'HOME_TOV',
	       'HOME_PF', 'HOME_PTS', 'HOME_+/-', 'HOME_TS%', 'HOME_eFG%', 'HOME_3PAr',
	       'HOME_FTr', 'HOME_ORB%', 'HOME_DRB%', 'HOME_TRB%', 'HOME_AST%',
	       'HOME_STL%', 'HOME_BLK%', 'HOME_TOV%', 'HOME_USG%', 'HOME_ORtg',
	       'HOME_DRtg']
	#print(df.columns)
	df = df[~df['DATE'].str.contains('Pla')]

	## Teams to replace:
	#'Charlotte Bobcats' -> 'Charlotte Hornets'
	#'New Orleans Hornets' -> 'New Orleans Pelicans'
	#'New Jersey Nets' -> 'Brooklyn Nets'
	df['VISITOR'] = df['VISITOR'].replace(['Charlotte Bobcats', 'New Orleans Hornets', 'New Jersey Nets'], \
	                                      ['Charlotte Hornets', 'New Orleans Pelicans', 'Brooklyn Nets'])

	df['HOME'] = df['HOME'].replace(['Charlotte Bobcats', 'New Orleans Hornets', 'New Jersey Nets'], \
	                                      ['Charlotte Hornets', 'New Orleans Pelicans', 'Brooklyn Nets'])

	df['VISITOR'] = df['VISITOR'].replace(['New Orleans/Oklahoma City Hornets', 'Seattle SuperSonics', 'Vancouver Grizzlies'], \
                                      ['New Orleans Pelicans', 'Oklahoma City Thunder', 'Memphis Grizzlies'])

	df['HOME'] = df['HOME'].replace(['New Orleans/Oklahoma City Hornets', 'Seattle SuperSonics', 'Vancouver Grizzlies'], \
                                      ['New Orleans Pelicans', 'Oklahoma City Thunder', 'Memphis Grizzlies'])


	dict_months = {'Oct': 10, 'Nov': 11, 'Dec': 12, 'Jan': 1, 'Feb': 2, 'Mar': 3, \
	               'Apr': 4, 'May': 5, 'Jun': 6}

	dict_day_of_the_week = {'Mon': 1, 'Tue': 2, 'Wed': 3, 'Thu': 4, 'Fri': 5, 'Sat': 6, \
	               'Sun': 7,}
	df['DAY_OF_WEEK'] = 0
	df['DAY_OF_WEEK'] = df['DATE'].apply(lambda x: map_day_of_the_week(x))
	df['DATE'] = pd.to_datetime(df['DATE'])
	df['LABEL'] = 0
	m1 = df['PTS'] > df['PTS.1']
	m2 = df['PTS'] < df['PTS.1']

	df['LABEL'] = np.select([m1, m2], [0, 1], default=1)
	df['YEAR'] = df['DATE'].apply(lambda x : map_year(x))

	#print('Saving...')
	df.to_csv( '../data/'+file_name +'.csv', mode = 'a', header= False)
	#print('Saved!!')

	df_all = pd.read_csv('../data/'+ file_name + '.csv', index_col=0)
	df_all.reset_index(drop=True, inplace=True)
	print('Len of the df before the drop_duplicates:')
	print(len(df_all))
	df_all.drop_duplicates(subset=['DATE', 'HOME', 'VISITOR'], inplace=True, keep='first')
	df_all.reset_index(drop=True, inplace=True)
	
	df_all['VISITOR'] = df_all['VISITOR'].replace(['Charlotte Bobcats', 'New Orleans Hornets', 'New Jersey Nets'], \
	                                      ['Charlotte Hornets', 'New Orleans Pelicans', 'Brooklyn Nets'])

	df_all['HOME'] = df_all['HOME'].replace(['Charlotte Bobcats', 'New Orleans Hornets', 'New Jersey Nets'], \
	                                      ['Charlotte Hornets', 'New Orleans Pelicans', 'Brooklyn Nets'])

	df_all['VISITOR'] = df_all['VISITOR'].replace(['New Orleans/Oklahoma City Hornets', 'Seattle SuperSonics', 'Vancouver Grizzlies'], \
                                      ['New Orleans Pelicans', 'Oklahoma City Thunder', 'Memphis Grizzlies'])

	df_all['HOME'] = df_all['HOME'].replace(['New Orleans/Oklahoma City Hornets', 'Seattle SuperSonics', 'Vancouver Grizzlies'], \
                                      ['New Orleans Pelicans', 'Oklahoma City Thunder', 'Memphis Grizzlies'])

	print('Len of the df after the drop_duplicates:')
	print(len(df_all))
	print('Saving...')
	df_all.to_csv( '../data/'+file_name +'.csv')
	print('Saved!!')
