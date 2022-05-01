from bs4 import BeautifulSoup as soup
from urllib.request import urlopen as uReq
from lxml.html import fromstring
import requests

import csv
import pandas as pd

import random
import re
import time
import os
from itertools import cycle
import traceback

def printProgressBar (iteration, total, decimals = 1, length = 45, fill = '█'):
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filledLength = int(length * iteration // total)
    bar = fill * filledLength + '-' * (length - filledLength)
    print('\r%s |%s| %s%% %s' % ("Progress:", bar, percent, "Complete"), end = '\r')
    if iteration == total: 
        print()

def jobInfoCrawler (searchRange: int, mode: bool):
    AttributeErrorNum = 0
    if mode:
        with open('result.csv', 'w', newline='') as of:
            f = csv.writer(of, delimiter=',')
            f.writerow(["title", "company", "addr", "salary", "summary"])
    user_agents = [
        'Mozilla/5.0 (Windows; U; Windows NT 5.1; it; rv:1.8.1.11) Gecko/20071127 Firefox/2.0.0.11',
        'Opera/9.25 (Windows NT 5.1; U; en)',
        'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; .NET CLR 1.1.4322; .NET CLR 2.0.50727)',
        'Mozilla/5.0 (compatible; Konqueror/3.5; Linux) KHTML/3.5.5 (like Gecko) (Kubuntu)',
        'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/535.19 (KHTML, like Gecko) Chrome/18.0.1025.142 Safari/535.19',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.7; rv:11.0) Gecko/20100101 Firefox/11.0',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.6; rv:8.0.1) Gecko/20100101 Firefox/8.0.1',
        'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.19 (KHTML, like Gecko) Chrome/18.0.1025.151 Safari/535.19']
    for i in range(0, searchRange, 1):
        headers = {"User-Agent": random.choice(user_agents)}
        page_html = None
        url = 'https://www.indeed.com/jobs?q=Python&l=New%20York%20State&start=' + str(i)
        page_html = requests.get(url, headers=headers)
        bs = soup(page_html.text, "html.parser")
        for item in bs.findAll("div", {"class": "jobsearch-SerpJobCard unifiedRow row result"}):
            try:
                cursor = item.find("a", {"class": "jobtitle turnstileLink"})
                title = cursor["title"].replace("\n", "")
                cursor = item.find("span", {"class": "company"})
                compnay = 'Null'
                if(cursor != None):
                    company = cursor.text.replace("\n", "")
                cursor = item.find("div", {"class": "location accessible-contrast-color-location"})
                addr = 'Null'
                if(cursor != None):
                    addr = cursor.text.replace("\n", "")
                cursor = item.find("span", {"class": "salaryText"})
                salary = 'Null'
                if(cursor != None):
                    salary = cursor.text.replace("\n", "")
                summary = ""
                count = 1
                for li in item.find("div", {"class": "summary"}).findAll("li"):
                    summary += str(count) + ". " + li.text.replace("\n", "") + "\n"
                    count += 1
                if mode:
                    with open('result.csv', 'a+', newline='') as of:
                        f = csv.writer(of, delimiter=',')
                        f.writerow([title, company, addr, salary, summary])
                else:
                    print("Title: " + title + "\nCompany: " + company + "\nAddress: " + addr
                        + "\nSalary: " + salary + "\nSummary: "+ summary + "\n")
            except AttributeError:
                AttributeErrorNum += 1
                continue
        if mode:
            printProgressBar(i, searchRange)
        random_int = random.randint(1, 2)
        time.sleep(random_int)
    print('\nDone! Attribute Error Occurs ' + str(AttributeErrorNum) + ' Times')

if __name__ == '__main__':
    print('Indeed Crawler starts... (New York Version)')
    proxy = ' '
    invalidInput = True
    while invalidInput:
        saveFile = input('Save to file (T/F): ')
        if saveFile.upper() == 'T' or saveFile.upper() == 'F':
            invalidInput = False
            print('Save to ' + os.getcwd() + '/result.csv')
        else:
            print('Invalid input. Please input T or F')
    invalidInput = True
    while invalidInput:
        searchRange = input('Please input search range(A num indicates how many job pages you want to get): ')
        if searchRange.isdigit():
            invalidInput = False
        else:
            print('You input is not a Num...\nTry again')
    if saveFile.upper() == 'T':
        jobInfoCrawler(int(searchRange), True)
    else:
        jobInfoCrawler(int(searchRange), False)