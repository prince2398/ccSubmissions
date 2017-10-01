import requests
from bs4 import BeautifulSoup
import re
from pprint import pprint
import os
cnt=0

#to return extension of file
def calcExt(lang) :
    return {
        'C' : 'cpp',
        'PYTH' : 'py',
        'JAVA' : 'java',
        'C99' : 'cpp',
        'ADA' : 'ada',
        'PYPY' : 'py'
    }[lang]
#To write in  a file
def writeCode(filename,code):
    global cnt
    codeFile = open(filename,'a')

    for line in code:
        codeFile.write(line.text)
        codeFile.write('\n')

    codeFile.close()
    cnt+=1
#main function to write code in a file by sub no.
def subNoToFile(subNo):
    url = 'https://www.codechef.com/viewsolution/'+subNo+'/index.html'
    #to get html content
    resp = requests.get(url)
    soup = BeautifulSoup(resp.content,'html5lib')
    soup = soup.findAll('div',attrs = {'id': 'solutiondiv'})

    if len(soup)!=0:
        soup = soup[0]

        #to assign filename
        head = soup.title.text
        title = re.findall('\w+',head)
        ext = calcExt(title[3])
        filename = subNo+'.'+ext
        try:
            os.makedirs('submissions')
        except OSError:
            pass
        path = 'submissions/'+filename

        #to get submitted code in list line by line

        code = soup.pre.ol
        code = code.findAll('li')

        writeCode(path,code)


#to get list of submission ids of a searched year and a particular page
def getSubNo(uName,pg,yr):
    subNos=[]

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
                    subNos.append(no)

    return subNos


#to get total no. of pages in a search by username and year
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


#to get total list of all submission ids of a particular user
def subList(username):
    subs = []

    for yr in range(2017,2009,-1):
        pg=int(getPg(username,yr))
        subs = subs + getSubNo(username,pg,yr)

    return subs



#main program from username to files
uName = 'pp2398'

Subs = subList(uName)
for Sub in Subs:
    subNoToFile(Sub)
no = len(Subs)
msg = str(cnt)+'/'+str(no)+" no. of submmissions are extracted."
print(msg)
