# -*- coding: utf-8 -*-
"""
Created on Fri Sep 21 08:18:44 2018

@author: elina
"""


import requests
import re
from lxml import etree
import random
import pymongo
import time
import json
import urllib
import multiprocessing as mp
import os
from http.cookies import SimpleCookie


MONGO_DB = 'test'
MONGO_COLLECTION = 'gamedetailupdated'
USER_AGENTS = [
        "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; AcooBrowser; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
        "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0; Acoo Browser; SLCC1; .NET CLR 2.0.50727; Media Center PC 5.0; .NET CLR 3.0.04506)",
        "Mozilla/4.0 (compatible; MSIE 7.0; AOL 9.5; AOLBuild 4337.35; Windows NT 5.1; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
        "Mozilla/5.0 (Windows; U; MSIE 9.0; Windows NT 9.0; en-US)",
        "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Win64; x64; Trident/5.0; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 2.0.50727; Media Center PC 6.0)",
        "Mozilla/5.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 1.0.3705; .NET CLR 1.1.4322)",
        "Mozilla/4.0 (compatible; MSIE 7.0b; Windows NT 5.2; .NET CLR 1.1.4322; .NET CLR 2.0.50727; InfoPath.2; .NET CLR 3.0.04506.30)",
        "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN) AppleWebKit/523.15 (KHTML, like Gecko, Safari/419.3) Arora/0.3 (Change: 287 c9dfb30)",
        "Mozilla/5.0 (X11; U; Linux; en-US) AppleWebKit/527+ (KHTML, like Gecko, Safari/419.3) Arora/0.6",
        "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.2pre) Gecko/20070215 K-Ninja/2.1.1",
        "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN; rv:1.9) Gecko/20080705 Firefox/3.0 Kapiko/3.0",
        "Mozilla/5.0 (X11; Linux i686; U;) Gecko/20070322 Kazehakase/0.4.5",
        "Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.8) Gecko Fedora/1.9.0.8-1.fc10 Kazehakase/0.5.6",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_3) AppleWebKit/535.20 (KHTML, like Gecko) Chrome/19.0.1036.7 Safari/535.20",
        "Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; fr) Presto/2.9.168 Version/11.52",
    ]
def getcookie():
    cookiejar=[  'wants_mature_content=1; steamCountry=US%7C20c625dd17f285a516433e01035279c9; browserid=1314379602007204256; sessionid=fcff5d39f75bb710c9a35b2d; timezoneOffset=-25200,0; _ga=GA1.2.636577821.1538027879; _gid=GA1.2.468698206.1538027879; birthtime=220953601; lastagecheckage=1-January-1977',
                'wants_mature_content=1; steamCountry=US%7C20c625dd17f285a516433e01035279c9; browserid=1322260325624384317; sessionid=afda18dfeb50d2cb4c61be6d; timezoneOffset=-25200,0; _ga=GA1.2.2077796312.1537647541; _gid=GA1.2.1120851630.1537647541; birthtime=441792001; lastagecheckage=1-January-1984',
            ]
    return convertcookie(random.choice(cookiejar))
def getproxy():
    count=db.realip.count()
    offset = random.randrange( 1, count )
    count=0
    while count<5:
        person =db['realip'].find().skip( offset ).limit(1)[0]
        proxies={'https':person['https']} 
        try:
            req=requests.get(r'https://store.steampowered.com/app/640820/Pathfinder_Kingmaker/', proxies=proxies, headers=getua(),cookies=getcookie(),timeout=3).text
            if len(req)>5000:
                return proxies
            else:
                count+=1
        except Exception:
            print('no')
            count+=1
  

def getua():
    headers={'User_Agent':random.choice(USER_AGENTS)}
    return headers

def geturl(url):
    for i in range(3):
        try:
            string222='wants_mature_content=1; steamCountry=US%7C20c625dd17f285a516433e01035279c9; browserid=1314379602007204256; sessionid=fcff5d39f75bb710c9a35b2d; timezoneOffset=-25200,0; _ga=GA1.2.636577821.1538027879; _gid=GA1.2.468698206.1538027879; birthtime=220953601; lastagecheckage=1-January-1977'
            string111='wants_mature_content=1; steamCountry=US%7C20c625dd17f285a516433e01035279c9; browserid=1322260325624384317; sessionid=afda18dfeb50d2cb4c61be6d; timezoneOffset=-25200,0; _ga=GA1.2.2077796312.1537647541; _gid=GA1.2.1120851630.1537647541; birthtime=441792001; lastagecheckage=1-January-1984'
    
            if i==1:
                req=requests.get(url,headers=getua(), cookies=getcookie()).text
        #=============================================================================
            if i==2:
                req=requests.get(url,headers=getua(), proxy=getproxy()).text
        # =============================================================================
                
            html=etree.HTML(req)
            popular=html.xpath('//div[@class="glance_tags popular_tags"]/a/text()')
            populartag=concatlist(popular)
            
            specific=html.xpath('//div[@class="block_content_inner"]/div[1]/a/text()')
            specifictag=concatlist(specific)
            
            publishers=re.findall('<b>Publisher:</b>.*?<a href=".*?">(.*?)</a>',req,re.S )
            publisher=concatlist(publishers)
            date=html.xpath('//div[@class="date"]/text()')[0]
            title=html.xpath('//div[@class="apphub_AppName"]/text()')[0]
            review=re.findall('<div class="user_reviews_summary_row".*?data-tooltip-text="(.*?)"',req,re.S )
            rating=re.findall('([0-9]+%)',review[-1],re.S )[0]
            
            popularity=re.findall('the (.*?) user',review[-1],re.S )[0]
            
            developer=html.xpath('//div[@id="developers_list"]/a/text()')
            developers=concatlist(developer)
            pricetag=html.xpath('//div[@class="game_purchase_action"]//div[@class="discount_original_price"]/text()')
            if pricetag:
                price=pricetag[0]
            if not pricetag:
                price=html.xpath('//div[@class="game_purchase_action"]//div[@class="game_purchase_price price"]/text()')[0]
            price=price.strip()
            
            price=concatlist(price)
            gamereview={
                    'title':title,
                    'date':date,
                    'rating':rating,
                    'popularity':popularity,
                    'price':price,
                    'publisher':publisher,
                    'developers':developers,
                    'populartag':populartag,
                    'genre':specifictag,
                    }
            return gamereview
        except Exception:
            print('reconnect')
            continue
        return
   
    
def concatlist(group):
    newstring=""
    for x in group:
        y=x.strip()
        newstring=newstring+y+'；'
    return newstring						

def gameurl(url):
    try: 
        print(url)
        data=geturl(url)
        
        if not data:
            #db.badurlgame.insert_one({'url':url})
            print('rolling back')
            return
        else:
            print('success')
            return data
    except:
        #db.badurlgame.insert_one({'url':url})
        print ('fail to save this url: '+url)
        return
    
        

			
def writetomongo(result):

    try:
        if db[MONGO_COLLECTION].insert_one(result):
            print('data saved')
    except Exception:
        print('failed to save data')
        return

#def agecheck ():

def convertcookie(data):
    cookie = SimpleCookie()
    cookie.load(data)
    cookies = {}
    for key, morsel in cookie.items():
        cookies[key] = morsel.value
    return cookies
        
#Referer: https://store.steampowered.com/agecheck/app/637650/


  

if __name__ == '__main__':
    
    client = pymongo.MongoClient()
    db = client[MONGO_DB]
    collection=db[MONGO_COLLECTION]
    getproxy()

    urllist=[]
    dataset=db.c3.find()
    result=[]
    for x in dataset:
        urllist.append(x)
    start=time.time()
    pool = mp.Pool(8)
    data=gameurl(urllist[0]['address'])
    print(data)
    what=[pool.apply_async(gameurl,(url['address'],)) for url in urllist]
    for k in what:
        try:  
            result.append(k.get(timeout=12))
        except Exception:
            print ('con')
            time.sleep(60)
            continue
    pool.close()
    pool.join()
    print(time.time()-start)
    result=filter(None,result)
    collection.insert_many(result)
    
# =============================================================================
#     start2=time.time()
#     for url in urllist:
#         try:
#             what=gameurl(url['address'])
#             print(what.get(timeout=8))
#         except Exception:
#             print ('con')
#             continue
#     print(time.time()-start2)
# =============================================================================
      
   
            
    


    
#