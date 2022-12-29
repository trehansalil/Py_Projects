from pymongo import MongoClient
import pandas as pd
from common import *

import sys

# Requires the PyMongo package.
# https://api.mongodb.com/python/current

# ls = ["Musk", "Tesla", "Elon"]
if len(sys.argv) != 1:
    if sys.argv[1] != '-f':
        ls = [i.strip().replace(",", "").replace(".", "").replace("'", "").replace("-", "") for i in sys.argv[1].split(",")]
        print(ls)
def data_pull(lis):
    headline_filter = [{
                'headlines': {
                    '$regex': i
                }
            } for i in lis]

    text_filter = [{
                'text': {
                    '$regex': i
                }
            } for i in lis]

    headline_filter.extend(text_filter)


    filter={
        '$or': headline_filter
    }
    sort=list({
        'date': -1
    }.items())

    result = news_data.find(
    filter=filter,
    sort=sort
    )


    df = pd.DataFrame.from_dict(result)

    # print(df.head(1))

    df.to_excel(f'data/{lis[0]}_data_pull.xlsx')

    # extracting the current file name
    file_name = sys.argv[0].split('/')[-1]

    # Closing all the open mongodb connections
    close_connections(file_name_to_be_closed=file_name)

    return df

data_pull(lis=ls)

