import os.path
import random
import time
import urllib.request
from datetime import datetime
import subprocess
from functools import partial
import requests
import pandas as pd

subprocess.Popen = partial(subprocess.Popen, encoding='utf-8')
import execjs
from configparser import ConfigParser
import urllib.parse

config = ConfigParser()


def set_sessionid():
    sessionid = input('请设置sessionid：')
    config.set('cookies', 'sessionid', sessionid)
    with open('config.ini', 'w') as f:
        config.write(f)
        f.close()
    return sessionid


# 配置数据

config.read('config.ini')
sessionid = config.get('cookies', 'sessionid')
with open('start.js', 'r', encoding='utf-8') as file:
    x_b = execjs.compile(file.read())
if not sessionid:
    sessionid = set_sessionid()
cookies = {
    "sessionid": sessionid,
}


# 判断速率限制

def reponse_info(info, url, headers):
    if info.strip() == 'ratelimit triggered' or '':
        print('{:-^30}'.format('速录限制触发'))
        print('{:-^30}'.format('等待30秒'))
        time.sleep(30)
        print('{:-^30}'.format('重新发送请求'))
        response = requests.get(url, headers=headers, cookies=cookies)
        if response.text.strip() == 'ratelimit triggered' or '':
            reponse_info(response.text, url, headers)
        else:
            print(response.text)
            return response


def download_video(url, name):
    print("{:=^30}".format(f'正在下载视频{name}'))
    for i in range(3):
        try:
            urllib.request.urlretrieve(url, name)
            time.sleep(random.random() + 1)
            break
        except:
            pass
    print("{:=^30}".format(f'已下载视频{name}'))


def sanitize_text(text):
    # Define the set of illegal characters
    illegal_chars = ['\\', '/', '*', '?', '[', ']', ':']

    # Remove illegal characters
    sanitized_text = ''.join(char for char in text if char not in illegal_chars)

    # Remove non-printable characters
    sanitized_text = ''.join(char for char in sanitized_text if char.isprintable())

    return sanitized_text


# 主函数
def get_data(url_: str, df_name: int):
    print(df_name)
    config.read('config.ini')
    sessionid = config.get('cookies', 'sessionid')
    if not sessionid:
        sessionid = set_sessionid()
    print(sessionid)
    cookies = {
        "sessionid": sessionid}
    count = 0
    id = url_.split('/')[-1]
    headers = {
        'referer': f'https://www.douyin.com/user/{id}',
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36 Edg/126.0.0.0"
    }
    page_number = 0
    df_data = []
    df_name = str(df_name)

    while True:
        params = {
            "device_platform": "webapp",
            "aid": "6383",
            "channel": "channel_pc_web",
            "sec_user_id": f"{id}",
            "max_cursor": f"{page_number}",
            "locate_query": "false",
            "show_live_replay_strategy": "1",
            "need_time_list": "0",
            "time_list_query": "0",
            "whale_cut_token": "",
            "cut_version": "1",
            "count": "18",
            "publish_video_strategy_type": "2",
            "update_version_code": "170400",
            "pc_client_type": "1",
            "version_code": "290100",
            "version_name": "29.1.0",
            "cookie_enabled": "true",
            "screen_width": "1440",
            "screen_height": "900",
            "browser_language": "zh-CN",
            "browser_platform": "Win32",
            "browser_name": "Edge",
            "browser_version": "126.0.0.0",
            "browser_online": "true",
            "engine_name": "Blink",
            "engine_version": "126.0.0.0",
            "os_name": "Windows",
            "os_version": "10",
            "cpu_core_num": "16",
            "device_memory": "8",
            "platform": "PC",
            "downlink": "10",
            "effective_type": "4g",
            "round_trip_time": "100",
            "webid": "7381322046573233705",
            "verifyFp": "verify_lxigv7hh_cxuS13l6_SJN9_4U0k_80VT_MFfpKdjVxI7c",
            "fp": "verify_lxigv7hh_cxuS13l6_SJN9_4U0k_80VT_MFfpKdjVxI7c",
            "msToken": "c9F-KKVTTXaHKSSMo36__CrOUuS7_Kb7yKEKQ0ULyaivq5inE_3vaABRn8UmddA34h0k6O4Rgsi-K54CAzl5pkItVFQj6sYpIrCiMFsoX5gGnTDviq5T"}
        result = urllib.parse.urlencode(params)
        a_bogus = x_b.call('get_a_bogus', result)
        result += f'&a_bogus={a_bogus}'
        url = "https://www.douyin.com/aweme/v1/web/aweme/post/?"
        url = url + result
        response = requests.get(url, headers=headers, cookies=cookies)
        info = response.text
        print('页面', info)
        response2 = reponse_info(info, url, headers)
        if response2 is None:
            data = response.json()
        else:
            data = response2.json()
        video_list = data.get('aweme_list')
        time.sleep(random.randint(2, 4))
        for video in video_list:
            # 发布时间
            create_time = video.get('create_time')
            create_time = datetime.fromtimestamp(int(create_time)).strftime('%Y-%m-%d-%H:%M:%S')
            info_data = video.get('statistics', {})
            # 收藏数
            collect_count = info_data.get('collect_count')
            # 评论数
            comment_count = info_data.get('comment_count')
            # 点赞数
            digg_count = info_data.get('digg_count')
            # 转发数
            share_count = info_data.get('share_count')
            # 文案
            desc = sanitize_text(video.get('desc'))
            # 下载视频
            video_download = video.get('video').get('play_addr').get('url_list')[0]
            # 抖音名
            name_douyin = video.get('author', {}).get('nickname')
            funs = video.get('author').get('follower_count')
            all_digg = video.get("author").get("total_favorited")
            if not os.path.exists(f'./{name_douyin}'):
                os.mkdir(f"./{name_douyin}")
            #if create_time[:7] == '2023-09':
             #   download_video(video_download, f"./{name_douyin}/{name_douyin + create_time.replace(':', '-')}.mp4")
            df_name = name_douyin
            temp = [name_douyin, create_time, collect_count, comment_count, digg_count, share_count, desc, funs,
                    all_digg]
            df_data.append(temp)
        if video_list == [] or len(video_list) == 0:
            print(f'{df_name}爬取成功，已生成Excel')
            break
        next = data.get('max_cursor')
        page_number = next
        count += int(len(video_list))
        print(f'已爬取{count}条,{df_name}')
    df = pd.DataFrame(df_data,
                      columns=['抖音名称', '发布时间', '收藏量', '评论量', '点赞量', '转发量', '文案', "粉丝数",
                               "总点赞数"])
    df.to_excel(f'{df_name}.xlsx', index=False)


if __name__ == '__main__':
    file_path = "/Users/amos/Desktop/xxpublish/xxpublish1new_8.txt"
    # input('请输入爬取的目录文件的完整路径：')
    file = open(file_path, 'r')
    """print('{:=^30}'.format('文件类型'))
    if file_path.endswith('.txt'):
        print('输入为文本文档')
        file = open(file_path,'r')
    elif file_path.endswith('.csv'):
        print('输入为csv表格文件')
    elif file_path.endswith('.xls') or file_path.endswith('.xlsx'):
        print('输入为Excel表格文件')
    else:
        print('输入为其他文件')
    print('{:=^30}'.format('正在获取内容'))"""
    data = file.readlines()
    for i in data:
        print(i.strip())
    print('{:=^30}'.format('正在执行爬虫'))
    for i, url in enumerate(data):
        if url:
            print(url.strip())
            get_data(url_=url.strip(), df_name=i)
