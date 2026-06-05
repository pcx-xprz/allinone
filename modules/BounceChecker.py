import requests
import console
from re import findall as reg
from concurrent.futures import ThreadPoolExecutor

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

def tt(email):
    payload = {
        'email': '{}'.format(email),
        'index': 0,
        'token': 12345,
        'frommail': '835468954@qq.com',
        'timeout': 10,
        'scan_port': 25
        }
    req = requests.post('https://check.emailverifier.online/bulk-verify-email/functions/quick_mail_verify_no_session.php' , headers=headers , data=payload).text
    if '"status":"invalid"' not in str(req):
        print('{}[{}+{}] {} >> {}VALID{}'.format(fw,fg,fw,email,fg,fw))
        open('Valid.txt','a',errors='ignore').write(email + '\n')
    else:
        print('{}[{}-{}] {} >> {}INVALID{}'.format(fw,fr,fw,email,fr,fw))
        open('InValid.txt','a',errors='ignore').write(email + '\n')

def check():
    lista = list(x.strip() for x in open(input('{}[{}#{}] List : '),'r',errors='ignore').readlines())
    try:
        ThreadPoolExecutor(100).map(tt, lista)
    except:
        pass

