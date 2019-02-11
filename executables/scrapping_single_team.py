import requests
from bs4 import BeautifulSoup
import pandas as pd


def get_table_from_url(url, df_tot):
        global team

        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'lxml')
        table = soup.find_all('table')[-1]

        with open('../data/example.html', 'w') as f:
            f.write(str(table))
            f.close()

        df = pd.read_html('../data/example.html',header=1, index_col = 0)[0]

        df = df.reset_index()
        df = df.drop(['Rk'], axis = 1)
        df = df.rename(columns={'Â' : 'H_V'})

        df_tot = df_tot.append(df)
        df_tot.to_csv('../data/teams/'+ team +'.csv')

        try: 
            
            next_page = get_next_url(url)
            df_tot = df_tot.append(get_table_from_url(next_page, df_tot))
        except:
            pass

        return df_tot   

def get_next_url(url):

    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'lxml')
    next_pages = soup.find('div', class_='p402_premium').find('p').find_all('a')

    for next_page in next_pages:
        if next_page.get_text() == 'Next page':
            print(next_page['href'])

            return 'https://www.basketball-reference.com'+next_page['href']


def get_team_data(url):
    df_tot = pd.DataFrame()

    df = get_table_from_url(url, df_tot)

   

    
    pass

team = 'MEM'

url = 'https://www.basketball-reference.com/play-index/tgl_finder.cgi?request=1&match=game&lg_id=NBA&is_playoffs=N&team_seed_cmp=eq&opp_seed_cmp=eq&year_min=2001&year_max=2019&is_range=N&game_num_type=team&team_id='+team+'&order_by=date_game'
df = get_team_data(url)

print(df.head())
print(df.tail())
print(len(df))

next_page = get_next_url(url)