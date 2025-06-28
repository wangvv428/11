import time
import requests
from bs4 import BeautifulSoup
import os

PRODUCTS = [
    ("Seyberts", "https://seyberts.com/products/predator-bk-rush-sport-wrap-break-cue"),
    ("Predator官网", "https://www.predatorcues.com/pool-cues/predator-bk-rush-break-cue-no-wrap.html")
]

HEADERS = {"User-Agent": "Mozilla/5.0"}
SERVER_CHAN_KEY = os.environ.get("SCKEY", "")

def send_wechat_push(title, message):
    if not SERVER_CHAN_KEY:
        print("未配置微信推送密钥")
        return
    try:
        data = {"title": title, "desp": message}
        response = requests.post(SERVER_CHAN_KEY, data=data, timeout=5)
        if response.status_code == 200:
            print("✅ 微信推送成功")
        else:
            print("⚠️ 微信推送失败:", response.text)
    except Exception as e:
        print("❌ 推送异常:", e)

def check_stock():
    for name, url in PRODUCTS:
        print(f"🔍 正在检查 {name}...")
        try:
            res = requests.get(url, headers=HEADERS, timeout=8)
            html = res.text
            if "Out of Stock" in html or "Sold Out" in html:
                print(f"❌ {name} 缺货中")
            elif "Add to Cart" in html or "In Stock" in html:
                print(f"✅ {name} 有货！准备推送通知")
                send_wechat_push(f"{name} BK Rush 有货", url)
            else:
                print(f"❓ {name} 库存状态未知")
        except Exception as e:
            print(f"🚫 检查 {name} 出错：{e}")

if __name__ == "__main__":
    print("🕒 开始检查库存:", time.strftime("%Y-%m-%d %H:%M:%S"))
    check_stock()
