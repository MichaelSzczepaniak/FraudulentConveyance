import sys, os, OsMerchantReportRecord as omrr

# Initialize some constants
toToken = "To"
contactToken = "Contact:"
phoneToken = "Phone:"
faxToken = "Fax:"
timeZoneToken = "Time Zone:"
merchantToken = "Merchant:"
siteToken = "Site:"
terminalToken = "Terminal:"
dateToken = "Date"

def usage():
    msg = """
    OsMerchantParser.py : reads all the monthly Open Solutions monthly merchant
    reports, parses them into raw merchant chuncks, parses those chuncks into
    merchant report records, and then persists those records. To run from
    ipython:  run OsMerchantParser.py ../data/rawOsMerchantReportsTxt/
    
    """
    print(msg)


def main():
    """ Iterates through data dir, reads each OS monthly merchant report file,
    parses that file into OsMerchant objects, and then persists those objects
    into a database.  The path to the data dir needs to passed as the first
    argument. For example:
    
    run OsMerchantParser.py ../data/rawOsMerchantReportsTxt/
    
    """
    data_dir = sys.argv[1]  # first arg should be path to data dir
    data_files = os.listdir(data_dir)
    for i in range(1): #len(data_files)):
        file = data_files[i]
        report_dict = getOsReportInfo(file)
        try:
            path = data_dir + file
            f = open(path)
            print("reading:", path)
        except IOError:
            print(path, "not found! Exiting.")
            sys.exit(0)
        lines = f.readlines()
        # if i == 0: testGetRawMerchantRecords(lines)
        raw_merchants = getRawMerchantRecords(lines)
        # parse raw merchants in merchant objects that can be persisted
        for j in range(len(raw_merchants)):
            merchant_dict = {}
            raw_merchant = raw_merchants[j]
            merchant_dict['busName'] = getBusinessName(raw_merchant)
            merchant_dict['corpName'] = getCorporateName(raw_merchant)
            merchant_record = omrr.OsMerchantReportRecord(report_dict, merchant_dict)
            print(merchant_record.toString())


def getRawMerchantRecords(lines):
    """ Parses a list of strings into another list of strings where each
    inner list are lines related to individual merchants.
    
    lines - list of strings containing information on a set of merchants
            for a given month
    
    Precondition: It's assumed that each merchant record starts with a line:
    To: <merchant name>
    and ends with 3 consecutive blank lines.
    
    """
    raw_records = []
    record = []
    build_record = False
    blank_lines = 0
    print("getRawMerchantRecords: number of lines = ", len(lines))
    for i in range(len(lines)):
        line = lines[i].strip()  # Remove leading white space
        if line.startswith(toToken):
            build_record = True
            record = [line, ]    # Add first line of new record
        elif len(line.strip()) < 1:      # At a blank line?
            blank_lines += 1
            # Last line of current record?
            if blank_lines >= 3:
                if build_record:
                    raw_records.append(record[:])
                    build_record = False
                    blank_lines = 0
        elif build_record:
            record.append(line)
            blank_lines = 0
            
    return raw_records
    
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
    
def getYearFromFileName(file_name):
    """ Returns an intger year for the report file_name: 2004 thru 2008
    
    file_name is expected to be of the form: iiP_ymm where:
    ii = 07 or 56
    y = last digit of the year 2004 through 2008
    mm = month of the report, zero padded: 01 through 12
    e.g. 07P_401.txt
    """
    return 2000 + int(file_name[4:5])
    
def getMonthFromFileName(file_name):
    """ Returns an integer report month from file_name: 1 thru 12
    
    file_name is expected to be of the form: iiP_ymm where:
    ii = 07 or 56
    y = last digit of the year 2004 through 2008
    mm = month of the report, zero padded: 01 through 12
    e.g. 07P_401.txt
    """
    return int(file_name[5:7])
    
def getOsReportInfo(file_name):
    result = dict(isoNum = getIsoNumFromFileName(file_name),
                  reportYear = getYearFromFileName(file_name),
                  reportMonth = getMonthFromFileName(file_name))
    
    return result
    
def getBusinessName(raw_osm):
    """ Returns the business name of raw OS merchant. The business name is
    listed at the start of the 2nd line just below the "To" field.
    
    raw_osm - raw os merchant record
    """
    return raw_osm[1].split(',')[0]
    
def getCorporateName(raw_osm):
    """ Returns the corporate name of raw OS merchant. The corporate name is
    listed immediately following the "To:" token in first line of raw_osm.
    
    raw_osm - raw os merchant record
    """
    return raw_osm[0].split("\t")[1]
    
def testGetRawMerchantRecords(lines):
    """ Tests the first 4 lines of the first, second to last, and
    last raw merchant record by printing both the parsed value and
    the expect value of the line.
    """
    # Get all the raw records in this monthly report file
    records = getRawMerchantRecords(lines)
    record_count = len(records)
    print("\n>>> testGetRawMerchantRecords: record count =", record_count, "<<<\n")
    first_rec = ("To:	NCE NEW CANASIAN ENT INC	Contact: CHRIS GREEN, Phone: 613-722-7797, Fax:   ",
                 "HARVEST LOAF, 1323 WELLINGTON",
                 "OTTAWA, ON,  K1Y 3B6	Time Zone:  Eastern Time ",
                 "Merchant: 07P282          Site:   07P28201")
    
    print("*** # of lines in 1st record = {} ***".format(len(records[0])))
    print("1st record, 1st line:", records[0][0])
    print("THIS LINE SHOULD BE :", first_rec[0])
    
    print("-------------------------------------")
    print("1st record, 2nd line:", records[0][1])
    print("THIS LINE SHOULD BE :", first_rec[1])
    
    print("-------------------------------------")
    print("1st record, 3rd line:", records[0][2])
    print("THIS LINE SHOULD BE :", first_rec[2])
    
    print("-------------------------------------")
    print("1st record, 4th line:", records[0][3])
    print("THIS LINE SHOULD BE :", first_rec[3])
    
    print("***********************************************")
    
    # 2nd to last record in first file should be:
    last_rec = ("To:	SUPER MODEL PIZZA	Contact: REZA GOLSHAN, Phone: 416-533-9099, Fax:   ",
                "SUPER MODEL PIZZA, 772 COLLEGE ST",
                "TORONTO, ON,  M6G 1C6	Time Zone:  Eastern Time ",
                "Merchant: 07P739          Site:   07P73901")
    print("2nd last record, 1st line:", records[record_count-2][0])
    print("THIS LINE SHOULD BE      :", last_rec[0])
    print("2nd last record, 1st line:", records[record_count-2][1])
    print("THIS LINE SHOULD BE      :", last_rec[1])
    print("2nd last record, 1st line:", records[record_count-2][2])
    print("THIS LINE SHOULD BE      :", last_rec[2])
    print("2nd last record, 1st line:", records[record_count-2][3])
    print("THIS LINE SHOULD BE      :", last_rec[3])
    
    # last record in first file should be:
    last_rec = ("To:	JOEYS PIZZA AND SUB	Contact: JOEY SPADAFORA, Phone: 905 687 9494, Fax:   ",
                "JOEYS PIZZA AND SUB, 224 LAKEPORT ROAD",
                "SAINT CATHARINES, ON,  L2S 1T1	Time Zone:  Eastern Time ",
                "Merchant: 07P731          Site:   07P73102")
    print("last record, 1st line:", records[record_count-1][0])
    print("THIS LINE SHOULD BE  :", last_rec[0])
    print("last record, 2nd line:", records[record_count-1][1])
    print("THIS LINE SHOULD BE  :", last_rec[1])
    print("last record, 3rd line:", records[record_count-1][2])
    print("THIS LINE SHOULD BE  :", last_rec[2])
    print("last record, 4th line:", records[record_count-1][3])
    print("THIS LINE SHOULD BE  :", last_rec[3])
                
                
if __name__ == "__main__" : main()