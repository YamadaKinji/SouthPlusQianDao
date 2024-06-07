import requests
import xml.etree.ElementTree as ET
import os
import brotli
import gzip
import io

cookie_value = os.getenv('COOKIE')
cookie_value = cookie_value.replace('\n', '').replace(' ', '')

url = 'https://south-plus.net/plugin.php'

common_headers = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'accept-encoding': 'gzip, deflate, br',
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
    
    # 打印响应头以便调试
    print(f"Headers for {type}: {response.headers}")

    # 处理多种编码格式
    data = None
    if response.headers.get('Content-Encoding') == 'br':
        try:
            data = brotli.decompress(response.content).decode('utf-8')
        except brotli.error as e:
            print(f"Brotli 解压失败: {e}")
    elif response.headers.get('Content-Encoding') == 'gzip':
        try:
            buf = io.BytesIO(response.content)
            f = gzip.GzipFile(fileobj=buf)
            data = f.read().decode('utf-8')
        except OSError as e:
            print(f"Gzip 解压失败: {e}")
    else:
        try:
            data = response.content.decode('utf-8')
        except UnicodeDecodeError as e:
            print(f"UTF-8 解码失败: {e}")
    
    if data is None:
        data = response.text  # 如果所有解码都失败，直接使用文本内容
    
    # 打印响应的前500个字符以便调试
    print(f"Response for {type}: {data[:500]}")

    # 保存原始响应内容到文件
    with open(f'raw_response_{type}.txt', 'w', encoding='utf-8') as f:
        f.write(data)

    try:
        # 检查返回的数据是否包含HTML标签
        if '<html' in data.lower():
            raise Exception("服务器返回的内容包含HTML标签，可能是错误的请求或服务器问题。")
        
        # 解析XML数据
        root = ET.fromstring(data)
        cdata = root.text
    except ET.ParseError as e:
        raise Exception(f"XML解析错误: {e}")

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

if tasks(url, ad_params, a_headers, "申请-日常: "):
    tasks(url, cd_params, c_headers, "完成-日常: ")
if tasks(url, aw_params, a_headers, "申请-周常: "):
    tasks(url, cw_params, c_headers, "完成-周常: ")
