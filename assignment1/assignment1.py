# This script gathers faculty names, departments and degrees from Amherst
# College then writes that information to a CSV.

import re
import urllib.request
import csv

# open faculty directory
dr = urllib.request.urlopen("https://www.amherst.edu/academiclife/faculty_profiles")
dr = dr.read()

# traverse directory for faculty URL names
text = re.findall(r'<a href="/people/facstaff/(.*?)"', dr.decode())

faculty = []

for i in text:
    url = 'https://www.amherst.edu/people/facstaff/' + i

    page = urllib.request.urlopen(url)
    a_string = page.read()

    # parse full name
    try:
        name = re.search(r'(?<=<title>).*?(?= \|)', a_string.decode()).group(0)
        # parse first and last names
        lastname = re.search(r'.*?(?=,)', name).group(0)
        firstname = re.search(r', (.*)', name).group(1)
 
        # parse department
        dept = re.search(r'(?<=<span class="category">)<(.*?)>(.*?)(?=</a>)', a_string.decode()).group(2)
        
        # The code below is commented out because the Amherst faculty pages
        # do not have a standardized way to indicate degrees. As a result, some
        # pages have no degrees, some are in paragraphs of text, etc. So I opted
        # to not list any, but below is some theoretical code if the degree were
        # in a standardized format.
        
        # try:
        #     degree = re.search(r'ph\.*d\.*\s*(.*?)[,\n]', a_string.decode()
        #     , re.I).group(1)
        # except AttributeError:
        degree = None
    
        faculty.append([lastname, firstname, dept, degree])   
    except AttributeError:
        pass

# create csv file and open
f = open('assignment1.csv', 'wt')

# iterate through faculty and write to csv
try:
    writer = csv.writer(f)
    writer.writerow( ('Last Name', 'First Name', 'Department', 'Degree') )
    for i in faculty:
        writer.writerow((i[0], i[1], i[2], i[3]))
finally:
    f.close()
