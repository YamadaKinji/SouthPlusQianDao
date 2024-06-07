import requests
import xml.etree.ElementTree as ET
import os

cookie_value = os.getenv('COOKIE')
cookie_value = cookie_value.replace('\n', '').replace(' ', '')

url = 'https://south-plus.net/plugin.php'

common_headers = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'accept-encoding': 'gzip, deflate, br, zstd',
    'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
    'cookie': cookie_value,
    'priority': 'u=0, i',
    'sec-ch-ua': '"Microsoft Edge";v="125", "Chromium";v="125", "Not.A/Brand";v="24"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'document',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'same-origin',
    'sec-fetch-user': '?1',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36 Edg/125.0.0.0'
}

a_headers = common_headers.copy()
a_headers.update({
    'referer': url+'?H_name-tasks-actions-newtasks.html.html'
})

c_headers = common_headers.copy()
c_headers.update({
    'authority': 'south-plus.net',
    'method': 'GET',
    'path': '/plugin.php?H_name-tasks-actions-newtasks.html.html',
    'scheme': 'https',
    'Referer': url+'?H_name-tasks.html.html'
})


common_params = {
    'H_name': 'tasks',
    'action': 'ajax',
    'nowtime': '1717167492479',
    'verify': '5af36471',
}

ad_params = common_params.copy()
ad_params.update({
    'actions': 'job',
    'cid': '15',
})

aw_params = common_params.copy()
aw_params.update({
    'actions': 'job',
    'cid': '14',
})

cd_params = common_params.copy()
cd_params.update({
    'actions': 'job2',
    'cid': '15',
})

cw_params = common_params.copy()
cw_params.update({
    'actions': 'job2',
    'cid': '14',
})

def tasks(url, params, headers, type):
    response = requests.get(url, params=params, headers=headers)

    response.encoding = 'utf-8'
    data = response.text
    print(f"Response for {type}: {data}")

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
    
if(tasks(url, ad_params, a_headers, "申请-日常: ")):
    tasks(url, cd_params, c_headers, "完成-日常: ")
if(tasks(url, aw_params, a_headers, "申请-周常: ")):
    tasks(url, cw_params, c_headers, "完成-周常: ")
