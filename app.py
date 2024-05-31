# from flask import Flask, render_template, request, jsonify
# import nltk
# import csv
# import os  # Added import for os module
# from nltk.tokenize import word_tokenize
# from nltk.stem import WordNetLemmatizer
# from sklearn.feature_extraction.text import CountVectorizer
# import openai

# app = Flask(__name__)

# # Download NLTK data
# nltk.download('punkt')
# nltk.download('wordnet')

# # Set up OpenAI API key from environment variable
# openai.api_key = os.environ.get('OPENAI_API_KEY')

# # Read the CSV dataset and preprocess it
# dataset_path = 'Mental_Health_FAQ.csv'
# conversations = []
# with open(dataset_path, 'r', encoding='utf-8') as file:
#     reader = csv.reader(file)
#     for row in reader:
#         conversations.append(row)

# lemmatizer = WordNetLemmatizer()

# def preprocess_text(text):
#     tokens = word_tokenize(text.lower())
#     lemmatized_tokens = [lemmatizer.lemmatize(token) for token in tokens]
#     return ' '.join(lemmatized_tokens)

# processed_conversations = [(preprocess_text(question), preprocess_text(answer)) for question, answer in conversations]

# # Vectorization
# vectorizer = CountVectorizer()
# vectorizer.fit_transform([question for question, _ in processed_conversations])

# # Function to get response using ChatGPT API
# def get_gpt_response(input_text):
#     response = openai.Completion.create(
#         engine="text-davinci-003",
#         prompt=f"You: {input_text}\nAI:",
#         max_tokens=150,
#         temperature=0.7,
#         n=1,
#         stop="\n"
#     )
#     return response.choices[0].text.strip()

# # Routes
# @app.route('/')
# def home():
#     intro_message = "Hello! I'm your mental health chatbot. How can I assist you today?"
#     return render_template('index.html', intro_message=intro_message)

# @app.route('/get_response', methods=['POST'])
# def get_bot_response():
#     try:
#         user_message = request.json['user_message']
#         bot_response = get_gpt_response(user_message)
#         return jsonify({'bot_response': bot_response})
#     except Exception as e:
#         # Log the error to a file or print it to the console
#         print(f"Error: {str(e)}")
#         return jsonify({'error': 'An error occurred. Please try again later.'})

# if __name__ == '__main__':
#     app.run(debug=True)

# from flask import Flask, render_template, request, jsonify
# import nltk
# import csv
# from nltk.tokenize import word_tokenize
# from nltk.stem import WordNetLemmatizer
# from sklearn.feature_extraction.text import CountVectorizer

# app = Flask(__name__)

# # Download NLTK data
# nltk.download('punkt')
# nltk.download('wordnet')

# # Read the CSV dataset and preprocess it
# dataset_path = 'Mental_Health_FAQ.csv'
# conversations = []
# with open(dataset_path, 'r', encoding='utf-8') as file:
#     reader = csv.reader(file)
#     for row in reader:
#         conversations.append(row)

# lemmatizer = WordNetLemmatizer()

# def preprocess_text(text):
#     tokens = word_tokenize(text.lower())
#     lemmatized_tokens = [lemmatizer.lemmatize(token) for token in tokens]
#     return ' '.join(lemmatized_tokens)

# processed_conversations = [(preprocess_text(question), preprocess_text(answer)) for question, answer in conversations]

# # Vectorization
# vectorizer = CountVectorizer()
# vectorizer.fit_transform([question for question, _ in processed_conversations])

# # Function to generate response
# def generate_bot_response(input_text):
#     # Replace this with your own logic to generate a response
#     return "Hello! How can I help you today?"

# # Routes
# @app.route('/')
# def home():
#     intro_message = "Hello! I'm your mental health chatbot. How can I assist you today?"
#     return render_template('index.html', intro_message=intro_message)

# @app.route('/get_response', methods=['POST'])
# def get_bot_response():
#     try:
#         user_message = request.json['user_message']
#         bot_response = generate_bot_response(user_message)  # Changed function name here
#         return jsonify({'bot_response': bot_response})
#     except Exception as e:
#         # Log the error to a file or print it to the console
#         print(f"Error: {str(e)}")
#         return jsonify({'error': 'An error occurred. Please try again later.'})

# if __name__ == '__main__':
#     app.run(debug=True)


from flask import Flask, render_template, request, jsonify
import nltk
import csv
import random
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

app = Flask(__name__)

# Download NLTK data
nltk.download('punkt')
nltk.download('wordnet')

# Read the CSV dataset and preprocess it
dataset_path = 'Mental_Health_FAQ.csv'
conversations = []
with open(dataset_path, 'r', encoding='utf-8') as file:
    reader = csv.reader(file)
    for row in reader:
        conversations.append(row)

lemmatizer = WordNetLemmatizer()
def preprocess_text(text):
    tokens = word_tokenize(text.lower())
    lemmatized_tokens = [lemmatizer.lemmatize(token) for token in tokens]
    return ' '.join(lemmatized_tokens)

processed_conversations = [(preprocess_text(question), preprocess_text(answer)) for question, answer in conversations]

# Vectorization
vectorizer = CountVectorizer()
vectorizer.fit_transform([question for question, _ in processed_conversations])

def get_most_similar_response(input_text, processed_conversations):
    input_vector = vectorizer.transform([input_text])
    similarities = [cosine_similarity(input_vector, vectorizer.transform([processed_question])).flatten()[0] for processed_question, _ in processed_conversations]
    max_similarity_idx = np.argmax(similarities)
    return processed_conversations[max_similarity_idx][1] if similarities[max_similarity_idx] > 0 else "I'm sorry, I don't understand."

# Routes
@app.route('/')
def home():
    intro_message = "Hello! I'm your mental health chatbot. How can I assist you today?"
    return render_template('index.html', intro_message=intro_message)

@app.route('/get_response', methods=['POST'])
def get_bot_response():
    try:
        user_message = request.json['user_message']
        bot_response = get_most_similar_response(user_message, processed_conversations)
        return jsonify({'bot_response': bot_response})
    except Exception as e:
        return jsonify({'error': str(e)})

if __name__ == '__main__':
    app.run(debug=True)
