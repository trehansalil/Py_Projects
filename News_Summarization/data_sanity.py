from common import *
import sys

print("Round 1\n")
result = news_data.aggregate([
    {
        '$group': {
            '_id': '$inshorts_url', 
            'cnt': {
                '$count': {}
            }
        }
    }, {
        '$match': {
            'cnt': {
                '$gt': 1
            }
        }
    }, {
        '$sort': {
            'cnt': -1
        }
    }, {
        '$project': {
            '_id': 1
        }
    }
])

result = [i['_id'] for i in result]
cnt=0
if len(result)!=0:
    for value in result:
        first_doc = news_data.find_one({'inshorts_url': value})
        news_data.delete_many({'inshorts_url': value, '_id': {'$ne': first_doc['_id']}})
        cnt+=1
    print(f"Data was cleaned for {len(result)} no. of urls, urls were {result}")
else:
    print("Data is perfectly Clean with unique inshorts urls")

print("Round 2\n")
result = news_data.aggregate([
    {
        '$unwind': {
            'path': '$category', 
            'includeArrayIndex': 'string', 
            'preserveNullAndEmptyArrays': False
        }
    }, {
        '$group': {
            '_id': [
                '$inshorts_url', '$category'
            ], 
            'count': {
                '$sum': 1
            }
        }
    }, {
        '$match': {
            'count': {
                '$gt': 1
            }
        }
    }, {
        '$project': {
            '_id': 1
        }
    }
])

result = [i['id'] for i in result]

cnt=0
if len(result)!=0:
    for i in result:
        url = i[0]
        a = news_data.find_one({"inshorts_url": url})
        a['category'] = list(set(a['category']))
        news_data.update_one({"inshorts_url": url}, {"$set": a}, upsert=True)
        cnt+=1
    print(f"Data was cleaned for {cnt} no. of urls, urls were {result}")
else:
    print("Data is perfectly Clean with unique category + urls")


# extracting the current file name
file_name = sys.argv[0].split('/')[-1]

# Closing all the open mongodb connections
close_connections(file_name_to_be_closed=file_name)