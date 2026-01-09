# Library Data Engineering & Monitoring Pipeline

This repository contains a Python-based ETL (Extract, Transform, Load) pipeline designed to process raw library book records and upload them to a SQL Server database. This repository also provides a real time Streamlit dashboard for pipeline metrics. 

## Project Architecture:
The pipeline follows a standard data engineering flow:

Extract: Ingests raw data from 03_Library Systembook.csv. 

Transform: Cleans data using Python (Pandas), handles type conversions, and validates date logic. 

Load: Standardised data is uploaded to SQL Server (STUDENT06). 

Monitor: Execution metrics (dropped rows, success rates) are logged to a separate SQL metrics table and visualised via Streamlit.

## Architecture Diagram:
See ArchitectureDiagram.png

## Project Structure:
data_clean.py: The core ETL script with metrics logging. 

dashboard.py: A Streamlit based monitoring dashboard for pipeline metrics.   

Data_Cleaning.ipynb: Interactive Jupyter Notebook for testing and visualisation.   

Dockerfile: Configuration for containerising data_clean.py.   

requirements.txt: Python dependency list (Pandas, SQLAlchemy, Streamlit, etc.).   

03_Library Systembook.csv: The raw source data. 

## Data Cleaning Logic
The pipeline ensures data is cleaned through several steps:

Type Conversion: IDs are standardised to integers and date strings are converted to datetime objects. 

Logic Validation:
- Removes records where the return date is earlier than the checkout date. 
- Filters for records within the valid range of 2000–2024. 

Calculated Fields: Generates a due_date based on the specific weeks allowed for each book. 

String Normalisation: Trims whitespace and enforces Title Case for book titles. 

Standardisation: Formats all column headers to snake_case for easier SQL querying.

## How to Run:
### Option 1: Local Execution

1. Install Dependencies:  
pip install -r requirements.txt
Note: Ensure Driver Availability: You must have the ODBC Driver 17 for SQL Server installed on your machine.

2. Run the ETL pipeline:  
python data_clean.py
Note: If SQL Server is unreachable, the script will automatically fallback and save output.csv and metrics.csv locally. 

2. Launch the Dashboard:  
streamlit run dashboard.py

### Option 2 (WIP): Docker Execution
Currently working only for ETL only (not Streamlit dashboard). If you run this script in an environment (like a basic Docker container) without the Microsoft ODBC Driver for SQL Server, the script will:  
1. Throw a `libodbc.so.2` or `ImportError`.  
2. Automatically catch the error.  
3. Save the cleaned data to `output.csv` and `metrics.csv` in the python app directory instead.  

1. Build the Image:  
docker build -t data_clean . 

2. Run the Container:  
docker run data_clean

Accessing Output Files:  
Since the script runs inside a container, local files like `output.csv` and `metrics.csv` are not visible by default.  

## Pipeline Monitoring & Metrics
The pipeline includes a dedicated monitoring system to track execution history and key metrics. Every run is logged to a specific SQL table named pipeline_metrics_history.

The Streamlit Dashboard (dashboard.py) provides:

High-Level Mertrics: View the total records processed, the number of blank rows removed , and rows dropped due to logic errors.
+1

Success Rate: A calculation of how much of the raw data successfully reached the final table.

Historical Trends: A line chart visualising fluctuations in data volume (Rows Imported v Final Rows) over time.

Run History: A searchable, detailed audit log of every run.

## Configuration
To adapt this pipeline for your own environment or different datasets, modify the variables within the if __name__ == "__main__": block at the bottom of the data_clean.py script.

Input File: Change FILE_NAME to update the path to your raw input CSV file.

SQL Server: Modify SQL_SERVER to match your SQL Server name.

Database Name: Update SQL_DATABASE to point the script toward your target database.

Data Table: Adjust TARGET_TABLE to define where the final cleaned library records will be stored.

Metrics History: Edit METRICS_TABLE to specify which table should store the historical pipeline metrics.

Fallback Export: Change OUTPUT_CSV to set the filename used if the script needs to save data locally if SQL is not connected.
