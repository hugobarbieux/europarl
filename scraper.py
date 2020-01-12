###########################################################################################
# We use a ScraperWiki library called pdftoxml to scrape PDFs.
# This is an example of scraping a simple PDF.
###########################################################################################

import scraperwiki
import urllib2
import lxml.etree

url = "https://www.europarl.europa.eu/doceo/document/PV-9-2019-07-15-RCV_FR.pdf"
pdfdata = urllib2.urlopen(url).read()
print "The pdf file has %d bytes" % len(pdfdata)

xmldata = scraperwiki.pdftoxml(pdfdata)
print "After converting to xml it has %d bytes" % len(xmldata)
print "Total nimber of characters", xmldata[0:]
root = lxml.etree.fromstring(xmldata)


#this line uses xpath, which is supported by lxml.etree (which has created root) to grab
#the contents of any <text> tags and put them all in a list variable called 'lines'
lines = root.findall('.//text[@font="8"]//b')

#create an empty dictionary variable called 'record'
record = {}

# loop through each item in the list, and assign it to a variable called 'line'
for line in lines:
    #create a variable called 'fontvalue', and use the get method to give it the value of
    #the <font> attribute of 'line'
    fontvalue = line.get("font")
    #print that variable
    print fontvalue
    
    #if that variable has a value of '3'
    if fontvalue == "10":
        #create a variable called 'result', use the find method to grab the contents of any
        #<b> tag (identified with XPath) in 'line', grab the text within that, and store it
        #in the variable
        result = line.find('.//b').text
        
        #continue on to next if statement
        continue
    #if 'fontvalue' is 8 AND the length of the text in 'line' is less than 11 characters
    #(counted with the len function)
    if fontvalue == "8" and len(line.text)<11:
        #grab the text in 'line' and put it in a new variable called 'party'
        party = line.text
        continue
        
    #if 'fontvalue' is 9
    if fontvalue == "9" and len(line.text)>1:
    #grab the text in 'line' and store it in a field called 'location' in the
    #dictionary variable 'names'
        record["names"] = line.text
        
        #store the value of the 'result' variable in a field called 'result' in the dictionary
        #variable 'record'
        record["result"] = result
        
        #store the value of the 'party' variable in a field called 'code' in the dictionary
        #variable 'party'
        record["party"] = party
        
        #print the value of 'record'
        print record
        
        #save those values in scraperwiki's sqlite database, with 'party' as the unique key
        scraperwiki.sqlite.save(['party'], record)
