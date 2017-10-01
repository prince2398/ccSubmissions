import requests
from bs4 import BeautifulSoup
import re
from pprint import pprint

uName = 'singh_prishita'


def getURL(uName,pg,yr):
    subURLs=[]

    for Pg in range(0,pg):

        url = 'https://www.codechef.com/submissions?page='+str(Pg)+'&sort_by=All&sorting_order=asc&language=All&status=All&year='+str(yr)+'&handle='+uName+'&pcode=&ccode=&Submit=GO'

        resp = requests.get(url)

        soup = BeautifulSoup(resp.content,'html5lib')

        table = soup.findAll('div',attrs = {'class':'tablebox'})

        if len(table)!=0:

            tbody = table[0].table.tbody

            submissions = tbody.findAll('tr')

            for sub in submissions:
                no = sub.td.text
                if no!='No Recent Activity':
                    subURLs.append('https://www.codechef.com/viewsolution/'+no)

    return subURLs

def getPg(uName,yr):
    url= 'https://www.codechef.com/submissions?sort_by=All&sorting_order=asc&language=All&status=All&year='+str(yr)+'&handle='+uName+'&pcode=&ccode=&Submit=GO'
    page = requests.get(url)

    soup = BeautifulSoup(page.content,'html5lib')

    soup = soup.findAll('div',attrs = {'class':'pageinfo'})
    if len(soup)!=0 :
        soup = soup[0].text
        soup = re.findall('\d+',soup)
        Pg = soup[1]
        return Pg
    else:
        return 1;

URLs = []

for yr in range(2017,2009,-1):
    pg=int(getPg(uName,yr))
    URLs = URLs + getURL(uName,pg,yr)
subCount = len(URLs)
pprint(URLs)
print("total no. of submissions = "+str(subCount))


#Got URLS of Every submission by a user above(from all previous years)
