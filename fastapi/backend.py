from transformers import pipeline
from transformers import AutoTokenizer, T5ForConditionalGeneration
import cv2
import pytesseract
import streamlit as st


def get_models():
    try:
        emo_classifier = pipeline('sentiment-analysis', model='distilroberta_emo')
    except Exception as e:
        print(e, 'Downloading weigths...')
        emo_classifier = pipeline("sentiment-analysis",model="j-hartmann/emotion-english-distilroberta-base")
        emo_classifier.save_pretrained('distilroberta_emo')
    
    ckpt = 'Narrativa/byt5-base-tweet-hate-detection'

    tokenizer = AutoTokenizer.from_pretrained(ckpt)
    hate_classifier = T5ForConditionalGeneration.from_pretrained(ckpt).to("cpu")
    return {'emo': emo_classifier, 'hate': hate_classifier, 'tok': tokenizer}

MODELS = get_models()
print('models ready')

def hate_clf(model, text, tokenizer):
    inputs = tokenizer([text], padding='max_length', truncation=True, max_length=512, return_tensors='pt')
    input_ids = inputs.input_ids.to('cpu')
    attention_mask = inputs.attention_mask.to('cpu')
    output = model.generate(input_ids, attention_mask=attention_mask)
    return tokenizer.decode(output[0], skip_special_tokens=True)

def blur_hate_speech(model, tokenizer, img):
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
        result = hate_clf(model, text, tokenizer)
        print("RESULT",result)
        if result == "hate-speech":
                    is_hate_speech = True
                
        if is_hate_speech:
            roi = img[y:y+h,  x:x+w]
            roi = cv2.GaussianBlur(roi, (23, 23), 30)
            img[y:y+roi.shape[0], x:x+roi.shape[1]] = roi

    return img

colors = {'anger': (255, 0, 0),
          'disgust': (100, 255, 255),
          'fear': (100, 255, 0),
          'joy': (0, 255, 0),
          'neutral': (255, 255, 255),
          'sadness': (0, 0, 255),
          'surprise': (100, 100, 100)
        }

def highlight_emotions(model, img):
    gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    ret, thresh1 = cv2.threshold(gray, 0, 255, cv2.THRESH_OTSU | cv2.THRESH_BINARY_INV)
    rect_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (18, 18))
    dilation = cv2.dilate(thresh1, rect_kernel, iterations = 1)
    contours, hierarchy = cv2.findContours(dilation, cv2.RETR_EXTERNAL,
                                                    cv2.CHAIN_APPROX_NONE)

    rgba = cv2.cvtColor(img, cv2.COLOR_RGB2RGBA)
        
    for cnt in contours:
        x, y, w, h = cv2.boundingRect(cnt)
        
        cropped = img[y:y + h, x:x + w]
        text = pytesseract.image_to_string(cropped)
        text = text.replace('\n', ' ')
        print("text",text)
        result = model(text)[0]['label']
        print("RESULT", result)
                
        if result != 'neutral':
            cv2.putText(rgba, result, (x, y - 5), cv2.FONT_HERSHEY_SIMPLEX, 1, colors[result], 1)
            cv2.rectangle(rgba, (x, y), (x+w, y+h), colors[result], 5)

    return rgba
    
