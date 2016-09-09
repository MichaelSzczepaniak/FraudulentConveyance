import sys, os, sqlite3, pandas as pd

def main():
    """ Connects to the database of OS merchants, queries the
    merchants_report_records and writes a new table osMonthlyMerchantsTerminals
    which contains the monthly merchant and terminal counts.  From this table,
    a dataframe is created with the monthly merchant and terminal drop rates.
    This table is then written out so it can be used as input for the
    regression analysis.
    
    This script takes two parameters: First, the path to the db. Second, the
    name of the table contianing the data needed to create the report file.
    From ipython:
    
    run OsMerchantTerminalCounts ../data/OsReportMerchants.sqlite osMonthlyMerchantsTerminals
    """
    if len(sys.argv) != 3 :
        print("Program takes two arg's: path to db & data table.  Exitting.")
        sys.exit(1)
    db_name = sys.argv[1]  # First and only arg should be the name of db.
    report_table_name = sys.argv[2]
    conn = sqlite3.connect(db_name)  # Connect to db.
    cur = conn.cursor()
    # Create osMonthlyMerchantsTerminals table used for fraud analysis
    # if it doesn't exist.
    check_table_query = getCheckTableQueryString(report_table_name)
    report_table = pd.read_sql_query(check_table_query, conn)
    # Check if table has been created already.
    if len(report_table) < 1 :
        make_table_command = buildMonthlyMerchantsTerminalsCommand()
        cur.execute(make_table_command)
    else :
        print("{} table already exists.".format(report_table_name))
    # Table is created. Now create dataframs and populate the merchant
    # and terminal drop rates.
    df = addDropRateColumns(conn)
    print(df)
    
def init() :
    import sys, os, sqlite3, pandas as pd
    db_name = "../data/OsReportMerchants.sqlite"
    table_name = "osMonthlyMerchantsTerminals"
    conn = sqlite3.connect(db_name)
    cur = conn.cursor()
    mer_ter_df = pd.read_sql_query("SELECT * from " + table_name, conn)
    # Add new columns and init to a recognizably unmodified value.
    mer_ter_df['merchant_adds'] = -1
    mer_ter_df['merchant_drops'] = -1
    mer_ter_df['terminal_adds'] = -1
    mer_ter_df['terminal_drops'] = -1
    mer_ter_df['merchant_drop_rate'] = -1
    mer_ter_df['terminal_drop_rate'] = -1
    # dev getDroppedMerchants & getDroppedTerminals
    year0=2004; month0=1; year1=2004; month1=2; table="merchants_report_records"
    
    
    pass
    
def getCheckTableQueryString(table_name) :
    query = "SELECT name FROM sqlite_master WHERE "
    query += "type='table' AND name='" + table_name + "'"
    
    return query

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
    
def addDropRateColumns(conn, table_name='osMonthlyMerchantsTerminals') :
    """ Builds and returns a dataframe with the following columns:
    yearFrac - float in the form yyyy.xx where xx is in 1/12 increments
               which should make it suitable for scatter plotting
    reportYear - int, year of a given merchants/terminals report: 2004-2008
    reportMonth - int, month of a given merchants/terminals report: 1-12
    merchants_dropped - 
    terminals_dropped - 
    merchant_drop_rate -
    terminal_drop_rate -
    """
    # cur = conn.cursor()
    df = pd.read_sql_query("SELECT * from " + table_name, conn)
    # Add new columns and init to a recognizably unmodified value.
    df['merchant_adds'] = -1
    df['merchant_drops'] = -1
    df['terminal_adds'] = -1
    df['terminal_drops'] = -1
    df['merchant_drop_rate'] = -1
    df['terminal_drop_rate'] = -1
    # Populate the values of above 4 created columns.
    # df = populateDroppedMersTers(df)
    
    return df
    
def populateDroppedMersTers(mer_ter_df, conn) :
    """ Populates the drops and drop_rate columns in the mer_ter_df dataframe.
    This function expect there to be the following 
    
    A dropped merchant is one that had a merchantId in the immediately
    preceding month which was absent in the current month. Similar for a
    dropped terminal: terminalId existed in prior but not current month
    """
    mer_ter_df.ix[None, 'merchant_adds']
    mer_ter_df.ix[None, 'merchant_drops']
    mer_ter_df.ix[None, 'terminal_adds']
    mer_ter_df.ix[None, 'terminal_drops']
    mer_ter_df.ix[None, 'merchant_drop_rate']
    mer_ter_df.ix[None, 'terminal_drop_rate']
    for i in range(1, len(mer_ter_df)) :
        current_year = mer_ter_df.ix[i, 'reportYear']
        current_month = mer_ter_df.ix[i, 'reportMonth']
        prior_year = current_year
        prior_month = current_month - 1
        # Adjust prior period if it crosses a year boundary
        if prior_month < 1 :
            prior_month = 12
            prior_year = current_year - 1
        drops = getDropped(prior_year, prior_month,
                           current_year, current_month, conn)
        
    pass                       
    # return df

def getUniques(year, month, conn, select_type="merchantId",
               table="merchants_report_records") :
    """ Returns an ndarray of unique merchantIds or terminalsIds for given
    month depending on value of select_type paramenter: default is merchantId
    year - int, year of the month the get unique merchantIds or terminalIds
    month - int, month of the month the get unique merchantIds or terminalIds
    conn - database connection to the database where table lives
    select_type - string, the type of unique items to be returned. Proper
                  values are either 'merchantId' or 'terminalId'
    table - string, the table name containing the data
    """
    # year=2004; month=1; table="merchants_report_records"
    query = "SELECT " + select_type + " FROM " + table
    query += " WHERE reportYear = " + str(year)
    query += " AND reportMonth = " + str(month)
    found_items = pd.read_sql_query(query, conn)
    
    return found_items[select_type].unique()
    

def getDropsAdds(year0, month0, year1, month1, conn) :
    """ Returns a 4-tuple with the following contents:
    result[0] - number of merchants dropped from month0 to month1
    result[1] - number of merchants added from month0 to month1
    result[2] - number of terminals dropped from month0 to month1
    result[3] - number of terminals added from month0 to month1
    
    year0 - the year of the prior month. Will be the same as the current
            year except when the current month = 1 (January)
    month0 - the prior month. Will be (1 - month1) except when current
             month (month1) = 1 (January)
    year1 - the year of the current report period
    month1 - the month fo the current report period
    conn - database connection
    table - table name were holding all the monthly merchant report records
            default value = merchants_report_records
    """
    dropped_merchants = list(set(getUniques(year0, month0, conn)) -
                             set(getUniques(year1, month1, conn))
    added_merchants = list(set(getUniques(year1, month1, conn)) -
                             set(getUniques(year0, month0, conn))
    dropped_terminals =
        list(set(getUniques(year0, month0, conn, "TerminalId")) -
             set(getUniques(year1, month1, conn, "TerminalId")))
    added_terminals =
        list(set(getUniques(year1, month1, conn, "TerminalId")) -
             set(getUniques(year0, month0, conn, "TerminalId")))
    
    return (dropped_merchants, added_merchants,
            dropped_terminals, added_terminals)
    

if __name__ == "__main__" : main()