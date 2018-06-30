# -*- coding: utf-8 -*-

import json
import os
import webbrowser
import tkinter as tk
from tkinter import ttk  #导入内部包

class App(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        self.tree = ttk.Treeview(master)
        self.load_items()
        self.tree.bind('<ButtonRelease-1>', self.treeview_click)
        self.tree.pack(expand=tk.YES, fill=tk.BOTH)

    def load_items(self):
        user_count = 0
        for userid in os.listdir("column"):
            user = self.tree.insert("", user_count, text=userid, values=(userid))
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
                self.tree.insert(user, item_count, text=title, values=(url, htmlfile))
                item_count = item_count + 1
            user_count = user_count + 1

    def treeview_click(self, event):
        item = self.tree.selection()[0]
        item_text = self.tree.item(item, "values")
        if (len(item_text) > 1):
            filename = "file://" + os.path.abspath(item_text[1])
            print("Open file: " + filename)
            webbrowser.open(filename)


win = tk.Tk()
w, h = win.maxsize()
win.geometry("{}x{}".format(w, h))
app = App(win)
app.mainloop()
