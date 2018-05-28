import requests
import pandas as pd
from lxml import etree as et
from collections import defaultdict
from data_clean import drop_duplicates
import settings

#   Create dictionary of required BM reports
bm_reports = {'B1770': ['imbalancePriceAmountGBP'],
               'B1780': ['imbalanceQuantityMAW']}
columns = ['settlementDate', 'settlementPeriod']
#bm_reports = {'B1780': ['imbalanceQuantityMAW']}
resultsList = []

def getXMLReport(reportCode):

    url = ("https://api.bmreports.com/BMRS/"+reportCode+""
    "/v1?APIKey="+settings.ELEXON_API_KEY+"&SettlementDate=2018-05-19"
    "&Period=*&ServiceType=xml")

    #   request for bm report
    r = requests.get(url).content

    return r

def convertToDF(xml, cols):

    #   get the xml root which is "<response>"
    root = et.fromstring(xml)

    #   add specific report columns
    colHeadings = [*columns]
    colHeadings.extend(cols)

    output = defaultdict(list)

    #   append revelant data to output dict
    for item in root.findall("./responseBody/responseList/item"):
        for child in item:
            if child.tag in colHeadings:
                output[child.tag].append(child.text)

    #   convert dict to a pandas dataframe
    df = pd.DataFrame().from_dict(output)

    #   reorder df to required format
    df_reindexed = df.reindex(columns=colHeadings)
    df_reindexed['settlementPeriod']= df_reindexed['settlementPeriod'].astype(int)
    sorted_df = df_reindexed.sort_values(by='settlementPeriod', ascending=True)

    if len(sorted_df) > 50:
        sorted_df.drop_duplicates(['settlementPeriod'], keep='first',inplace = True)

    resultsList.append(output)
    return

def mergeFrames():

    print(len(resultsList))
    return

def main():
    bm_reports_list = [*bm_reports]

    #for report in bm_reports_list:
    for report, cols in bm_reports.items():
        xmlReport = getXMLReport(report)
        convertToDF(xmlReport, cols)

    mergeFrames()

if __name__ == '__main__':
    main()
