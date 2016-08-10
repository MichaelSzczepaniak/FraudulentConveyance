

class OsMerchant:
    def __init__(self, report_file_name, raw_merchant):
        self.isoNum = self.getIsoNumFromFileName(report_file_name)
        self.reportYear = self.getYearFromFileName(report_file_name)
        self.reportMonth = self.getMonthFromFileName(report_file_name)
    
    def toString(self):
        return "{}, {}, {}".format(self.isoNum, self.reportYear, self.reportMonth)
    
    @staticmethod
    def getIsoNumFromFileName(file_name):
        """ Returns the first three characters from file_name: 07p or 56p
        with p being lower case.

        file_name is expected to be of the form: iiP_ymm where:
        ii = 07 or 56
        y = last digit of the year 2004 through 2008
        mm = month of the report, zero padded: 01 through 12
        e.g. 07P_401.txt
        """
        return file_name[:3].lower()
    
    @staticmethod
    def getYearFromFileName(file_name):
        """ Returns an intger year for the report file_name: 2004 thru 2008
        
        file_name is expected to be of the form: iiP_ymm where:
        ii = 07 or 56
        y = last digit of the year 2004 through 2008
        mm = month of the report, zero padded: 01 through 12
        e.g. 07P_401.txt
        """
        return 2000 + int(file_name[4:5])
    
    @staticmethod
    def getMonthFromFileName(file_name):
        """ Returns an integer report month from file_name: 1 thru 12
        
        file_name is expected to be of the form: iiP_ymm where:
        ii = 07 or 56
        y = last digit of the year 2004 through 2008
        mm = month of the report, zero padded: 01 through 12
        e.g. 07P_401.txt
        """
        return int(file_name[5:7])