import requests
import pandas as pd
from lxml import etree as et
import settings

#   Create dictionary of required BM reports
bm_reports = {'B1770': ['imbalancePriceAmountGBP', 'priceCategory'],
               'B1780': ['imbalanceQuantityMAW']}

def getReport(reportCode):

    url = ("https://api.bmreports.com/BMRS/"+reportCode+""
    "/v1?APIKey="+settings.ELEXON_API_KEY+"&SettlementDate=2018-05-19"
    "&Period=1&ServiceType=xml")

    #   request for bm report
    r = requests.get(url)

    #   convert xml string to object
    tree = et.parse(r.content)
    root = tree.getroot()

    print(root.tag)

    return


def main():
    bm_reports_list = [*bm_reports]

    for report in bm_reports_list:
         getReport(report)

if __name__ == '__main__':
    main()
