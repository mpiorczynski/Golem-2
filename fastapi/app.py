from fastapi import FastAPI, File, UploadFile, Form
import backend
import cv2
import numpy as np
import base64

app = FastAPI()


@app.get('/test')
async def test():
    return 'test successful'

@app.get('/pred/hate/im')
async def pred_hate_img(file_hate: UploadFile = File(...)):
    contents_hate = await file_hate.read()
    nparr_hate = np.fromstring(contents_hate, np.uint8)
    img_hate = cv2.imdecode(nparr_hate, cv2.IMREAD_COLOR)

    img_dimensions_hate = str(img_hate.shape)
    return_img_hate = backend.blur_hate_speech(backend.MODELS['hate'], backend.MODELS['tok'], img_hate)

    # line that fixed it
    _, encoded_img_hate = cv2.imencode('.PNG', return_img_hate)

    encoded_img_hate = base64.b64encode(encoded_img_hate)

    return {
        'filename': file_hate.filename,
        'dimensions': img_dimensions_hate,
        'encoded_img': encoded_img_hate
    }


@app.get('/pred/hate/txt')
def pred_hate_txt(text: str = "I like you"):
    return backend.hate_clf(backend.MODELS['hate'], backend.MODELS['tok'], text)

@app.get('/pred/emo/im')
async def pred_emo_im(file_emo: UploadFile = File(...)):
    contents_emo = await file_emo.read()
    nparr_emo = np.fromstring(contents_emo, np.uint8)
    img_emo = cv2.imdecode(nparr_emo, cv2.IMREAD_COLOR)

    img_dimensions_emo = str(img_emo.shape)
    return_img_emo = backend.highlight_emotions(backend.MODELS['emo'], img_emo)

    # line that fixed it
    _, encoded_img_emo = cv2.imencode('.PNG', return_img_emo)

    encoded_img_emo = base64.b64encode(encoded_img_emo)

    return {
        'filename': file_emo.filename,
        'dimensions': img_dimensions_emo,
        'encoded_img': encoded_img_emo
    }

@app.get('/pred/emo/txt')
def pred_emo_txt(text: str = "I like you"):
    return "text"
    #backend.hate_clf(backend.MODELS['hate'], backend.MODELS['tok'], text)



