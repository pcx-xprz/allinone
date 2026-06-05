import os
import time

fg = '\033[92m'
fr = '\033[91m'
fw = '\033[97m'
fy = '\033[93m'
fb = '\033[94m'
flc = '\033[96m'
bd = '\u001b[1m'
res = '\u001b[0m'

def laravel():
    print("{}                     ______                                 ".center(os.get_terminal_size().columns," ").format(fg))
    print('                  .-"      "-.                                '.center(os.get_terminal_size().columns," "))
    print("                 /            \\                              ".center(os.get_terminal_size().columns," "))
    print("                |              |                              ".center(os.get_terminal_size().columns," "))
    print("                |,  .-.  .-.  ,|                              ".center(os.get_terminal_size().columns," "))
    print("                | )(__/  \__)( |                              ".center(os.get_terminal_size().columns," "))
    print("                |/     /\     \|                              ".center(os.get_terminal_size().columns," "))
    print("      (@_       (_     ^^     _)         {}LARAVEL CRACKER{}  ".center(os.get_terminal_size().columns," ").format(fr,fg))
    print(" _     ) \_______\__|IIIIII|__/__________________________     ".center(os.get_terminal_size().columns," "))
    print("(_)@8@8<><________|-\IIIIII/-|___________________________>    ".center(os.get_terminal_size().columns," "))
    print("       )_/        \          /                                ".center(os.get_terminal_size().columns," "))
    print("      (@           `--------`               {}@Nyx_FallagaTn{}".center(os.get_terminal_size().columns," ").format(fr,fw))


def main():
    msg = """{}     ⣰⡆                      ⠐⣆           \    ⣴⠁⡇    {}@Nyx_FallagaTn{}    ⢀⠃⢣           \    ⢻ ⠸⡀                     ⡜ ⢸⠇           \    ⠘⡄⢆⠑⡄     ⢀⣀⣀⣠⣄⣀⣀⡀     ⢀⠜⢠⢀⡆           \     ⠘⣜⣦⠈⢢⡀⣀⣴⣾⣿⡛⠛⠛⠛⠛⠛⡿⣿⣦⣄ ⡠⠋⣰⢧⠎           \      ⠘⣿⣧⢀⠉⢻⡟⠁⠙⠃    ⠈⠋ ⠹⡟⠉⢠⢰⣿⠏           \       ⠘⣿⡎⢆⣸⡄          ⠠⣿⣠⢣⣿⠏           \       ⡖⠻⣿⠼⢽            ⢹⠹⣾⠟⢳⡄           \       ⡟⡇⢨ ⢸⡀           ⡎ ⣇⢠⢿⠇           \       ⢹⠃⢻⡤⠚    {}⣀  ⢀{}    ⠙⠢⡼ ⢻           \       ⠸⡓⡄{}⢹⠦⠤⠤⠤⢾⣇  ⢠⡷⠦⠤⠤⠴⢺{}⢁⠔⡟           \       ⢠⠁⣷{}⠈⠓⠤⠤⠤⣞⡻  ⢸⣱⣤⠤⠤⠔⠁{}⣸⡆⣇           \       ⠘⢲⠋⢦⣀⣠⢴⠶ {}⠁  ⠈⠁{}⠴⣶⣄⣀⡴⠋⣷⠋           \        ⣿⡀  ⢀⡘⠶⣄⡀   ⣠⡴⠞⣶ ⢀ ⣼           \        ⠈⠻⣌⢢⢸⣷⣸⡈⠳⠦⠤⠞⠁⣷⣼⡏⣰⢃⡾⠋           \          ⠙⢿⣿⣿⡇⢻⡶⣦⣤⡴⡾⢸⣿⣿⣷⠏           \            ⢿⡟⡿⡄⣳⣤⣤⣴⢁⣾⠏⡿⠁           \            ⠈⣷⠘⠒⠚⠉⠉⠑⠒⠊⣸⠇           \             ⠈⠳⠶⠔⠒⠒⠲⠴⠞⠋{}           \ """.format(fg,fr,fg,fr,fg,fr,fg,fr,fg,fr,fg,fw)
    line = ''
    lines = []
    for i in msg:
        if str(i) == '\\':
            lines.append(line)
            line = ''
        else:
            line += str(i)
    maxlen = 0
    for line in lines:
        if int(len(line)) > maxlen:
            maxlen = int(len(line))
    for line in lines:
        while int(len(line)) < maxlen:
            line += ' '
        print(str(line).center(os.get_terminal_size().columns , " "))
        time.sleep(0.12)

def shellfinder():
    colm = os.get_terminal_size().columns
    print("{}   .    _  .     _____________              ".center(colm," ").format(fg))
    time.sleep(0.12)
    print("   |\_|/__/|    /             \               ".center(colm," "))
    time.sleep(0.12)
    print("  / / \/ \  \  /  {}LET'S HACK{}   \          ".center(colm," ").format(fr,fg))
    time.sleep(0.12)
    print(" /__|{}O{}||{}O{}|__ \ \  {}EVERYTHING{}   /  ".center(colm," ").format(fr,fg,fr,fg,fr,fg))
    time.sleep(0.12)
    print("|/_ \_/\_/ _\ | \  ___________/               ".center(colm," "))
    time.sleep(0.12)
    print("| | (____) | ||  |/                           ".center(colm," "))
    time.sleep(0.12)
    print("\/\___/\__/  // _/                            ".center(colm," "))
    time.sleep(0.12)
    print("(_/         ||                                ".center(colm," "))
    time.sleep(0.12)
    print(" |          ||\                               ".center(colm," "))
    time.sleep(0.12)
    print("  \        //_/                               ".center(colm," "))
    time.sleep(0.12)
    print("   \______//                                  ".center(colm," "))
    time.sleep(0.12)
    print("  __|| __||      {}ICQ{} : @Nyx_FallagaTn{}   ".center(colm," ").format(fg,fw,fg))
    time.sleep(0.12)
    print(" (____(____)     {}TELEGRAM{} : @Nyx_FallagaTn".center(colm," ").format(fb,fw))
    time.sleep(0.12)
    print('\n\n')


def rev():
        print(f'{fr}██{fw}╗  {fr}██{fw}╗{fr}███████{fw}╗{fr}██████{fw}╗ {fr}███████{fw}╗{fr}██{fw}╗   {fr}██{fw}╗{fr}███████{fw}╗{fr}██████{fw}╗ {fr}███████{fw}╗{fr}███████{fw}╗{fr}██████{fw}╗                             '.center(os.get_terminal_size().columns , " "))
        time.sleep(0.12)
        print(f'{fw}╚{fr}██{fw}╗{fr}██{fw}╔╝{fr}██{fw}╔════╝{fr}██{fw}╔══{fr}██{fw}╗{fr}██{fw}╔════╝{fr}██{fw}║   {fr}██{fw}║{fr}██{fw}╔════╝{fr}██{fw}╔══{fr}██{fw}╗{fr}██{fw}╔════╝{fr}██{fw}╔════╝{fr}██{fw}╔══{fr}██{fw}╗'.center(os.get_terminal_size().columns , " "))
        time.sleep(0.12)
        print(f' {fw}╚{fr}███{fw}╔╝ {fr}███████{fw}╗{fr}██████{fw}╔╝{fr}█████{fw}╗  {fr}██{fw}║   {fr}██{fw}║{fr}█████{fw}╗  {fr}██████{fw}╔╝{fr}███████{fw}╗{fr}█████{fw}╗  {fr}██████{fw}╔╝                                '.center(os.get_terminal_size().columns , " "))
        time.sleep(0.12)
        print(f' {fr}██{fw}╔{fr}██{fw}╗ ╚════{fr}██{fw}║{fr}██{fw}╔══{fr}██{fw}╗{fr}██{fw}╔══╝  ╚{fr}██{fw}╗ {fr}██{fw}╔╝{fr}██{fw}╔══╝  {fr}██{fw}╔══{fr}██{fw}╗╚════{fr}██{fw}║{fr}██{fw}╔══╝  {fr}██{fw}╔══{fr}██{fw}╗    '.center(os.get_terminal_size().columns , " "))
        time.sleep(0.12)
        print(f'{fr}██{fw}╔╝ {fr}██{fw}╗{fr}███████{fw}║{fr}██{fw}║  {fr}██{fw}║{fr}███████{fw}╗ ╚{fr}████{fw}╔╝ {fr}███████{fw}╗{fr}██{fw}║  {fr}██{fw}║{fr}███████{fw}║{fr}███████{fw}╗{fr}██{fw}║  {fr}██{fw}║            '.center(os.get_terminal_size().columns , " "))
        time.sleep(0.12)
        print(f'{fw}╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝╚══════╝  ╚═══╝  ╚══════╝╚═╝  ╚═╝╚══════╝╚══════╝╚═╝  ╚═╝                                                                                                                        '.center(os.get_terminal_size().columns , " "))
        time.sleep(0.12)
        print('\n\n')
        

def bounce():
        print('{}╔╗ ╔═╗╦ ╦╔╗╔╔═╗╔═╗  ╔═╗╦ ╦╔═╗╔═╗╦╔═╔═╗╦═╗'.center(os.get_terminal_size().columns , " ").format(fg))
        print('╠╩╗║ ║║ ║║║║║  ║╣   ║  ╠═╣║╣ ║  ╠╩╗║╣ ╠╦╝  '.center(os.get_terminal_size().columns , " "))
        print('╚═╝╚═╝╚═╝╝╚╝╚═╝╚═╝  ╚═╝╩ ╩╚═╝╚═╝╩ ╩╚═╝╩╚═{}'.center(os.get_terminal_size().columns , " ").format(fw))
        print('\n\n')

def other_checker():
    print('{}╔═╗╔╦╗╦ ╦╔═╗╦═╗  ╔═╗╦ ╦╔═╗╔═╗╦╔═╔═╗╦═╗╔═╗'.center(os.get_terminal_size().columns , " ").format(fg))
    print('║ ║ ║ ╠═╣║╣ ╠╦╝  ║  ╠═╣║╣ ║  ╠╩╗║╣ ╠╦╝╚═╗  '.center(os.get_terminal_size().columns , " "))
    print('╚═╝ ╩ ╩ ╩╚═╝╩╚═  ╚═╝╩ ╩╚═╝╚═╝╩ ╩╚═╝╩╚═╚═╝{}'.center(os.get_terminal_size().columns , " ").format(fw))