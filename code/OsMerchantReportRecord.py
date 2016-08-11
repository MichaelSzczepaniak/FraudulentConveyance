


class OsMerchantReportRecord:
    def __init__(self, os_report_dict, os_merchant_dict):
        self._isoNum = os_report_dict['isoNum']
        self._reportYear = os_report_dict['reportYear']
        self._reportMonth = os_report_dict['reportMonth']
        self._busName = os_merchant_dict['busName']
        self._corpName = os_merchant_dict['corpName']
        
    def getIso():
        return self._isoNum
        
    def getMonth():
        return self._reportMonth
        
    def getYear():
        return self._reportYear
        
    def getBusName():
        return self._busName
        
    def getCorpName():
        return self._corpName
    
    def toString(self):
        return "{}, {}, {}, {}, {}".format(self._busName, self._corpName,
        self._isoNum, self._reportYear, self._reportMonth, )
    
    
        
if "__name__" == "__main__" : main()