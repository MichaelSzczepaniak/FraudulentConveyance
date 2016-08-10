


class OsMerchantReportRecord:
    def __init__(self, os_report_dict, os_merchant_dict):
        self._isoNum = os_report_dict['isoNum']
        self._reportYear = os_report_dict['reportYear']
        self._reportMonth = os_report_dict['reportMonth']
        self._busName = os_merchant_dict['busName']
        
    def getIso():
        return self._isoNum
        
    def getMonth():
        return self._reportMonth
        
    def getYear():
        return self._reportYear
    
    def toString(self):
        return "{}, {}, {}, {}".format(self._isoNum, self._reportYear, self._reportMonth, self._busName)
    
    
        
if "__name__" == "__main__" : main()