import streamlit as st
import sqlalchemy
from google.cloud.sql.connector import Connector, IPTypes

############# DATA FETCHING ##############

# Connect with remote analytics DB

# Initialize connector object
connector = Connector()

# Configure connector
def getconn():

    conn = connector.connect(
        st.secrets["USER_ANALYTICS_DB_CONNECTION_NAME"],
        "pymysql",
        user=st.secrets["USER_ANALYTICS_DB_USERNAME"],
        password=st.secrets["USER_ANALYTICS_DB_PASSWORD"],
        db="user_analytics",
        ip_type=IPTypes.PUBLIC,  # IPTypes.PRIVATE for private IP
    )

    return conn

db_pool = sqlalchemy.create_engine(
    "mysql+pymysql://",
    creator=getconn,
)

# Fetch all records

# 

############# PAGE STYLING ##############

# Page title

# Chart displaying data visualization,
# based on selections from below table

# Data selector tool

# Table of filtered queries that's collapsed
# by default