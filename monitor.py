import time
import requests
from bs4 import BeautifulSoup

PRODUCTS = [
    ("Seyberts", "https://seyberts.com/products/predator-bk-rush-sport-wrap-break-cue"),
    ("Manning", "https://manningcues.com/Predator-BK-RUSH-Sport-Wrap-Break-Cue.html"),
    ("ProPoolStore", "https://propoolstore.com/products/predator-bk-rush-jump-prerbjn-black-no-wrap"),
    ("PoolDawg", "https://www.pooldawg.com/predator-bk-rush-break-cue"),
    ("Predator官网", "https://www.predatorcues.com/pool-cues/predator-bk-rush-break-cue-no-wrap.html")
]

HEADERS = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}

# 请替换为你的Server酱推送地址，格式如下
SERVER_CHAN_KEY = "https://sctapi.ftqq.com/SCT285119TmMr86U7lD646Bo9xXVjjBEoM.send"

def send_wechat_push(title, message):
    try:
        data = {"title": title, "desp": message}
        response = requests.post(SERVER_CHAN_KEY, data=data)
        if response.status_code == 200:
            print("微信推送成功")
        else:
            print("微信推送失败:", response.text)
    except Exception as e:
        print("微信推送异常:", e)

def check_stock():
    for name, url in PRODUCTS:
        try:
            res = requests.get(url, headers=HEADERS, timeout=10)
            html = res.text
            if "Out of Stock" in html or "Sold Out" in html:
                print(f"{name} 缺货中")
            elif "Add to Cart" in html or "In Stock" in html:
                print(f"{name} 有货啦！")
                send_wechat_push(f"{name} BK Rush 有货", url)
            else:
                print(f"{name} 库存状态未知")
        except Exception as e:
            print(f"检查 {name} 时出错:", e)

if __name__ == "__main__":
    while True:
        print("开始检查库存:", time.strftime("%Y-%m-%d %H:%M:%S"))
        check_stock()
        time.sleep(600)  # 每10分钟检查一次
