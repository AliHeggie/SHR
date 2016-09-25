#!/usr/bin/python
import csv, sys, getopt, os, urllib2, re, glob, time, datetime, numpy
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

# html page processing function
# def processData(html, out):
#     ''' take the data from an html file and append to our csv file '''
#     soup = BeautifulSoup(html)
#     # Comment info
#     posts = []
#     authors = []
#     times = []
#     
#     # Header info
#     victimName = []
#     victimAge = []
#     victimLocation = []
#     description = []
#     uploadDate = []
#     pageviews = []
#     description = []
#     
#     # extract comment data
#     for html in soup.findAll("div", { "class" : "trimbox" }):
#         for commentbody in html.findAll("div", { "class" : "comment-body" }): 
#             if len(commentbody.findAll("p")) > 0:
#                 posts.append(' '.join([p.contents[0] for p in commentbody.findAll("p")]))
#             else:
#                 print "WARNING: Comment found with no text"
#                 posts.append('')
#         for cite in html.findAll("cite", { "class" : "fn" }):
#             authors.append(cite.contents[0])
#         for commentmetadata in html.findAll("div", { "class" : "comment-meta commentmetadata" }):
#             times.append(commentmetadata.find("a").contents[0].strip())
#    
#     # extract header data and create array length of comments
#     for html in soup.findAll("div", { "class" : "profilehead" }):
#         viewsAndDate = html.find("div", { "class" : "views" } ).text
#         reDate = re.compile(r'(?<=Added )(.{12})')
#         reViews = re.compile(r'(\d{1,10})(?= Views)')
#         reAge = re.compile(r'\d{1,3}(?=\s+years old)')
#         reLoc = re.compile(r'(?<=years old)\s+in\s+([()\w\s-]+,[()\w\s-]+)')
#         try:
#             uploadDate = [re.search(reDate, viewsAndDate).group(0)]*len(posts)
#         except:
#             pass
#         try:
#             pageviews = [re.search(reViews, viewsAndDate).group(0)]*len(posts)  
#         except:
#             pass
#         try:
#             victimName = [html.find("h1").text]*len(posts)
#         except:
#             pass
#         try:
#             victimAge = [re.search(reAge, re.sub('\s+',' ',html.text)).group(0)]*len(posts)
#         except:
#             pass
#         try:
#             victimLocation = [re.search(reLoc, re.sub('\s+',' ',html.text)).group(1)]*len(posts)
#         except:
#             pass
#     
#     for html in soup.findAll("div", { "class" : "profilecontent"}):
#         description = [re.sub('\s+',' ',html.text)]*len(posts)
#     
#     csvfile = open(out, 'ab')
#     writer = csv.writer(csvfile)
# 
#     # iterate through and write all the data
#     for time, author, post, date, name, age, loc, description, views in zip(times, authors, posts, uploadDate, victimName, victimAge, victimLocation, description, pageviews):
#         row = [time, author, post, date, name, age, loc, description, views]
#         writer.writerow([col.encode('utf-8') for col in row])
# 
#     # close file
#     csvfile.close()
# 
# processData(
#     urllib2.urlopen("http://www.myex.com/virginia/norfolk/tahlia-ari/15952/"),
#     "test.csv"
# )

posts=[]
times=[]
# html = urllib2.urlopen("http://www.myex.com/new-york/harrison/christina-scarlettfever-goon/17522/")
html = urllib2.urlopen("http://www.myex.com/illinois/lake-villa/emily-neurater/19252/")
soup = BeautifulSoup(html)
for html in soup.findAll("div", { "class" : "trimbox" }):
    for commentbody in html.findAll("div", { "class" : "comment-body" }): 
        if len(commentbody.findAll("p")) > 0:
            posts.append(' '.join([p.contents[0].encode('utf-8') for p in commentbody.findAll("p")]).decode('utf-8'))
        else:
            print "WARNING: Comment found with no text"
            posts.append('')
        for commentmetadata in html.findAll("div", { "class" : "comment-meta commentmetadata" }):
            times.append(commentmetadata.find("a").contents[0].strip())
# print posts
print times
            