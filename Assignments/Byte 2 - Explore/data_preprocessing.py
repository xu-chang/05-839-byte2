import csv
import httplib2
from apiclient.discovery import build
import urllib
import json
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib as mpl
import matplotlib.pyplot as plt

# This API key is provided by google as described in the tutorial
API_KEY = 'AIzaSyB0IyiAZn6vBo_nqx702gAXz7h2t7KT7tw'

# This is the table id for the fusion table
TABLE_ID = '19owEO_WXTz5PzzIjx2MAYgne-EInIBHumiFu0fly'

try:
    fp = open("data.json")
    response = json.load(fp)
except IOError:
    service = build('fusiontables', 'v1', developerKey=API_KEY)
    query = "SELECT startYear, primaryTitle, genres, runtimeMinutes, averageRating, numVotes "
    query += "FROM 19owEO_WXTz5PzzIjx2MAYgne-EInIBHumiFu0fly "
    query += "WHERE numVotes > 10000 ORDER BY averageRating DESC"
    response = service.query().sql(sql=query).execute()
    fp = open("data.json", "w+")
    json.dump(response, fp)

black_list = {'News', 'Documentary', 'Film-Noir'}
genre_rating_count = {}  # {genre: [count, total_rating]}
max_genres_cnt = 0
df = pd.DataFrame(response[u'rows'], columns = response[u'columns'])
for index, row in df[['genres', 'averageRating']].iterrows():
    genres = set(row[0].split(','))
    if set.intersection(genres, black_list):
        continue
    max_genres_cnt = max(max_genres_cnt, len(genres))
    for genre in genres:
        if genre not in genre_rating_count:
            genre_rating_count[genre] = [1, row[1]]
        else:
            genre_rating_count[genre][0] += 1
            genre_rating_count[genre][1] += row[1]
genre_ratings = []
for g in genre_rating_count:
    v = genre_rating_count[g]
    genre_ratings.append([g, v[1]/v[0], v[0]])
    
result = pd.DataFrame(genre_ratings, columns = ['genre', 'avg_rating', 'count'])
result.sort_values(['avg_rating'], inplace=True)
plt.figure(figsize=(16,20))
plt.rc('xtick', labelsize=14)
plt.rc('ytick', labelsize=14)
plt.xlabel('Average Ratings', fontsize=16)
plt.ylabel('Genres', fontsize=16)
g = sns.barplot(x=list(result['avg_rating']), y=list(result['genre']));
g.set(xlim=(6, 7.5))
# You can save to file here, but I directly saved the image in Datalab, so this part
# is not implemented.