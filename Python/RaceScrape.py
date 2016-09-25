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

def processIndividualRace(soup,out):
    Race = soup.find("span", id = "lblRaceName").text
    print Race
    try:
        Venue = soup.find("span", id = "lblVenue").text
    except:
        Venue = "-"
    try:
        Distance = soup.find("span", id = "lblDistance").text
    except:
        Distance = "-"
    try:
        Climb = soup.find("span", id = "lblClimb").text
    except:
        Climb = "-"
    try:
        M_record_time = soup.find("span", id = "lblMensRecordTime").text
    except:
        M_record_time = "-"
    try:
        M_record_holder = soup.find("span", id = "lblMensRecordHolder").text
    except:
        try:
            M_record_holder = soup.find("span", id = "hypMensRecordHolder").text
        except:
            M_record_holder = "-"
    try:
        M_record_year = soup.find("span", id = "lblMensRecordYear").text
    except:
        M_record_year = "-"
    try:
        F_record_time = soup.find("span", id = "lblWomensRecordTime").text
    except:
        F_record_time = "-"
    try:
        F_record_holder = soup.find("span", id = "lblWomensRecordHolder").text
    except:
        try:
            F_record_holder = soup.find("span", id = "hypWomensRecordHolder").text
        except:
            F_record_holder = "-"
    try:
        F_record_year = soup.find("span", id = "lblWomensRecordYear").text
    except:
        F_record_year = "-"


    csvfile = open(out, 'ab')
    writer = csv.writer(csvfile)
    try:
        row = [Race, Venue, Distance, Climb, M_record_time, M_record_holder, M_record_year, F_record_time, F_record_holder, F_record_year]
        writer.writerow([col.encode('utf-8') for col in row])
    except:
        print "ERROR: Didn't write to CSV correctly"
    csvfile.close()

def processRaces(driver,soup,out):
    for linkbox in soup.findAll("span", id = re.compile('^ctl04_lbl')):
        try:
            link= linkbox.find(href = re.compile('^RaceDetails.aspx'))
            address = 'http://scottishhillracing.co.uk/' + link.attrs['href']
            print address
            driver.get(address)
            RaceSoup = BeautifulSoup(driver.page_source,"lxml")
            processIndividualRace(RaceSoup,out)
        except:
            print "Error"

def main(argv):

    csvFile = 'Races' #init
    csvfile = open(csvFile, 'wb')
    writer = csv.writer(csvfile)
    writer.writerow(["Race", "Venue", "Distance", "Climb", "M_record_time", "M_record_holder", "M_record_year", "F_record_time", "F_record_holder", "F_record_year"])
    csvfile.close()

    page = 1

    driver = webdriver.Chrome('/home/alastair/anaconda2/bin/chromedriver')
    driver.implicitly_wait(10)
    driver.get('http://scottishhillracing.co.uk/ResultsSummary.aspx')

    soup = BeautifulSoup(driver.page_source,"lxml")
    processRaces(driver,soup,csvFile)




if __name__ == "__main__":
    main(sys.argv[1:])