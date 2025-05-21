import streamlit as st

select_options = {
  "Name": "name",
  "Endpoint": "endpoint",
  "Method": "method",
}

def create_time_filter_menu():
  with st.form("time_filter_menu"):
    st.session_state.year_option = st.selectbox(
      label="Year:",
      options=["All", "2024", "2025"],
    )
    st.session_state.month_option = st.selectbox(
      label="Month:",
      options=["All", "January", "February", "March", "April", "May", "June",
               "July", "August", "September", "October", "November", "December"],
    )

    st.session_state.group_option = st.selectbox(
      label="Group by:",
      options=select_options.keys(),
      index=0,
    )

    st.form_submit_button("Submit")