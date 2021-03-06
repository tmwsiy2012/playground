__author__ = 'tmwsiy'

import pymongo, re, time, traceback
from dateutil.parser import parse
from geopy.geocoders import Nominatim
import requests, json
from urllib import quote
import pprint
from collections import OrderedDict

postal_abbreviation_lookup={
    "AB": "Alberta",
    "BC": "British Columbia",
    "MB": "Manitoba",
    "NB": "New Brunswick",
    "NL": "Newfoundland",
    "NS": "Nova Scotia",
    "NT": "Nortwest Territories",
    "NU": "Nunavut",
    "ON": "Ontario",
    "PE": "Prince Edward Island",
    "QC": "Quebec",
    "SK": "Saskatchewan",
    "YT": "Yukon",
    "AL": "Alabama",
    "AK": "Alaska",
    "AS": "American Samoa",
    "AZ": "Arizona",
    "AR": "Arkansas",
    "CA": "California",
    "CO": "Colorado",
    "CT": "Connecticut",
    "DE": "Delaware",
    "DC": "District Of Columbia",
    "FM": "Federated States Of Micronesia",
    "FL": "Florida",
    "GA": "Georgia",
    "GU": "Guam",
    "HI": "Hawaii",
    "ID": "Idaho",
    "IL": "Illinois",
    "IN": "Indiana",
    "IA": "Iowa",
    "KS": "Kansas",
    "KY": "Kentucky",
    "LA": "Louisiana",
    "ME": "Maine",
    "MH": "Marshall Islands",
    "MD": "Maryland",
    "MA": "Massachusetts",
    "MI": "Michigan",
    "MN": "Minnesota",
    "MS": "Mississippi",
    "MO": "Missouri",
    "MT": "Montana",
    "NE": "Nebraska",
    "NV": "Nevada",
    "NH": "New Hampshire",
    "NJ": "New Jersey",
    "NM": "New Mexico",
    "NY": "New York",
    "NC": "North Carolina",
    "ND": "North Dakota",
    "MP": "Northern Mariana Islands",
    "OH": "Ohio",
    "OK": "Oklahoma",
    "OR": "Oregon",
    "PW": "Palau",
    "PA": "Pennsylvania",
    "PR": "Puerto Rico",
    "RI": "Rhode Island",
    "SC": "South Carolina",
    "SD": "South Dakota",
    "TN": "Tennessee",
    "TX": "Texas",
    "UT": "Utah",
    "VT": "Vermont",
    "VI": "Virgin Islands",
    "VA": "Virginia",
    "WA": "Washington",
    "WV": "West Virginia",
    "WI": "Wisconsin",
    "WY": "Wyoming"
}

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/37.0.2049.0 Safari/537.36'
}



def try_search_suggestion(location_string):
    tld= 'com'
    lang='en'
    query= quote(location_string.encode('utf-8') )
    ds=''

    url = "http://clients1.google.%s/complete/search?hl=%s&q=%s&json=t&ds=%s&client=serp" %(tld, lang, query, ds)
    #print url
    response = requests.get(url,timeout=10, headers=headers)
    result = json.loads(response.content)
    suggestions = [i for i in result[1]]
    return suggestions

def set_description(new_document):
        new_description = ''
        #print 'new', post['description']
        indexes = [(m.start(0), m.end(0)) for m in re.finditer('[a-z\.{1,3}][A-Z]', post['description'])]
        count=0
        prev_end=0
        for index in indexes:
            new_description = new_description + post['description'][prev_end:index[0]+1] + ' '
            prev_end= index[1]-1
            count += 1
        new_description = new_description + post['description'][prev_end:]
        m = re.search('\(\((NUFORC Note:.*\))\)',new_description)
        if m:
            #found match
            new_document['description']= new_description[:-len(m.group(0))]
            new_document['nuforc_notes']= m.group(0)[16:-5].strip()
            new_document['nuforc_editor']= m.group(0)[-5:-2].strip()

        else:
            # 'did NOT find match'
            new_document['description']=new_description

stop_words = set(['facing', 'counties', 'county', 'looking', 'at', 'sea', 'up', 'area', 'above', 'near', 'of', 'outside' ])

def set_location(new_document, geolocator):
        try:
            #new_document['sanitized_location'] = re.sub(r'\([.*)]*\)', '', post['location'].strip())
            sanitized_location = post['location'].strip()

            # first remove stop words
            #" ".join(filter(lambda word: word not in stop_words, sanitized_location.split()))
            sanitized_location = ' '.join([word for word in sanitized_location.split() if word.lower() not in stop_words])


            # remove stuff in parenthesis but save to try later if we have problems
            paren_stuff = ''
            m = re.search('\((.*)\)',sanitized_location)
            if m:
                paren_stuff = sanitized_location[m.start(0)+1:m.end(0)-1]
                test_paren= paren_stuff.split('/')
                if len(test_paren) > 1:
                    paren_stuff = test_paren[1]
                #print 'parenstuff:', paren_stuff
                sanitized_location = sanitized_location[:m.start(0)] + sanitized_location[m.end(0)+1:]
                #print 'NEWFIX', sanitized_location

            test_slash = sanitized_location.split('/')
            if len(test_slash) > 1 :
                #print 'fixed slash, new location', test_slash[1], 'previous:', sanitized_location
                sanitized_location = test_slash[1]


            new_document['sanitized_location'] = sanitized_location
            location = geolocator.geocode(sanitized_location, timeout=15)
            if location:
                # validate
                location_parts = sanitized_location.split(',')
                # sanity check for correct US state
                if len(location_parts) == 2:
                    state = location_parts[-1].upper().strip()
                    if state in postal_abbreviation_lookup:
                        if postal_abbreviation_lookup[state] not in location.address:
                            #print state, 'not correct state for ', location.address
                            #
                            new_location = ''
                            for i in location_parts[:-1]:
                                new_location = new_location + i
                            new_location = new_location + ' '+ postal_abbreviation_lookup[state]
                            #print new_location
                            location = geolocator.geocode(new_location, timeout=15)
                            if location and postal_abbreviation_lookup[state] not in location.address:
                                #print 'town not found, just do state', states[state]
                                location = geolocator.geocode(postal_abbreviation_lookup[state], timeout=15)
                                if not location:
                                    raise Exception('failed on just state/country')
                if len(location_parts) > 2:
                    print 'found more than two parts from initial split().. sanitaized_location', sanitized_location, ':', location.address


            else:
                #first attempt failed
                ## try and add back the paren stuff to the end

                location = geolocator.geocode(sanitized_location + ' ' + paren_stuff, timeout=15)
                if not location:
                    #ok now replace any state/province abbreviations with full text
                    for word in sanitized_location.split():
                        for postal_abbr in postal_abbreviation_lookup:
                            sanitized_location.replace(postal_abbr, postal_abbreviation_lookup[postal_abbr])
                    # try again
                    location = geolocator.geocode(sanitized_location + ' ' + paren_stuff, timeout=15)
                    if not location:
                        # next try google
                        suggestions= try_search_suggestion(sanitized_location+ ' ' + paren_stuff)
                        if suggestions:
                            location = geolocator.geocode(suggestions[0], timeout=15)



            new_document['lat'] = location.latitude
            new_document['lon'] = location.longitude
            new_document['location']= location.address
            new_document['raw_location']= post['location'].strip()

        except Exception,e:
            print 'problem parsing address:', post['location'].strip()
            print 'after sanitation:', sanitized_location
            if len(paren_stuff) > 1:
                print 'paren_stuff', paren_stuff
            print str(e.message)
            traceback.print_exc()

# Connection to Mongo DB
source_data = None
destination_data = None
try:
    source_data= pymongo.MongoClient()
    destination_data= pymongo.MongoClient()
    print "Connected successfully!!!"
except pymongo.errors.ConnectionFailure as e:
   print "Could not connect to MongoDB: " + str(e)

geolocator = Nominatim()
source_db = source_data.corpus
source_collection = source_db.sightings
dest_db = destination_data.corpus
dest_collection = dest_db.sightings_geo
source_collection
dest_collection.remove()
for post in source_collection.find().batch_size(10):
    if 'description' in post:
        #time.sleep(0.025)
        #print '\n\n'
        new_document= {}
        set_description(new_document)
        set_location(new_document, geolocator)
        try:
            new_document['occurred']= parse(post['occurred'].split('(')[0].strip())
            new_document['reported']= parse(post['reported'].split('M')[0] + 'M')
            new_document['posted']= parse(post['posted'].strip())
            new_document['shape']= post['shape'].strip()
            new_document['duration']= post['duration']
            dest_collection.insert(new_document)
        except Exception,e:
            print str(e)
            print 'post[\'reported\']', post['reported']
            print 'post[\'occurred\']',post['occurred']
            print 'post[\'posted\']',post['posted']
            print 'post[\'location\'].strip()', post['location'].strip()



#re.finditer(pattern, string[, flags])