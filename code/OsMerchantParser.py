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
    reports, parses them into raw merchant chuncks and  parses those chuncks
    into merchant report records.  To run from ipython:
    
    run OsMerchantParser.py <path to Open Solutions text reports>
    e.g.
    run OsMerchantParser.py ../data/rawOsMerchantReportsTxt/
    
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
    for i in range(len(data_files)):
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
        record_count = len(raw_merchants)
        for j in range(record_count):
            raw_merchant = raw_merchants[j]
            merchant_dict = loadMerchantInfo(raw_merchant)
            merchant_record = omrr.OsMerchantReportRecord(report_dict, merchant_dict)
            print(merchant_record.toString())
        print("{}{} records processed for {}-{}{}".format("\n", record_count,
            report_dict.get('reportMonth'), report_dict.get('reportYear'),
            "\n"))


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
    
def parseBusinessName(raw_osm):
    """ Returns the business name of raw OS merchant. The business name is
    listed at the start of the 2nd line just below the "To" field.
    
    raw_osm - raw os merchant record
    """
    return raw_osm[1].split(',')[0].strip()
    
def parseCorporateName(raw_osm):
    """ Returns the corporate name of raw OS merchant. The corporate name is
    listed immediately following the "To:" token in first line of raw_osm.
    
    raw_osm - raw os merchant record
    """
    return raw_osm[0].split("\t")[1].strip()
    
def parseContact(raw_osm):
    """ Returns the contact field of raw OS merchant. The conctact is
    the field following the "Contact:" token in first line of raw_osm.
    
    raw_osm - raw os merchant record
    """
    contact_part = raw_osm[0].split(contactToken)[1]
    return contact_part.split(",")[0].strip()
    
def parsePhone(raw_osm):
    """ Returns the phone field of raw OS merchant. The phone # is
    the field following the "Phone:" token in first line of raw_osm.
    
    raw_osm - raw os merchant record
    """
    phone_part = raw_osm[0].split(phoneToken)
    if(len(phone_part) > 1):
        phone_part = phone_part[1].split(",")[0].strip()
    else: 
        phone_part = ""
        
    return phone_part.strip()
    
def parseAddress(raw_osm):
    """ Returns the address field of raw OS merchant. The address is
    the field following the business name field in 2nd line of raw_osm.
    
    raw_osm - raw os merchant record
    """
    address_part = raw_osm[1].split(",")[1]
    
    return address_part.strip()
    
def parseCity(raw_osm):
    """ Returns the city field of raw OS merchant. The city is
    the field following the 1st field in 3rd line of raw_osm.
    
    raw_osm - raw os merchant record
    """
    city_part = raw_osm[2].split(",")[0].strip()
    
    return city_part
    
def parseProvince(raw_osm):
    """ Returns the province field of raw OS merchant. The province
    is the field following the city field in 3rd line of raw_osm.
    
    raw_osm - raw os merchant record
    """
    prov_part = raw_osm[2].split(",")[1].strip()
    
    return prov_part
    
def parsePostalCode(raw_osm):
    """ Returns the postal code field of raw OS merchant. The postal code
    is the field following the province field in 3rd line of raw_osm.
    
    raw_osm - raw os merchant record
    """
    postal_part = raw_osm[2].split(",")[2].strip()  # has postal code and TZ
    postal_part = postal_part[:7]
    
    return postal_part
    
def parseTimeZone(raw_osm):
    """ Returns the Time Zone field of raw OS merchant. The Time Zone
    is the field following the postal code field in 3rd line of raw_osm.
    
    raw_osm - raw os merchant record
    """
    # Next 3 lines needed because report format changed
    tz_line = ""
    if timeZoneToken in raw_osm[2] : tz_line = raw_osm[2]   # older reports
    elif timeZoneToken in raw_osm[1] : tz_line = raw_osm[1] # newer reports
    
    time_zone_part = "NO TIME ZONE"
    if timeZoneToken in tz_line :
        time_zone_part = tz_line.split("Time Zone:")[1].strip()
    
    return time_zone_part
    
def parseMerchantId(raw_osm):
    mid_part = raw_osm[3].split(siteToken)[0]
    mid_part = mid_part.replace(merchantToken, "").strip()
    
    return mid_part
    
def parseSiteId(raw_osm):
    sid_part = raw_osm[3].split(siteToken)[1].strip()
    
    return sid_part
    
def parseTerminalId(raw_osm):
    terminal_part = raw_osm[4].split(terminalToken)[1].strip()
    
    return terminal_part
    
def loadMerchantInfo(raw_osm):
    """ Returns a dictionary populated with all the merchant information
    contained in the raw os merchant record.
    
    raw_osm - raw os merchant record
    """
    merchant = {}
    merchant['busName'] = parseBusinessName(raw_osm)
    merchant['corpName'] = parseCorporateName(raw_osm)
    merchant['contact'] = parseContact(raw_osm)
    merchant['phone'] = parsePhone(raw_osm)
    merchant['address'] = parseAddress(raw_osm)
    merchant['city'] = parseCity(raw_osm)
    merchant['province'] = parseProvince(raw_osm)
    merchant['postalCode'] = parsePostalCode(raw_osm)
    merchant['timeZone'] = parseTimeZone(raw_osm)
    merchant['merchantId'] = parseMerchantId(raw_osm)
    merchant['siteId'] = parseSiteId(raw_osm)
    merchant['terminalId'] = parseTerminalId(raw_osm)
    
    return merchant
    
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
                 "Merchant: 07P282          Site:   07P28201",
                 ""
                 "Terminal: 07P10008")
    
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
    
    print("-------------------------------------")
    print("1st record, 5th line:", records[0][4])
    print("THIS LINE SHOULD BE :", first_rec[4])  # Jumps to Terminal line
    
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