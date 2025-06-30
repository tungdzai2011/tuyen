import requests
import time
from concurrent.futures import ThreadPoolExecutor
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
API_URL = 'https://proxy.thanhdieu.com/api/proxy'
HEADERS = {
    'accept': '*/*',
    'accept-language': 'vi-VN,vi;q=0.9',
    'content-type': 'application/x-www-form-urlencoded',
    'origin': 'https://proxy.thanhdieu.com',
    'referer': 'https://proxy.thanhdieu.com/',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36',
}
DATA = {
    'protocol': 'http',
    'count': '999999'
}

def get_proxy_list():
    try:
        response = requests.post(API_URL, headers=HEADERS, data=DATA)
        response.raise_for_status()

        result = response.json()  # ✅ Parse JSON đúng cách
        proxies = result.get("data", [])  # ✅ Lấy proxy từ mảng "data"

        print(f"🔎 Đã lấy {len(proxies)} proxy từ API")
        return proxies

    except Exception as e:
        print(f"❌ Lỗi khi lấy proxy: {e}")
        return []

def check_proxy(proxy):
    try:
        proxies = {"http": proxy, "https": proxy}
        r = requests.get("http://httpbin.org/ip", proxies=proxies, timeout=5)
        if r.status_code == 200:
            print(f"[LIVE] {proxy}")
            return proxy
    except:
        pass
    print(f"[DIE] {proxy}")
    return None

def main_loop():
    while True:
        print("\n🔄 Đang lấy proxy mới và kiểm tra live...")
        proxy_list = get_proxy_list()

        if not proxy_list:
            print("⚠️ Không có proxy để kiểm tra. Đợi 60 giây rồi thử lại.")
            time.sleep(60)
            continue

        with ThreadPoolExecutor(max_workers=50) as executor:
            results = executor.map(check_proxy, proxy_list)

        live_proxies = [proxy for proxy in results if proxy]

        with open("proxy.txt", "w") as f:
            for proxy in live_proxies:
                f.write(proxy + "\n")

        print(f"✅ Đã lưu {len(live_proxies)} proxy LIVE vào proxy.txt")
        print("🕐 Đợi 60 giây...\n")
        time.sleep(60)

if __name__ == "__main__":
    main_loop()
