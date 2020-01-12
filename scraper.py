#import our libraries
import scraperwiki
import urllib2
import lxml.etree

#create a variable called 'url' and then read what's there
url = "https://www.europarl.europa.eu/doceo/document/PV-9-2019-07-15-RCV_FR.pdf"
pdfdata = urllib2.urlopen(url).read()
print "The pdf file has %d bytes" % len(pdfdata)

#convert to xml and print some info
xmldata = scraperwiki.pdftoxml(pdfdata)
print "After converting to xml it has %d bytes" % len(xmldata)
root = lxml.etree.fromstring(xmldata)

# this line uses xpath, which is supported by lxml.etree (which has created root) to grab the contents of any <text tags and put them all in a list variable called 'lines'
lines = root.findall('.//text')
#create an empty dictionary variable called 'record'
record = {}
#Create a variable to store an index that we can use as a unique key
uniquekey = 0
# loop through each item in the list, and assign it to a variable called 'line'
for line in lines:
    #create a variable called 'fontvalue', and use the get method to give it the value of the <font attribute of 'line'
    fontvalue = line.get("font")
    #print that variable
    print fontvalue
    #if that variable has a value of '12'
    if fontvalue == "12":
        #create a variable called 'date', use the find method to grab the contents of any <b> tag (identified with XPath) in 'line', grab the text within that, and store it in the variable
        date = line.find('.//b').text
        #continue on to next if statement
        continue
    #if 'fontvalue' is 9 AND the length of the text in 'line' is more than 1 characters
    if fontvalue == "9" and len(line.text)>1:
        #grab the text in 'line' and store it in a field called 'location' in the dictionary variable 'record'
        record["location"] = line.text
        #store the value of the 'date' variable in a field called 'date' in the dictionary variable 'record'
        record["date"] = date
        #print the value of 'record'
        print record
        #increment our uniquekey variable by 1
        uniquekey += 1
        #store it in 'record' with the same label
        record["uniquekey"] = uniquekey
        #save those values in scraperwiki's sqlite database, with 'code' as the unique key
        scraperwiki.sqlite.save(['uniquekey'], record)
