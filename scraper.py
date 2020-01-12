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
print "All pdf characters are: ", xmldata[0:]
root = lxml.etree.fromstring(xmldata)

# this line uses xpath, to find <text> tags
lines = root.findall('.//text[@height="13"]//b')
print lines
for line in lines:
    print line.text
    
#create a variable, record, and make it an empty dictionary
record = {}
for line in lines:
    record["result"] = line.text
    scraperwiki.sqlite.save(['result'], record)
