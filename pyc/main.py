import asyncio
from pprint import pprint
import json
import aiohttp
import aiofiles
import os
from typing import TypeAlias, IO, BinaryIO, TextIO
import re
from loguru import logger
from urllib.parse import unquote
import time
import requests
import subprocess
from utils import Annotation
from utils import Desc_modify
from config import ParametersInit
from typing import NewType
from utils import Get_a_b
import sys
import os
import mysql.connector

conn = mysql.connector.connect(
    host="localhost",        
    user="root",             
    password="",
    database=""       
)
cursor = conn.cursor()
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

Video = NewType("Video", bytes)
Pic = NewType("Pic", bytes)

@Annotation.func_desc("这是单个视频下载函数")
@Annotation.api_desc('https://www.douyin.com/user/self?from_tab_name=main&modal_id={视频id号}&showTab=like')
async def download_videos_pics(url, nickname, desc) -> Video:
    async with aiohttp.ClientSession() as session:
        async with session.get(url=url,headers=cfg.video_headers, cookies=cfg.video_cookies) as response:
            response_text = await response.text()
            json_str = re.findall('<script id="RENDER_DATA" type="application/json">(.*?)</script>', response_text)[0]
            json_dict = json.loads(unquote(json_str))
            # pprint(json_dict)
            try:
                video_url = json_dict['app']['videoDetail']['video']['bitRateList'][0]['playAddr'][0]['src']
                async with session.get(url=video_url, headers=cfg.video_headers, cookies=cfg.video_cookies) as response:
                    video_content = await response.read()
                    save_path_0 = "pyc\\videos"
                    save_path_1 = os.path.join(save_path_0, Desc_modify.clean_filename(nickname))
                    await asyncio.to_thread(os.makedirs, save_path_1, exist_ok=True)
                    video_path = os.path.join(save_path_1, f"{desc}.mp4")
                    async with aiofiles.open(video_path, mode='wb') as f:
                        await f.write(video_content)
            except:
                    pic_urls = json_dict['app']['videoDetail']['images'][0]['urlList']
                    # if pic_mode == "all":
                    for i, pic_url in enumerate(pic_urls):
                        # print(i, pic_url)
                        # print("*******************************************")
                        async with session.get(url=pic_url, headers=cfg.video_headers, cookies=cfg.video_cookies) as response:
                            pic_content = await response.read()
                            save_path_0 = "pyc\\videos"
                            save_path_1 = os.path.join(save_path_0, Desc_modify.clean_filename(nickname))
                            save_path_2 = os.path.join(save_path_1, Desc_modify.clean_filename(desc))
                            # 异步创建目录
                            await asyncio.to_thread(os.makedirs, save_path_2, exist_ok=True)
                            pic_jpg_path = os.path.join(save_path_2, f"{desc}_{i}.jpg")
                            pic_png_path = os.path.join(save_path_2, f"{desc}_{i}.png")
                            async with aiofiles.open(pic_jpg_path, mode='wb') as jf:
                                await jf.write(pic_content)
                            await asyncio.to_thread(lambda: open(pic_png_path, 'wb').write(pic_content))
                    
@Annotation.func_desc("这是批量获取aweme_id的函数,调用download_videos_pics进行批量下载")
@Annotation.api_desc('https://www.douyin.com/aweme/v1/web/aweme/post/')
async def get_aweme_ids(get_info_flag=False) -> str:
    async with aiohttp.ClientSession() as session:
        async with session.get(url=cfg._video_list_url,
                               params=cfg.video_list_params,
                               cookies=cfg._video_list_cookies,
                               headers=cfg._video_list_headers
                               ) as response:
            # print(response.status)
            response_text = await response.text()
            # pprint(response_text)
            json_dict = json.loads(response_text)
            # pprint(json_dict)
            for index in json_dict['aweme_list']:
                nickname = index['author']['nickname']
                aweme_id = index['aweme_id']
                desc = index['desc']
                # print(aweme_id)
                if get_info_flag == True:
                  collect_count = index['collect_count']
                  comment_count = index['comment_count']
                  digg_count = index['digg_count']
                  share_count = index['share_count']
                  admire_count = index['admire_count']

                url = f"https://www.douyin.com/user/self?from_tab_name=main&modal_id={aweme_id}&showTab=like"
                print(url)
                await download_videos_pics(url=url, nickname=nickname, desc=desc)

@Annotation.func_desc("这是下载指定博主的直播视频函数")
@Annotation.api_desc("https://live.douyin.com/webcast/room/web/enter/")
async def get_live_video_download() -> Video:
    params = cfg.live_video_params.copy()
    params = Get_a_b.get_a_b(params, cfg.live_video_headers)
    async with aiohttp.ClientSession() as session:
        async with session.get(url='https://live.douyin.com/webcast/room/web/enter/', params=params, headers=cfg.live_video_headers) as response:
            json_dict = await response.json()
            # pprint(json_dict)
            live_url = json_dict['data']['data'][0]['stream_url']['flv_pull_url']['FULL_HD1'] # 默认下载最高蓝光品质直播流
            print(live_url)
            nickname = json_dict['data']['user']['nickname']
            print(nickname)
            start_time = time.time()
            output_file = f'{nickname}_{start_time}.flv'
            # 使用ffmpeg命令持续下载直播流
            ffmpeg_command = [
                'ffmpeg',
                '-i', live_url,         
                '-c', 'copy',           
                '-f', 'flv',            #
                output_file
            ]
            # 使用subprocess运行ffmpeg命令
            try:
                process = subprocess.Popen(ffmpeg_command)
                print(f'正在从 {live_url} 持续下载直播流，并保存为 {output_file}')
                # 等待下载过程
                process.wait(timeout=10)
            except:
                pass
            end_time = time.time()
            print(f'本次下载共计耗时为：{end_time - start_time}')
            return nickname

async def get_all_my_followings():
    conn = mysql.connector.connect(
        host="localhost",        
        user="root",             
        password="",
        database=""       
    )
    cursor = conn.cursor()

    offset = 0
    # ClientSession 在循环外创建，复用连接
    async with aiohttp.ClientSession() as session:
        while True:
            cfg.my_followings_params['offset'] = offset
            async with session.get(
                url=cfg.my_followings_url,
                params=cfg.my_followings_params,
                headers=cfg.video_headers,
                cookies=cfg.my_followings_cookies
            ) as response:
                json_str = await response.text()
                json_dict = json.loads(json_str)
                has_more = json_dict['has_more']
                for i in json_dict['followings']:
                    nickname = i['nickname']
                    sec_user_id = i['sec_uid']
                    print(nickname, sec_user_id)
                    sql = "INSERT INTO my_following_bloggers (nickname, sec_user_id) VALUES (%s, %s)"
                    data = (nickname, sec_user_id)
                    cursor.execute(sql, data)
                conn.commit()  # 提交插入操作
            offset += 20
            if not has_more:
                break

    # 查询所有数据
    cursor.execute("SELECT * FROM my_following_bloggers")
    res = cursor.fetchall()
    for row in res:
        print(row)

    cursor.close()
    conn.close()



if __name__ == "__main__":
    cfg = ParametersInit.JsonParametersConfig()
    # asyncio.run(get_aweme_ids(get_info_flag=False))
    asyncio.run(get_live_video_download())
    # asyncio.run(get_all_my_followings())
    
    # sql = "select * from my_following_bloggers"
    # cursor.execute(sql)
    # res = cursor.fetchall()
    # for i in res:
    #     print(i)
