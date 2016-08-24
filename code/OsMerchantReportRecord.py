


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
        self._merchantId = os_merchant_dict['merchantId']
        self._siteId = os_merchant_dict['siteId']
        self._terminalId = os_merchant_dict['terminalId']
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
    def getIsoNum(self):
        return self._isoNum
        
    def getMonth(self):
        return self._reportMonth
        
    def getYear(self):
        return self._reportYear
        
    def getBusName(self):
        return self._busName
        
    def getCorpName(self):
        return self._corpName
        
    def getContact(self):
        return self._contact
        
    def getPhone(self):
        return self._phone
    
    def getAddress(self):
        return self._address
        
    def getCity(self):
        return self._city
        
    def getProvince(self):
        return self._province
        
    def getPostalCode(self):
        return self._postalCode
        
    def getTimeZone(self):
        return self._timeZone
        
    def getMerchantId(self):
        return self._merchantId
        
    def getSiteId(self):
        return self._siteId
        
    def getTerminalId(self):
        return self._terminalId
    
    def asTuple(self):
        osm_tuple = (self._busName, self._corpName, self._contact,
                     self._phone, self._address, self._city,
                     self._province, self._postalCode, self._timeZone,
                     self._merchantId, self._siteId, self._terminalId,
                     self._isoNum, self._reportYear, self._reportMonth)
                       
        return osm_tuple
    
    def toString(self):
        osm_fields = []
        for item in self.asTuple():
            osm_fields.append(str(item))
        
        return ",".join(osm_fields)

# if "__name__" == "__main__" : main()