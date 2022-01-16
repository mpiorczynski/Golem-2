import streamlit as st
from PIL import Image
import cv2
import requests
import base64



BASE_URL = 'http://127.0.0.1:8000'


def app():
    # to be changed

    st.markdown('## Upload')
    st.write('\n')

    use_cloud = st.checkbox('Use cloud', value=True)

    # ogarnąć rozszerzenia
    uploaded_file = st.file_uploader("Choose a file", type=['png', 'jpg'])

    if uploaded_file is not None:
        image = Image.open(uploaded_file)

        st.image(image, caption='Uploaded image')
        image.save("img.jpg")

        # if use_cloud:
        files_hate = {'file_hate': ('img.jpg', open('img.jpg', 'rb'), "image/jpeg")}
        resp_hate_img = requests.get(f'{BASE_URL}/pred/hate/im', files=files_hate)
        blured_img = base64.b64decode(resp_hate_img.json().get('encoded_img'))

        st.image(blured_img, caption='Blured image')

        files_emo = {'file_emo': ('img.jpg', open('img.jpg', 'rb'), "image/jpeg")}
        resp_emo_img = requests.get(f'{BASE_URL}/pred/emo/im', files=files_emo)
        print(resp_emo_img)
        print(resp_emo_img.json())
        highligted_img = base64.b64decode(resp_emo_img.json().get('encoded_img'))

        st.image(highligted_img, caption='Highlihted emotions')


        # else:
            # import hate_speech_classifier
            # import hate_speech_blur
            # import highlight_emotions

            # cv_image = cv2.imread("img.jpg")
            # blurred_img = hate_speech_blur.blur_hate_speech(cv_image)
            # highligted_img = highlight_emotions.highlight_emotions(cv_image)
            # pass





    # text_input = st.text_input('Text', 'I like you')

    # if text_input is not None:
    #     with st.spinner('Wait for it...'):
    #         prediction = hate_speech_classifier.classify(text_input)
    #     if prediction == 'no-hate-speech':
    #         st.success(prediction)
    #         st.balloons()
    #     else:
    #         st.error(prediction)

