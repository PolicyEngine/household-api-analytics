import streamlit as st
from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session

from data.setup import getconn

############# DATA FETCHING ##############

# Connect with remote analytics DB
db_engine = create_engine(
    "mysql+pymysql://",
    creator=getconn,
)

# Fetch all records
# with Session(db_engine) as db_session:
    

# 

############# PAGE STYLING ##############

# Page title

# Chart displaying data visualization,
# based on selections from below table

# Data selector tool

# Table of filtered queries that's collapsed
# by default