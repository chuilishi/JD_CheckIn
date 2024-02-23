import pickle

import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

options = Options()
options.add_argument("--headless")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
options.add_experimental_option("detach", True)
options.add_argument(
    "--user-agent=Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Mobile Safari/537.36")

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

# 打开网页
driver.get("https://m.jd.com/")

# 利用pickle来加载cookies
with open("cookies.pkl", "rb") as file:
    cookies = pickle.load(file)
    for cookie in cookies:
        driver.add_cookie(cookie)

# 重新加载页面以应用cookies
driver.refresh()

# 利用pickle来保存cookies
with open("cookies.pkl", "wb") as file:
    pickle.dump(driver.get_cookies(), file)
# find "pin" in cookies and write into pt.txt
with open("pt.txt", "w") as file:
    pt_key = ""
    pt_pin = ""
    for cookie in cookies:
        if cookie["name"] == "pt_key":
            pt_key = cookie["value"]
            print(cookie["value"])
        if cookie["name"] == "pt_pin":
            pt_pin = cookie["value"]
            print(cookie["value"])
    if pt_key == "" or pt_pin == "":
        print("error")
    file.write(pt_key+"\n"+pt_pin)
    file.flush()
    file.close()

with open("pt.txt") as file:
    pt_key = file.readline()
    pt_key = pt_key.replace("\n", "")
    pt_pin = file.readline()
    pt_pin= pt_pin.replace("\n", "")
    file.close()
cookie="pt_key={}; pt_pin={}".format(pt_key, pt_pin)
url = "https://api.m.jd.com/client.action?functionId=signBeanAct&body=%7B%22fp%22%3A%22-1%22%2C%22shshshfp%22%3A%22-1%22%2C%22shshshfpa%22%3A%22-1%22%2C%22referUrl%22%3A%22-1%22%2C%22userAgent%22%3A%22-1%22%2C%22jda%22%3A%22-1%22%2C%22rnVersion%22%3A%223.9%22%7D&appid=ld";
headers = {
    "Content-Type":"application/x-www-form-urlencoded; charset=UTF-8",
    "User-Agent": "okhttp/3.12.1;jdmall;android;version/10.3.4;build/92451;",
    "Cookie": cookie
}
response = requests.post(url=url, headers=headers)
print(response.text)
if response.json()["code"] != "0":
    raise Exception("签到失败")