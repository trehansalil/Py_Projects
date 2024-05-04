from pymongo import MongoClient

# Requires the PyMongo package.
# https://api.mongodb.com/python/current

client = MongoClient('mongodb+srv://thanos_inshorts:thanos@cluster0.hlbuku7.mongodb.net/?retryWrites=true&w=majority')
filter={
    '$expr': {
        '$eq': [
            {'$year': '$created_at'},
            2024
        ]
    }
}
sort=list({
    'updated_at': -1
}.items())

result = client['inshorts_db']['news_data'].count_documents(
  filter=filter
)
print(result)