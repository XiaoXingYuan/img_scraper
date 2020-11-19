from bs4 import BeautifulSoup  # 載入插件
import requests
import os


def reform(url):  # 網址處理
    if url.startswith("//"):
        return "http:" + url
    else:
        return url


def getInfo():
    global page, path
    page = requests.get(input("請輸入網址："))  # 查詢網址
    path = os.path.abspath(input("請輸入下載路徑："))  # 查詢下載路徑


def download(tag):
    global soup, times, img_count
    for img in soup.select("img"):  # 篩選圖片鏈接
        try:  # 偵測錯誤
            img = reform(img[tag])  # 篩選"data-src"類別圖片
            times += 1
            print(f"圖片{times}網址：{img}")
            download_path = f"{path}\\img{times}.png"  # 設定下載目標路徑
            r = requests.get(img)  # 獲取圖片
            with open(download_path, 'wb') as f:  # 儲存圖片
                f.write(r.content)
            f.close()
        except KeyError:  # 路徑錯誤
            continue
        else:  # 下載成功
            print(f"圖片{times}已下載")
            img_count += 1


def main():
    global soup, times, img_count
    getInfo()
    soup = BeautifulSoup(page.content, 'html.parser')  # 獲取&分析網頁源代碼
    times = 0
    img_count = 0
    download("data-src")
    download("src")
    print(f"{img_count}個圖片已下載到該資料夾")  # 所有圖片下載完畢
    end = input("請按任意鍵離開")


if __name__ == "__main__":
    main()
