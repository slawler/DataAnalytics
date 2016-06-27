# -*- coding: utf-8 - Python 2.7.11 *-
"""
Description: Grab Veg Type from Soil Classification Data
Input(s): List of URLS
Output(s):Text field from URL
slawler@dewberry.com
Created on Tue Apr 19 15:08:33 2016
"""
#------------Load Python Modules--------------------#
import urllib
from bs4 import BeautifulSoup
#---From : http://stackoverflow.com/questions/1936466/beautifulsoup-grab-visible-webpage-text
#------------------------------BEGIN SCRIPT----------------------------------#

u1 = 'https://soilseries.sc.egov.usda.gov/OSD_Docs/D/DEERFIELD.html'
u2 = 'https://soilseries.sc.egov.usda.gov/OSD_Docs/W/WINDSOR.html'
urls = [u1,u2]
 
for url in urls:   
    html = urllib.urlopen(url).read()
    soup = BeautifulSoup(html)
    
    
    for script in soup(["script", "style"]):
        script.extract()    
    
    text = soup.get_text()
    lines = (line.strip() for line in text.splitlines())
    chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
    text = '\n'.join(chunk for chunk in chunks if chunk)
    
    textformat = text.encode('utf-8')
    splittext = textformat.splitlines()
    
    
    lookfor = 'USE AND VEGETATION'   
    idx = [i for i, s in enumerate(splittext) if lookfor in s] 
    veg = splittext[int(idx[0])] 
    
    print url 
    print veg + '\n'


