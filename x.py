

fg = '\033[92m'
fr = '\033[91m'
fw = '\033[97m'
fy = '\033[93m'
fb = '\033[94m'
flc = '\033[96m'
bd = '\u001b[1m'
res = '\u001b[0m'

colors = [fg,fr,fy,fb,flc]

def moduleinstaller():
    modules = ['requests','colorama','bs4','selenium','console','html5lib','multiprocessing','wget','easygui','zipfile']
    for module in modules:
        try:
            if (sys.version_info[0] < 3):
                os.system('cd C:\Python27\Scripts & pip install {}'.format(module))
            else :
                os.system('py -m pip install {}'.format(module))
            print (' ')
            print (' [+] {} has been installed successfully.'.format(module))
            print (' ')
        except:
            print (' [-] Install {} manually.'.format(module))
            print (' ')

import os
import random
import time
import sys
try:
    from modules.Grabber import grab
    from modules.Grabber import reverse
    from modules import Laravel , logos , ShellFinder , BounceChecker , Checkers
except:
    moduleinstaller()

def clrscr():
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')
    return

def menu():
    print()
    time.sleep(0.12)
    print('{}[{}!{}]{} CODERS : {}@Nyx_FallagaTn{} & {}@Zingstrok{}'.center(os.get_terminal_size().columns , " ").format(flc,fr,flc,fw,fr,fw,fr,fw))
    time.sleep(0.12)
    print('{}[{}!{}]{} @Nyx_FallagaTn\'s GITHUB : {}https://github.com/NyxFallagaTn{}'.center(os.get_terminal_size().columns , " ").format(flc,fr,flc,fw,fg,fw))
    time.sleep(0.12)
    print('{}[{}!{}]{} @Zingstrok\'s GITHUB : {}https://github.com/kalvelign{}  '.center(os.get_terminal_size().columns , " ").format(flc,fr,flc,fw,fg,fw))
    time.sleep(0.12)
    print('\n\n')
    time.sleep(1)
    print('\t{}{}[{}+{}] {}SITES GRABBER :{}                    [{}+{}] {}REVERSERS :{} '.format(bd,fw,fg,fw,fr,fw,fg,fw,fr,fw))
    print()
    print('  {}[{}1{}]{} Zone-H + Auto Grab Cookies                 {}[{}8{}]{} ReverseIP'.format(fg,fr,fg,fw,fg,fr,fg,fw))
    print('  {}[{}2{}]{} Zone-Xsec                                  {}[{}9{}]{} Lews'.format(fg,fr,fg,fw,fg,fr,fg,fw))
    print('  {}[{}3{}]{} Haxor                                      {}[{}10{}]{} Rapiddns'.format(fg,fr,fg,fw,fg,fr,fg,fw))
    print('  {}[{}4{}]{} Defacer Pro                                {}[{}11{}]{} TnTcode'.format(fg,fr,fg,fw,fg,fr,fg,fw))
    print('  {}[{}5{}]{} HypeStat                                   {}[{}12{}]{} AskDNS'.format(fg,fr,fg,fw,fg,fr,fg,fw))
    print('  {}[{}6{}]{} Cubdomain                                  {}[{}13{}]{} Reverse with all [{} All Previous Options Together {}]'.format(fg,fr,fg,fw,fg,fr,fg,fw,fr,fw))
    print('  {}[{}7{}]{} SiteRankData'.format(fg,fr,fg,fw))
    print()
    print('\t{}{}[{}+{}] {}LARAVEL CRACKER :{}                  [{}+{}] {}OTHER CHECKERS :{}'.format(bd,fw,fg,fw,fr,fw,fg,fw,fr,fw))
    print()
    print('  {}[{}14{}]{} Laravel Cracker                           {}[{}19{}]{} Twillio Balance Checker  '.format(fg,fr,fg,fw,fg,fr,fg,fw))
    print('  [{}SMTP {}/{} AWS {}/{} TWILIO {}/{} SMS {}/{} ...{}]              {}[{}20{}]{} Movider Balance Checker  '.format(random.choice(colors),fw,random.choice(colors),fw,random.choice(colors),fw,random.choice(colors),fw,random.choice(colors),fw,fg,fr,fg,fw))
    print('                                                 {}[{}21{}]{} Textlocal Balance Checker'.format(fg,fr,fg,fw))
    print('\t{}{}[{}+{}] {}SHELL FINDER :{}                       {}[{}22{}]{} cPanel Checker           '.format(bd,fw,fg,fw,fr,fw,fg,fr,fg,fw))
    print('                                                 {}[{}23{}]{} Whm Checker              '.format(fg,fr,fg,fw))
    print('  {}[{}15{}]{} Shell Finder [ {}By Known Names{} ]           {}[{}24{}]{} Webmail Checker          '.format(fg,fr,fg,fw,fg,fw,fg,fr,fg,fw))
    print('       + Index Of Searcher')
    print('  {}[{}16{}]{} Shell Finder [ {}By Given Names{} ]'.format(fg,fr,fg,fw,fg,fw))
    print('  {}[{}17{}]{} Shell Checker [ {}Check & Filter Shells{} ]'.format(fg,fr,fg,fw,fr,fw))
    print()
    print('\t{}{}[{}+{}] {}VALIDATORS :{} '.format(bd,fw,fg,fw,fr,fw))
    print()
    print('  {}[{}18{}]{} Validate Emails [{}Bounce Checker{}]'.format(fg,fr,fg,fw,fr,fw))
    print('\n')
    choice = input('{}Choose >{} '.format(fr,fw))
    match choice:
        case '1':
            clrscr()
            logos.main()
            grab.zone_h()
        case '2':
            clrscr()
            logos.main()
            grab.zone_xsec()
        case '3':
            clrscr()
            logos.main()
            grab.haxor()
        case '4':
            clrscr()
            logos.main()
            grab.defacerPro()
        case '5':
            clrscr()
            logos.main()
            grab.Hypestat()
        case '6':
            clrscr()
            logos.main()
            grab.cubdomain()
        case '7':
            clrscr()
            logos.main()
            grab.siterankdata()
        case '8':
            clrscr()
            logos.main()
            reverse.reverse_ip(choice)
        case '9':
            clrscr()
            logos.main()
            reverse.lews_reverse(choice)
        case '10':
            clrscr()
            logos.main()
            reverse.rapiddns(choice)
        case '11':
            clrscr()
            logos.main()
            reverse.tntcode(choice)
        case '12':
            clrscr()
            logos.main()
            reverse.askdns(choice)
        case '13':
            clrscr()
            logos.rev()
            reverse.AllInOne()
        case '14':
            clrscr()
            logos.laravel()
            Laravel.check()
        case '15':
            clrscr()
            logos.shellfinder()
            ShellFinder.SFsearch()
        case '16':
            clrscr()
            logos.shellfinder()
            ShellFinder.SFsearch_names()
        case '17':
            clrscr()
            logos.shellfinder()
            ShellFinder.SFcheck()
        case '18':
            clrscr()
            logos.bounce()
            BounceChecker.check()
        case '19':
            clrscr()
            logos.other_checker()
            Checkers.twillio()
        case '20':
            clrscr()
            logos.other_checker()
            Checkers.movider()
        case '21':
            clrscr()
            logos.other_checker()
            Checkers.textlocal()
        case '22':
            clrscr()
            logos.other_checker()
            Checkers.cpanel()
        case '23':
            clrscr()
            logos.other_checker()
            Checkers.whm()
        case '24':
            clrscr()
            logos.other_checker()
            Checkers.webmail()

if __name__ == '__main__':
    clrscr()
    logos.main()
    menu()