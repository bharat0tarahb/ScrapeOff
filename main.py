#import necessary libraries
import requests
import bs4
import pandas as pd
import argparse
import scraper
import re
import os

if __name__ == '__main__':
    # construct the argument parse and parse the arguments
    ap = argparse.ArgumentParser() 
    ap.add_argument("-w", "--website", required=True, help="Website to scrape") # i is an argument which denoted input string
    args = vars(ap.parse_args())

    #importing global attributes from scraper
    html_attributes = scraper.html_attributes 
    container_content_types = scraper.container_content_types
    table_content_types = scraper.table_content_types
    
    
    res = requests.get(args["website"]) #send a GET request to website and store the response
    soup = bs4.BeautifulSoup(res.text, 'lxml') #make response a usable content with bs4 and lxml format
    
    # Fetching Name of the company
    companyName = scraper.fetchItem(soup, html_attributes['title'], class_type = None).text.strip().split(",")[0].split('-')[0].strip()
    
    #Initiate pandas excelwriter with the company name as file  name
    output_directory = 'outputs'
    if not os.path.exists(output_directory):
        os.mkdir(output_directory)
    writer = pd.ExcelWriter(f'{output_directory}/{companyName}.xlsx', engine='xlsxwriter') 
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
                rows = scraper.case1(content) #Handles case1 usecase and outputs a list of rows from tables
            elif tableName == 'Director Details':
                rows = scraper.case2(content) #Handles case2 usecase and outputs a list of rows from tables
            elif tableName == 'Contact Details':
                rows = scraper.case3(content) #Handles case3 usecase and outputs a list of rows from tables

            dfs.append([pd.DataFrame(rows), tableName]) #output rows are strored as data frame objects and contained in a list
    scraper.writeDftoexcell(writer, dfs) #each dataframe containing data from each table is been written to excell sheets and stored in to a file
    print(f'File {output_directory}/{companyName}.xlsx has been saved')

            