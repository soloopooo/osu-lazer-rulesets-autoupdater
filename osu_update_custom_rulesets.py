# -*- coding: utf-8 -*-
# @author: soloopooo, github: https://github.com/soloopooo
# last modify time: 2022/07/08 20:17 CST

# How to use this python script:
# Install dependencies: pip install requests bs4
# Change the folder to your own osu!lazer's custom rulesets folder.
# Then, Input your github-custom rulesets in the bottom as original files.
# And run it. That'll be okay.
# 中文文档：
# 先安装依赖：pip install requests bs4
# 更改'FOLDER'变量为你的osu lazer的rulesets文件夹。
# 之后在最底端仿照例子插入你所需要的rulesets。
# 最后运行。就这么简单。

# rulesets: if full url is https://github.com/EVAST9919/lazer-sandbox, just use '/EVAST9919/lazer-sandbox'.
# 如果链接是 https://github.com/EVAST9919/lazer-sandbox，仅需使用'/EVAST9919/lazer-sandbox'。
import requests
from bs4 import BeautifulSoup
import time
import os
import json

from requests.exceptions import RequestException

requests.packages.urllib3.disable_warnings()
RETRY_NUM = 5  # The max retries.
DEBUG = False  # For Debugging.
# Change this to your own osu! rulesets folder. Please use '\\' as '\'.
FOLDER = 'D:\\osulazer\\rulesets\\'
# Change this to your proxy. If no need, simply let this = {}.
PROXY = {"http": "http://127.0.0.1:7890", "https": "http://127.0.0.1:7890"}


def download(url):
    respon = requests.get(proxies=PROXY, url=url, stream=True, verify=False)
    version = url.split('/')[7]
    size = 0
    chunk_size = 1024
    if DEBUG:
        print(respon.headers)
    try:
        if respon.status_code == 200:
            filename = str(
                respon.headers['Content-Disposition'].split('filename=')[1])
            content_size = int(respon.headers['content-length'])
            sizeall = content_size
            unita = 'B'
            if sizeall >= 1024 and sizeall <= 1024*1024:
                sizeall = sizeall/1024
                unita = 'KB'
            elif sizeall > 1024*1024:
                sizeall = sizeall / 1024 / 1024
                unita = 'MB'
            with open(FOLDER + filename, 'wb') as file:
                for data in respon.iter_content(chunk_size=chunk_size):
                    file.write(data)
                    size += len(data)
                    sizep = size
                    unit = 'B'
                    if sizep >= 1024 and sizep <= 1024*1024:
                        sizep = sizep/1024
                        unit = 'KB'
                    elif sizep > 1024*1024:
                        sizep = sizep / 1024 / 1024
                        unit = 'MB'
                    printlog('Downloading, [Downloaded]:{sizenow:.2f} {unit:} [File size]:{sizeall:.2f} {unita:} {percent:.2f}% |{progressbar:}|'.format(
                        sizenow=sizep, sizeall=sizeall, unit=unit, unita=unita, percent=(size / content_size*100), progressbar=('█'*int(size/content_size*35)+' ' *
                                                                                                                                (35-int(size/content_size*35)))), type='Info', end='    ', flush=True, begin='\r')
            print(' '*145, end='\r')
            printlog("Successful in updating {name:} -- {version:}".format(
                name=filename, version=version), 'Info')
    except Exception as e:
        printlog(e, 'Error')


def printlog(msg, type, flush=False, end='\n', begin=''):
    lctime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    if type == "Info":
        color = "32m"
    elif type == "Error":
        color = "31m"
    elif type == "Warning":
        color = "33m"
    else:
        color = "0m"

    msg_full = begin+"\033[1;35m"+lctime+"\033[0m" + \
        " [\033[1;"+color+type+"\033[0m] "+str(msg)+"\033[0m"
    terminal = os.get_terminal_size()
    print((msg_full + " "*(terminal.columns - len(msg_full)-len(end)+1)),
          flush=flush, end=end)


def convert_link(mode_link, source):
    link_head = "https://"
    link_end = ""
    if source == "github":
        link_head = "https://api.github.com/repos"
        link_end = "/releases/latest"
    link = link_head + mode_link + link_end
    return link


def update(link, source='github'):
    j = RETRY_NUM

    def try_get(j):
        try:
            res = requests.get(proxies=PROXY, url=link, verify=False)
            res.encoding = 'utf-8'
            if res.status_code == 200:
                printlog("Success in getting contents", "Info")
                row = res.text
                row_json = json.loads(row)
                if DEBUG:
                    print(row)
                if source == 'github':
                    prep_link = row_json["assets"][0]["browser_download_url"]
                    final_link = prep_link
                download(final_link)
            else:
                j = j - 1
                printlog("Failed to get, retrying, left \033[1;31m" +
                         str(j)+"\033[0m time(s)", "Warning")
                time.sleep(2)
                if j >= 0:
                    try_get(j)
                else:
                    raise RequestException
        except Exception as e:
            j = j - 1
            printlog(e, "Error")
            if j >= 0:
                printlog("Failed to get, retrying, left \033[1;31m" +
                         str(j)+"\033[0m time(s)", "Warning")
                time.sleep(2)
                try_get(j)
    try_get(j)


def trueupdate(uri, source):
    update(convert_link(uri, source=source))


# Add your custom rulesets link here. use trueupdate(uri,source).
if __name__ == '__main__':
    trueupdate('/karaoke-dev/karaoke', 'github')
    trueupdate('/EVAST9919/bosu', 'github')
    trueupdate('/LumpBloom7/sentakki', 'github')
    trueupdate('/Beamographic/rush', 'github')
    trueupdate('/Flutterish/Hitokori', 'github')
    trueupdate('/EVAST9919/lazer-swing', 'github')
    trueupdate('/LumpBloom7/hishigata', 'github')
    trueupdate('/goodtrailer/soyokaze', 'github')
    trueupdate('/EVAST9919/touhosu', 'github')
    trueupdate('/EVAST9919/lazer-sandbox', 'github')
