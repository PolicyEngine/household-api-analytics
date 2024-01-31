import streamlit as st
from google.cloud.sql.connector import Connector, IPTypes

connector = Connector()

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