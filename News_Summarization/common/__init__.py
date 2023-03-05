from datetime import date, datetime
from pymongo import MongoClient
import os
from configparser import ConfigParser
import json
import requests
import time
import keyboard
from dateutil.parser import parse


import logging
import sentry_sdk
from sentry_sdk.integrations.logging import LoggingIntegration

# All of this is already happening by default!
sentry_logging = LoggingIntegration(
    level=logging.INFO,        # Capture info and above as breadcrumbs
    event_level=logging.ERROR  # Send errors as events
)
sentry_sdk.init(
    dsn="https://7d46e7c4e8714cec93854073b1f68291@o1211210.ingest.sentry.io/6347259",
    integrations=[sentry_logging]
)

cur_dir = os.getcwd().replace("/common", '')
print(cur_dir)
exec_file_path = os.path.join(cur_dir, 'properties.config')
print(exec_file_path)

parser = ConfigParser()
parser.read(exec_file_path)

mongo_dbname = parser.get("config", "mongo_dbname")
mongo_collection = parser.get("config", "mongo_collection")

dev_DB_URI = parser.get("config", "dev_DB_URI")
stage_DB_URI = parser.get("config", "stage_DB_URI")


proxies = {"http": "http://salilt:thanosi_country-in@proxy.iproyal.com:12323",
           "https": "http://salilt:thanosi_country-in@proxy.iproyal.com:12323"
           }

NEWS_CRAWLER_ENV = os.getenv("NEWS_PROJ_ENV", "STAGE")
print(NEWS_CRAWLER_ENV)
if NEWS_CRAWLER_ENV == 'DEV':
    client = MongoClient(dev_DB_URI, maxPoolSize=10000, connect=False)
    db = client[mongo_dbname]
    news_data = db[mongo_collection]

elif NEWS_CRAWLER_ENV == 'STAGE':
    client = MongoClient(stage_DB_URI, maxPoolSize=10000, connect=False)
    db = client[mongo_dbname]
    news_data = db[mongo_collection]

# sentry_sdk.init(
#     "https://7d46e7c4e8714cec93854073b1f68291@o1211210.ingest.sentry.io/6347259",
#
#     # Set traces_sample_rate to 1.0 to capture 100%
#     # of transactions for performance monitoring.
#     # We recommend adjusting this value in production.
#     traces_sample_rate=1.0
# )


def update_data(collection, record, enum, type, key='tconst'):
    print(record)
    if type == 'insert':
        record['inserted_at'] = datetime.now()
        record['updated_at'] = datetime.now()
        try:
            collection.insert_one(record, upsert=True)
            print(f"Record {enum} inserted")
        except Exception as e:
            a = f"Record {enum} insert failed for {key}: {record[key]} with error as {e}"
            sentry_sdk.capture_exception(e)
            sentry_sdk.capture_message(a)
    elif type == 'update':
        record['updated_at'] = datetime.now()
        try:
            collection.update_one({key: record[key]}, {"$set": record}, upsert=True)
            print(f"Record {enum} updated")
        except Exception as e:
            a = f"Record {enum} update failed for {key}: {record[key]} with error as {e}"
            sentry_sdk.capture_exception(e)
            sentry_sdk.capture_message(a)
    elif type == 'delete':
        try:
            collection.delete_one({key: record[key]})
            print(f"Record {enum} deleted")
        except Exception as e:
            a = f"Record {enum} delete failed for {key}: {record[key]} with error as {e}"
            sentry_sdk.capture_exception(e)
            sentry_sdk.capture_message(a)
    else:
        print(f"Record {enum} not updated")


def chunks(sequence, chunk_size=10000):
    # Chunks of 1000 documents at a time.
    for j in range(0, len(sequence), chunk_size):
        yield sequence[j:j + chunk_size]


def close_connections(file_name_to_be_closed=None):
    client.close()
    print("Both connections closed for file: {}".format(file_name_to_be_closed))