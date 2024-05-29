# 20220127 쿠팡 검색결과
import random
import re
import tkinter.filedialog
from datetime import *
from tkinter import *

import requests
from bs4 import BeautifulSoup

market_no_id = [''] # 마켓 아이디
market_roc_id = [''] # 제품 아이디

market_plus_id = market_no_id, market_roc_id

def deleteTextBox():
    result_ent.delete('1.0', END)

def searchkeyword(word):
    deleteTextBox()
    cookienum = random.randint(27352723261168547964133, 47352723261168547964133)

    header = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.99 Safari/537.36 Edg/97.0.1072.69',
          'cookie': 'PCID='+str(cookienum)+';'
          }

    word = word_area.get()
    result_ent.insert(tkinter.INSERT, "== " + str(datetime.now().strftime('%m-%d %H:%M')) + " " + word + " [PC] 쿠팡 == \n\n")
    rank = 0
    r = requests.get("https://www.coupang.com/np/search?component=&q="+str(word), headers=header)
    soup = BeautifulSoup(r.text, "html.parser")

    # pro = soup.find_all("li", attrs={"class" : re.compile("^search-product")})  # 상품 영역
    pro = soup.find_all("li", attrs={"class" : "search-product"})  # 상품 영역

    for i in pro:
        product_name = i.find("div", {"class": "name"}).text
        rank += 1
        ad_badge = i.find("span", attrs={"class": "ad-badge-text"})
        non = i.find("span", attrs={"class": re.compile("badges")})
        roc = i.find("span", attrs={"class": re.compile("badge rocket")})

        if str(market_plus_id).find(str(i['data-vendor-item-id'])) != -1:
            if ad_badge:
                result_ent.insert(tkinter.INSERT, str(rank) + ". [📃 AD] " + product_name[0:] + "\n\n")
            elif roc:
                result_ent.insert(tkinter.INSERT, str(rank) + ". [🚀 Rocket] " + product_name[0:] + "\n\n")
            else:
                result_ent.insert(tkinter.INSERT, str(rank) + ". [🚛 일반] " + product_name[0:] + "\n\n")

# Main Window 디자인 영역
root = Tk()
root.title('Coupang PC Search')
root.geometry("370x350")  # 가로 X 세로
root.resizable(FALSE, FALSE)

# Word area
word_area = tkinter.Entry(master=root, font=11)
word_area.place(x=70, y=10, width=250, height=25)

# Result area
result_ent = Text(root)
result_ent.place(x=10, y=50, width=350, height=290)
# result_ent.config(width=41, height=9)

# Enter Event
root.bind('<Return>', searchkeyword)
root.mainloop()
