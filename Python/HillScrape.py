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

def processIndividualRunner(soup,out):
    Runner = soup.find("span", id = "lblRunner")
    print Runner.text
    Club = soup.find("span", id = "lblClubName")
    print Club.text

    Runners = []
    Clubs = []
    Positions = []
    Races = []
    Dates = []
    Times = []
    WinnerPercentages = []

    for results in soup.findAll(id="dgRunnerResults"):
        for run in results.find_all('tr', class_=lambda x: x != 'StandardGridHeader'):
#        for run in results.findAll("tr"):
            Runners.append(Runner.text)
            Clubs.append(Club.text)
            Positions.append(run.contents[2].text)
            Races.append(run.contents[3].text)
            Dates.append(run.contents[4].text)
            Times.append(run.contents[5].text)
            WinnerPercentages.append(run.contents[6].text)

    csvfile = open(out, 'ab')
    writer = csv.writer(csvfile)
    try:
        for Runner, Club, Postition, Race, Date, Time, WinnerPercentage in zip(Runners, Clubs, Positions, Races, Dates, Times, WinnerPercentages):
            row = [Runner, Club, Postition, Race, Date, Time, WinnerPercentage]
            writer.writerow([col.encode('utf-8') for col in row])
    except:
        print "ERROR: Didn't write to CSV correctly"
    csvfile.close()

def processRunners(driver,soup,out,nr):
    nr=len(soup.findAll(href = re.compile('^RunnerDetails.aspx')))
    for link in soup.findAll(href = re.compile('^RunnerDetails.aspx')):
        address = 'http://scottishhillracing.co.uk/' + link.attrs['href']
        print address
        driver.get(address)
        RunnerSoup = BeautifulSoup(driver.page_source,"lxml")
        processIndividualRunner(RunnerSoup,out)

def main(argv):

    csvFile = 'SHR' #init
    csvfile = open(csvFile, 'wb')
    writer = csv.writer(csvfile)
    writer.writerow(["Runner", "Position", "Race", "Date", "Time", "%Winner"])
    csvfile.close()

    page = 1
    runnersOnPage = 75

    driver = webdriver.Chrome('/home/alastair/anaconda2/bin/chromedriver')
    driver.implicitly_wait(10)
    driver.get('http://scottishhillracing.co.uk/Runners.aspx')
    driver2 = webdriver.Chrome('/home/alastair/anaconda2/bin/chromedriver')
    driver2.implicitly_wait(10)
    driver2.get('http://scottishhillracing.co.uk/Runners.aspx')

    while runnersOnPage >=75:
    #while page <=6:


        soup = BeautifulSoup(driver.page_source,"lxml")
        processRunners(driver2,soup,csvFile,runnersOnPage)

        if runnersOnPage >=75:
            if page ==5:
                nextpage = driver.find_element_by_link_text('...')
            elif page%5 == 0:
                nextpage = driver.find_elements_by_link_text('...')[1]
            else:
                nextpage = driver.find_element_by_link_text(str(page+1))
            nextpage.click()
            page += 1





if __name__ == "__main__":
    main(sys.argv[1:])