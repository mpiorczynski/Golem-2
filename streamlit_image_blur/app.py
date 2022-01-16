import streamlit as st

from multipage import MultiPage
import app_cloud

app = MultiPage()

st.title("Title to be changed")

app.add_page("Tweet demo", app_cloud.app)
app.add_page("Cloud demo", app_cloud.app)

if __name__ == '__main__':
    app.run()
