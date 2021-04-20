# ScrapeOff
A Web scraper to collect information about startups from Zuaba Corp

# Design
<img src="https://github.com/bharat0tarahb/ScrapeOff/blob/main/ScrapOff%20Design.png" width=1000>

# How does it work?
When the user enters a company's profile from zaubacorp
    e.g: 'https://www.zaubacorp.com/company/YNOS-VENTURE-ENGINE-CC-PRIVATE-LIMITED/U74999TN2017PTC115985'
* The contents of the web page is extracted into a usable format
* The webpage is constructed using several componets such as Divisions, Tables etc.
* Each of the components is analysed and information is extracted.

# How to run?
* install python3.6.7
* Open Terminal
* pip install -r requirements.txt
* Make this repo your 'Present Working Directory': Open Terminal and navigate to location where you have cloned the repo
* Type python3.6.7 main.py -w COMPANY WEB LINK 