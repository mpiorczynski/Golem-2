import streamlit as st
from PIL import Image
import cv2

import hate_speech_classifier
import hate_speech_blur
import highlight_emotions

def app():
    # to be changed
    
    st.markdown('## Upload')
    st.write('\n')


    uploaded_file = st.file_uploader("Choose a file", type=['png', 'jpg'])

    if uploaded_file is not None:
        image = Image.open(uploaded_file)

        st.image(image, caption='Uploaded image')

        # ogarnąć rozszerzenia
        image.save("img.png")
        cv_image = cv2.imread("img.png")

        blurred = hate_speech_blur.blur_hate_speech(cv_image)

        st.image(blurred, caption='Blurred image', channels="BGR")

        cv_image = cv2.imread("img.png")
        st.image(highlight_emotions.highlight_emotions(cv_image), caption='Highlihted emotions')
