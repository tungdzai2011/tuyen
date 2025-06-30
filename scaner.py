import requests
import concurrent.futures
import os
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
print(banner)
GET_URLS = [
    'https://www.proxyscan.io/api/proxy?format=txt&type=http',
    'https://raw.githubusercontent.com/TheSpeedX/PROXY-List/master/http.txt',
    'https://raw.githubusercontent.com/monosans/proxy-list/main/proxies/http.txt',
    'https://raw.githubusercontent.com/sunny9577/proxy-scraper/master/proxies.txt',
    'https://raw.githubusercontent.com/jetkai/proxy-list/main/online-proxies/txt/proxies-http.txt'
]

OUTPUT_FILE = 'proxy.txt'
TEST_URL = 'http://httpbin.org/ip'
TIMEOUT = 5
MAX_THREADS = 100

live_proxies = set()

def fetch_proxies():
    proxies = set()
    print('[INFO] Fetching proxies...')
    for url in GET_URLS:
        try:
            res = requests.get(url, timeout=10)
            if res.status_code == 200:
                fetched = res.text.strip().splitlines()
                proxies.update(p.strip() for p in fetched if p.strip())
                print(f'[+] {len(fetched)} proxies from {url}')
        except Exception as e:
            print(f'[ERROR] Failed to fetch from {url}: {e}')
    print(f'[INFO] Total fetched: {len(proxies)} proxies\n')
    return proxies

def is_proxy_alive(proxy):
    try:
        proxies = {
            'http': f'http://{proxy}',
            'https': f'http://{proxy}',
        }
        res = requests.get(TEST_URL, proxies=proxies, timeout=TIMEOUT)
        if res.status_code == 200:
            print(f'[LIVE] {proxy}')
            return proxy
    except:
        pass
    return None

def check_proxies(proxies):
    print('[INFO] Checking proxies...')
    with concurrent.futures.ThreadPoolExecutor(max_workers=MAX_THREADS) as executor:
        results = list(executor.map(is_proxy_alive, proxies))
    live = [p for p in results if p]
    return list(set(live))  # Loại bỏ proxy trùng

def save_to_file(proxies):
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        for proxy in proxies:
            f.write(proxy + '\n')
    print(f'\n[SAVED] {len(proxies)} live proxies saved to "{OUTPUT_FILE}"')

def main():
    if os.path.exists(OUTPUT_FILE):
        os.remove(OUTPUT_FILE)
    all_proxies = fetch_proxies()
    alive_proxies = check_proxies(all_proxies)
    save_to_file(alive_proxies)
    print('\n[FINISHED] Proxy scan done.')

if __name__ == '__main__':
    main()
