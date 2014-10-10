__author__ = 'tmwsiy'

from geopy.geocoders import Nominatim


geolocator = Nominatim()
location = geolocator.geocode("Mississauga Canada ON")
print(location.address)