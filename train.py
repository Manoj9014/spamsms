import pandas as pd
import pickle
import nltk
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB
import string
import os


def create_model():
    print("Starting model training...")

    # Download required NLTK data
    print("Downloading NLTK data...")
    nltk.download('stopwords')
    nltk.download('punkt')

    def transform_text(text):
        # Convert to lowercase
        text = text.lower()

        # Tokenize the text
        text = nltk.word_tokenize(text)

        y = []
        # Keep only alphanumeric words
        for i in text:
            if i.isalnum():
                y.append(i)
        text = y[:]
        y.clear()

        # Remove stopwords and punctuation
        for i in text:
            if i not in stopwords.words('english') and i not in string.punctuation:
                y.append(i)
        text = y[:]
        y.clear()

        # Apply stemming
        ps = PorterStemmer()
        for i in text:
            y.append(ps.stem(i))

        return " ".join(y)

    print("Loading dataset...")
    # Load the dataset
    df = pd.read_csv('C:\\Users\\manoj\\Downloads\\spamsms\\spam.csv', encoding='ISO-8859-1')

    # Drop unnecessary columns
    df.drop(columns=['Unnamed: 2', 'Unnamed: 3', 'Unnamed: 4'], inplace=True)

    # Rename columns
    df.rename(columns={'v1': 'target', 'v2': 'text'}, inplace=True)

    # Convert labels to binary values
    df['target'] = df['target'].map({'ham': 0, 'spam': 1})

    print("Transforming text data...")
    # Transform the text data
    df['transformed_text'] = df['text'].apply(transform_text)

    print("Creating TF-IDF vectors...")
    # Create TF-IDF vectors
    tfidf = TfidfVectorizer(max_features=3000)
    X = tfidf.fit_transform(df['transformed_text']).toarray()
    y = df['target'].values

    # Split the data
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=2)

    print("Training the model...")
    # Train the model
    model = MultinomialNB()
    model.fit(X_train, y_train)

    # Calculate accuracy
    accuracy = model.score(X_test, y_test)
    print(f"Model accuracy: {accuracy * 100:.2f}%")

    # Create a directory for models if it doesn't exist
    if not os.path.exists('models'):
        os.makedirs('models')

    print("Saving the model and vectorizer...")
    # Save the model and vectorizer
    pickle.dump(tfidf, open('models/vectorizer.pkl', 'wb'))
    pickle.dump(model, open('models/model.pkl', 'wb'))

    print("Training complete! Model and vectorizer have been saved.")


if __name__ == "__main__":
    create_model()