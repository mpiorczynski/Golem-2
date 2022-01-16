import streamlit as st
from PIL import Image
import cv2

import hate_speech_classifier
import hate_speech_blur

def app():
    st.markdown('## Upload')
    st.write('\n')


    uploaded_file = st.file_uploader("Choose a file", type=['png', 'jpg'])

    if uploaded_file is not None:
        image = Image.open(uploaded_file)

        st.image(image, caption='Uploaded image')

        image.save("img.jpg")
        cv_image = cv2.imread("img.jpg")

        blurred = hate_speech_blur.blur_hate_speech(cv_image)

        st.image(blurred, caption='Blurred image', channels="BGR")


    text_input = st.text_input('Text', None)

    if text_input is not None:
        with st.spinner('Wait for it...'):
            prediction = hate_speech_classifier.classify(text_input)
        if prediction == 'no-hate-speech':
            st.success(prediction)
        else:
            st.error(prediction)

if __name__ == '__main__':
    app()
