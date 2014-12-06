__author__ = 'tmwsiy'

from geopy.geocoders import Nominatim


geolocator = Nominatim()
location = geolocator.geocode("Heswall  YT England", timeout=15)
print(location.address)