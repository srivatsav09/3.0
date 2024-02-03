# # server.py

from flask import Flask, request, jsonify,render_template
from scraper import scrape_website
from transformers import pipeline
from model_loader import load_and_predict_model  # Import the model loader function

app = Flask(__name__)

summarizer = pipeline("summarization")

import json

def save_predictions_to_txt(predictions, output_file):
    with open(output_file, 'w') as file:
        for entry in predictions:
            if entry['prediction'] == 1:
                file.write(f"{entry['text']}\n\n")

# Rest of your code remains unchanged...

@app.route('/scrape', methods=['POST'])
def scrape_and_predict():
    try:
        data = request.json
        url = data.get('url')  # Assuming the URL is sent in the 'url' field of the JSON request
        if not url:
            return jsonify({'error': 'Missing URL in the request'})

        scraped_data_file = scrape_website(url)
        
        if scraped_data_file:
            # Call the model loading and prediction function
            predictions = load_and_predict_model(scraped_data_file)

            # Format predictions for better readability
            formatted_predictions = [{'text': entry['text'], 'prediction': entry['prediction']} for entry in predictions]

            # Save predictions with value 1 to a text file
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

@app.route('/summarize', methods=['POST'])
def summarize():
    if request.method == 'POST':
        article = request.form['article']

        # Define the maximum length for each chunk
        max_chunk_length = 1000

        # Split the article into chunks
        chunks = [article[i:i + max_chunk_length] for i in range(0, len(article), max_chunk_length)]

        # Summarize each chunk and store the summaries
        chunk_summaries = []
        for chunk in chunks:
            summary = summarizer(chunk, max_length=150, min_length=30, do_sample=False)[0]['summary_text']
            chunk_summaries.append(summary)

        # Combine the chunk summaries into a total summary
        total_summary = ' '.join(chunk_summaries)

        return render_template('index.html', article=article, summary=total_summary)
if __name__ == '__main__':
    app.run(port=5000,debug=True)
