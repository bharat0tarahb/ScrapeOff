import requests
import bs4


def fetchItem(data, attribute, class_type):
  try:
    if class_type is not None:
      item = data.find(attribute, class_ = class_type)
    else:
      item = data.find(attribute)
  except Exception as e:
    item = None
  return item


def fetchAllItems(data, attribute, class_type):
  try:
    if class_type is not None:
      items = data.find_all(attribute, class_ = class_type)
    else:
      items = data.find_all(attribute)
  except Exception as e:
    items = None
  return items


def fetchTableHead(table, table_attributes, special_attribute):
  try:
    tableHeadItem = fetchItem(table, table_attributes['tableHead'], class_type = None)
    tableHead = fetchTableRows(tableHeadItem, table_attributes, special_attribute)
  except Exception as e:
    tableHead = None
  return tableHead


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


def fetchTableRows(table, table_attributes, special_attribute):
  rows = []
  rowItems = fetchAllItems(table, table_attributes['tableRow'], class_type = None)
  for rowItem in rowItems:
    row = fetchTableData(rowItem , table_attributes, special_attribute)
    rows.append(row)
  return rows


def fetchTableBody(table, table_attributes, special_attribute):
  try:
    tableBodyItem = fetchItem(table, table_attributes['tableBody'], class_type = None)
    if tableBodyItem is None:
      tableRows = fetchTableRows(table, table_attributes, special_attribute)
    else:
      tableRows = fetchTableRows(tableBodyItem, table_attributes, special_attribute)
  except Exception as e:
    tableRows = None
  return tableRows


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