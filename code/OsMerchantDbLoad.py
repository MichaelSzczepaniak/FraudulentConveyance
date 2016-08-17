import sys, os, sqlite3
import OsMerchantReportRecord as omrr, OsMerchantParser as omp
from datetime import datetime as dt

def usage():
    msg = """
    OsMerchantDBLoad.py : reads all the monthly Open Solutions monthly merchant
    reports, parses them into raw merchant chuncks, parses those chuncks into
    OsMerchantReportRecord objects and then persists those objects into a
    SQLite3 database.  The path to the data dir needs to passed as the first
    argument. For example, from ipython shell:
    
    run OsMerchantDBLoad.py <path to Open Solutions text reports>
    e.g.
    run OsMerchantDBLoad.py ../data/rawOsMerchantReportsTxt/
    
    """
    print(msg)

def main():
    print("START DB LOAD at: {}".format(str(dt.now())))
    data_dir = sys.argv[1]  # first arg should be path to data dir
    db = sqlite3.connect('OsReportMerchants.sqlite')  # Connect to db.
    drop_table_command = buildDropTableCommand()
    db.execute(drop_table_command)
    create_table_command = buildCreateTableCommand()
    db.execute(create_table_command)
    data_files = os.listdir(data_dir)
    for i in range(len(data_files)):
        file = data_files[i]
        report_dict = omp.getOsReportInfo(file)
        try:
            path = data_dir + file
            f = open(path)
            print("reading:", path)
        except IOError:
            print(path, "not found! Exiting.")
            sys.exit(0)
        lines = f.readlines()
        # Parse out the raw merchant report records for this file
        raw_merchants = omp.getRawMerchantRecords(lines)
        record_count = len(raw_merchants)
        # Now parse each raw merchant report records into OsMerchantReportRecord objects
        # which are then persisted to the db.
        for j in range(record_count):
            raw_merchant = raw_merchants[j]
            merchant_dict = omp.loadMerchantInfo(raw_merchant)
            merchant_record = omrr.OsMerchantReportRecord(report_dict, merchant_dict)
            persistMerchantRecord(db, merchant_record)
            
        print("finished processing file: {}".format(file))
    db.close()     
    print("FINISH DB LOAD at: {}".format(str(dt.now())))
            
def buildDropTableCommand(table_name = "merchants_report_records"):
    drop_table_command = "drop table if exists " + table_name
    
    return drop_table_command

def getOSMfields():
    """ Returns of tuple of 3 lists. First list are the fields of
    the OsMerchantReportRecord objects. Second list are the data types
    of each of the OsMerchantReportRecord object fields. Third list
    are the fields and types separated by space. This third field is
    intended to be used with call that insert data into the db.
    
    Note: Need to preserve order of asTuple() method
    """
    fields = ['busName', 'corpName', 'contact', 'phone', 'address',
              'city', 'province', 'postalCode', 'timeZone',
              'merchantId', 'siteId', 'terminalId',
              'isoNum', 'reportYear', 'reportMonth']
    types = ['text', 'text', 'text', 'text', 'text', 'text',
             'text', 'text', 'text', 'text', 'text', 'text',
             'text', 'int', 'int']
    combo = []
    for i in range(len(fields)):
        combo.append(fields[i] + " " + types[i])
    
    return (fields, types, combo)

def buildCreateTableCommand(record_fields = getOSMfields()[2],
                            table_name = "merchants_report_records"):
    """ Returns a string which is a SQL command to create a new table with the
    records that are defined in the record_fields list.  E.g.
    
    'create table merchants_report_records (isoNum text, reportMonth int, reportYear int)'
    """
    create_table_command = "create table " + table_name + " ("
    for field in record_fields:
        create_table_command += field
        create_table_command += ", "
    create_table_command = create_table_command.rstrip(", ") + ")"
    
    return create_table_command

def buildInsertCommand(table_name = "merchants_report_records",
                       record_fields = getOSMfields()[0]):
    insert_command = "insert into " + table_name + " ("
    for field in record_fields:
        insert_command += field
        insert_command += ", "
    insert_command = insert_command.rstrip(", ") + ") values ("
    # Insert ? placeholders for values to load
    for marker in range(len(record_fields)):
        insert_command += "?, "
    insert_command = insert_command.rstrip(", ") + ")"
    
    return insert_command
            
def persistMerchantRecord(data_base, mrec, table_name = "merchants_report_records"):
    insert_command = buildInsertCommand()
    data_base.execute(insert_command, mrec.asTuple())
    # db.execute('insert into merchants (isoNum, reportMonth, reportYear) values (?, ?, ?)', ('99q', 2, 2005))
    # db.execute('insert into merchants (isoNum, reportMonth, reportYear) values (?, ?, ?)', ('58x', 3, 2004))
    # db.execute('insert into merchants (isoNum, reportMonth, reportYear) values (?, ?, ?)', ('34s', 1, 2007))
    data_base.commit()
    # cursor = data_base.execute("select busName from " + table_name + " order by reportMonth")
    # for row in cursor:
        # print(row)

if __name__ == "__main__" : main()