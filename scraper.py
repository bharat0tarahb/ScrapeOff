#import necessary libraries
import requests 
import bs4
import re

#standard HTML/CSS tags
global html_attributes
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

#container types specific to zuaba corp page
global container_content_types
container_content_types = ['col-lg-12 col-md-12 col-sm-12 col-xs-12', 'col-12']

#table types specific to zuaba corp page
global table_content_types
table_content_types = ['table table-striped']


# with given parameters, this methods help fetch contents of 1 item
def fetchItem(data, attribute, class_type):
  try:
    if class_type is not None:
      item = data.find(attribute, class_ = class_type)
    else:
      item = data.find(attribute)
  except Exception as e:
    item = None
  return item

# with given parameters, this methods help fetch contents of all items
def fetchAllItems(data, attribute, class_type):
  try:
    if class_type is not None:
      items = data.find_all(attribute, class_ = class_type)
    else:
      items = data.find_all(attribute)
  except Exception as e:
    items = None
  return items

# this method helps in fetching information from <thead> tags
def fetchTableHead(table, table_attributes, special_attribute, class_type):
  try:
    tableHeadItem = fetchItem(table, table_attributes['tableHead'], class_type = None)
    tableHead = fetchTableRows(tableHeadItem, table_attributes, special_attribute, class_type)
  except Exception as e:
    tableHead = None
  return tableHead

# this method helps in fetching information from <td> tag
def fetchTableData(table, table_attributes, special_attribute):
  try:
    tableDatas = fetchAllItems(table, table_attributes['tableData'], class_type = None)
    row = []
    for tableData in tableDatas:
      tdResult = fetchItem(tableData, special_attribute, class_type = None)
      if tdResult is not None:
        row.append(tdResult.text.strip())
      else:
        row.append('Unable to fetch Value')
  except Exception as e:
    row = None
  return row

# this method helps in fetching information from <tr> tag
def fetchTableRows(table, table_attributes, special_attribute, class_type):
  rows = []
  rowItems = fetchAllItems(table, table_attributes['tableRow'], class_type = class_type)
  for rowItem in rowItems:
    row = fetchTableData(rowItem , table_attributes, special_attribute)
    rows.append(row)
  return rows

# this method helps in fetching information from <tbody tag
def fetchTableBody(table, table_attributes, special_attribute, class_type):
  try:
    tableBodyItem = fetchItem(table, table_attributes['tableBody'], class_type = None)
    if tableBodyItem is None:
      tableRows = fetchTableRows(table, table_attributes, special_attribute, class_type)
    else:
      tableRows = fetchTableRows(tableBodyItem, table_attributes, special_attribute, class_type)
  except Exception as e:
    tableRows = None
  return tableRows

#this method helps in writing data frame objects to excell file 
def writeDftoexcell(writer, dfList):
    for df in dfList:
        try:
            sheetName = df[1]
            sheetName = re.sub('/','', sheetName)
            df[0].to_excel(writer, sheet_name=str(sheetName[:29]))
        except Exception as e:
            print(e)
            pass
    writer.save()

# this method handles case1 type of contents where there are multiple tables of interest are nested in one class
def case1(content):
    rows = []
    tables = fetchAllItems(content, html_attributes['table'], class_type = table_content_types[0])
    for table in tables:
        tableHead = fetchTableHead(table, html_attributes, html_attributes['para1'], None)
        if tableHead is None or tableHead[0][0] == 'Unable to fetch Value':
            tableHead = fetchTableHead(table, html_attributes, html_attributes['para2'], None)
        if tableHead is not None:
            for th in tableHead:
                rows.append(th)
                print(th)
        tableRows = fetchTableBody(table, html_attributes, html_attributes['para1'], None)
        if tableRows[0] is None:
            tableRows = tableRows = fetchTableBody(table, html_attributes, html_attributes['para2'], None)
        if tableRows is not None:
            for tr in tableRows:
                rows.append(tr)
                print(tr)
    return rows

# this method handles case2 type of contents where there is only 1 table of interest in class
def case2(content):
    rows = []
    table = fetchItem(content, html_attributes['table'], class_type = table_content_types[0])
    tableHead = fetchTableHead(table, html_attributes, html_attributes['para1'], None)
    if tableHead is None or tableHead[0][0] == 'Unable to fetch Value':
        tableHead = fetchTableHead(table, html_attributes, html_attributes['para2'], None)
    if tableHead is not None:
        for th in tableHead:
            rows.append(th)
            print(th)
    tableRows = fetchTableBody(table, html_attributes, html_attributes['para1'], "accordion-toggle main-row")
    if tableRows[0] is None:
        tableRows = tableRows = fetchTableBody(table, html_attributes, html_attributes['para2'], "accordion-toggle main-row")
    if tableRows is not None:
        for tr in tableRows:
            rows.append(tr)
            print(tr)
    return rows

# this method handles case3 type of contents where there are only para <p> tags of interest
def case3(content):
    rows = []
    rowList = fetchAllItems(content, html_attributes['para1'], class_type = None)
    for row in rowList:
        rows.append(row.text.strip())
    return rows