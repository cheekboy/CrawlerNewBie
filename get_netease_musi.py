#!/usr/bin/python
# -*- coding:utf-8 -*-

from urllib.request import urlopen
from bs4 import BeautifulSoup

html=urlopen('http://music.163.com/#/discover/playlist')
# print(html.read())
bs_obj = BeautifulSoup(html.read(), 'html.parser')
text_list = bs_obj.find_all('span', 'nb')
for text in text_list:
    print(text.get_text())
html.close()

if __name__ == "__main__":
    pass