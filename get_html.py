#!/usr/bin/python
# -*- coding:utf-8 -*-

from urllib.request import urlopen
from bs4 import BeautifulSoup

html = urlopen('http://jr.jd.com')
# print(html.read())
bs_obj = BeautifulSoup(html.read(), 'html.parser')
text_list=bs_obj.find_all("a", "nav-item-primary")
for text in text_list:
    print(text.get_text())
html.close()

if __name__ == "__main__":
    pass