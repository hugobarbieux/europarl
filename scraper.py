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
print "The first 2000 characters are: ", xmldata[0:]
root = lxml.etree.fromstring(xmldata)

# this line uses xpath to find <text> tags
lines = root.findall('.//text[@font="9"]//text')
print lines
for line in lines:
    print line.text
    
record = {}
for line in lines:
    record["date"] = line.text
    scraperwiki.sqlite.save(["date"], record)
    print record
