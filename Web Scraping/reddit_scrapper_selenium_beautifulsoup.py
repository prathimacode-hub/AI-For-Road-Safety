from selenium import webdriver  
import time  
import random
from selenium.webdriver.common.keys import Keys  
from selenium import webdriver
from selenium.webdriver.common.by import By
from webdriver_manager.firefox import GeckoDriverManager
from urllib.request import urlopen
from bs4 import BeautifulSoup
import requests
from tqdm import tqdm
from newspaper import Article
from lxml import etree
import pandas as pd
driver = webdriver.Firefox(executable_path=GeckoDriverManager().install())


#parameters
number_of_links_to_be_scrapped=10
key_word='futurspot'


#reddit url
base_url="https://www.reddit.com"
driver.get(base_url)
time.sleep(5)
#sending tag words to the search bar
driver.find_element(By.XPATH,"//input[@id='header-search-bar']").send_keys(key_word)
driver.find_element(By.XPATH,"//input[@id='header-search-bar']").send_keys(Keys.ENTER)
time.sleep(5)

#driver.get(str(base_url)+str(search_url))
data={'url_reddit_post':[],'title':[],'out_bound_link':[],'text_post':[],'image_links':[],'meta_descriptions':[],'keywords':[],'news_body':[],'summary':[]}

# Get scroll height
last_height = driver.execute_script("return document.body.scrollHeight")

while True:
    # Scroll down to bottom
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    SCROLL_PAUSE_TIME = random.randint(15,23)
    time.sleep(SCROLL_PAUSE_TIME)
    #number of titles extracted
    number_elements=len(driver.find_elements(By.XPATH,"//h3[@class='_eYtD2XCVieq6emjKBH3m']/span"))

    # Calculate new scroll height and compare with last scroll height
    new_height = driver.execute_script("return document.body.scrollHeight")
    if (new_height == last_height) or (number_elements >= number_of_links_to_be_scrapped) :
        break
    last_height = new_height
time.sleep(10)
#collecting links of posts present in the page
href_of_posts=driver.find_elements(By.XPATH,"//a[@class='SQnoC3ObvgnGjWt90zD9Z _2INHSNB8V5eaWp4P0rY_mE']")
print('links collected : ',len(href_of_posts))

#header file
headers = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:66.0) Gecko/20100101 Firefox/66.0", "Accept-Encoding":"gzip, deflate", "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8", "DNT":"1","Connection":"close", "Upgrade-Insecure-Requests":"1"}

#extracting title,out bound links ,image url ,post body
for i in tqdm(range(len(href_of_posts))):
    try:

        link=href_of_posts[i].get_attribute('href')
        print(link)
        url=requests.get(link,headers=headers)
        time.sleep(2)
        content=url.content
        soup = BeautifulSoup(content,"html.parser")
        dom = etree.HTML(str(soup))
        title=dom.xpath('//h1[@class="_eYtD2XCVieq6emjKBH3m"]')[0].text
        out_bound_link=dom.xpath("//a[@class='_13svhQIUZqD9PVzFcLwOKT styled-outbound-link']/@href")
        para=dom.xpath('//div[@class="_3xX726aBn29LDbsDtzr_6E _1Ap4F5maDtT1E1YuCiaO0r D3IL3FD0RFy_mkKLPwL4"]/div[@class="_292iotee39Lmt0MkQZ2hPV RichTextJSON-root"]/p[@class="_1qeIAgB0cPwnLhDF9XSiJM"]/text()')
        image_links=dom.xpath('//div[@class="_2Ev7WJU0f45KxlmClce9t8"]/ul[@class="_1apobczT0TzIKMWpza0OhL"]/li[@class="_28TEYBuEdOuE3kN6UyoKMa"]//a[@class="_3BxRNDoASi9FbGX01ewiLg iUP9nbvcaxfwKrQTgt0sw"]/@href')
        
        #appending collected datas
        data['url_reddit_post'].append(link)
        data['title'].append(title)
        data['text_post'].append(para)
        data['image_links'].append(image_links)
        #extacting meta description from out bound links
    #meta description from outbound link
        #if meta description is not empty
        if out_bound_link != [] :
            #collecting metadescription if the link is available
            try:
                url=requests.get(out_bound_link[0],headers=headers,timeout=40) 
                content=url.content
                soup = BeautifulSoup(content,"html.parser")
                description=soup.find("meta",{"property":"og:description"})
                data['meta_descriptions'].append(description.attrs['content'])
                data['out_bound_link'].append(out_bound_link[0])
                url=str(out_bound_link[0])
                article = Article(url)
                article.download()
                article.parse()
                data['news_body'].append(article.text)
                article.nlp()
                data['keywords'].append(article.keywords)
                data['summary'].append(article.summary)





                #if it throws error 
            except:
                data['out_bound_link'].append('NA')
                data['meta_descriptions'].append('NA')
                data['news_body'].append('NA')
                data['keywords'].append('NA')
                data['summary'].append('NA')

        #if out_bound_link is empty append value 'NA'  
        else:

            data['out_bound_link'].append('NA')
            data['meta_descriptions'].append('NA')
            data['news_body'].append('NA')
            data['keywords'].append('NA')
            data['summary'].append('NA')

    except:
        print('Skipping')
 

#saving it into dataframe
print(len(data['out_bound_link']),len(data['keywords']),len(data['summary']),len(data['news_body']))
df = pd.DataFrame(data)


df.to_csv(key_word.replace(' ','_')+'_scrapped.csv')

driver.close()
