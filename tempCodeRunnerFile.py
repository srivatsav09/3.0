from flask import Flask, request, jsonify, render_template
from scraper import scrape_website
from transformers import pipeline
from model_loader import load_and_predict_model

app = Flask(__name__)

@app.route('/scrape', methods=['POST'])
def scrape_data():
    try:
        data = request.json
        url = data.get('url')
        if not url:
            return jsonify({'error': 'Missing URL in the request'})

        scraped_data_file = scrape_website(url)
        
        if scraped_data_file:
            predictions = load_and_predict_model(scraped_data_file)
            formatted_predictions = [{'text': entry['text'], 'prediction': entry['prediction']} for entry in predictions]

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
        max_chunk_length = 1000
        chunks = [article[i:i + max_chunk_length] for i in range(0, len(article), max_chunk_length)]

        chunk_summaries = []
        for chunk in chunks:
            summary = summarizer(chunk, max_length=150, min_length=30, do_sample=False)[0]['summary_text']
            chunk_summaries.append(summary)

        total_summary = ' '.join(chunk_summaries)

        return render_template('index.html', article=article, summary=total_summary)

if __name__ == '__main__':
    summarizer = pipeline("summarization")  # Moved inside the if block
    app.run(port=5000)
