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
with db_engine.connect() as db_conn:
  data_df = pd.read_sql_table('visits', db_conn)

############# PAGE STYLING ##############

# Page title
st.title("Household API Analytics")
st.write("View visitor analytics from the PolicyEngine household API below")

# Chart displaying data visualization,
# based on selections from below table

# Data selector tool

# Table of filtered queries that's collapsed
# by default
# st.write(data_df)