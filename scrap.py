import requests
from bs4 import BeautifulSoup

uname = 'pp2398'
url = 'https://www.codechef.com/submissions?sort_by=All&sorting_order=asc&language=All&status=All&year=2017&handle='+uname+'&pcode=&ccode=&Submit=GO'

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
    url = 'https://www.codechef.com/viewsolution/'+sNo
    print(url+'\n')
