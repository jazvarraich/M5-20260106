import streamlit as st
import pandas as pd
from sqlalchemy import create_engine
import urllib

if __name__ == "__main__":
    
    # Retrieve data from SQL
    server = 'STUDENT06'
    db = 'LibraryProject'
    conn_str = f"DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={server};DATABASE={db};Trusted_Connection=yes;"
    engine = create_engine(f"mssql+pyodbc:///?odbc_connect={urllib.parse.quote_plus(conn_str)}")
    metric_df = pd.read_sql("SELECT * FROM pipeline_metrics_history ORDER BY run_timestamp DESC", engine)

    server = 'STUDENT06'
    db = 'LibraryProject'
    conn_str = f"DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={server};DATABASE={db};Trusted_Connection=yes;"
    engine = create_engine(f"mssql+pyodbc:///?odbc_connect={urllib.parse.quote_plus(conn_str)}")
    library_df = pd.read_sql("SELECT * FROM pipeline_metrics_history ORDER BY run_timestamp DESC", engine)   
    
    
    # Setup dashboard
    st.set_page_config(page_title="Library Data Dashboard", layout="wide")
    st.title("Pipeline Performance Manager")
    
    # 1. High level metrics
    latest_metric = metric_df.iloc[0]
    col1, col2, col3, col4, = st.columns(4)
    col1.metric("Last Run Total", f"{int(latest_metric['final_row_count'])}")
    col2.metric("Blanks Dropped", f"{int(latest_metric['blank_rows_dropped'])}")
    col3.metric("Logic Drops", f"{int(latest_metric['logic_rows_dropped'])}")
    col4.metric("Success Rate", f"{(latest_metric['final_row_count']/latest_metric['rows_imported']*100):.1f}%")

    # -- Divider -- 
    st.divider()

    # 2. Visualisations
    st.subheader("Historical Trends")
    st.line_chart(metric_df.set_index('run_timestamp')[['rows_imported', 'final_row_count']])

    # -- Divider -- 
    st.divider()

    # 3. Run history
    st.subheader("Run History")
    st.dataframe(metric_df, use_container_width=True)
