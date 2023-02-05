import PySimpleGUI as sg
#--------------------vvv
#【1.使うライブラリをimport】
import re
import requests
from bs4 import BeautifulSoup

#【2.アプリに表示する文字列を設定】
title = "RSSのタイトル一覧を表示"
label1, value1 = "RSS URL", "https://www.shoeisha.co.jp/rss/book/index.xml"
label2, value2 = "タグ", "title"

#【3.関数: RSSのタグを取得する】
def readRSSitem(url, tag):
    msg = ""
    r = requests.get(url)                   #URLのデータを取得
    r.encoding = r.apparent_encoding        #文字コードを自動判別
    soup = BeautifulSoup(r.text, "lxml")     #XMLデータを解析して
    tags = soup.findAll(name=tag)
    for i, element in enumerate(tags):
        msg += str(i) + ":" + element.text + "\n" #タグの要素を追加
        if i == len(tags) - 1: #最後の要素なら
            break
    else: #for文がbreakで抜けなかったら
        msg = "タグが見つかりません"
    return msg
#--------------------^^^
def execute():
    value1 = values["input1"]
    value2 = values["input2"]
    url_pattern = "https?://[\w/:%#\$&\?\(\)~\.=\+\-]+" #URLの正規表現
    if value1 == "" or not re.match(url_pattern, value1):
        sg.popup("RSS URLを入力してください")
        return
    if value2 == "":
        sg.popup("タグを入力してください")
        return
    #--------------------vvv
    #【4.関数を実行】
    msg = readRSSitem(value1, value2)
    #--------------------^^^
    window["text1"].update(msg)
#アプリのレイアウト
layout = [[sg.Text(label1, size=(14,1)), sg.Input(value1, key="input1")],
          [sg.Text(label2, size=(14,1)), sg.Input(value2, key="input2")],
          [sg.Button("実行", size=(20,1), pad=(5,15), bind_return_key=True)],
          [sg.Multiline(key="text1", size=(60,10))]]
#アプリの実行処理
window = sg.Window(title, layout, font=(None,14))
while True:
    event, values = window.read()
    if event == None:
        break
    if event == "実行":
        execute()
window.close()
