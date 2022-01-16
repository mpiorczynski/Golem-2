import streamlit as st
from PIL import Image
import cv2
import requests
import base64
import time


BASE_URL = 'http://127.0.0.1:8000'


def app():
    st.markdown('## Emotions classification and hate speech detection')
    st.write('\n')

    use_cloud = st.checkbox('Use cloud', value=True)

    # ogarnąć rozszerzenia
    uploaded_file = st.file_uploader("Choose a file", type=['png', 'jpg'])

    option = st.selectbox(
     'Select classification',
     ('Hate speech detection', 'Emotion classification'))


    if uploaded_file is not None:
        image = Image.open(uploaded_file)

        st.image(image, caption='Uploaded image')
        image.save("img.jpg")

        with st.spinner('Wait for it...'):
            if option == 'Hate speech detection' and use_cloud:
                files_hate = {'file_hate': ('img.jpg', open('img.jpg', 'rb'), "image/jpeg")}
                resp_hate_img = requests.get(f'{BASE_URL}/pred/hate/im', files=files_hate)
                blured_img = base64.b64decode(resp_hate_img.json().get('encoded_img'))

                st.image(blured_img, caption='Blured image')

            elif option == 'Emotion classification':
                files_emo = {'file_emo': ('img.jpg', open('img.jpg', 'rb'), "image/jpeg")}
                resp_emo_img = requests.get(f'{BASE_URL}/pred/emo/im', files=files_emo)
                highligted_img = base64.b64decode(resp_emo_img.json().get('encoded_img'))

                st.image(highligted_img, caption='Highlihted emotions')

            else: # Local Hate speech detection
                time.sleep(0.3)
                local_blurred_image = Image.open('./tweets/blured/output.jpg')
                st.image(local_blurred_image, caption='Blured image')


    if option == 'Hate speech detection':
        text_input = st.text_input('Detect hate speech in text', '')

        if text_input:
            with st.spinner('Wait for it...'):
                resp = requests.get(f'{BASE_URL}/pred/hate/txt', params={'text': text_input})
                prediction = resp.json().get('pred')
                # prediction = hate_speech_classifier.classify(text_input)
            if prediction == 'no-hate-speech':
                st.success(prediction)
                # st.balloons()
            else:
                st.error(prediction)
    else:
        text_input = st.text_input('Classify emotion in text', '')

        if text_input:
            with st.spinner('Wait for it...'):
                resp = requests.get(f'{BASE_URL}/pred/emo/txt', params={'text': text_input})
                prediction = resp.json().get('pred')
            st.write(prediction)
