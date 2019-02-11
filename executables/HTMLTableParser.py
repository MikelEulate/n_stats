## Python Script to parse HTML Tables:

import requests
import pandas as pd
from bs4 import BeautifulSoup

class HTMLTableParser:
   
    def get_table_from_url(self, url):

        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'lxml')
        table = soup.find_all('table')[-1]

        with open('../data/example.html', 'w') as f:
            f.write(str(table))
            f.close()

        df = pd.read_html('../data/example.html',header=0, index_col = 0)[0]

        return df

    def get_table_from_url_old(self, url):


        df = pd.DataFrame()

        #with open(url, 'r') as f:
        #    content = f.readlines()


        

        return df

#######################################3
