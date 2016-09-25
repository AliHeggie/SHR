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

# TODO: make pause function with this code:
# import thread, time
# 
# def input_thread(L):
#     raw_input()
#     L.append(None)
#     
# def do_print():
#     L = []
#     thread.start_new_thread(input_thread, (L,))
#     while 1:
#         time.sleep(.1)
#         if L: break
#         print "Hi Mom!"

# html page processing function
def processData(soup, out):
    ''' take the data from an html file and append to our csv file '''
    # Comment info
    posts = []
    authors = []
    times = []
    
    # Header info
    victimName = []
    victimAge = []
    victimLocation = []
    description = []
    uploadDate = []
    pageviews = []
    description = []
    
    # extract comment data
    try:
        if len(soup.findAll("div", { "class" : "trimbox" })) > 0:
            for html in soup.findAll("div", { "class" : "trimbox" }):
                for commentbody in html.findAll("div", { "class" : "comment-body" }): 
                    if len(commentbody.findAll("p")) > 0:
                        posts.append(' '.join([p.contents[0].encode('utf-8') for p in commentbody.findAll("p")]).decode('utf-8'))
                    else:
                        print "WARNING: Comment found with no text"
                        posts.append(' ')
                for cite in html.findAll("cite", { "class" : "fn" }):
                    authors.append(cite.contents[0])
                for commentmetadata in html.findAll("div", { "class" : "comment-meta commentmetadata" }):
                    times.append(commentmetadata.find("a").contents[0].strip())
        else: # so that row in csv is created
            print "WARNING: No comments found"
            posts.append('N/A')
            authors.append('N/A')
            times.append('N/A')
    except:
        print "ERROR: Comments did not extract successfully"
    # extract header data and create array length of comments
    try:
        for html in soup.findAll("div", { "class" : "profilehead" }):
            viewsAndDate = html.find("div", { "class" : "views" } ).text
            reDate = re.compile(r'(?<=Added )(.{12})')
            reViews = re.compile(r'(\d{1,10})(?= Views)')
            reAge = re.compile(r'\d{1,3}(?=\s+years old)')
            reLoc = re.compile(r'(?<=years old)\s+in\s+([()\w\s-]+,[()\w\s-]+)')
            try:
                uploadDate = [re.search(reDate, viewsAndDate).group(0)]*len(posts)
            except:
                pass
            try:
                pageviews = [re.search(reViews, viewsAndDate).group(0)]*len(posts)  
            except:
                pass
            try:
                victimName = [html.find("h1").text]*len(posts)
            except:
                pass
            try:
                victimAge = [re.search(reAge, re.sub('\s+',' ',html.text)).group(0)]*len(posts)
            except:
                pass
            try:
                victimLocation = [re.search(reLoc, re.sub('\s+',' ',html.text)).group(1)]*len(posts)
            except:
                pass
        for html in soup.findAll("div", { "class" : "profilecontent"}):
            description = [re.sub('\s+',' ',html.text)]*len(posts)
    except:
        print "ERROR: Headings did not extract successfully"
    
        
    
    csvfile = open(out, 'ab')
    writer = csv.writer(csvfile)

    # iterate through and write all the data
            
    try:
        for time, author, post, date, name, age, loc, description, views in zip(times, authors, posts, uploadDate, victimName, victimAge, victimLocation, description, pageviews):
            row = [time, author, post, date, name, age, loc, description, views]
            writer.writerow([col.encode('utf-8') for col in row])
    except:
        print "ERROR: Didn't write to CSV correctly"
    
    # close file
    csvfile.close()

def scroll_element_into_view(driver, elems, i, page):
    """Scroll element into view"""
    try:
        y = elems[i].location['y']
        return y
    except StaleElementReferenceException:
        print "WARNING: Stale reference while scrolling: reloading %s and retrying" % (page)
        driver.get(page)
        time.sleep(5)
        elems = find_elems(driver, page)
        return scroll_element_into_view(driver, elems, i, page)
    driver.execute_script('window.scrollTo(0, {0})'.format(y))

def scroll_next_into_view(driver, next, page):
    """Scroll next into view"""
    try:
        y = next.location['y']
        return y
    except StaleElementReferenceException:
        print "WARNING: Stale reference while scrolling: reloading %s and retrying" % (page)
        driver.get(page)
        time.sleep(5)
        attempt_next(driver, next, page)
        return scroll_next_into_view(driver, next, page)
    driver.execute_script('window.scrollTo(0, {0})'.format(y))

def find_elems(driver, page, minLen=3):
#       <img src="/wp-content/themes/MyEXTheme/images/btnNude.png">
    elems = driver.find_elements_by_xpath("//img[contains(@src,'/wp-content/themes/MyEXTheme/images/btnNude.png')]")
    max = 10
    t = 0
    elemLens = []
    while len(elems) < minLen and t < max:
        elemLens.append(len(elems))
        driver.get(page)
        print "WARNING: Found fewer than %d elements on %s. Reloading %s" % (minLen, driver.current_url, page)
        time.sleep(1)
        elems = driver.find_elements_by_xpath("//img[contains(@src,'/wp-content/themes/MyEXTheme/images/btnNude.png')]")
        t = t + 1 
    if t > max:
        if round(numpy.mean(elemLens)) == 0:
            print "WARNING: Appears to be zero links to profiles from %s. Going to next page..." % (driver.current_url)
            attempt_next(driver, page)
            find_elems(driver, page)
        elif round(numpy.mean(elemLens)) > 0:
            print "NOTE: Seems there are only %d links to profiles from %s. Proceeding..." % (round(numpy.mean(elemLens)), driver.current_url)
            find_elems(driver, page, minLen=1)
        else:
            print "WARNING: Stuck, trying back button..."
            driver.back()
        return find_elems(driver, page)
    return elems

def attempt_click(driver, elems, i, page):
    try:
        elems[i].click()
    except StaleElementReferenceException:
        print "WARNING: Stale reference while clicking on %s: reloading %s and retrying" % (driver.current_url, page)
        driver.get(page)
        time.sleep(5)
        elems = find_elems(driver, page)
        attempt_click(driver, elems, i, page)
    except WebDriverException:
        print "WARNING: WebDriverException, element not clickable on %s. Retrying..." % (driver.current_url)
        elems = find_elems(driver, page)
        attempt_click(driver, elems, i, page)

def attempt_next(driver, page):
    next = driver.find_element_by_class_name("next")
    max = 10
    t = 0
    while driver.title.lower().startswith('naked pics of') and t < max:
        driver.get(page)
        print "WARNING: Couldn't find the 'next' button on %s. Reloading %s" % (driver.current_url, page)
        time.sleep(1)
        next = driver.find_element_by_class_name("next")
    scroll_next_into_view(driver, next, page)
    try:
        next.click()
    except WebDriverException:
        print "WARNING: WebDriverException, next button not clickable on %s. Retrying..." % (driver.current_url)
        attempt_next(driver, page)
    if t == 10:
        if driver.find_element_by_class_name("disabled"): done = 1
        else: 
            print "WARNING: Next page didn't load. Trying the back button..."
            driver.back()

def main(argv):
    max = 10
    start = time.time()
    total = 1 #init
    csvFile = '' #init
    profile = '' # init
    try:
        opts, args = getopt.getopt(argv,"ht:o:",["total=","csvFile="])
    except getopt.GetoptError:
        print 'test.py -t <total> -o <csvFile>'
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print 'test.py -t <total> -o <csvFile>'
            sys.exit()
        elif opt in ("-t", "--total"):
            total = int(arg)
        elif opt in ("-o", "--csvFile"):
            csvFile = arg

    # insert the column titles to csv
    csvfile = open(csvFile, 'wb')
    writer = csv.writer(csvfile)
    writer.writerow(["Time", "Author", "Post", "Upload Date", "Victim Name", "Age", "Location", "Description", "Page Views"])
    csvfile.close()
    
    driver = webdriver.Chrome()
    driver.implicitly_wait(10)
    driver.get('http://myex.com')
#     time.sleep(0.2) # Let the page load, will be added to the API
    done = 0
    count = 1
    print "Spider beginning to crawl. The time is: %s" % (time.strftime("%a, %d %b %Y %H:%M:%S"))
    print "Scraping %d profiles" % (total)
    while done != 1:
        time.sleep(0.2)
        t = 0
        while not (driver.title.lower().startswith('myex.com')) and t < max:
            time.sleep(.1)
            t = t + 1
        if t == max:
            print "WARNING: not on a home page...trying back"
            driver.back()
        current_page = driver.current_url
        elems = find_elems(driver, current_page)
        print "New search page with %d elements: %s" % (len(elems), current_page)
        for i in range(len(elems)):
            scroll_element_into_view(driver, elems, i, current_page)
            attempt_click(driver, elems, i, current_page)
            t = 0
            while not (driver.title.lower().startswith('naked pics of')) and t < max:
                time.sleep(0.2)
                if driver.title.lower().startswith('myex.com'):
                    driver.get(current_page)
                    print "WARNING: Profile slow to load. Reloading %s" % (current_page)
                    elems = find_elems(driver, current_page)
                    scroll_element_into_view(driver, elems, i, current_page)
                    attempt_click(driver, elems, i, current_page)
                else: 
                    time.sleep(0.05)
                    t = t + .05
            if t > max: print "WARNING: PAGE WITH TITLE %s NOT LOADED" % (driver.title)
            if driver.current_url == profile: #check if same profile i.e. one has been added at the top shifting them all along
                print "WARNING: skipping profile; duplicate of last [%s, %s]" % (driver.current_url, profile)
            else:
                profile = driver.current_url
                print "Processing profile %d: %s" % (count, driver.current_url)
                soup = BeautifulSoup(driver.page_source)
                while len(soup.findAll("div", { "class" : "profilehead" })) == 0:
                    time.sleep(0.1)
                    soup = BeautifulSoup(driver.page_source)
                processData(soup, csvFile)
            elems = []
            driver.back()
            elems = find_elems(driver, current_page)
            if count == total: 
                done = 1
                break
            count = count + 1
        attempt_next(driver, current_page)  
        print "Runtime: %s" % (str(datetime.timedelta(seconds=(time.time()-start))))  
    print "SUCCESS! File exported to %s. It took %s" % (csvFile, str(datetime.timedelta(seconds=(time.time()-start))))
    print "The average page took %d seconds to scrape" % ((time.time()-start)/count)
    driver.quit()

if __name__ == "__main__":
    main(sys.argv[1:])    
