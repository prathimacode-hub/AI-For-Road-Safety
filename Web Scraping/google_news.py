import requests, lxml
from bs4 import BeautifulSoup
import time
import urllib.request as urllib2
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36 Edge/18.19582"
}

params = {
    "q": "gta san andreas",
    "hl": "en",
    "tbm": "nws",
}

response = requests.get('https://news.google.com/search?for=accidents+in+india&hl=en-IN&gl=IN&ceid=IN%3Aen', headers=headers,timeout=10)

soup = BeautifulSoup(response.content, "html.parser")
base_url='https://news.google.com'
#results = soup.select('.lBwEZb')
results=soup.find("div", class_="lBwEZb BL5WZb xP6mwf")
job_elements = results.find_all("div", class_="NiLAwe y6IFtc R7GTQ keNKEd j7vNaf nID9nc")
for element in job_elements:
    title=element.find("h3", class_="ipQwMb").text
    href=str(element.find("a", class_="DY5T1d RZIKme")['href']).replace('.','')
    response = urllib2.urlopen(base_url+href) # 'www.google.com/url?q=https://en.wikipedia.org/wiki/Turtle&sa=U&ved=0ahUKEwja-oaO7u3XAhVMqo8KHYWWCp4QFggVMAA&usg=AOvVaw31hklS09NmMyvgktL1lrTN'
    print(response.geturl()) 
    source=element.find("a", class_="wEwyrc AVN2gc uQIVzc Sksgp").text
    
    try :
        time=element.find("time", class_="WW6dff uQIVzc Sksgp")['datetime']
    except TypeError:
        time='Nan'
