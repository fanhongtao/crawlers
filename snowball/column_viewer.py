# -*- coding: utf-8 -*-

import json
import os
import webbrowser
from tkinter import *
from tkinter import ttk  #导入内部包

def treeviewClick(event):
    item = tree.selection()[0]
    item_text = tree.item(item, "values")
    # print(item_text[0])
    if (len(item_text) > 1):
        filename = "file://" + os.path.abspath(item_text[1])
        print("Open file: " + filename)
        webbrowser.open(filename)

win = Tk()
#w = win.winfo_screenwidth()
#h = win.winfo_screenheight()
#win.geometry("%dx%d" %(w, h))
w, h = win.maxsize()
win.geometry("{}x{}".format(w, h)) #看好了，中间的是小写字母x
tree = ttk.Treeview(win)

user_count = 0
for userid in os.listdir("column"):
    user = tree.insert("", user_count, text=userid, values=(userid))
    column_path = "column/" + userid
    filename = column_path + "/" + "column_" + userid + ".json"
    with open(filename, 'r', encoding='utf-8') as f:
        items = json.load(f)['items']

    item_count = 0
    for item in items:
        title = item['title']
        url = item['link']
        page = url.split("//")[-1]
        htmlfile = column_path + "/" + page.strip("/").replace("/", "_")
        if (not (htmlfile.endswith(".html") or htmlfile.endswith(".htm"))):
            htmlfile = htmlfile + ".html"
        tree.insert(user, item_count, text=title, values=(url, htmlfile))
        item_count = item_count + 1
    user_count = user_count + 1

tree.bind('<ButtonRelease-1>', treeviewClick)
tree.pack(expand=YES, fill=BOTH)
win.mainloop()
