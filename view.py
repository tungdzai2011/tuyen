import requests
import threading
import secrets
import datetime
import time
import random
import re
from hashlib import md5
from concurrent.futures import ThreadPoolExecutor
from collections import defaultdict
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

class Signature:
    def __init__(self, params: str, data: str, cookies: str) -> None:
        self.params = params
        self.data = data
        self.cookies = cookies

    def hash(self, data: str) -> str:
        return str(md5(data.encode()).hexdigest())

    def calc_gorgon(self) -> str:
        gorgon = self.hash(self.params)
        gorgon += self.hash(self.data) if self.data else "0" * 32
        gorgon += self.hash(self.cookies) if self.cookies else "0" * 32
        gorgon += "0" * 32
        return gorgon

    def get_value(self):
        gorgon = self.calc_gorgon()
        return self.encrypt(gorgon)

    def encrypt(self, data: str):
        unix = int(time.time())
        len_key = 0x14
        key = [
            0xDF, 0x77, 0xB9, 0x40, 0xB9, 0x9B, 0x84, 0x83,
            0xD1, 0xB9, 0xCB, 0xD1, 0xF7, 0xC2, 0xB9, 0x85,
            0xC3, 0xD0, 0xFB, 0xC3,
        ]

        param_list = []
        for i in range(0, 12, 4):
            temp = data[8 * i : 8 * (i + 1)]
            for j in range(4):
                H = int(temp[j * 2 : (j + 1) * 2], 16)
                param_list.append(H)

        param_list.extend([0x0, 0x6, 0xB, 0x1C])
        H = int(hex(unix), 16)
        param_list.extend([(H >> 24) & 0xFF, (H >> 16) & 0xFF, (H >> 8) & 0xFF, H & 0xFF])

        eor_result_list = [A ^ B for A, B in zip(param_list, key)]

        for i in range(len_key):
            C = self.reverse(eor_result_list[i])
            D = eor_result_list[(i + 1) % len_key]
            E = C ^ D
            F = self.rbit(E)
            H = ((F ^ 0xFFFFFFFF) ^ len_key) & 0xFF
            eor_result_list[i] = H

        return {
            "X-Gorgon": "840280416000" + ''.join(self.hex_string(x) for x in eor_result_list),
            "X-Khronos": str(unix)
        }

    def rbit(self, num):
        return int(bin(num)[2:].zfill(8)[::-1], 2)

    def hex_string(self, num):
        return hex(num)[2:].zfill(2)

    def reverse(self, num):
        tmp = self.hex_string(num)
        return int(tmp[1:] + tmp[0], 16)

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
                                                @DucTuyenDev
"""
print(banner)
link = input('Link Video TIKTOK: ')
headers_id = {
    'Connection': 'close',
    'Pragma': 'no-cache',
    'Cache-Control': 'no-cache',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.114 Safari/537.36',
    'Accept': 'text/html'
}
try:
    page = requests.get(link, headers=headers_id, timeout=10).text
    match = re.search(r'"video":\{"id":"(\d+)"', page)
    if match:
        video_id = match.group(1)
        print(f'[+] Lấy ID Video thành công: {video_id}')
    else:
        print('[-] Không tìm thấy ID Video')
        exit(1)
except Exception as e:
    print(f'[-] Lỗi khi lấy ID Video: {e}')
    exit(1)

# ====== PROXY ======
proxy_fails = defaultdict(int)

def selec_proxy():
    with open('proxy.txt', 'r', encoding='utf8') as f:
        proxy_lines = [line.strip() for line in f if line.strip()]
        available = [p for p in proxy_lines if proxy_fails[p] < 5]
        if not available:
            print("\033[93m[!] HẾT PROXY SỐNG, RESET TOÀN BỘ\033[0m")
            for p in proxy_lines:
                proxy_fails[p] = 0
            available = proxy_lines.copy()
        proxy = random.choice(available)
        return {"http": proxy}, proxy

# ====== GỬI VIEW ======
def send_view():
    url_view = 'https://api16-core-c-alisg.tiktokv.com/aweme/v1/aweme/stats/?ac=WIFI&op_region=VN'
    while True:
        random_hex = secrets.token_hex(16)
        device_id = str(random.randint(10**18, 10**19 - 1))
        headers_view = {
            'Host': 'api16-core-c-alisg.tiktokv.com',
            'Content-Length': '138',
            'Content-Type': 'application/x-www-form-urlencoded',
            'Sdk-Version': '2',
            'Passport-Sdk-Version': '5.12.1',
            'X-Tt-Token': '01023a1f6dd9980263ef2c0909abcdefabcdefabcdefabcdefabcdefabcdefabcdefabcdef - 1.0.0',
            'User-Agent': f'com.ss.android.ugc.trill/300305 (Linux; Android 12; CPH{random.randint(1000,9999)} Build/SP1A.210812.016)',
            'Accept-Encoding': 'gzip',
            'X-Ss-Stub': '1188F3E45D4C09AA34A9F6D9B9ACD34B',
            'X-Tt-Store-Idc': 'sg',
            'X-Tt-Store-Region': 'sg',
            'X-Ss-Dp': '1233',
            'X-Tt-Trace-Id': '00-abcdef11223344556677889900abcdef-01',
            'X-Khronos': '1721483333',
            'X-Gorgon': '0404b0d84006',
            'X-Common-Params-V2': (
                f"version_code=30.3.5&app_name=trill&app_version=30.3.5&carrier_region=VN"
                f"&channel=googleplay&mcc_mnc=45201&device_id={device_id}"
                f"&iid=7214447777888888888&openudid=aabbccddeeff1122"
                f"&cdid=22334455-6677-8899-aabb-ccddeeff0011&tz_offset=25200"
                f"&tz_name=Asia%2FHo_Chi_Minh&os_version=12&os_api=31"
                f"&device_platform=android&build_number=300305"
                f"&device_type=CPH2333&device_brand=oppo&account_region=VN"
                f"&sys_region=VN&aid=1233"
            )
        }

        cookie_view = {'sessionid': random_hex}
        start = datetime.datetime(2020, 1, 1, 0, 0, 0)
        end = datetime.datetime(2024, 12, 31, 23, 59, 59)
        delta_seconds = int((end - start).total_seconds())
        random_dt = start + datetime.timedelta(seconds=random.randint(0, delta_seconds))
        data = {
            'action_time': int(time.time()),
            'aweme_type': 0,
            'first_install_time': int(random_dt.timestamp()),
            'item_id': video_id,
            'play_delta': 1,
            'tab_type': 4
        }

        try:
            proxy, proxy_str = selec_proxy()
            r = requests.post(url_view, data=data, headers=headers_view, cookies=cookie_view, proxies=proxy, timeout=10, verify=False)

            try:
                json_data = r.json()
                print(f"\033[92m[Y] THÀNH CÔNG {proxy_str}\033[0m ➜ \033[96m{json_data}\033[0m")
            except Exception:
                proxy_fails[proxy_str] += 1
                
        except Exception as e:
            proxy_fails[proxy_str] += 1
            
# ====== CHẠY 500 LUỒNG ======
with ThreadPoolExecutor(max_workers=500) as executor:
    while True:
        executor.submit(send_view)
        time.sleep(0.01)
