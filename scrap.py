import requests
from bs4 import BeautifulSoup
import re
from pprint import pprint

uName = 'nikhilksingh97'

def getURL(uName,pg):
    subURLs=[]

    for Pg in range(0,pg):

        url = 'https://www.codechef.com/submissions?page='+str(Pg)+'&sort_by=All&sorting_order=asc&language=All&status=All&year=2017&handle='+uName+'&pcode=&ccode=&Submit=GO'

        resp = requests.get(url)

        soup = BeautifulSoup(resp.content,'html5lib')

        table = soup.findAll('div',attrs = {'class':'tablebox'})

        tbody = table[0].table.tbody

        submissions = tbody.findAll('tr')

        subnos=[]

        for sub in submissions:
            no = sub.td.text
            subnos.append(no)


        for sNo in subnos:
            sNo = 'https://www.codechef.com/viewsolution/'+sNo
            subURLs.append(sNo)

    return subURLs

def getPg(uName):
    url= 'https://www.codechef.com/submissions?sort_by=All&sorting_order=asc&language=All&status=All&year=2017&handle='+uName+'&pcode=&ccode=&Submit=GO'
    page = requests.get(url)

    soup = BeautifulSoup(page.content,'html5lib')

    soup = soup.findAll('div',attrs = {'class':'pageinfo'})
    soup = soup[0].text
    soup = re.findall('\d+',soup)
    Pg = soup[1]
    return Pg

pg=int(getPg(uName))
URLs = getURL(uName,pg)
subCount = len(URLs)
print(pg)
print("total no. of submissions = "+str(subCount))
pprint(URLs)
