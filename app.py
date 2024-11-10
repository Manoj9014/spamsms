from flask import Flask, render_template, request, jsonify
import pickle
import nltk
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
import string
import os
from train import create_model

app = Flask(__name__)

# Download NLTK data
nltk.download('stopwords', quiet=True)
nltk.download('punkt', quiet=True)

# Initialize Porter Stemmer
ps = PorterStemmer()


def load_models():
    global tfidf, model
    try:
        # Check if model files exist, if not create them
        if not os.path.exists('models/vectorizer.pkl') or not os.path.exists('models/model.pkl'):
            print("Model files not found. Training new model...")
            create_model()

        tfidf = pickle.load(open('models/vectorizer.pkl', 'rb'))
        model = pickle.load(open('models/model.pkl', 'rb'))
        print("Model loaded successfully!")
    except Exception as e:
        print(f"Error loading model: {str(e)}")
        raise


def transform_text(text):
    text = text.lower()
    text = nltk.word_tokenize(text)

    y = []
    for i in text:
        if i.isalnum():
            y.append(i)
    text = y[:]
    y.clear()

    for i in text:
        if i not in stopwords.words('english') and i not in string.punctuation:
            y.append(i)
    text = y[:]
    y.clear()

    for i in text:
        y.append(ps.stem(i))

    return " ".join(y)


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/predict', methods=['POST'])
def predict():
    try:
        message = request.form['message']
        if not message:
            return jsonify({'error': 'Please enter a message'})

        # Transform the message
        transformed_message = transform_text(message)

        # Vectorize the message
        vector_input = tfidf.transform([transformed_message])

        # Make prediction
        result = model.predict(vector_input)[0]
        probability = model.predict_proba(vector_input)[0]

        return jsonify({
            'prediction': "Spam" if result == 1 else "Not Spam",
            'confidence': f"{max(probability) * 100:.2f}%"
        })
    except Exception as e:
        print(f"Error during prediction: {str(e)}")
        return jsonify({'error': str(e)})


if __name__ == '__main__':
    print("Initializing Spam Detection System...")
    load_models()
    app.run(debug=True, port=5000)