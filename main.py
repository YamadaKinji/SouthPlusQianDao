from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os
import xml.etree.ElementTree as ET

cookie_value = os.getenv('COOKIE')
cookie_value = cookie_value.replace('\n', '').replace(' ', '')

url = 'https://south-plus.net/plugin.php'

chrome_options = Options()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')

driver = webdriver.Chrome(options=chrome_options)

def tasks(url, params, cookie_value, type):
    try:
        driver.get(url)

        for cookie in cookie_value.split(';'):
            name, value = cookie.split('=', 1)
            driver.add_cookie({'name': name.strip(), 'value': value.strip()})

        driver.get(f"{url}?{params}")
        
        # 等待并获取页面内容
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, "body"))
        )
        data = driver.page_source
        
        # 打印响应内容的前500个字符以便调试
        print(f"Response for {type}: {data[:500]}")

        # 保存原始响应内容到文件
        with open(f'raw_response_{type}.html', 'w', encoding='utf-8') as f:
            f.write(data)

        # 检查返回的数据是否包含HTML标签
        if '<html' in data.lower():
            raise Exception("服务器返回的内容包含HTML标签，可能是错误的请求或服务器问题。")

        # 解析XML数据
        root = ET.fromstring(data)
        cdata = root.text

        # 提取变量值
        values = cdata.split('\t')
        if '申请' in type:
            value_len = 2
        else:
            value_len = 3
        if len(values) == value_len:
            message = values[1]
            print(type + message)
        else:
            raise Exception("XML格式不正确，请检查COOKIE设置")
        if "还没超过" in message:
            return False
        else:
            return True

    except Exception as e:
        print(f"任务执行错误: {e}")
        return False
    finally:
        driver.quit()

params = "H_name=tasks&action=ajax&nowtime=1717167492479&verify=5af36471&actions=job&cid=15"

if tasks(url, params, cookie_value, "申请-日常: "):
    params = "H_name=tasks&action=ajax&nowtime=1717167492479&verify=5af36471&actions=job2&cid=15"
    tasks(url, params, cookie_value, "完成-日常: ")

params = "H_name=tasks&action=ajax&nowtime=1717167492479&verify=5af36471&actions=job&cid=14"

if tasks(url, params, cookie_value, "申请-周常: "):
    params = "H_name=tasks&action=ajax&nowtime=1717167492479&verify=5af36471&actions=job2&cid=14"
    tasks(url, params, cookie_value, "完成-周常: ")
