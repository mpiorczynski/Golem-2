import streamlit as st
from PIL import Image
import time

def app():
    st.markdown('## Hate speech blur demonstration')
    st.write('\n')

    if not st.button('Blur first tweet'):
        image = Image.open('./tweets/unblured/hate_tweet.jpeg')
        st.image(image, caption='First tweet before blur')
    else:
        with st.spinner('Wait for it...'):
            time.sleep(0.3)
            image = Image.open('./tweets/blured/output.png')
        st.image(image, caption='First tweet after blur')

    if not st.button('Blur second tweet'):
        image = Image.open('./tweets/unblured/nice_tweet1.png')
        st.image(image, caption='Second tweet before blur')
    else:
        with st.spinner('Wait for it...'):
            time.sleep(0.3)
            image = Image.open('./tweets/unblured/nice_tweet1.png')
        st.image(image, caption='Second tweet after blur')

    if not st.button('Blur third tweet'):
        image = Image.open('./tweets/unblured/nice_tweet2.jpeg')
        st.image(image, caption='Third tweet before blur')
    else:
        with st.spinner('Wait for it...'):
            time.sleep(0.3)
            image = Image.open('./tweets/unblured/nice_tweet2.jpeg')
        st.image(image, caption='Third tweet after blur')

    if not st.button('Blur fourth tweet'):
        image = Image.open('./tweets/unblured/bad_tweet5.jpg')
        st.image(image, caption='Fourth tweet before blur')
    else:
        with st.spinner('Wait for it...'):
            time.sleep(0.3)
            image = Image.open('./tweets/blured/output2.png')
        st.image(image, caption='Fourth tweet after blur')
