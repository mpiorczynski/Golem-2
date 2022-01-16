from transformers import pipeline
import streamlit as st

@st.cache
def classify(text):
    try:    
        classifier = pipeline('sentiment-analysis', model='distilroberta_emo')
    except FileNotFoundError as e:
        print(e, 'Downloading weigths...')
        classifier = pipeline("sentiment-analysis",model="j-hartmann/emotion-english-distilroberta-base")
        classifier.save_pretrained('distilroberta_emo')

    print(text)
    return classifier(text)