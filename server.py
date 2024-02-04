# server.py

from flask import Flask, render_template, request, jsonify
from scraper import scrape_website
from transformers import pipeline
from model_loader import load_and_predict_model
from textblob import TextBlob
import spacy

app = Flask(__name__)
summarizer = pipeline("summarization")
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

def save_predictions_to_txt(predictions, output_file):
    with open(output_file, 'w') as file:
        for entry in predictions:
            if entry['prediction'] == 1:
                file.write(f"{entry['text']}\n\n")

@app.route('/scrape', methods=['POST'])
def scrape_and_predict():
    try:
        data = request.json
        url = data.get('url')
        if not url:
            return jsonify({'error': 'Missing URL in the request'})
        print(url)
        scraped_data_file = scrape_website(url,'output_file.txt')

        if scraped_data_file:
            predictions = load_and_predict_model(scraped_data_file)
            formatted_predictions = [{'text': entry['text'], 'prediction': entry['prediction']} for entry in predictions]
            save_predictions_to_txt(formatted_predictions, 'final.txt')

            return jsonify({'status': 'Data scraped and predicted successfully', 'predictions': formatted_predictions})
        else:
            return jsonify({'error': 'Error during data scraping'})
    except Exception as e:
        error_message = f'Error during scraping and prediction: {str(e)}'
        return jsonify({'error': error_message})

@app.route('/')
def index():
    return render_template('index.html')
def index1():
    return render_template('index1.html')

@app.route('/summarize', methods=['POST'])
def summarize():
    if request.method == 'POST':
        article = request.form['article']
        max_chunk_length = 1000
        chunks = [article[i:i + max_chunk_length] for i in range(0, len(article), max_chunk_length)]

        chunk_summaries = []
        for chunk in chunks:
            summary = summarizer(chunk, max_length=150, min_length=30, do_sample=False)[0]['summary_text']
            chunk_summaries.append(summary)

        total_summary = ' '.join(chunk_summaries)

        return render_template('index.html', article=article, summary=total_summary)

@app.route('/compare', methods=['POST', 'GET'])
@app.route('/compare', methods=['POST', 'GET'])
def compare():
    if request.method == 'POST':
        government_policy = request.form.get('government_policy')
        company_policy = request.form.get('company_policy')

        if government_policy is not None and company_policy is not None:
            result = calculate_compatibility(government_policy, company_policy)
            return render_template('index1.html', result=result)

    # Handle GET requests or invalid POST requests
    return render_template('index1.html')


def check_texts_in_scraped_data(scraped_file_path, texts_to_check_file_path, output_file_path='final_charge.txt'):
    try:
        # Read the scraped data
        with open(scraped_file_path, 'r', encoding='utf-8') as scraped_file:
            scraped_data = scraped_file.read()

        # Read the texts to check
        with open(texts_to_check_file_path, 'r', encoding='utf-8') as texts_file:
            texts_to_check = texts_file.readlines()
        print("Texts to check:", texts_to_check)

        # Initialize a list to store found texts
        found_texts = []

        # Check each text from the second file
        for text in texts_to_check:
            text = text.strip()  # Remove leading/trailing whitespace
            if text in scraped_data:
                found_texts.append(text)
        print("Found texts:", found_texts)

        # Write found texts to the output file
        with open(output_file_path, 'w', encoding='utf-8') as output_file:
            for found_text in found_texts:
                output_file.write(found_text + '\n')

        print("Found texts written to", output_file_path)
        return found_texts

    except Exception as e:
        print("An error occurred:", str(e))
        return False




@app.route('/extra_charge',methods=['POST'])
def extra_charge():
    try:
        data = request.json
        url = data.get('url')
        print(url)
        if not url:
            return jsonify({'error': 'Missing URL in the request'})
        scraped_data_file = scrape_website(url,output_file_path='charge_scraper.txt')
        if scraped_data_file:
            text = check_texts_in_scraped_data('charge_scraper.txt','extra_charge.txt')
            return jsonify({'status': 'Data scraped and predicted successfully','found_texts':text})
        else:
            return jsonify({'error': 'Error during data scraping'})
    except Exception as e:
        error_message = f'Error during scraping: {str(e)}'
        return jsonify({'error': error_message})

# @app.route('/search',methods=['POST'])
# def search():
#     try:
#         data = request.json
#         url = data.get('url')

#     except Exception as e:
#         error_message = f'Error during scraping: {str(e)}'
#         return jsonify({'error': error_message})

if __name__ == '__main__':
    app.run(port=5000, debug=True)
