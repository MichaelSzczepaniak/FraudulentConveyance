


class OsMerchantReportRecord:
    def __init__(self, os_report_dict, os_merchant_dict):
        ## info extracted from file name
        self._isoNum = os_report_dict['isoNum']
        self._reportYear = os_report_dict['reportYear']
        self._reportMonth = os_report_dict['reportMonth']
        ## info extracted from reports
        self._busName = os_merchant_dict['busName']
        self._corpName = os_merchant_dict['corpName']
        self._contact = os_merchant_dict['contact']
        self._phone = os_merchant_dict['phone']
        self._address = os_merchant_dict['address']
        self._city = os_merchant_dict['city']
        self._province = os_merchant_dict['province']
        self._postalCode = os_merchant_dict['postalCode']
        self._timeZone = os_merchant_dict['timeZone']
        # self._merchantID = os_merchant_dict['merchandID']
        # self._siteID = os_merchant_dict['siteID']
        # self._termID = os_merchant_dict['termID']
        # sum of the col "# of Batches"
        #self._totalBatches = os_merchant_dict['']
        # totalCompleteIdpOnly & totalCompleteIdpCB non-existent (-1) tabs 7-19
        # sum of the col "# Complete IDP Only"
        #self._totalCompleteIdpOnly = os_merchant_dict['']
        #self._totalCompleteIdpCB = os_merchant_dict['']   # sum of the col "# Complete IDP+Cashbk"
        # These 8 fields are present on all 2004-01 through 2008-04 reports
        # sum of the col "Total # Complete"
        #self._totalComplete = os_merchant_dict['']
        # sum of the col "Total # Incomplete"
        #self._totalIncomplete = os_merchant_dict['']
        # sum of the col "Total $ Approved"
        #self._totalApproved = os_merchant_dict['']
        #sum of the col "Total $ User Fee
        #self._totalUserFee = os_merchant_dict['']
        # sum of the col "Purchase Less User Fee
        #self._totalPurchaseLessUser = os_merchant_dict['']
        # sum of the col "Haulage Fee Owing"
        #self._haulageFeeOwing = os_merchant_dict['']
        # sum of the col "Haulage Fee Collected Daily"
        #self._haulageFeeCd = os_merchant_dict['']
        # sum of the col "Merchant Settlement"
        #self._merchantSettlement = os_merchant_dict['']
        
    #### All we need are getters because all instance var's should never
    #### change after instantiation.
    def getIsoNum():
        return self._isoNum
        
    def getMonth():
        return self._reportMonth
        
    def getYear():
        return self._reportYear
        
    def getBusName():
        return self._busName
        
    def getCorpName():
        return self._corpName
        
    def getContact():
        return self._contact
        
    def getPhone():
        return self._phone
    
    def getAddress():
        return self._address
        
    def getCity():
        return self._city
        
    def getProvince():
        return self._province
        
    def getPostalCode():
        return self._postalCode
        
    def getTimeZone():
        return self._timeZone
        
    # def getMerchantId():
        # return self._merchantID
        
    # def getSiteId():
        # return self._siteID
        
    # def getTerminalId():
        # self._termID
    
    
    
    
    def toString(self):
        osmrr_string = (self._busName, self._corpName, self._contact,
                        self._phone, self._address,
                        self._city, self._province, self._postalCode,
                        self._timeZone,
                        self._isoNum, str(self._reportYear),
                        str(self._reportMonth))
        
        return ",".join(osmrr_string)
    
    def asTuple(self):
        osmrr_tuple = (self._busName, self._corpName, self._contact,
                        self._phone, self._address, 
                        self._city, self._province, self._postalCode,
                        self._timeZone,
                        self._isoNum, str(self._reportYear),
                        str(self._reportMonth))
                        
        return osmrr_tuple
    
        
# if "__name__" == "__main__" : main()