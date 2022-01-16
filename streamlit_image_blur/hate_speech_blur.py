import cv2
import pytesseract
import streamlit as st
from hate_speech_classifier import classify

@st.cache
def blur_hate_speech(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    ret, thresh1 = cv2.threshold(gray, 0, 255, cv2.THRESH_OTSU | cv2.THRESH_BINARY_INV)
    rect_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (18, 18))
    dilation = cv2.dilate(thresh1, rect_kernel, iterations = 1)
    contours, hierarchy = cv2.findContours(dilation, cv2.RETR_EXTERNAL,
                                                    cv2.CHAIN_APPROX_NONE)
        
    for cnt in contours:
        x, y, w, h = cv2.boundingRect(cnt)
        
        cropped = img[y:y + h, x:x + w]
        is_hate_speech = False
        text = pytesseract.image_to_string(cropped)
        text = text.replace('\n', ' ')
        print("text",text)
        result = classify(text)
        print("RESULT",result)
        if result == "hate-speech":
                    is_hate_speech = True
                
        if is_hate_speech:
            roi = img[y:y+h,  x:x+w]
            roi = cv2.GaussianBlur(roi, (23, 23), 30)
            img[y:y+roi.shape[0], x:x+roi.shape[1]] = roi

    return img
