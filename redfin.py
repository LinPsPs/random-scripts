from bs4 import BeautifulSoup as soup
from urllib.request import urlopen as uReq
from lxml.html import fromstring
import requests

import csv
import pandas as pd

import random
import re
import time
import sys
from itertools import cycle
import traceback

def printProgressBar (iteration, total, decimals = 1, length = 45, fill = '█'):
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filledLength = int(length * iteration // total)
    bar = fill * filledLength + '-' * (length - filledLength)
    print('\r%s |%s| %s%% %s' % ("Progress:", bar, percent, "Complete"), end = '\r')
    if iteration == total: 
        print()

def getValue(item):
    if(item != None):
        return item.get_text()
    return ''

def InfoCrawler():
    AttributeErrorNum = 0
    df = pd.read_csv('redfin_2019_2020.csv')
    # add new rows
    df.insert(8, 'EST', value='')
    df.insert(9, 'WALK SCORE', value='')
    df.insert(10, 'BIKE SCORE', value='')
    df.insert(11, 'BEFORE 2018', value='')
    df.insert(12, 'ELEMENTARY', value='')
    df.insert(13, 'MIDDLE', value='')
    df.insert(14, 'HIGH', value='')
    # agents online ->
    user_agents = [
        'Mozilla/5.0 (Windows; U; Windows NT 5.1; it; rv:1.8.1.11) Gecko/20071127 Firefox/2.0.0.11',
        'Opera/9.25 (Windows NT 5.1; U; en)',
        'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; .NET CLR 1.1.4322; .NET CLR 2.0.50727)',
        'Mozilla/5.0 (compatible; Konqueror/3.5; Linux) KHTML/3.5.5 (like Gecko) (Kubuntu)',
        'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/535.19 (KHTML, like Gecko) Chrome/18.0.1025.142 Safari/535.19',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.7; rv:11.0) Gecko/20100101 Firefox/11.0',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.6; rv:8.0.1) Gecko/20100101 Firefox/8.0.1',
        'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.19 (KHTML, like Gecko) Chrome/18.0.1025.151 Safari/535.19']
    # get the website row
    count = -1
    for index, row in df.iterrows():
        count += 1
        website = row['URL (SEE http://www.redfin.com/buy-a-home/comparative-market-analysis FOR INFO ON PRICING)']
        header = {"User-Agent": random.choice(user_agents)}
        proxies = {'http': 'http://auto:2FX2L59pCkN2a8CZTeacYJbHF@proxy.apify.com:8000'}
        # get page url
        # page_html = requests.get(website, headers=header)
        page_html = requests.get(website, headers=header, proxies=proxies)
        print(page_html)
        bs = soup(page_html.text, 'html.parser')
        # redfin estimate
        item = bs.find('div', {'class': 'statsValue'})
        df.at[index, 'EST'] = getValue(item)
        # walk score & bike score
        for walkscore in bs.findAll('div', {'class': 'viz-container'}):
            df.at[index, 'WALK SCORE'] = getValue(walkscore.find('span', {'class': 'value fair'}))
            df.at[index, 'BIKE SCORE'] = getValue(walkscore.find('span', {'class': 'value poor'}))
        # school rate
        school = {}
        for school_entity in bs.findAll('tr', {'class': 'schools-table-row'}):
            school_name = school_entity.find('div', {'class': 'school-title'}).get_text()
            school_rate = school_entity.find('span', {'class': 'rating-num'}).get_text()
            school_distance = school_entity.find('td', {'class': 'distance-col'})
            school_distance = school_distance.find('div', {'class': 'value'}).get_text()
            if('Elementary' in school_name):
                if(school.setdefault('Elementary', None) != None):
                    if(int(school['Elementary'][1]) <= school_rate):
                        school['Elementary'] = [school_name, school_rate, school_distance]
                else:
                    school['Elementary'] = [school_name, school_rate, school_distance]
            elif('Middle' in school_name):
                if(school.setdefault('Middle', None) != None):
                    if(int(school['Middle'][1]) <= school_rate):
                        school['Middle'] = [school_name, school_rate, school_distance]
                else:
                    school['Middle'] = [school_name, school_rate, school_distance]
            elif('High' in school_name):
                if(school.setdefault('High', None) != None):
                    if(int(school['High'][1]) <= school_rate):
                        school['High'] = [school_name, school_rate, school_distance]
                else:
                    school['High'] = [school_name, school_rate, school_distance]
        # export school
        if('Elementary' in school.keys()):
            df.at[index, 'ELEMENTARY'] = school['Elementary']
        if('Middle' in school.keys()):
            df.at[index, 'MIDDLE'] = school['Middle']
        if('High' in school.keys()):
            df.at[index, 'HIGH'] = school['High']
        
        random_int = random.randint(5, 6)
        time.sleep(random_int)

        printProgressBar(count, df.shape[0] - 1)
    df.to_csv('out.csv')

def InfoCrawlerTest():
    AttributeErrorNum = 0
    df = pd.read_csv('foo.csv')
    # add new rows
    df.insert(1, 'EST', value='')
    df.insert(2, 'WALK SCORE', value='')
    df.insert(3, 'BIKE SCORE', value='')
    df.insert(4, 'BEFORE 2018', value='')
    df.insert(5, 'ELEMENTARY', value='')
    df.insert(6, 'MIDDLE', value='')
    df.insert(7, 'HIGH', value='')
    # get page url
    page_html = open('target.html', 'r')
    # page_html = requests.get(website, headers=header, proxies=proxies)
    bs = soup(page_html, 'html.parser')
    # redfin estimate
    item = bs.find('div', {'class': 'statsValue'})
    df.at[0, 'EST'] = getValue(item)
    # walk score & bike score
    for walkscore in bs.findAll('div', {'class': 'viz-container'}):
        df.at[0, 'WALK SCORE'] = getValue(walkscore.find('span', {'class': 'value fair'}))
        df.at[0, 'BIKE SCORE'] = getValue(walkscore.find('span', {'class': 'value poor'}))
    # school rate
    school = {}
    for school_entity in bs.findAll('tr', {'class': 'schools-table-row'}):
        school_name = school_entity.find('div', {'class': 'school-title'}).get_text()
        school_rate = school_entity.find('span', {'class': 'rating-num'}).get_text()
        school_distance = school_entity.find('td', {'class': 'distance-col'})
        school_distance = school_distance.find('div', {'class': 'value'}).get_text()
        if('Elementary' in school_name):
            if(school.setdefault('Elementary', None) != None):
                if(int(school['Elementary'][1]) <= school_rate):
                    school['Elementary'] = [school_name, school_rate, school_distance]
            else:
                school['Elementary'] = [school_name, school_rate, school_distance]
        elif('Middle' in school_name):
            if(school.setdefault('Middle', None) != None):
                if(int(school['Middle'][1]) <= school_rate):
                    school['Middle'] = [school_name, school_rate, school_distance]
            else:
                school['Middle'] = [school_name, school_rate, school_distance]
        elif('High' in school_name):
            if(school.setdefault('High', None) != None):
                if(int(school['High'][1]) <= school_rate):
                    school['High'] = [school_name, school_rate, school_distance]
            else:
                school['High'] = [school_name, school_rate, school_distance]
    # export school
    if('Elementary' in school.keys()):
        df.at[0, 'ELEMENTARY'] = school['Elementary']
    if('Middle' in school.keys()):
        df.at[0, 'MIDDLE'] = school['Middle']
    if('High' in school.keys()):
        df.at[0, 'HIGH'] = school['High']
    print(school)
    print(school.keys())
    df.to_csv('out_test.csv')

if __name__ == '__main__':
    print('Redfin Crawler starts... (Detroit Version)')
    InfoCrawler()

