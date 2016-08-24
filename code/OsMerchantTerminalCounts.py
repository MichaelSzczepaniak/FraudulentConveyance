import sys, os, sqlite3

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

if __name__ == "__main__" : main()