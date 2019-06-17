# Runs on Python 3.7. Packages that you need to have downloaded to run the code: beautiful soup, urlib.request

from bs4 import BeautifulSoup
from urllib.request import urlopen, Request
import re, os, csv

myfile = open("senate_websites.csv", "r")  # "r" to only read the file
senatefile = csv.reader(myfile)  # Get rows in the file
senatefilelist = []
for row in senatefile:
     senatefilelist.append(row)  # Storing all the info from the csv


def print_rows():
    for row in senatefilelist:
        print (row)    # Print all rows in the file, doing this to double-check info was read in correctly


# Creating empty lists to be filled in and used for naming files later
state = []
partyid = []
name = []
sourceAddress = []

def get_csv_fields():
    # Filling in those lists with info from csv
    for row in senatefilelist:
        state.append(row[0])
        partyid.append(row[1])
        name.append(row[2])
        sourceAddress.append(row[3])


def parse_data():
    # Beginning the scraping
    hdr = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
        'Accept-Encoding': 'none',
        'Accept-Language': 'en-US,en;q=0.8',
        'Connection': 'keep-alive'}  # Some of the websites have security, this pretends I'm manually going to each site
    for z in range(0, len(sourceAddress)):
        url = ''
        try:
            r = Request(sourceAddress[z], headers=hdr)
            url = urlopen(r).read()
        except  Exception as e:  # Checking for errors, keeps looping even if errors
            print(e)  # Prints error associated with not being able to access the website
            print(sourceAddress[z])  # Print website if not being accessed
        if url:
            soup = BeautifulSoup(url)
            # Get the text
            paragraphs = soup.findAll('p') # Catches all html tags <p>, this gets most of the text for us. To learn more inspect individual webpages and notice what tags they use.
            text = ''
            for paragraph in paragraphs:
                text += paragraph.text  # For each webpage, everytime python finds a <p> tag it adds the text for that tag to "text" for each page.
            if text:
                # Writing filenames
                filename = state[z] + "_" + partyid[z] + "_" + name[z] + '.txt'
                # Writing the files
                source = 'Senate Files/%s' % (filename)
                output = open(source, 'w')
                output.write(text)
                output.close()
            else:
                print(sourceAddress[z])  # Which websites don't use <p> in their formatting





# These can be uncommented when I want to re-create the files
if __name__ == '__main__':
   # print_rows()  # Uncomment only to check the data was read in correctly
   # get_csv_fields()  # Uncomment to get the data
   # parse_data()  # Uncomment to write the files
