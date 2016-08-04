import sys, os

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

def main():
    """ Iterates through data dir, reads each OS monthly merchant report file,
    parses that file into an OsMerchant object, and then stores it into a
    database
    
    run OsMerchantParser.py ../data/rawOsMerchantReportsTxt/
    
    """
    data_dir = sys.argv[1]
    data_files = os.listdir(data_dir)
    for i in range(2): #len(data_files)):
        file = data_files[i]
        try:
            path = data_dir + file
            f = open(path)
            print("reading:", path)
        except IOError:
            print(path, "not found! Exiting.")
            sys.exit(0)
        lines = f.readlines()
        # Get all the raw records in this monthly report file
        records = getRawMerchantRecords(lines)
        print('i =', i, ", record count =", len(records))
        # quick test
        # To:	NCE NEW CANASIAN ENT INC	Contact: CHRIS GREEN, Phone: 613-722-7797, Fax:
        print("1st record, 1st line:", records[0][0]) 
        # MILLENNIUM VARIETY, 1405 OTTAWA ST N
        print("3rd record, 2st line:", records[2][1])
        # Merchant: 07P045          Site:   07P04501
        print("4th record, 4th line:", records[3][3])
                
                
def getRawMerchantRecords(lines):
    raw_records = []
    record = []
    for i in range(len(lines)):
        line = lines[i].strip()  # Remove leading white space
        if line.startswith(toToken):
            if len(record) > 0:
                raw_records.append(record)  # Add prior record
            record = [line, ]  # First line of new record
        else:
            record.append(line)
            
    return raw_records
                
                
if __name__ == "__main__" : main()