from flask import Flask, render_template, request, jsonify
from sklearn.datasets import fetch_20newsgroups
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import TruncatedSVD
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.preprocessing import normalize
import numpy as np
import nltk
from nltk.corpus import stopwords

# nltk.download('stopwords')

app = Flask(__name__)

# Fetch dataset
newsgroups = fetch_20newsgroups(subset='all')
documents = newsgroups.data  # List of documents

# Initialize vectorizer and LSA
stop_words = stopwords.words('english')
vectorizer = TfidfVectorizer(stop_words=stop_words)
X = vectorizer.fit_transform(documents)  # Term-document matrix

# Apply SVD to reduce dimensionality
svd = TruncatedSVD(n_components=100, random_state=42)
X_reduced = svd.fit_transform(X)
X_normalized = normalize(X_reduced)

def search_engine(query):
    """
    Function to search for top 5 similar documents given a query
    Input: query (str)
    Output: documents (list), similarities (list), indices (list)
    """
    # Transform the query using the same vectorizer
    query_tfidf = vectorizer.transform([query])
    # Project the query into the LSA space
    query_reduced = svd.transform(query_tfidf)
    query_normalized = normalize(query_reduced)
    # Compute cosine similarities
    similarities = cosine_similarity(query_normalized, X_normalized).flatten()
    # Get the top 5 documents
    top_indices = similarities.argsort()[::-1][:5]
    top_similarities = similarities[top_indices]
    top_documents = [documents[i] for i in top_indices]
    return top_documents, top_similarities.tolist(), top_indices.tolist()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search', methods=['POST'])
def search():
    query = request.form['query']
    documents, similarities, indices = search_engine(query)
    return jsonify({'documents': documents, 'similarities': similarities, 'indices': indices})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000, debug=True)
