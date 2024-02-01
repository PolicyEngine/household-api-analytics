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


############# PAGE STYLING ##############

# Page title
st.title("Household API Analytics")
st.write("View visitor analytics from the PolicyEngine household API below")

# Data visualization options dict
data_view_options = [
  {
    "label": "Cumulative number of requests, by client ID",
  },
  {
    "label": "Cumulative data transfered, by client ID",
  },
]

# Chart displaying data visualization,
# based on selections from below table

# Data selector tool

data_view_labels = list(map(
  lambda k: k["label"],
  data_view_options
))
data_view_selection = st.radio(
  "Select a data visualization option",
  data_view_labels,
  index=0
)

# Table of filtered queries that's collapsed
# by default
with st.expander(
  label="Database of all requests",
  expanded=False
):
  
  df_config = {
    "client_id": "Client ID",
    "datetime": "Date & Time",
    "endpoint": "Endpoint",
    "method": "HTTP Method",
    "content_length_bytes": "Size (bytes)"
  }
  st.dataframe(
    data_df,
    column_config=df_config
  )