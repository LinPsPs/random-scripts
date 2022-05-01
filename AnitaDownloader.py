from bs4 import BeautifulSoup as soup
import requests
import random
import urllib.request
import urllib.error

def Crawler(downloadPath, targetUrl):
    http = 'http'
    email = '@'
    user_agents = [
        'Mozilla/5.0 (Windows; U; Windows NT 5.1; it; rv:1.8.1.11) Gecko/20071127 Firefox/2.0.0.11',
        'Opera/9.25 (Windows NT 5.1; U; en)',
        'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; .NET CLR 1.1.4322; .NET CLR 2.0.50727)',
        'Mozilla/5.0 (compatible; Konqueror/3.5; Linux) KHTML/3.5.5 (like Gecko) (Kubuntu)',
        'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/535.19 (KHTML, like Gecko) Chrome/18.0.1025.142 Safari/535.19',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.7; rv:11.0) Gecko/20100101 Firefox/11.0',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.6; rv:8.0.1) Gecko/20100101 Firefox/8.0.1',
        'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.19 (KHTML, like Gecko) Chrome/18.0.1025.151 Safari/535.19']
    headers = {"User-Agent": random.choice(user_agents)}
    page_url = targetUrl
    page_html = requests.get(page_url, headers=headers)
    bs = soup(page_html.text, "html.parser")
    for link in bs.findAll('a', href = True):
        name = link.getText()
        file = link['href']
        if http in file:
            continue
        if email in file:
            continue
        href = link['href']
        filePath = page_url + href
        if '.' in href:
            postfix = (href.split('.'))[1]
        else:
            postfix = ''
        print("Name: " + name + "File: " + filePath)
        try :
            urllib.request.urlretrieve(filePath, downloadPath + name + postfix)
        except urllib.error.URLError:
            print("404")

if __name__ == '__main__':
    downloadPath = input("Input download path(ex: /home/user/): ")
    targetUrl = input("Anita Url: ")
    Crawler(downloadPath, targetUrl);
