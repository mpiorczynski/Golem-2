from ibm_watson import SpeechToTextV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator


def get_prediction(filename):
    authenticator = IAMAuthenticator('nZEaBYnRaHaruAF-ClKF77qiHrhgZlvgd6TEzXGtRg8Z')
    speech_to_text = SpeechToTextV1(
        authenticator=authenticator,
        
    )
    speech_to_text.set_service_url(
        'https://api.eu-gb.speech-to-text.watson.cloud.ibm.com/instances/026698af-d0b1-4f66-9596-748d15f5faf1'
    )

    extension = filename.split('.')[-1]
    with open(filename, 'rb') as audiofile:
        speech_recognition_results = speech_to_text.recognize(
            audio=audiofile,
            content_type=f'audio/{extension}',
            profanity_filter=False
        ).get_result()
        try:
            transcript_response = speech_recognition_results['results'][0] \
            ['alternatives'][0]['transcript']
        except Exception as e:
            print(e)
            return None
    return transcript_response
