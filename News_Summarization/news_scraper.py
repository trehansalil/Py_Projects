import requests
from bs4 import BeautifulSoup
import pandas as pd

from common import *
import sys

url = "https://www.inshorts.com/en/read"
try:
    param = sys.argv[1]
    url += f"/{param}"
except:
    print("Processing all categories")

print(len(url.split("/")))

payload={}
headers = {
  'authority': 'www.inshorts.com',
  'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
  'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
  'cache-control': 'max-age=0',
#   'cookie': '_ga=GA1.2.1990707699.1659023345; _gid=GA1.2.1173172147.1659023345',
  'dnt': '1',
  'referer': 'https://www.inshorts.com/en/read/national',
  'sec-ch-ua': '".Not/A)Brand";v="99", "Google Chrome";v="103", "Chromium";v="103"',
  'sec-ch-ua-mobile': '?0',
  'sec-ch-ua-platform': '"Linux"',
  'sec-fetch-dest': 'document',
  'sec-fetch-mode': 'navigate',
  'sec-fetch-site': 'same-origin',
  'sec-fetch-user': '?1',
  'upgrade-insecure-requests': '1',
  'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36'
}

response = requests.request("GET", url, headers=headers, data=payload)

soup = BeautifulSoup(response.text, 'html.parser')

dict={"headlines":[],"text":[],"date":[],"author":[],"read_more":[], "image_url": [], 'inshorts_url':[], 'original_source': []}


def storedata(soup):
    for data in soup.findAll("div",{"class":"news-card z-depth-1"}):
        #print(dict["headlines"],data.find(itemprop="headline").getText())
        # print(data.find(itemprop="description")['content'].strip())
        if data.find(itemprop="description")['content'].strip() not in dict["headlines"]:
            #print(data.find(itemprop="headline").getText(),dict["headlines"].index(data.find(itemprop="headline").getText()))
            dict["headlines"].append(data.find(itemprop="description")['content'].strip())
            dict["image_url"].append(data.find(itemprop="url")['content'].strip())
            dict["text"].append(data.find(itemprop="articleBody").getText().strip())
            dict["date"].append(data.find("span",{"clas":"date"}).getText().strip())
            dict["author"].append(data.find("span",{"class":"author"}).getText().strip())
            dict["inshorts_url"].append(data.find(itemprop="mainEntityOfPage").get("itemid").strip())
            if data.find("a",{"class":"source"}):
                dict["read_more"].append(data.find("a",{"class":"source"}).get("href").strip())
                dict["original_source"].append(data.select_one(".source").get_text().strip())
            else:
                dict["read_more"].append("None")
                dict["original_source"].append('Inshorts')

start_id=soup.findAll("script",{"type":"text/javascript"})[-1].get_text().split()[3].strip(";").strip('"')
print(start_id)

import json

for i in range(100):
    print(i,len(dict["headlines"]),start_id)
    ajax_url="https://inshorts.com/en/ajax/more_news"
    if len(url.split("/")) == 6:
        payload={"news_offset":start_id,"category":param}
    else:
        payload={"news_offset":start_id,"category":''}
    try:
        r=requests.post(ajax_url,payload,headers=headers)
        start_id=r.content.decode("utf-8")[16:26]
        print(start_id)
        soup = BeautifulSoup(json.loads(r.text)['html'])
        
        storedata(soup)
    except:
        print('Skipping')
        pass
    if i%1000==0:
        
        df = pd.DataFrame(dict)
        df['day'] = df['date'].apply(lambda x: x.split(',')[1].strip())
        df['date'] = df['date'].apply(lambda x: parse(x.split(',')[0]))
        data_dict = df.to_dict(orient='records')
        for enum, record in enumerate(data_dict):
            # print(i)
            update_data(collection=news_data, record=record, enum=enum, type='update', key='inshorts_url')
        if len(url.split("/")) == 6:
            df.to_csv(f"data/data_{param}_{str(i/1000)}.csv", index=False)
        else:
            df.to_csv("data"+str(i/1000)+".csv", index=False)
        dict={"headlines":[],"text":[],"date":[],"author":[],"read_more":[], "image_url": [], 'inshorts_url':[], 'original_source': []}
