__author__ = 'tmwsiy'

import requests, time, random
import bs4, pymongo

# http://www.nltk.org/


# Connection to Mongo DB
conn = None
try:
    conn=pymongo.MongoClient()
    print ("Connected successfully!!!")
except pymongo.errors.ConnectionFailure as e:
   print("Could not connect to MongoDB: " + e)

db = conn.corpus
collection = db.sightings
#url_prefix='https://web.archive.org/web/20140824090651/'
url_prefix=''
current_doc={}
#response = requests.get(url_prefix+'http://www.nuforc.org/webreports/ndxevent.html')
#time.sleep(1)
max_retry_count=20
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/37.0.2049.0 Safari/537.36'
}
with open('months.txt', 'r') as f:
    months = [line.strip() for line in f]
for month in months:
    if month.endswith(".html") and not "HREF" in month:
        print 'starting month:', month
        monthly_page = ''
        timeout_counter=0
        success = False
        while not success:
            if timeout_counter < max_retry_count :
                try:
                    monthly_page = requests.get(url_prefix+'http://www.nuforc.org/webreports/' + month,timeout=10, headers=headers)
                    success = True
                except:
                    print 'Problem retrieving ', 'http://www.nuforc.org/webreports/' + month
                    time.sleep(10)
                    timeout_counter+=1
            else:
                print 'Retry count exceeded:', 'http://www.nuforc.org/webreports/' + month
                break

        #print monthly_page.text
        soup = bs4.BeautifulSoup(monthly_page.text.replace("HREF","href").replace("<A","<a"), "html5lib")
        #print soup.get_text()
        for link in soup.find_all('a'):
            if not link.get('href').startswith("http"):
                url = link.get('href')
                current_doc={}
                time.sleep(random.randrange(2,8,1))
                detail_page = ''
                timeout_counter=0
                success = False
                while not success:
                    if timeout_counter < max_retry_count :
                        try:
                            detail_page = requests.get(url_prefix+'http://www.nuforc.org/webreports/' + url, timeout=10, headers=headers)
                            success = True
                        except:
                            print 'Problem retrieving ', 'http://www.nuforc.org/webreports/' + url
                            time.sleep(10)
                            timeout_counter+=1
                    else:
                        print 'Retry count exceeded:', 'http://www.nuforc.org/webreports/' + url
                        break

                detail_soup = bs4.BeautifulSoup(detail_page.text)
                #for tag in soup.find_all('td'):
                #    print(tag.get_text())
                text = detail_soup.get_text()
                #print text
                # set counter to find text blurb set to high number so it will not trigger until the first "Occured" line is found
                counter=100
                for line in text.split('\n'):
                    #line = line.strip()
                    if line.startswith('Occurred :'):
                        print 'header:', line
                        occ_start=11
                        occ_end=line.find('Reported:')
                        print 'occurred:', line[occ_start:occ_end]
                        current_doc['occurred'] = line[occ_start:occ_end]
                        rep_start=occ_end+10
                        rep_end=line.find('Posted:')
                        print 'reported:', line[rep_start:rep_end]
                        current_doc['reported'] = line[rep_start:rep_end]
                        pos_start=rep_end+7
                        pos_end=line.find('Location:')
                        print 'posted:', line[pos_start:pos_end]
                        current_doc['posted'] = line[pos_start:pos_end]
                        loc_start=pos_end+9
                        loc_end=line.find('Shape:')
                        print 'location:', line[loc_start:loc_end]
                        current_doc['location'] = line[loc_start:loc_end]
                        shp_start=loc_end+6
                        shp_end=line.find('Duration:')
                        print 'shape:', line[shp_start:shp_end]
                        current_doc['shape'] = line[shp_start:shp_end]
                        dur_start=shp_end+9
                        print 'duration:', line[dur_start:]
                        current_doc['duration'] = line[dur_start:]

                        #print 'posted:', line[102:111]
                        counter=0
                    if counter == 5:
                        print 'blurb:', line
                        current_doc['description'] = line
                    counter+=1
                collection.insert(current_doc)

        time.sleep(1)

#print response.text
#print response.text.replace("HREF= ","HREF=\"").replace(".html>",".html\">")

#soup = bs4.BeautifulSoup(response.text.replace("HREF= ","HREF=\"").replace(".html>",".html\">"))

#print soup.get_text()

