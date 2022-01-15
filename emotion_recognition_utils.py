import pandas as pd
import numpy as np
from transformers import RobertaTokenizerFast, TFRobertaForSequenceClassification, pipeline
from sklearn.metrics import confusion_matrix, accuracy_score
from seaborn import heatmap


def get_prediction(text):
    try:
        classifier = pipeline('sentiment-analysis', model='distilroberta_emo')
    except FileNotFoundError as e:
        print(e, 'Downloading weigths...')
        classifier = pipeline("sentiment-analysis",model="j-hartmann/emotion-english-distilroberta-base")
        classifier.save_pretrained('distilroberta_emo')

    return classifier(text)