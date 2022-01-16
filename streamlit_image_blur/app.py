import streamlit as st

from multipage import MultiPage
import app_cloud
import app_tweet

app = MultiPage()

st.title("Demonstration of our work")

app.add_page("Tweet demo", app_tweet.app)
app.add_page("Cloud demo", app_cloud.app)

if __name__ == '__main__':
    app.run()
