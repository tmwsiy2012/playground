__author__ = 'tmwsiy'

import requests, time
import bs4



response = requests.get('http://www.nuforc.org/webreports/ndxevent.html')
time.sleep(1)
for chunk in response.text.split(">"):
    if chunk.endswith(".html") and not "HREF" in chunk[-15:]:
        monthly_page = requests.get('http://www.nuforc.org/webreports/' + chunk[-15:])
        #print monthly_page.text
        soup = bs4.BeautifulSoup(monthly_page.text.replace("HREF","href").replace("<A","<a"), "html5lib")
        #print soup.get_text()
        for link in soup.find_all('a'):
            if not link.get('href').startswith("http"):
                detail_page = requests.get('http://www.nuforc.org/webreports/' + link.get('href'))
                detail_soup = bs4.BeautifulSoup(detail_page.text, "html5lib")

                print detail_soup.get_text()
        time.sleep(1)

#print response.text
#print response.text.replace("HREF= ","HREF=\"").replace(".html>",".html\">")

#soup = bs4.BeautifulSoup(response.text.replace("HREF= ","HREF=\"").replace(".html>",".html\">"))

#print soup.get_text()

