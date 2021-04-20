import requests
import bs4
import pandas as pd
import argparse
import scraper
import re

html_attributes = {
    "title": "title",
    "division": "div",
    "table": "table",
    "tableHead": "thead",
    "tableRow": "tr",
    "tableData": "td",
    "tableBody": "tbody",
    "para1": "p",
    "para2": "strong"
}

container_content_types = ['col-lg-12 col-md-12 col-sm-12 col-xs-12', 'col-12']
table_content_types = ['table table-striped']

if __name__ == '__main__':
    # construct the argument parse and parse the arguments
    ap = argparse.ArgumentParser() 
    ap.add_argument("-w", "--website", required=True, help="Website to scrape") # i is an argument which denoted input string
    args = vars(ap.parse_args())
    
    
    res = requests.get(args["website"]) #send a GET request to website and store the response
    soup = bs4.BeautifulSoup(res.text, 'lxml') #make response a usable content with bs4 and lxml format
    
    # Fetching Name of the company
    companyName = scraper.fetchItem(soup, html_attributes['title'], class_type = None).text.strip().split(",")[0].split('-')[0].strip()
    
    #Initiate pandas excelwriter with the company name as file  name
    writer = pd.ExcelWriter(f'{companyName}.xlsx', engine='xlsxwriter') 
    print(companyName)
    
    # Fetch decription of the company
    info = scraper.fetchItem(soup, html_attributes['division'], class_type = 'container information').text.strip()
    summary = info.replace('\r', '').split('\n')[0].strip()
    print(summary)

    dfs = [] #create a list object to store multiple data frames into different sheets.
    df = pd.DataFrame([['Company Name', companyName], ['Summary', summary]]) # load the data as data frame to easily write it into excell file
    dfs.append([df, 'Profile']) #each item of the data frames list will have dataframe and sheet name as a list
    
    #tables
    for content_type in container_content_types: #for each content type
        contents = scraper.fetchAllItems(soup, html_attributes['division'], class_type = content_type) #fetch all contents for the content type
        for content in contents: #iterate over each content
            tableName = scraper.fetchItem(content, 'h4', class_type = None).text.strip() #fetch table name
            print(tableName)
            rows = [] #create a list object to store rows and heads of the table 
            if tableName not in  ['Director Details', 'Contact Details']:
                tables = scraper.fetchAllItems(content, html_attributes['table'], class_type = table_content_types[0])
                for table in tables:
                    tableHead = scraper.fetchTableHead(table, html_attributes, html_attributes['para1'], None)
                    if tableHead is None or tableHead[0][0] == 'Unable to fetch Value':
                        tableHead = scraper.fetchTableHead(table, html_attributes, html_attributes['para2'], None)
                    if tableHead is not None:
                        for th in tableHead:
                            rows.append(th)
                            print(th)
                    tableRows = scraper.fetchTableBody(table, html_attributes, html_attributes['para1'], None)
                    if tableRows[0] is None:
                        tableRows = tableRows = scraper.fetchTableBody(table, html_attributes, html_attributes['para2'], None)
                    if tableRows is not None:
                        for tr in tableRows:
                            rows.append(tr)
                            print(tr)
            elif tableName == 'Director Details':
                table = scraper.fetchItem(content, html_attributes['table'], class_type = table_content_types[0])
                tableHead = scraper.fetchTableHead(table, html_attributes, html_attributes['para1'], None)
                if tableHead is None or tableHead[0][0] == 'Unable to fetch Value':
                    tableHead = scraper.fetchTableHead(table, html_attributes, html_attributes['para2'], None)
                if tableHead is not None:
                    for th in tableHead:
                        rows.append(th)
                        print(th)
                tableRows = scraper.fetchTableBody(table, html_attributes, html_attributes['para1'], "accordion-toggle main-row")
                if tableRows[0] is None:
                    tableRows = tableRows = scraper.fetchTableBody(table, html_attributes, html_attributes['para2'], "accordion-toggle main-row")
                if tableRows is not None:
                    for tr in tableRows:
                        rows.append(tr)
            elif tableName == 'Contact Details':
                rowList = content.find_all('p')
                for row in rowList:
                    rows.append(row.text.strip())

            dfs.append([pd.DataFrame(rows), tableName])
    scraper.writeDftoexcell(writer, dfs)

            