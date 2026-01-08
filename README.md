# Library Data Cleaning Pipeline

This repository contains a Python-based ETL (Extract, Transform, Load) pipeline designed to process raw library book records and upload them to a SQL Server database.

## Project Structure:
python app/: The root directory for the application.
data_clean.py: The main Python script containing the cleaning logic.
03_Library Systembook.csv: The raw input data file.
Data_Cleaning.ipynb: A Jupyter Notebook version of the script for interactive testing and visualisation.
Dockerfile: Configuration for containerising the application.
requirements.txt: List of Python dependencies required for both local and Docker environments.

## Architecture Diagram:
See ArchitectureDiagram.png

## User Stories:
As a Librarian, I want to upload raw book data to a central spot stop using manual spreadsheets.
As a Data Analyst, I want Python to automatically clean the data to ensure the analysis is reliable and error-free.
As a Developer, I want automated tests to run on every change to make sure the cleaning code doesn't break.
As a Data Engineer, I want a PowerBI dashboard to see pipeline metrics/trends 

## Kanban Board:
### To Do (Backlog)
• Define data cleaning requirements (e.g. remove nulls).
• Research Azure DevOps pipeline syntax (yaml).
• Design PowerBI dashboard layout.

### In Progress
• Write Python script for data manipulation (using Pandas).
• Set up GitHub Repository and push initial code.
• Write Unit Tests for the Python script.

### Testing/Review
• Configure Azure CI/CD Pipeline to run Python script on every "Commit".
• Verify data output matches library standards.

## Data Cleaning Script:
The script performs the following cleaning steps to ensure data integrity
Type Conversion: Standardises IDs to integers and dates to datetime objects.
String Normalisation: Trims whitespace and title-cases book titles.

### Date Validation -
Calculates a Due Date based on the allowed borrowing weeks.
Flags and removes records where the Book Returned date is earlier than the Book checkout date.
Filters for records within a valid date range (2000–2024).
Formatting: Standardises all column headers to snake_case for easier SQL querying.

### How to Run:
#### Option 1: Local Execution

Install Dependencies:
Bash
pip install -r requirements.txt
Ensure Driver Availability: You must have the ODBC Driver 17 for SQL Server installed on your machine.

Run the Script:
Bash
python data_clean.py

#### Option 2 (WIP): Docker Execution
If you run this script in a environment (like a basic Docker container) without the **Microsoft ODBC Driver for SQL Server**, the script will:
1. Throw a `libodbc.so.2` or `ImportError`.
2. Automatically catch the error.
3. Save the cleaned data to `output.csv` in the python app directory instead.

Build the Image:
Bash
docker build -t data_clean .

Run the Container:
Bash
docker run data_clean

Accessing Output Files:
Since the script runs inside a container, local files like `output.csv` are not visible by default.

### Configuration:
The script is currently configured with the following defaults in the if __name__ == "__main__": block:

File name = '03_Library Systembook.csv'
Server: STUDENT06
Database: LibraryProject
Table: cleaned_library_data
Output CSV = output.csv