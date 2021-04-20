# relevancyMatcher
A typo-tolerant search algorithm to identify the top matches.

# Design
<img src="https://github.com/bharat0tarahb/relevancyMatcher/blob/main/Relevancy%20Match%20Design.png" width=1000>

# How does it work?
When the user enters his word
    e.g: 'ynos'
* Startup names which have been stored in a csv file gets splitup into lists words
    e.g: 'Agnikul Cosmos' as ['Agnikul', 'Cosmos'] 
* The input string is the compared with each of the list item
    e.g: 'ynos' will be compared with each item in the list [['guvi', 'geek', 'labs', 'private', 'limited'], [.,.,.], ...]
* if any of the list items matches with the input string enterd by the user, the company name is fetched. 
    e.g: 'ynos' -> ['ynos', 'venture', 'engine'] = 'YNOS Venture Engine'

# How to run?
* install python3.6.7
* Open Terminal
* pip install -r requirements.txt
* Make this repo your 'Present Working Directory': Open Terminal and navigate to location where you have cloned the repo
* Type python3.6.7 main.py -i "YOUR INPUT STRING" -f "StartupNames.csv"