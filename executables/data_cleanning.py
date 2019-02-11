import pandas as pd
import datetime
import numpy as np
from collections import Counter



def map_dates(x):
    
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


df = pd.read_csv('../data/nba_data.csv', index_col=0)
df.reset_index(drop=True, inplace=True)
df = df.drop('NOTES', axis=1)
df = df[~df['DATE'].str.contains('Pla')]

## Teams to replace:
#'Charlotte Bobcats' -> 'Charlotte Hornets'
#'New Orleans Hornets' -> 'New Orleans Pelicans'
#'New Jersey Nets' -> 'Brooklyn Nets'

df['VISITOR'] = df['VISITOR'].replace(['Charlotte Bobcats', 'New Orleans Hornets', 'New Jersey Nets'], \
                                      ['Charlotte Hornets', 'New Orleans Pelicans', 'Brooklyn Nets'])

df['HOME'] = df['HOME'].replace(['Charlotte Bobcats', 'New Orleans Hornets', 'New Jersey Nets'], \
                                      ['Charlotte Hornets', 'New Orleans Pelicans', 'Brooklyn Nets'])




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


df.to_csv('../data/nba.csv')