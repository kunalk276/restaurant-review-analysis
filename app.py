import requests, os, uuid, json
import numpy as np
from flask import Flask, request, render_template
import joblib

app = Flask(__name__)
model = joblib.load(open('model.pkl', 'rb'))
cv = joblib.load(open('cv.pkl', 'rb'))

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    '''
    For rendering results on HTML GUI
    '''

    if request.method == 'POST':
        text = request.form['Review']
        data = [text]
        vectorizer = cv.transform(data).toarray()
        prediction = model.predict(vectorizer)
    if prediction:
        return render_template('index.html', prediction_text='The review is Postive')
    else:
        return render_template('index.html', prediction_text='The review is Negative')


if __name__ == "__main__":
    app.run(debug=True)
@app.route('/', methods=['POST'])
def index_post():
    # Read the values from the form
    original_text = request.form['text']
    target_language = request.form['language']

    # Load the values from .env
    key = '180a6081ed03416e874752c6f85ccfee'
    endpoint = 'https://api.cognitive.microsofttranslator.com/'
    location = 'eastus'

    # Indicate that we want to translate and the API version (3.0) and the target language
    path = '/translate?api-version=3.0'
    # Add the target language parameter
    target_language_parameter = '&to=' + target_language
    # Create the full URL
    constructed_url = endpoint + path + target_language_parameter

    # Set up the header information, which includes our subscription key
    headers = {
        'Ocp-Apim-Subscription-Key': -6136-4430-be31-d1e38ec2c358
,
        'Ocp-Apim-Subscription-Region': eastus,
        'Content-type': 'application/json',
        'X-ClientTraceId': str(uuid.uuid4())
    }

    # Create the body of the request with the text to be translated
    body = [{ 'text': original_text }]

    # Make the call using post
    translator_request = requests.post(constructed_url, headers=headers, json=body)
    # Retrieve the JSON response
    translator_response = translator_request.json()
    # Retrieve the translation
    translated_text = translator_response[0]['translations'][0]['text']

    # Call render template, passing the translated text,
    # original text, and target language to the template
    return render_template(
        'result.html',
        translated_text=translated_text,
        original_text=original_text,
        target_language=target_language
    )
