import requests
from bs4 import BeautifulSoup
import pandas as pd


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
		new_url = link.find('a')
		#print('https://www.basketball-reference.com' +new_url['href'])
		list_links.append('https://www.basketball-reference.com' +new_url['href'])

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



#url = 'https://www.basketball-reference.com/leagues/NBA_2018_games-october.html'

#df = get_nba_data(url)

#print(df.head())
#print(df.columns)

def get_months(url):

	list_months = []
	response = requests.get(url)
	soup = BeautifulSoup(response.text, 'lxml')
	links = soup.find('div', class_='filter').find_all('a')

	for link in links:

		#print('https://www.basketball-reference.com/'+link['href'])
		list_months.append('https://www.basketball-reference.com/'+link['href'])

	return list_months


def get_seasons():

	list_seasons = []
	for i in range(2,10):

		#print('https://www.basketball-reference.com/leagues/NBA_201'+str(i)+'_games.html')
		list_seasons.append('https://www.basketball-reference.com/leagues/NBA_200'+str(i)+'_games.html')


	return list_seasons


def nba():

	df = pd.DataFrame()

	list_seasons = get_seasons()

	for season in list_seasons:

		print('SEASON:')
		print(season)

		list_months = get_months(season)

		df_season = pd.DataFrame()

		for i, month in enumerate(list_months):
			
			print('MONTH:')
			print(month)

			if i == 0:
				df_month = get_nba_data(month)
				df_month.to_csv('nba_data_seasons_02_10.csv')
			
			else:
				try:
					df_month = get_nba_data(month)
					df_month.to_csv('nba_data_seasons_02_10.csv', mode='a', header=False)
				except:
					pass

			df_season = df_season.append(df_month)
			
		print('######################')

		df = df.append(df_season)

	return df


df = nba()

print('A first look at the dataframe:')
print(df.head())
print('Total Lenght:')
print(len(df))
print('Saving...')
df.to_csv('nba_old.csv')
print('Saved!!')


