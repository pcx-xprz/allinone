import os
import wget
import socket
import console
import requests
import threading
from zipfile import ZipFile
from selenium import webdriver
from bs4 import BeautifulSoup as bs
from datetime import date, timedelta
from re import findall as reg , match
requests.packages.urllib3.disable_warnings()
from concurrent.futures import ThreadPoolExecutor
from selenium.webdriver.firefox.options import Options

fg = '\033[92m'
fr = '\033[91m'
fw = '\033[97m'
fy = '\033[93m'
fb = '\033[94m'
flc = '\033[96m'
bd = '\u001b[1m'
res = '\u001b[0m'

colors = [fg,fr,fy,fb,flc]

cas = ''

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36'}

class grab :
    def save_in_file(string,file):
        open(file,'a')
        if '/' in str(string):
            string = str(string).replace('www.','').replace('<','').replace('>','').split('/')[0]
        else:
            string = str(string).replace('www.','').replace('<','').replace('>','')
        check = list(x.strip() for x in open(file, 'r',errors='ignore').readlines())
        found = 0
        for sss in check:
            if str(string) == str(sss):
                found +=1
                break
        if found == 0:
            print('{}>>{} {}'.format(fg,fw,string))
            open(file,'a',errors='ignore').write(string + '\n')
        else:
            print('{}>>{} {}'.format(fr,fw,string))
        return
    
    def space_between(string1,string2,length):
        open('sites.txt','a')
        msg = '{}'.format(string1)
        count = int(len(string1)) + int(len(string2))
        while True:
            if count < int(length):
                count += 1
            else:
                break
        count = int(count) - (int(len(string1)) + int(len(string2)))
        for i in range(count):
            msg += ' '
        msg += '[ {}{}{} ]'.format(fr,string2,fw)
        check = list(x.strip() for x in open('sites.txt', 'r',errors='ignore').readlines())
        found = 0
        for chk in check:
            if str(string1) == str(chk):
                found +=1
                break
        if found == 0:
            msg = '{}[{}+{}]{} >>{} '.format(fw,fg,fw,fg,fw) + str(msg)
            open('sites.txt','a',errors='ignore').write(string1 + '\n')
        else:
            msg = '{}[{}-{}]{} >>{} '.format(fw,fr,fw,fr,fw) + str(msg)
        print(msg)
        return

    def zone_h():
        currentpath = os.path.dirname(os.path.abspath(__file__))
        if 'geckodriver.exe' not in os.listdir(currentpath):
            link = 'https://github.com/mozilla/geckodriver/releases/download/v0.31.0/geckodriver-v0.31.0-win64.zip'
            wget.download(link,currentpath)
            filename = str(link).split('/')[-1]
            with ZipFile('modules/{}'.format(filename), 'r') as zip: 
                zip.printdir()
                zip.extractall()
            os.remove('modules/{}'.format(filename))
        try:
            options = Options()
            options.headless = True
            driver = webdriver.Firefox(options=options)
        except:
            os.system('winget install --id Mozilla.Firefox')
            grab.zone_h()
        print('{}[{}INFO{}] GRABBING COOKIES..\n'.format(fw,fg,fw))
        driver.get('https://zone-h.org/archive')
        cookies = ''
        for i in driver.get_cookies():
            cookies += str(i)
        ZHE = reg("'ZHE', 'value': '(.*?)'", cookies)[0]
        PHPSESSID = reg("'PHPSESSID', 'value': '(.*?)'", cookies)[0]
        print('{}[{}INFO{}] COOKIES :\n[{}+{}] ZHE : {}{}{}\n[{}+{}] PHPSESSID : {}{}{}\n'.format(fw,fg,fw,fg,fw,fr,ZHE,fw,fg,fw,fr,PHPSESSID,fw))
        page = 0
        cookies = {'ZHE': '{}'.format(ZHE),'PHPSESSID': '{}'.format(PHPSESSID)}
        while True:
            page += 1
            url = 'https://zone-h.org/archive/page={}'.format(page)
            r = requests.get(url , headers=headers ,cookies=cookies).text
            r = str(r).replace('\n','').replace(' ','').replace('\t','')
            sites = reg('"></td><td></td><td>(.*?)</td><td>',str(r))
            sites = [sites for sites in sites if '...' not in str(sites)and '....' not in str(sites) and '..' not in str(sites)]
            sites = [*set(sites)]
            if str(sites) != '[]' and 'inputtype="text"name="captcha"value=""' not in str(r):
                for site in sites:
                    grab.save_in_file(site,'sites.txt')
            elif str(sites) == '[]' and 'inputtype="text"name="captcha"value=""' not in str(r):
                print('{}[{}+{}] FINISHED GRABBING ALL FROM {}ZONE-H{}'.format(fw,fg,fw,fr,fw))
                break
            else:
                options = Options()
                options.headless = False
                driver = webdriver.Firefox(options=options)
                driver.get('https://zone-h.org/archive')
                input('{}[{}!{}]{}CAPTCHA DETECTED! .\n{}[{}!{}]{} Press {}Enter{} to Continue!'.format(flc,fr,flc,fw,flc,fr,flc,fw,fr,fw))
                page = 0
        return
    
    def zone_xsec():
        page = 0
        while True:
            page += 1
            url = 'https://zone-xsec.com/archive/page={}'.format(page)
            r = requests.get(url , headers=headers).text
            r = str(r).replace('\n','')
            sites = reg('"></td><td></td><td>(.*?)</td><td><a',str(r))
            sites = [sites for sites in sites if '...' not in str(sites) and '....' not in str(sites) and '..' not in str(sites)]
            sites = [*set(sites)]
            if str(sites) != '[]':
                for site in sites:
                    grab.save_in_file(site,'sites.txt')
            else:
                break
        print('{}[{}+{}] FINISHED GRABBING ALL FROM {}ZONE-XSEC{}'.format(fw,fg,fw,fr,fw))
        return

    def haxor():
        page = 0
        while True:
            page += 1
            url = 'https://haxor.id/archive?page={}'.format(page)
            r = requests.get(url , headers=headers).text
            sites = reg("<a rel='nofollow' title='(.*?)'",str(r))
            sites = [sites for sites in sites if '...' not in str(sites) and '....' not in str(sites) and '..' not in str(sites)]
            sites = [*set(sites)]
            if str(sites) != '[]':
                for site in sites:
                    grab.save_in_file(site,'sites.txt')
            else:
                break
        print('{}[{}+{}] FINISHED GRABBING ALL FROM {}HAXOR{}'.format(fw,fg,fw,fr,fw))
        return

    def defacerProNotif(notif,cookies):
        try:
            url = 'https://defacer.pro/notif.php?id={}'.format(notif)
            r =requests.get(url , headers=headers, cookies=cookies,timeout=8).text
            site = reg('<div class="alert alert-warning" role="alert">(.*?)</div>',str(r))[0]
            site = str(site).strip().replace('///','//').replace('http://','').replace('https://','').replace('//','/').split('/')[0]
            grab.save_in_file(site,'sites.txt')
        except:
            pass

    def defacerPro():
        currentpath = os.path.dirname(os.path.abspath(__file__))
        if 'geckodriver.exe' not in os.listdir(currentpath):
            link = 'https://github.com/mozilla/geckodriver/releases/download/v0.31.0/geckodriver-v0.31.0-win64.zip'
            wget.download(link,currentpath)
            filename = str(link).split('/')[-1]
            with ZipFile(filename, 'r') as zip: 
                zip.printdir()
                zip.extractall()
            os.remove(filename)
        try:
            options = Options()
            options.headless = True
            driver = webdriver.Firefox(options=options)
        except:
            os.system('winget install --id Mozilla.Firefox')
            grab.defacerPro()
        print('{}[{}INFO{}] GRABBING COOKIES..\n'.format(fw,fg,fw))
        driver.get('https://defacer.pro/archive')
        cookies = ''
        for i in driver.get_cookies():
            cookies += str(i)
        PHPSESSID = reg("'PHPSESSID', 'value': '(.*?)'", cookies)[0]
        print('{}[{}INFO{}] COOKIES :\n[{}+{}] PHPSESSID : {}{}{}\n'.format(fw,fg,fw,fg,fw,fr,PHPSESSID,fw))
        cookies = {'PHPSESSID': '{}'.format(PHPSESSID)}
        print('{}[{}!{}]{} Please Wait Until Finishing grabbing all the Notifs.'.format(flc,fr,flc,fw))
        notifs = []
        page = 0
        while page < 50:
            page += 1
            url = 'https://defacer.pro/archive?page={}'.format(page)
            r = requests.get(url , headers=headers , cookies=cookies).text
            r = bs(r,'html.parser')
            links = r.find_all('a', href=True)
            for link in links:
                if 'notif.php?id=' in str(link):
                    notif = link.get('href')
                    notifs.append(str(notif).split('id=')[1].strip())
        notifs = [*set(notifs)]
        print('{}[{}!{}]{} Extracting Websites From [ {}{}{} ] Notifs.'.format(flc,fr,flc,fw,fr,len(notifs),fw))
        for n in notifs:
            threading.Thread(target=grab.defacerProNotif , args=[n,cookies]).start()

    def Hypestat():
        page = 0
        while True:
            page += 1
            url = 'https://hypestat.com/recently-updated/{}'.format(page)
            r = requests.get(url , headers=headers).text
            dates = reg('<dd>(.*?)<br>',str(r))
            r = bs(r,'html.parser')
            links = r.find_all('a', href=True)
            links = [str(link).split('https://hypestat.com/info/')[1].split('">')[0] for link in links if 'https://hypestat.com/info/' in str(link)]
            links = [*set(links)]
            for i in range(len(links)):
                grab.space_between(links[i],dates[i],50)

    def cubdomain():
        yesterday = date.today() - timedelta(days=1)
        yesterday = yesterday.strftime('%Y-%m-%d')
        page = 0
        while True:
            page += 1
            url = 'https://www.cubdomain.com/domains-registered-by-date/{}/{}'.format(yesterday , page)
            r = requests.get(url , headers=headers).text
            r = bs(r,'html.parser')
            links = r.find_all('a', href=True)
            sites = [str(link).split('https://www.cubdomain.com/site/')[1].split('">')[0] for link in links if 'https://www.cubdomain.com/site/' in str(link)]
            if str(sites) != '[]':
                for site in sites:
                    grab.save_in_file(site,'sites.txt')
            else:
                break

    def siterankdata():
        url = 'https://siterankdata.com/show/detected'
        r = requests.get(url , headers=headers).text
        r = str(r).split(' Newly detected sites')[1]
        r = bs(r , 'html.parser')
        firstdate = r.find('a',{'class':'btn btn-block btn-outline btn-default'},href = True)
        firstdate = str(firstdate).split('</i> ')[1].split('</a>')[0]
        x1 = 1
        x2 = 0
        while True:
            if (x1 == 1) and (x2 == 0):
                url = 'https://siterankdata.com/show/detected/{}/'.format(firstdate)
            else:
                url = 'https://siterankdata.com/show/detected/{}/{}-{}'.format(firstdate,x1,x2)
            req = requests.get(url).text
            req = bs(req,'html.parser')
            sites = req.find_all('h4',{'class':'m-b-xs'})
            if sites == []:break
            for site in sites:
                site = str(site).split('href="/')[1].split('"')[0]
                grab.save_in_file(site,'sites.txt')
            x1 +=1
            x2+=50

class reverse:
    def save(lista):
        rep = ['www.','cpanel.','ns1.','ns2.','ns3.','ns4.','cpcontacts.','cpcalendars.','webdisk.','hostmaster.','autodiscover.','webmail.','smtp.','whm.','mail.']
        for i in lista:
            if '<' not in str(i) and '>' not in str(i):
                for x in rep:
                    i = str(i).replace(x,'')
                open('Reversed.txt','a',errors='ignore').write(i + '\n')
        return

    def reverse_ip(host):
        try:
            url = 'https://api.reverseip.my.id/?ip={}'.format(host)
            req = requests.get(url , headers).text
            if '403 Forbidden' not in str(req):
                req = str(req).split('[')[1]
                sites = reg('"(.*?)"',str(req))
                sites = [*set(sites)]
                for i in sites:
                    allsites.append(i)
        except:
            pass
        return

    def lews_reverse(host):
        sites = []
        limit = 10
        try:
            url = 'https://lews.dev/r.php?ip={}'.format(host)
            req = requests.get(url , headers).text
            if '403 Forbidden' not in str(req):
                count = 0
                while str(req) == '':
                    req = requests.get(url , headers).text
                    count += 1
                    if count == limit : break
                if str(req) != '':
                    sites = reg('(.*?)\n',str(req))
                    sites = [str(sites).replace('www.','') for sites in sites]
                    sites = [*set(sites)]
                    for i in sites:
                        allsites.append(i)
        except:
            pass
        return

    def rapiddns(host):
        sites = []
        try:
            url = 'https://rapiddns.io/sameip/{}?full=1&down=1&t=None'.format(host)
            req = requests.get(url).text
            if '403 Forbidden' not in str(req):
                req = bs(req,'html.parser')
                if 'Total: <span style="color: #39cfca; ">0' not in str(req):
                    table = req.find('tbody')
                    table = str(table).replace('\n','')
                    sites = reg('</th><td>(.*?)</td><td><a',str(table))
                    sites = [str(sites).replace('www.','') for sites in sites]
                    sites = [*set(sites)]
                    for i in sites:
                        allsites.append(i)
        except:
            pass
        return

    def tntcode(host):
        try:
            url = 'https://domains.tntcode.com/ip/{}'.format(host)
            req = requests.get(url, headers).text
            if '403 Forbidden' not in str(req):
                sites = reg('<a href="/domain/(.*?)" style="text-decoration:none;"',str(req))
                sites = [*set(sites)]
                for i in sites:
                    allsites.append(i)
        except:
            pass
        return

    def askdns(host):
        try:
            url = 'https://askdns.com/ip/{}'.format(host)
            req = requests.get(url, headers).text
            if '403 Forbidden' not in str(req):
                sites = reg('<a href="/domain/(.*?)">',str(req))
                sites = [*set(sites)]
                for i in sites:
                    allsites.append(i)
        except:
            pass
        return

    def caller(host):
        global allsites
        allsites = []
        check = match(r"^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$",host)
        if check:
            reverse.reverse_ip(host)
            reverse.lews_reverse(host)
            reverse.rapiddns(host)
            reverse.tntcode(host)
            reverse.askdns(host)
            allsites = [*set(allsites)]
            if int(len(allsites)) != 0:
                print('{}[{}+{}] \u001b[42;1m{}\u001b[0m [{}{}{}]'.format(fw,fg,fw,host,fg,len(allsites),fw))
                reverse.save(allsites)
            else:
                print('{}[{}-{}] \u001b[41;1m{}\u001b[0m [{}{}{}]'.format(fw,fr,fw,host,fr,len(allsites),fw))
        else:
            ip = socket.gethostbyname(host)
            reverse.reverse_ip(ip)
            reverse.lews_reverse(ip)
            reverse.rapiddns(ip)
            reverse.tntcode(ip)
            reverse.askdns(ip)
            allsites = [*set(allsites)]
            if int(len(allsites)) != 0:
                print('{}[{}+{}] \u001b[42;1m{}\u001b[0m [{}{}{}]'.format(fw,fg,fw,host,fg,len(allsites),fw))
                reverse.save(allsites)
            else:
                print('{}[{}-{}] \u001b[41;1m{}\u001b[0m [{}{}{}]'.format(fw,fr,fw,host,fr,len(allsites),fw))

    def caller2(host):
        global allsites
        allsites = []
        check = match(r"^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$",host)
        if check:
            if cas == '8':
                reverse.reverse_ip(host)
            elif cas == '9':
                reverse.lews_reverse(host)
            elif cas == '10':
                reverse.rapiddns(host)
            elif cas == '11':
                reverse.tntcode(host)
            elif cas == '12':
                reverse.askdns(host)
            if int(len(allsites)) != 0:
                    print('{}[{}+{}] \u001b[42;1m{}\u001b[0m [{}{}{}]'.format(fw,fg,fw,host,fg,len(allsites),fw))
                    reverse.save(allsites)
            else:
                print('{}[{}-{}] \u001b[41;1m{}\u001b[0m [{}{}{}]'.format(fw,fr,fw,host,fr,len(allsites),fw))
        else:
            ip = socket.gethostbyname(host)
            if cas == '8':
                reverse.reverse_ip(ip)
            elif cas == '9':
                reverse.lews_reverse(ip)
            elif cas == '10':
                reverse.rapiddns(ip)
            elif cas == '11':
                reverse.tntcode(ip)
            elif cas == '12':
                reverse.askdns(ip)
            if int(len(allsites)) != 0:
                    print('{}[{}+{}] \u001b[42;1m{}\u001b[0m [{}{}{}]'.format(fw,fg,fw,host,fg,len(allsites),fw))
                    reverse.save(allsites)
            else:
                print('{}[{}-{}] \u001b[41;1m{}\u001b[0m [{}{}{}]'.format(fw,fr,fw,host,fr,len(allsites),fw))
        return

    def single_rev(cas):
        lista = list(x.strip() for x in open(input('{}[{}#{}] List : '),'r',errors='ignore').readlines())
        try:
            ThreadPoolExecutor(100).map(reverse.caller2 , lista)
        except:
            pass

    def AllInOne():
        lista = list(x.strip() for x in open(input('{}[{}+{}] List : '.format(fw,fg,fw)),'r',errors='ignore').readlines())
        try:
            ThreadPoolExecutor(100).map(reverse.caller , lista)
        except Exception as e:
            print(e)
            pass