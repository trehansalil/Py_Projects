from pymongo import MongoClient
import pandas as pd
from common import *

import sys

# Requires the PyMongo package.
# https://api.mongodb.com/python/current


filter={
    '$or': [
        {
            'headlines': {
                '$regex': 'Musk'
            }
        }, {
            'text': {
                '$regex': 'Musk'
            }
        }, {
            'text': {
                '$regex': 'Tesla'
            }
        }, {
            'headlines': {
                '$regex': 'Tesla'
            }
        }, {
            'text': {
                '$regex': 'Elon'
            }
        }, {
            'headlines': {
                '$regex': 'Elon'
            }
        }
    ]
}
sort=list({
    'date': -1
}.items())

result = news_data.find(
  filter=filter,
  sort=sort
)


df = pd.DataFrame.from_dict(result)

print(df.head())

df.to_excel('data/musk_data_pull.xlsx')

# extracting the current file name
file_name = sys.argv[0].split('/')[-1]

# Closing all the open mongodb connections
close_connections(file_name_to_be_closed=file_name)

