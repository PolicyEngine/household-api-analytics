import streamlit as st
from sqlalchemy import create_engine 
from sqlalchemy.ext.automap import automap_base
import pandas as pd

from data.setup import getconn
from data.models import Visit

############# DATA FETCHING ##############

# Connect with remote analytics DB
db_engine = create_engine(
    "mysql+pymysql://",
    creator=getconn,
)
Base = automap_base()
Base.prepare(db_engine)

# Fetch all records and convert to dataframe
data_df = None
with db_engine.connect() as db_conn:
  data_df = pd.read_sql_table(
    table_name='visits', 
    con=db_conn,
    parse_dates=["datetime"],
    columns=[
      "client_id",
      "datetime",
      "endpoint",
      "method",
      "content_length_bytes"
    ]
  )

data_df.rename(
  columns={
    "client_id": "Client ID",
    "datetime": "Date & Time",
    "endpoint": "Endpoint",
    "method": "HTTP Method",
    "content_length_bytes": "Size (bytes)"
  },
  inplace=True
)

############# PAGE STYLING ##############

# Page title
st.title("Household API Analytics")
st.write("View visitor analytics from the PolicyEngine household API below")

# Chart displaying data visualization,
# based on selections from below table

# Data selector tool

# Table of filtered queries that's collapsed
# by default
with st.expander(
  label="Database of all requests",
  expanded=False
):
  st.write(data_df)