import cloudscraper
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
cw_params.update(
