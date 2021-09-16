'''
MIT License
Copyright (c) 2018 Vrushabh Jambhulkar
Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:
The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.
THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
'''
'''
Before using this program, please install pip, bs4 and update your python
-------------------------------------------------------------
pip
if you don't have pip installed, run the following lines->
curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
python get-pip.py
-------------------------------------------------------------
bs4
if you don't have bs4, run the following (note: pip is a pre-requsite) ->
pip install bs4
'''


from bs4 import BeautifulSoup
import requests
import re
import urllib2
import os
import cookielib
import json

# you can change the following parameres as per your requirements
DIR="Downloads"
MAX_DOWNLOAD_COUNT = 5
SHOULD_PUT_IN_SEPERATE_FOLDERS = True

# Change the following list according to your requirements
imageQueryList = ["FarCry 4", "GTA 6", "DMC", "Bayonetta"]


#don't chnage anything below
HEADER = {'User-Agent':"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.134 Safari/537.36"}
def get_soup(url,header):
    return BeautifulSoup(urllib2.urlopen(urllib2.Request(url,headers=header)),'html.parser')

def getImageWithTerm(query):
    global DIR
    global MAX_DOWNLOAD_COUNT
    global HEADER
    global SHOULD_PUT_IN_SEPERATE_FOLDERS
    print("\nGetting 5 images for: "+query)
    split_query= query.split()
    split_query='+'.join(split_query)
    url="https://www.google.co.in/search?q="+split_query+"&tbm=isch" 
    soup = get_soup(url, HEADER)
    imageList=[] #contains the link for Large original images, type of image
    current_count = 0
    for a in soup.find_all("div",{"class":"rg_meta"}):
        if(current_count == MAX_DOWNLOAD_COUNT):
            break
        link , Type =json.loads(a.text)["ou"]  ,json.loads(a.text)["ity"]
        imageList.append((link,Type))
        current_count+=1
    if not os.path.exists(DIR):
        os.mkdir(DIR)
    query_dir = DIR
    if SHOULD_PUT_IN_SEPERATE_FOLDERS:
        query_dir = os.path.join(DIR, query)
        if not os.path.exists(query_dir):
            os.mkdir(query_dir)
    for i , (img , Type) in enumerate(imageList):
        try:
            req = urllib2.Request(img, headers={'User-Agent' : HEADER})
            raw_img = urllib2.urlopen(req).read()

            cntr = len([i for i in os.listdir(query_dir) if query in i]) + 1
            print("file downloaded", query + "_"+ str(cntr)+".jpg")
            if len(Type)==0:
                f = open(os.path.join(query_dir , query + "_"+ str(cntr)+".jpg"), 'wb')
            else :
                f = open(os.path.join(query_dir , query + "_"+ str(cntr)+"."+Type), 'wb')
            f.write(raw_img)
            f.close()
        except Exception as e:
            print("could not load : "+img)
            print(e) 
    return

def getAllImages():
    print("----------------------------------------------------------------------------")
    print("Sould use seperate folders: ", SHOULD_PUT_IN_SEPERATE_FOLDERS)
    print("Main download directory: ", DIR)
    print("Max batch-download size: ", MAX_DOWNLOAD_COUNT, "\n----------------------------------------------------------------------------")
    for i, query in enumerate(imageQueryList):
        getImageWithTerm(query)
    return

getAllImages()
