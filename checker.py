import requests
import time
from concurrent.futures import ThreadPoolExecutor

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
