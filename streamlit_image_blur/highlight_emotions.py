import cv2
import pytesseract
import streamlit as st

from emotion_classifier import classify

colors = {'anger': (255, 0, 0),
          'disgust': (100, 255, 255),
          'fear': (100, 255, 0),
          'joy': (0, 255, 0),
          'neutral': (255, 255, 255),
          'sadness': (0, 0, 255),
          'surprise': (100, 100, 100)
        }

@st.cache
def highlight_emotions(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    ret, thresh1 = cv2.threshold(gray, 0, 255, cv2.THRESH_OTSU | cv2.THRESH_BINARY_INV)
    rect_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (18, 18))
    dilation = cv2.dilate(thresh1, rect_kernel, iterations = 1)
    contours, hierarchy = cv2.findContours(dilation, cv2.RETR_EXTERNAL,
                                                    cv2.CHAIN_APPROX_NONE)

    rgba = cv2.cvtColor(img, cv2.COLOR_BGR2RGBA)
        
    for cnt in contours:
        x, y, w, h = cv2.boundingRect(cnt)
        
        cropped = img[y:y + h, x:x + w]
        text = pytesseract.image_to_string(cropped)
        text = text.replace('\n', ' ')
        print("text",text)
        result = classify(text)[0]['label']
        print("RESULT", result)
                
        if result != 'neutral':
            cv2.putText(rgba, result, (x, y - 5), cv2.FONT_HERSHEY_SIMPLEX, 1, colors[result], 1)
            cv2.rectangle(rgba, (x, y), (x+w, y+h), colors[result], 5)

    return rgba