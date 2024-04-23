#readxml.py - imports data from NS Power XML file and exports as CSV
#
#Usage: readxml.py (xmlFile.xml) (output.csv)
#
#March 12, 2024

import sys
from bs4 import BeautifulSoup
import datetime
import os

sensor = "sensor.nspower_energy_wh" #rename with your Home Assistant entity

units = "kWh"

#TSV/CSV column headers:
headers = ["statistic_id","unit","start","sum","state"]
delimiter = "\t" #either "\t" for tab separated values, or "," for comma separated value
lastdata = "latest.csv" #data file to store most recently imported data (so only new data is imported each time) (this file will be created if it doesn't exist)
header = delimiter.join(headers) + "\n" #join it all together

if len(sys.argv) < 3:
    print("Usage: python readxml.py INPUTFILE.xml OUTPUTFILE.csv")
    exit()

filename = sys.argv[1]
newfile = sys.argv[2]

if not os.path.exists(lastdata): #if the file doesn't exist, it must be first run, so create the data file and fill it with zeros
    with open(lastdata, 'w+') as l:
        l.write("0\n0")
        l.close()

with open(lastdata, 'r') as l:
    records = l.readlines()
    l.close()

latest = float(records[0]) #timestamp of most recent data
accumPower = float(records[1]) #last meter stamp

with open(filename, 'r') as f:
    data = f.read()

bs_data = BeautifulSoup(data, features="xml")
entries = bs_data.find_all('entry')

counter = 0

#create and/or erase the file
file = open(newfile, "w")
file.write(header)

for entry in entries:
    interval_readings = entry.find_all('espi:IntervalReading')
    output = []
    for interval_reading in interval_readings:
        start_tag = interval_reading.find('espi:start')
        value_tag = interval_reading.find('espi:value')

        # Get the text content of the tags if they exist
        start = start_tag.text if start_tag else None
        value = float(value_tag.text) if value_tag else 0
        value = value / 1000.0 #convert to kWh

        # convert epoch time to local time
        time = datetime.datetime.fromtimestamp(int(start))

        #generate list:

        output.append([time, value])

    hourSum = 0

    #if the generated list is empty, OR if the maximum value of all the power in a processed element is 0, then we know it's junk data (either solar or something else we aren't interested in, so we can ignore it)
    if len(output) > 0:
        if max(output, key=lambda x: x[1])[1] > 0:
            for element in output:
                counter = counter + 1
                hourSum = hourSum + element[1]
                if element[0].minute == 45:
                    #home assistant will only accept timestamps with :00 for the minutes
                    newLine = '{0}\t{1}\t{2}\t{3}\t{4}\n'.format(sensor, units, element[0].strftime('%d.%m.%Y %H:00'), str(accumPower), hourSum)
                    if float(element[0].timestamp()) > float(latest): #we only want to keep the data that's newer than what we've already imported
                        file.write(newLine)
                        latest = element[0].timestamp()
                        accumPower = accumPower + hourSum #keep the meter up to date
                        #print(accumPower)
                        print(f"{counter} {newLine}", end='') # prevent new linefeed, since we already have one
                    hourSum = 0

file.close()

with open(lastdata, 'w') as l:
    l.write(str(latest) + "\n" + str(accumPower))
    l.close()


