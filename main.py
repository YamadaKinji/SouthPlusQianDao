import requests
import os
import xml.etree.ElementTree as ET
from bs4 import BeautifulSoup

cookie_value = os.getenv('COOKIE')
cookies = {cookie.split('=')[0]: cookie.split('=')[1] for cookie in cookie_value.split('; ')}

a_headers = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'accept-language': 'zh-CN,zh-TW;q=0.9,zh;q=0.8,en;q=0.7',
    'dnt': '1',
    'priority': 'u=0, i',
    'referer': 'https://www.south-plus.net/plugin.php?H_name-tasks-actions-newtasks.html.html',
    'sec-ch-ua': '"Google Chrome";v="125", "Chromium";v="125", "Not.A/Brand";v="24"',
    'sec-ch-ua-arch': '"x86"',
    'sec-ch-ua-bitness': '"64"',
    'sec-ch-ua-full-version': '"125.0.6422.142"',
    'sec-ch-ua-full-version-list': '"Google Chrome";v="125.0.6422.142", "Chromium";v="125.0.6422.142", "Not.A/Brand";v="24.0.0.0"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-model': '""',
    'sec-ch-ua-platform': '"Windows"',
    'sec-ch-ua-platform-version': '"15.0.0"',
    'sec-fetch-dest': 'iframe',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'same-origin',
    'sec-fetch-user': '?1',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36',
}

c_headers = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'accept-language': 'zh-CN,zh-TW;q=0.9,zh;q=0.8,en;q=0.7',
    'dnt': '1',
    'priority': 'u=0, i',
    'referer': 'https://www.south-plus.net/plugin.php?H_name-tasks-actions-newtasks.html.html',
    'sec-ch-ua': '"Google Chrome";v="125", "Chromium";v="125", "Not.A/Brand";v="24"',
    'sec-ch-ua-arch': '"x86"',
    'sec-ch-ua-bitness': '"64"',
    'sec-ch-ua-full-version': '"125.0.6422.142"',
    'sec-ch-ua-full-version-list': '"Google Chrome";v="125.0.6422.142", "Chromium";v="125.0.6422.142", "Not.A/Brand";v="24.0.0.0"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-model': '""',
    'sec-ch-ua-platform': '"Windows"',
    'sec-ch-ua-platform-version': '"15.0.0"',
    'sec-fetch-dest': 'iframe',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'same-origin',
    'sec-fetch-user': '?1',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36',
}

ad_params = {
    'H_name': 'tasks',
    'action': 'ajax',
    'actions': 'job',
    'cid': '15',
    'nowtime': '1717167492479',
    'verify': '5af36471',
}

aw_params = {
    'H_name': 'tasks',
    'action': 'ajax',
    'actions': 'job',
    'cid': '14',
    'nowtime': '1717167492479',
    'verify': '5af36471',
}

cd_params = {
    'H_name': 'tasks',
    'action': 'ajax',
    'actions': 'job2',
    'cid': '15',
    'nowtime': '1717167492479',
    'verify': '5af36471',
    }

cw_params = {
    'H_name': 'tasks',
    'action': 'ajax',
    'actions': 'job2',
    'cid': '14',
    'nowtime': '1717167492479',
    'verify': '5af36471',
}

url = 'https://www.south-plus.net/plugin.php'
coin_url = 'https://www.south-plus.net/'

def tasks(url, params, cookies, headers, type, get_coin=False):
    response = requests.get(url, params=params, cookies=cookies, headers=headers)

    data = response.text

    if(get_coin):
        soup = BeautifulSoup(data, 'html.parser')
        # 找到包含SP币值的<span>标签
        sp_coin_span = soup.find('span', class_='s3 f10')
        # 提取SP币值
        sp_coin_value = sp_coin_span.text
        # 输出SP币值
        print("SP币:", sp_coin_value)
        return True

    # 解析XML数据
    root = ET.fromstring(data)
    cdata = root.text

    # 提取变量值
    values = cdata.split('\t')
    if('申请' in type):
        value_len = 2
    else:
        value_len = 3
    if len(values) == value_len:
        message = values[1]

        print(type + message)
    else:
        raise Exception("XML格式不正确，请检查COOKIE设置")
    if("还没超过" in message):
        return False
    else:
        return True
    
if(tasks(url, ad_params, cookies, a_headers, "申请-日常: ")):
    tasks(url, cd_params, cookies, c_headers, "完成-日常: ")
if(tasks(url, aw_params, cookies, a_headers, "申请-周常: ")):
    tasks(url, cw_params, cookies, c_headers, "完成-周常: ")
tasks(coin_url, cw_params, cookies, c_headers, "", True)
