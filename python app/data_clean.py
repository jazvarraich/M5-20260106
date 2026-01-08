import pandas as pd
from sqlalchemy import create_engine
import urllib
import logging

# Set up basic logging to track progress
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')

def load_data(file_path):
    # Loads the raw CSV file
    logging.info(f"Loading data from {file_path}...")
    return pd.read_csv(file_path)

def transform_data(df):
    # Cleans and standardises dataframe
    logging.info("Starting data transformation...")
    
    # Convert IDs to integers
    df['Id'] = df['Id'].astype('Int64')
    df['Customer ID'] = df['Customer ID'].astype('Int64')

    # Format date columns
    df['Book checkout'] = pd.to_datetime(df['Book checkout'].astype(str).str.replace('"', ''), 
                                         dayfirst=True, errors='coerce')
    df['Book Returned'] = pd.to_datetime(df['Book Returned'], 
                                         dayfirst=True, errors='coerce')

    # Clean strings and drop empty rows
    df.dropna(how='all', inplace=True)
    df['Books'] = df['Books'].str.strip().str.title()
    df['Books'] = df['Books'].str.replace('Return Of The Kind', 'Return of the King', case=False)

    # Identify incorrect dates
    df['Incorrect Date'] = df['Book Returned'] < df['Book checkout']
    
    # Extract weeks and convert to days
    df['borrow_days'] = df['Days allowed to borrow'].str.extract('(\d+)').fillna(0).astype(int) * 7
    df['Due Date'] = df['Book checkout'] + pd.to_timedelta(df['borrow_days'], unit='D')
    
    # Flag invalid dates
    df['Valid_Date'] = df['Book checkout'].between('2000-01-01', '2024-12-31')

    # Filter and standardise columns
    filtered_df = df.loc[(df['Incorrect Date'] == False) & (df['Valid_Date'] == True)].copy()
    filtered_df.columns = filtered_df.columns.str.lower().str.replace(' ', '_')
    
    logging.info(f"Transformation complete. {len(filtered_df)} records ready.")
    return filtered_df

def upload_to_sql(df, server, database, table_name):
    # Connection and upload to SQL Server
    driver = 'ODBC Driver 17 for SQL Server'
    conn_str = (
        f"DRIVER={{{driver}}};"
        f"SERVER={server};"
        f"DATABASE={database};"
        f"Trusted_Connection=yes;"
    )
    
    quoted_conn = urllib.parse.quote_plus(conn_str)
    engine = create_engine(f"mssql+pyodbc:///?odbc_connect={quoted_conn}")

    try:
        with engine.connect() as conn:
            logging.info("Connected to SQL Server successfully.")
            df.to_sql(table_name, con=engine, if_exists='replace', index=False)
            logging.info(f"Table '{table_name}' updated in database '{database}'.")
    except Exception as e:
        logging.error(f"Failed to upload to SQL: {e}")

# Gatekeeper
if __name__ == "__main__":
    # Configuration
    FILE_NAME = '03_Library Systembook.csv'
    SQL_SERVER = 'STUDENT06'
    SQL_DATABASE = 'LibraryProject'
    TARGET_TABLE = 'cleaned_library_data'
    OUTPUT_CSV = 'output.csv'

    # Execution
    raw_df = load_data(FILE_NAME)
    clean_df = transform_data(raw_df)
    try:
        logging.info("Attempting to upload to SQL Server...")
        upload_to_sql(clean_df, SQL_SERVER, SQL_DATABASE, TARGET_TABLE)
    except Exception as e:
        logging.warning(f"SQL Upload failed: {e}")
        logging.info(f"Falling back to CSV export. Saving to {OUTPUT_CSV}...")
        clean_df.to_csv(OUTPUT_CSV, index=False)
        logging.info("CSV export complete.")