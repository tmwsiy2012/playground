__author__ = 'tmwsiy'
import urllib, zipfile, tempfile, os

data_url = "http://www.csc.uncw.edu/mac_lists.zip"

tmp_zip = tempfile.mkdtemp()
name, hdrs = urllib.urlretrieve(data_url, tmp_zip + '\mac_lists.zip')
zip = zipfile.ZipFile(name)
zip.extractall(path=tmp_zip)
for f in os.listdir(os.path.join(tmp_zip,'mac_lists')):
    print 'new file', f
    csv_file = open(os.path.join(tmp_zip,'mac_lists',f), "r")
    for line in csv_file.readlines():
        split_line = line.split(',')
        if len(split_line) > 6 and not "Workstation" in split_line[0]:
            print split_line[0], split_line[7]

