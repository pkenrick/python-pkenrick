import json
import requests
from flask import current_app

def translate(text, source_language, dest_language):
    if 'MS_TRANSLATOR_KEY' not in current_app.config or not current_app.config['MS_TRANSLATOR_KEY']:
        return _('Error: the translation service is not configured')

    headers = {'Ocp-Apim-Subscription-Key': current_app.config['MS_TRANSLATOR_KEY']}
    url = 'https://api.cognitive.microsofttranslator.com/translate?api-version=3.0&to={}&from={}'.format(
        dest_language, source_language
    )
    body = [{'Text': text}]

    response = requests.post(url, headers=headers, json=body)

    if response.status_code != 200:
        return _('Error: the translation service failed')

    try:
        return json.loads(response.content.decode('utf-8-sig'))[0]['translations'][0]['text']
    except:
        return _('Error: the translation service responsed with unexpected format')
