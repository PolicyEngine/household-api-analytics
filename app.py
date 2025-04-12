import streamlit as st
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy.ext.automap import automap_base
import pandas as pd
import numpy as np
import altair as alt
import datetime

from data.setup import getconn
from data.models import User

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
st.subheader("View by time period")
year_option = st.selectbox(
  label="Year:",
  options=["All", "2024", "2025"],
)
month_option = st.selectbox(
  label="Month:",
  options=["All", "January", "February", "March", "April", "May", "June",
           "July", "August", "September", "October", "November", "December"],
)

group_option = st.selectbox(
  label="Group by:",
  options=select_options.keys(),
  index=0,
)

year_filter = None if year_option == "All" else int(year_option)
if month_option == "All":
  month_filter = None
else:
  month_filter = datetime.datetime.strptime(month_option, "%B").month

if year_filter is not None:
  data_df = data_df[
    (data_df["datetime"].dt.year == year_filter) ]
if month_filter is not None:
  data_df = data_df[
    (data_df["datetime"].dt.month == month_filter) ]

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

# Input new user
st.markdown("##")
st.subheader("Add a new user")
user_client_id = st.text_input(
  label="Client ID (no quotation marks, taken from auth0)"
)
user_name = st.text_input(
  label="Name"
)
if st.button("Submit") and user_client_id and user_name:
  with Session(db_engine) as db_session:
    new_user = User(
      client_id = user_client_id,
      name = user_name
    )
    db_session.add_all([new_user])
    db_session.commit()

  # Not going to verify success - if there's
  # failure, Streamlit pops up a detailed trace
  