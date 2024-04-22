# gb-to-ha
Converts GreenButton XML files (as prepared by Nova Scotia Power) to a CSV format importable to Home Assistant (homeassistant-statistics).

It will keep track of the most recently imported data and on subsequent runs, will only put new data into the output CSV file.

For instructions on how to then import the generated file into Home Assistant, please see klausj1's excellent integration: https://github.com/klausj1/homeassistant-statistics

<h1>Usage</h1>
<code>python3 readxml.py inputfile.xml output.csv</code>

This has been tested on NS Power generated power usage XML files. Theoretically, it should work for other Green Button-generated XML files, but it hasn't been tested. If you have a chance to test it, let me know how it works!

