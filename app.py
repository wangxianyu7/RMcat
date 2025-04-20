import streamlit as st

# Define the pages
main_page = st.Page("catalog.py", title="Catalog", icon="")
page_2 = st.Page("simulator.py", title="RM simulator", icon="")
page_3 = st.Page("softwares.py", title="Modeling softwares", icon="")

# Set up navigation
pg = st.navigation([main_page, page_2, page_3])

# Run the selected page
pg.run()