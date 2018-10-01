# -*- coding: utf-8 -*-
"""
Created on Sun Sep 23 15:33:11 2018

@author: elina
"""
from multiprocessing import Pool, TimeoutError
import time
import os
import pandas as pd
import re
from datetime import datetime
from datetime import date

path=r"C:\Users\elina\Desktop\gamereview.json"
st=pd.read_json(path, lines=True)

genrelist=[]
taglist={}
def strangecharacters(name):
    if not name:
        return "UNKNOWN"
    else:
        x=name[0]
        newword=re.sub('[^0-9A-Za-z.\'\:\s ]',' ',x)
        if not newword:
            return'UNKNOWN'
        return newword
 
st['title']=st['title'].map(lambda x: strangecharacters(x))
st=st.drop_duplicates(subset='title',keep='first')  
def checkempty(list1):
    if not list1:
        return -1
    else:
        newnum=re.sub('[^0-9.]','',list1[-1])
        if not newnum:
            return 0
        if newnum=='.':
            return 0
        else:
            return float(newnum)

st['popularity']=st['popularity'].map(lambda x: checkempty(x))
st['newprice']=st['price'].map(lambda x: checkempty(x))
st['rating']=st['rating'].map(lambda x: checkempty(x))
def checkdate(date):
    if not date:
        return None
    else:
        day=date[0]
        relist=re.findall('([a-zA-Z]+? [0-9]+?, [0-9]+?)', day,re.S)
        
        if not relist:
            return None
        else:
            try:
                getdate=datetime.strptime(day, '%b %d, %Y')
                return getdate
            except Exception:
                return datetime.strptime(day, '%B %d, %Y')

st['date']=st['date'].map(lambda x: checkdate(x))
st['publisher']=st['publisher'].map(lambda x: strangecharacters(x))

def getgenre(genres, genrelist):
    for genre in genres:
        if genre not in genrelist:
            genrelist.append(genre)
            st[genre+':genre']=0
    return genres
st['genre']=st['genre'].map(lambda x: getgenre(x, genrelist))
def parsephase(li):
    string=''
    for x in li:
        string=string+x+', '
    if len(string)<=2:
        return ''
    string=string[:-2]
    return string
def gettag(tags, taglist):
    for tag in tags:
        if tag not in taglist:
            taglist[tag]=1
        else:
            taglist[tag]+=1
    return tags
st['developers']=st['developers'].map(lambda x: parsephase(x))
st['populartag']=st['populartag'].map(lambda x: gettag(x,taglist))
taglist={k:v for k,v in taglist.items() if v>=200}
for tag in taglist:
    st[tag+':tag']=0

for idx, row in st.iterrows():
    for x in genrelist:
        if x in row['genre']:
            st.at[idx,x+':genre']=1
    for id1,val in taglist.items():
        if id1 in row['populartag']:
            st.at[idx,id1+':tag']=1


            
st=st.drop(columns=['_id','genre','price','populartag'])

st.to_csv(r'C:\Users\elina\Desktop\gamere.csv')