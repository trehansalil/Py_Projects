import json
from bs4 import BeautifulSoup
import requests
from datetime import datetime
from typing import Dict, List
from common import *

class InshortsAPI:
    def __init__(self, category: str):
        self.category = category if category!='' else "top_stories"
        self.essentials()
        self.enum = 0
        
    def essentials(self):
        self.page = 1
        
        self.cookies = {
            '_ga': 'GA1.1.460094762.1714749078',
            '_tenant': '[object Object]',
            'MicrosoftApplicationsTelemetryDeviceId': '74fba70d-0e85-4068-8cca-3e748bf9fea8',
            'MicrosoftApplicationsTelemetryFirstLaunchTime': '2024-05-03T15:11:28.252Z',
            '_ga_L7P7D50590': 'GS1.1.1714769101.4.1.1714770021.28.0.0',
        }


        self.headers = {
            'accept': '*/*',
            'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
            'content-type': 'application/json',
            # 'cookie': '_ga=GA1.1.460094762.1714749078; _tenant=[object Object]; MicrosoftApplicationsTelemetryDeviceId=74fba70d-0e85-4068-8cca-3e748bf9fea8; MicrosoftApplicationsTelemetryFirstLaunchTime=2024-05-03T15:11:28.252Z; _ga_L7P7D50590=GS1.1.1714769101.4.1.1714770021.28.0.0',
            'dnt': '1',
            'priority': 'u=1, i',
            'referer': 'https://inshorts.com/en/read' if self.category=='top_stories' else f'https://inshorts.com/en/read/{self.category}',
            'sec-ch-ua': '"Chromium";v="124", "Google Chrome";v="124", "Not-A.Brand";v="99"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36',
        }
        if self.category =='top_stories':
        
            url = f"https://inshorts.com/en/read"      

        else:
            url = f"https://inshorts.com/en/read/{self.category}"

        response = requests.get(url).text

        soup = BeautifulSoup(response, "html.parser")
        for i in soup.find_all("script"):
            if 'news_list' in str(i):
                data =i.string.replace("window.__STATE__ = ", "")

        self.news_offset = data.split('"hash_id":')[1].split(",")[0].strip('"')    
            
        print(self.news_offset)
    def process_json(self, a: Dict):
        '''
        This function processes a JSON object and returns a dictionary with various key-value pairs.
        '''
        data_dict = {}

        # Initialize an empty dictionary to store the processed data

        data_dict['headlines'] = a['title'].strip()
        # Extract the title from the JSON object, strip any leading/trailing whitespace, and store it in the 'headlines' key

        data_dict['image_url'] = a['image_url'].strip()
        # Extract the image URL from the JSON object, strip any leading/trailing whitespace, and store it in the 'image_url' key

        data_dict["text"] = a['content'].strip()
        # Extract the content from the JSON object, strip any leading/trailing whitespace, and store it in the 'text' key

        data_dict['datetime'] = datetime.fromtimestamp(int(a['created_at']/1000))
        # Convert the created_at timestamp from milliseconds to seconds, then convert it to a datetime object and store it in the 'datetime' key

        data_dict['date'] = data_dict['datetime'].replace(minute=0, hour=0, second=0, microsecond=0)
        # Extract the date from the datetime object and store it in the 'date' key

        data_dict['day'] = data_dict['datetime'].strftime('%A')
        # Format the datetime object to extract the day of the week (e.g. Monday, Tuesday, etc.) and store it in the 'day' key

        data_dict['author'] = a['author_name']
        # Extract the author name from the JSON object and store it in the 'author' key

        data_dict['inshorts_url'] = "https://inshorts.com/en/news/" + a['old_hash_id']
        # Construct the InShorts URL by concatenating the base URL with the old hash ID and store it in the 'inshorts_url' key

        data_dict['read_more'] = a['source_url']
        # Extract the source URL from the JSON object and store it in the 'read_more' key

        data_dict['original_source'] = a['source_name']
        # Extract the source name from the JSON object and store it in the 'original_source' key

        data_dict['category'] = a['category_names']
        # Extract the category names from the JSON object and store it in the 'category' key

        data_dict['relevancy_tags'] = a['relevancy_tags']
        # Extract the relevancy tags from the JSON object and store it in the 'relevancy_tags' key
        
        data_dict['created_at'] = datetime.now()
        self.news_offset = a['hash_id']
        if self.category == 'top_stories':
            self.enum += 1
        else:
            self.enum += 1       
            self.page += 1    

        update_data(collection=news_data, record=data_dict, enum=self.enum, type='update', key='inshorts_url')

        return data_dict
    
    def scrape(self):
        
        '''
        This function scrapes news articles from the InShorts API and returns a list of dictionaries containing the scraped data.

        The function first initializes a dictionary called 'params' with various key-value pairs that will be used as parameters in the API request.

        The 'category' key is set to the category that the user has specified.

        The 'max_limit' key is set to '200' to specify the maximum number of news articles to retrieve.

        The 'include_card_data' key is set to 'true' to include additional data in the response.

        The 'news_offset' key is set to the current value of the 'news_offset' attribute of the class instance.

        The function then sends a GET request to the InShorts API using the 'requests' library, passing in the 'params' dictionary as parameters.

        The response from the API is then loaded as a JSON object using the 'json' library.

        The 'news_offset' attribute of the class instance is updated to the minimum news ID in the response.

        The length of the scraped data is stored in the 'len_scraped' attribute of the class instance.

        If the length of the scraped data is not zero, the 'data' attribute of the class instance is set to a list of dictionaries, where each dictionary contains the processed data for a single news article.

        The 'process_json' function is used to process the JSON object for each news article.

        If the length of the scraped data is zero, the 'data' attribute of the class instance is set to an empty list.

        Finally, the 'data' attribute of the class instance is returned.
        '''
        if self.category == "top_stories":
            params = {
                'category': self.category,
                'max_limit': '5',
                'include_card_data': 'true',
                'news_offset': self.news_offset,
            }
            
            # print(params)

            response = requests.get(
                'https://inshorts.com/api/en/news',
                params=params,
                # cookies=cookies,
                headers=self.headers
            )
        else:

            params = {
                'page': str(self.page),
                'type': 'NEWS_CATEGORY',
            }    
            
            response = requests.get(
                f'https://inshorts.com/api/en/search/trending_topics/{self.category}',
                params=params,
                # cookies=cookies,
                headers=self.headers
            )                    

        a = json.loads(response.text)

        # self.news_offset = a['data']['min_news_id']
        self.len_scraped = len(a['data']['news_list'])
        # print(a['data']['news_list'])
        # print(a['data']['reload_required'])
        if self.len_scraped!=0:
            self.data = [self.process_json(a=record['news_obj']) for record in a['data']['news_list'] if 'news_obj' in record]
        else:
            self.data = []
            
        self.page += 1 
    
    
    