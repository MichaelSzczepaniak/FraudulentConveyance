import sys, os, sqlite3, pandas as pd

def main():
    """ Connects to the database of OS merchants, queries the
    merchant_report_records and writes a new table osMonthlyMerchantsTerminals
    which contains the monthly merchant and terminal counts.
    This script takes the path to the db as a single parameter.
    From ipython:
    
    run OsMerchantTerminalCounts ../data/OsReportMerchants.sqlite
    """
    if len(sys.argv) != 2 :
        print("Program takes a single arg: the path to the db.  Exitting...")
        sys.exit(1)
    db_name = sys.argv[1]  # First and only arg should be the name of db.
    conn = sqlite3.connect(db_name)  # Connect to db.
    cur = conn.cursor()
    # Create osMonthlyMerchantsTerminals table used for fraud analysis.
    make_table_command = buildMonthlyMerchantsTerminalsCommand()
    cur.execute(make_table_command)

def buildMonthlyMerchantsTerminalsCommand() :
    """ Builds and returns the SQL command what creates the
    osMonthlyMerchantsTerminals table.
    """
    create_table = "CREATE TABLE IF NOT EXISTS osMonthlyMerchantsTerminals "
    create_table += "AS SELECT ROUND((reportYear + (reportMonth/12.)), 2) "
    create_table += "AS yearFrac, "
    create_table += "reportYear, reportMonth, "
    create_table += "COUNT(DISTINCT merchantId) AS merchantCount, "
    create_table += "COUNT(DISTINCT terminalId) AS terminalCount "
    create_table += "FROM merchants_report_records "
    create_table += "GROUP BY reportYear, reportMonth "
    create_table += "ORDER BY reportYear, reportMonth"
    
    return create_table
    
def addDropRateColumns(db_name='../data/OsReportMerchants.sqlite',
                       table_name='osMonthlyMerchantsTerminals') :
    """ Builds and returns a dataframe with the following columns:
    yearFrac - float in the form yyyy.xx where xx is in 1/12 increments
               which should make it suitable for scatter plotting
    merchants_dropped - 
    terminals_dropped - 
    merchant_drop_rate -
    terminal_drop_rate -
    """
    conn = sqlite3.connect(db_name)  # Connect to db.
    cur = conn.cursor()
    df = pd.read_sql_query("SELECT * from " + table_name, conn) # get all data
    # add new columns
    df['merchant_drops'] = -1
    df['terminal_drops'] = -1
    df['merchant_drop_rate'] = -1
    df['terminal_drop_rate'] = -1
    
    return df
    
def computeDroppedMerchants(db_name='../data/OsReportMerchants.sqlite',
                            table_name='merchants_report_records') :
    """ Returns a 2 column dataframe: yearFrac and droppedMerchants
    yearFrac - float in the form yyyy.xx where xx is in 1/12 increments
               which should make it suitable for scatter plotting
    dropped_merchants - integer number of merchants dropped in a given month
    
    A dropped merchant is one that had a merchantId in the immediately
    preceding month which was absent in the current month
    """
    conn = sqlite3.connect(db_name)  # Connect to db.
    cur = conn.cursor()
    query_string = "SELECT ROUND((reportYear + (reportMonth/12.)), 2)"
    query_string += " AS yearFrac, merchantId from " + table_name
    df = pd.read_sql_query(query_string, conn)
    # 
    
                           
    return df
    
    

if __name__ == "__main__" : main()