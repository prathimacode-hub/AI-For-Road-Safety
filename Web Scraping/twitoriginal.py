from selenium import webdriver  
import time  
import random
import json
from selenium import webdriver
from webdriver_manager.firefox import GeckoDriverManager
from urllib.request import urlopen
from bs4 import BeautifulSoup
import requests
from tqdm import tqdm
import pandas as pd
from urllib.parse import quote
driver = webdriver.Firefox(executable_path=GeckoDriverManager().install())

import re




class tweetscrap:
                       
    def __init__(self):

            self.data_dic={'id':[],'tweet':[],'time':[]}    
            self.base_url="https://twitter.com/explore"
            self.url = (
                        f'https://api.twitter.com/2/search/adaptive.json?'
                        f'include_profile_interstitial_type=1'
                        f'&include_blocking=1'
                        f'&include_blocked_by=1'
                        f'&include_followed_by=1'
                        f'&include_want_retweets=1'
                        f'&include_mute_edge=1'
                        f'&include_can_dm=1'
                        f'&include_can_media_tag=1'
                        f'&skip_status=1'
                        f'&cards_platform=Web-12'
                        f'&include_cards=1'
                        f'&include_ext_alt_text=true'
                        f'&include_quote_count=true'
                        f'&include_reply_count=1'
                        f'&tweet_mode=extended'
                        f'&include_entities=true'
                        f'&include_user_entities=true'
                        f'&include_ext_media_color=true'
                        f'&include_ext_media_availability=true'
                        f'&send_error_codes=true'
                        f'&simple_quoted_tweet=true'
                        f'&query_source=typed_query'
                        f'&pc=1'
                        f'&spelling_corrections=1'
                        f'&ext=mediaStats%2ChighlightedLabel'
                        f'&count=20'
                        f'&tweet_search_mode=live'
                    )
                    # regex for finding next cursor
            self.cursor_re = re.compile('"(scroll:[^"]*)"')
            self.url = self.url + '&q={query}'
            
            self.number_tweets=100000
            self.search_word="road accident india"#alltheword in search
            self.phrase=""#'accident in india'(comma seprated)
            self.hashtags=""# '#accidents,#india'(#wordcomma seprated)
            self.keywords=""#'india,cricket'(comma seprated)#anyoftheword in keywords
            self.date_until=''#2022-01-05 (yyyy-mm-dd)
            self.date_since=''#2022-01-05 (yyyy-mm-dd)
                    
    
    def   cookies_collection(self):

                        #reddit url
                        
                        driver.get(self.base_url)
                        time.sleep(10)
                        cookies_list=driver.get_cookies()

                        cookies_dict = []
                        for cookie in cookies_list:
                            cookies_dict.append([cookie['name'],cookie['value']])
                        self.cookies_dict = dict(cookies_dict)

                        self.x_guest_token = driver.get_cookie('gt')['value']

                        self.headers = {
                                    'authorization': 'Bearer AAAAAAAAAAAAAAAAAAAAANRILgAAAAAAnNwIzUejRCOuH5E6I8xnZz4puTs%3D1Zv7ttfk8LF81IUq16cHjhLTvJu4FA33AGWWjCpTnA',
                                    'x-guest-token': self.x_guest_token,
                                    # 'x-csrf-token': self.x_csrf_token,
                                }
    def    scrap(self):



                        self.cookies_collection()
                       
                    
                   
                        self.query="{search_word}{phrases} {words} {hashtags} {date_until} {date_since}"
                        self.que=self.query.format(search_word=str(self.search_word) if self.search_word !='' else '',phrases='"'+str(self.phrase)+'"' if self.phrase !='' else '',words=("("+self.keywords.replace(',',' OR ')+")") if self.keywords !='' else '',hashtags=("("+ str(self.hashtags.replace(',',' OR '))+")") if self.hashtags !='' else '', date_until= ('until:'+str(self.date_until) if self.date_until !='' else ''),date_since = ('since:'+str(self.date_since) if self.date_since !='' else ''))

                        #print(que)
                        self.burl = self.url.format(query=quote(self.que.strip()))



                        r = requests.get(self.burl, cookies=self.cookies_dict, headers=self.headers)
                        
                        data = json.loads(r.text)
                        tweet=data['globalObjects']['tweets']
                        cursor = self.cursor_re.search(r.text).group(1)
                        for i in tweet:
                                self.data_dic['id'].append(tweet[i]['id'])
                                self.data_dic['tweet'].append(tweet[i]['full_text'])
                                self.data_dic['time'].append(tweet[i]['created_at'])
                              
                        time.sleep(5)

                        for i in tqdm(range(self.number_tweets//20)):
                                
                               # time.sleep(random.randrange(3))
                                cur=self.parse_page(cursor)
                                cursor=cur
                                
             
                                #time.sleep(random.randrange(5))
                        csv_data=pd.DataFrame(self.data_dic)
                        csv_data.to_csv('twitter2.csv')
                        driver.close()        
    
    def parse_page(self,cursor):
        

        if cursor:
              url = self.burl + '&cursor={cursor}'
              url = url.format(cursor=quote(cursor))


        r = requests.get(url, cookies=self.cookies_dict, headers=self.headers)
        data = json.loads(r.text)
        tweet=data['globalObjects']['tweets']

        for i in tweet:
                 self.data_dic['id'].append(tweet[i]['id'])
                 self.data_dic['tweet'].append(tweet[i]['full_text'])
                 self.data_dic['time'].append(tweet[i]['created_at'])
        cursor = self.cursor_re.search(r.text).group(1)
        return cursor


                        


s=tweetscrap()
s.scrap()