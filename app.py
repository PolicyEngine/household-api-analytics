import streamlit as st
from sqlalchemy import create_engine 
from sqlalchemy.ext.automap import automap_base
import pandas as pd
import numpy as np
import altair as alt

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
user_df = None
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

  user_df = pd.read_sql_table(
    table_name='users',
    con=db_conn,
    columns=[
      "client_id",
      "name"
    ]
  )

############# PAGE STYLING ##############

# Add "name" row by merging in user_df  
data_df = data_df.merge(user_df, how="inner", on="client_id")

# Add a count row to the original dataframe
data_df["count"] = np.zeros(len(data_df))
data_df["date"] = pd.to_datetime(data_df["datetime"].dt.date)
data_df = data_df.sort_values(by="datetime", ascending=False)

# Underlying data
select_options = {
  "Name": "name",
  "Endpoint": "endpoint",
  "Method": "method",
}

# Page title
st.title("Household API Analytics")
st.write("View visitor analytics from the PolicyEngine household API below")

# Usage overview chart
st.markdown("##")
st.subheader("Total API requests per day, per user")

overview_df = data_df.groupby(["date", "name"]).count().reset_index()
pivoted_df = pd.pivot(overview_df, index="date", columns="name", values="count").reset_index()
pivoted_df = pivoted_df.rename(
  columns={
    "date": "Date"
  }
)

st.bar_chart(
  data=pivoted_df,
  x="Date",
)

# Data selector tool
st.markdown("##")
st.subheader("Advanced data visualization")
date_option = st.selectbox(
  label="Data period:",
  options=["All time"],
  disabled=True
)
group_option = st.selectbox(
  label="Group by:",
  options=select_options.keys(),
  index=0,
)

# Filter the dataframe by that count
filtered_df = data_df.groupby(select_options[group_option]).count().reset_index()

# Chart displaying data visualization,
# based on selections from below table
st.markdown("##")
st.bar_chart(
  data=filtered_df,
  x=select_options[group_option],
  y="count"
)

# Table of filtered queries that's collapsed
# by default
st.markdown("##")
st.subheader("Filtered database of all requests, newest first")
df_config = {
  "name": "Name",
  "datetime": "Date & Time",
  "endpoint": "Endpoint",
  "method": "HTTP Method",
  "content_length_bytes": "Size (bytes)",
  "client_id": "Client ID",
  "date": None,
  "count": None
}

st.dataframe(
  data_df,
  column_config=df_config,
  height=400,
  hide_index=True,
)