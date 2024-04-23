# gb-to-ha
Converts GreenButton XML files (as prepared by Nova Scotia Power) to a CSV format importable to Home Assistant (homeassistant-statistics).

It will keep track of the most recently imported data and on subsequent runs, will only put more recent data into the output CSV file.

For instructions on how to then import the generated file into Home Assistant, please see klausj1's excellent integration: https://github.com/klausj1/homeassistant-statistics

This has been tested on NS Power generated power usage XML files. Theoretically, it should work for other Green Button-generated XML files, but it hasn't been tested. If you have a chance to test it, let me know how it works!

<h1>Installation Requirements</h1>
Requires Beautiful Soup 4 (tested with version 4.12.2-2) - <code>sudo apt install python3-bs4</code> on Ubuntu.

<h1>Usage</h1>
<code>python3 readxml.py inputfile.xml output.csv</code><br><br>
You can then import <code>output.csv</code> via homeassistant-statistics.

