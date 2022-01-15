from email.mime import image
import streamlit as st
from PIL import Image

import hate_speech_classifier

def app():
    st.markdown('## Upload')
    st.write('\n')


    uploaded_file = st.file_uploader("Choose a file", type=['png', 'jpg'])

    if uploaded_file is not None:
        image = Image.open(uploaded_file)

        st.image(image, caption='Uploaded image')

    text_input = st.text_input('Text', 'Example text')

    if text_input is not None:
        # st.text(text_input)
        with st.spinner('Wait for it...'):
            prediction = hate_speech_classifier.classify(text_input)
        if prediction == 'no-hate-speech':
            st.success(prediction)
        else:
            st.error(prediction)

if __name__ == '__main__':
    app()
