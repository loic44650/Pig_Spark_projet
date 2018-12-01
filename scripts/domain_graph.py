#!/usr/bin/env python
import sys
import os
from urllib.request import urlopen
from urllib.parse import urlparse
from bs4 import BeautifulSoup
import re
import string

url = sys.argv[1]

exclude = set(string.punctuation)
hostname = urlparse(url).hostname
name = ''.join(c for c in hostname.split(".")[1] if c not in exclude)

def getLinks(html, out):
    links = []
    empty = True;
    for link in html.findAll('a'):
        l = link.get('href')
        #print(l)
        isresource = l is not None and len(l)>0 and "#" not in l and "?" not in l and "&" not in l and ("." not in l.split("/")[-1] or l.split(".")[-1]=="html")
        #print(isresource)
        if isresource and (hostname in l or l[0]=="/"):
            l = "http://"+hostname+l if l[0]=="/" else l
            #print("\t -"+l)
            links.append(l)
            out.write("(<"+l+">),")
            empty = False
    if not empty:
        pass
        out.seek(0, os.SEEK_END)
        out.seek(file.tell() - 1, os.SEEK_SET)
        out.truncate()

    return links

def deepConstruct(url, out):
    if url not in urls:
        try:
            htmlResp = urlopen(url)
        except Exception as e:
            return
            #print ("WARN "+url+" - "+str(e))
        #print(url)
        out.write("<"+url+"> ")
        html = htmlResp.read()
        soup = BeautifulSoup(html,"lxml")
        out.write("1.0 {")
        urls[url] = getLinks(soup, out)
        out.write("}\n")
        for link in urls[url]:
            deepConstruct(link, out)

urls = {}

file = open("../data/"+name,"w")
deepConstruct(url, file)
file.close()
