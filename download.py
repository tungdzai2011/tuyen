import requests
import os

def get_video_info(platform, url):
    if platform == "youtube":
        api_url = f"https://subhatde.id.vn/youtube/download?url={url}"
    elif platform == "tiktok":
        api_url = f"https://subhatde.id.vn/tiktok/downloadvideo?url={url}"
    elif platform == "facebook":
        api_url = f"https://subhatde.id.vn/fb/download?url={url}"
    else:
        return None

    response = requests.get(api_url)
    if response.status_code == 200:
        return response.json()
    else:
        print("Lỗi khi gọi API!")
        return None

def download_video(video_url, title, platform="youtube"):
    response = requests.get(video_url, stream=True)
    if response.status_code == 200:
        filename = f"{title}.mp4".replace("/", "-")
        with open(filename, 'wb') as f:
            for chunk in response.iter_content(chunk_size=1024 * 1024):
                if chunk:
                    f.write(chunk)
        print(f"[{platform.upper()}] Tải xuống hoàn tất: {filename}")
    else:
        print(f"[{platform.upper()}] Lỗi khi tải video!")

def youtube_download():
    url = input("Nhập link YouTube: ").strip()
    video_info = get_video_info("youtube", url)

    if video_info:
        title = video_info['title']
        video_links = [media for media in video_info['media'] if media['type'] == 'video']

        if video_links:
            print(f"Tiêu đề: {title}")
            print("Chất lượng có sẵn:")
            for i, video in enumerate(video_links):
                print(f"{i + 1}. {video['quality']} - {video['mimeType']}")
            
            choice = int(input("Chọn chất lượng cần tải (nhập số): "))
            if 1 <= choice <= len(video_links):
                selected_video = video_links[choice - 1]
                download_video(selected_video['url'], title, platform="youtube")
            else:
                print("Lựa chọn không hợp lệ!")
        else:
            print("Không tìm thấy link video!")
    else:
        print("Không lấy được thông tin video!")

def tiktok_download():
    url = input("Nhập link TikTok: ").strip()
    video_info = get_video_info("tiktok", url)

    if video_info and 'url' in video_info:
        title = video_info.get('title', 'tiktok_video')
        download_video(video_info['url'], title, platform="tiktok")
    else:
        print("Không lấy được thông tin video TikTok!")

def facebook_download():
    url = input("Nhập link Facebook: ").strip()
    video_info = get_video_info("facebook", url)

    if video_info and 'url' in video_info:
        title = video_info.get('title', 'facebook_video')
        download_video(video_info['url'], title, platform="facebook")
    else:
        print("Không lấy được thông tin video Facebook!")

def main():
    while True:
        print("""\n
███████╗ ██████╗  ██████╗██╗ █████╗ ██╗         ███╗   ██╗███████╗████████╗██╗    ██╗ ██████╗ ██████╗ ██╗  ██╗
██╔════╝██╔═══██╗██╔════╝██║██╔══██╗██║         ████╗  ██║██╔════╝╚══██╔══╝██║    ██║██╔═══██╗██╔══██╗██║ ██╔╝
███████╗██║   ██║██║     ██║███████║██║         ██╔██╗ ██║█████╗     ██║   ██║ █╗ ██║██║   ██║██████╔╝█████╔╝ 
╚════██║██║   ██║██║     ██║██╔══██║██║         ██║╚██╗██║██╔══╝     ██║   ██║███╗██║██║   ██║██╔══██╗██╔═██╗ 
███████║╚██████╔╝╚██████╗██║██║  ██║███████╗    ██║ ╚████║███████╗   ██║   ╚███╔███╔╝╚██████╔╝██║  ██║██║  ██╗
╚══════╝ ╚═════╝  ╚═════╝╚═╝╚═╝  ╚═╝╚══════╝    ╚═╝  ╚═══╝╚══════╝   ╚═╝    ╚══╝╚══╝  ╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═╝
                                                                                                              
██████╗  ██████╗ ██╗    ██╗███╗   ██╗██╗      ██████╗  █████╗ ██████╗                                         
██╔══██╗██╔═══██╗██║    ██║████╗  ██║██║     ██╔═══██╗██╔══██╗██╔══██╗                                        
██║  ██║██║   ██║██║ █╗ ██║██╔██╗ ██║██║     ██║   ██║███████║██║  ██║                                        
██║  ██║██║   ██║██║███╗██║██║╚██╗██║██║     ██║   ██║██╔══██║██║  ██║                                        
██████╔╝╚██████╔╝╚███╔███╔╝██║ ╚████║███████╗╚██████╔╝██║  ██║██████╔╝                                        
╚═════╝  ╚═════╝  ╚══╝╚══╝ ╚═╝  ╚═══╝╚══════╝ ╚═════╝ ╚═╝  ╚═╝╚═════╝                                         
                                                                                                              
@DucTuyenDev
                            """)
        print("1. Download YouTube")
        print("2. Download TikTok")
        print("3. Download Facebook")
        print("0. Thoát")
        choice = input("Chọn nền tảng (0-3): ").strip()

        if choice == "1":
            youtube_download()
        elif choice == "2":
            tiktok_download()
        elif choice == "3":
            facebook_download()
        elif choice == "0":
            print("Đã thoát chương trình.")
            break
        else:
            print("Lựa chọn không hợp lệ!")

if __name__ == "__main__":
    main()
