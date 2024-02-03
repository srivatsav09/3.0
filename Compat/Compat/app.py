from flask import Flask, render_template, request
from textblob import TextBlob
import spacy

app = Flask(__name__)

nlp = spacy.load("en_core_web_md")

def calculate_compatibility(government_policy, company_policy):
    # Use spaCy for text similarity
    gov_doc = nlp(government_policy)
    comp_doc = nlp(company_policy)
    similarity_score = gov_doc.similarity(comp_doc)

    # Use TextBlob for sentiment analysis
    gov_sentiment = TextBlob(government_policy).sentiment.polarity
    comp_sentiment = TextBlob(company_policy).sentiment.polarity

    # Combine scores for a compatibility score
    compatibility_score = (similarity_score + (gov_sentiment + comp_sentiment) / 2) / 2

    # Determine color based on the compatibility score
    if compatibility_score >= 0.7:
        color = "#4caf50"  # Green
    elif compatibility_score >= 0.4:
        color = "#ffc107"  # Yellow
    else:
        color = "#e53935"  # Red

    return {
        "score": round(compatibility_score, 2),
        "color": color
    }

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/compare', methods=['POST'])
def compare():
    government_policy = request.form['government_policy']
    company_policy = request.form['company_policy']

    result = calculate_compatibility(government_policy, company_policy)

    return render_template('index.html', result=result)

if __name__ == '__main__':
    app.run(debug=True)
