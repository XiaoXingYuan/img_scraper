import tkinter as tk
from tkinter import filedialog
from bs4 import BeautifulSoup  # 載入插件
import requests
import os


def show_log(log):
    t.insert('insert', log)


def reform(url):  # 網址處理
    if url.startswith("//"):
        return "http:" + url
    else:
        return url


def select_path():  # 路徑選擇
    e2.delete('0', 'end')
    e2.insert('insert', os.path.abspath(filedialog.askdirectory()))  # 查詢並寫入下載路徑


def run():  # 開始運行
    path = e2.get()
    page = requests.get(e1.get())  # 查詢網址
    soup = BeautifulSoup(page.content, 'html.parser')  # 獲取&分析網頁源代碼
    times = 0
    img_count = 0
    for img in soup.select("img"):  # 篩選圖片鏈接
        try:  # 偵測錯誤
            img = reform(img["data-src"])  # 篩選"data-src"類別圖片
            times += 1
            show_log(f"圖片{times}網址：{img}")
            download_path = f"{path}\\img{times}.png"  # 設定下載目標路徑
            r = requests.get(img)  # 獲取圖片
            with open(download_path, 'wb') as f:  # 儲存圖片
                f.write(r.content)
            f.close()
        except KeyError:  # 路徑錯誤
            continue
        else:  # 下載成功
            show_log(f"圖片{times}已下載")
            img_count += 1
    for img in soup.select("img"):  # 篩選圖片鏈接
        try:  # 偵測錯誤
            img = reform(img["src"])  # 篩選"src"類別圖片
            times += 1
            show_log(f"圖片{times}網址：{img}")
            download_path = f"{path}\\img{times}.png"  # 設定下載目標路徑
            r = requests.get(img)  # 獲取圖片
            with open(download_path, 'wb') as f:  # 儲存圖片
                f.write(r.content)
            f.close()
        except KeyError:  # 路徑錯誤
            continue
        else:  # 下載成功
            show_log(f"圖片{times}已下載")
            img_count += 1
    show_log(f"{img_count}個圖片已下載到該資料夾")  # 所有圖片下載完畢


gui = tk.Tk()

gui.title('網頁圖片爬蟲')
gui.geometry('550x250')
gui.configure(background='white')

l1 = tk.Label(gui,
              text='網址:',
              font=('Arial', 12),
              width=16, height=1
              )
l1.grid(row=0, column=0)

e1 = tk.Entry(gui, width=38)
e1.grid(row=0, column=1, columnspan=2)  # 網址輸入框

l2 = tk.Label(gui,
              text='下載目標路徑:',
              font=('Arial', 12),
              width=16, height=1
              )
l2.grid(row=1, column=0)

e2 = tk.Entry(gui)
e2.grid(row=1, column=1)  # 下載目標地址輸入框

b2 = tk.Button(gui, text="路径选择", command=select_path)  # 選擇目標地址
b2.grid(row=1, column=2)

b1 = tk.Button(gui, text="開始", command=run)  # 開始按鈕
b1.grid(row=2, column=0, columnspan=3)

t = tk.Text(gui, height=2)
t.grid(row=3, column=0, columnspan=3)

gui.mainloop()
