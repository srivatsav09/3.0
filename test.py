from flask import Flask, request, jsonify
from scraper import scrape_website
from model_loader import load_and_predict_model  # Import the model loader function

app = Flask(__name__)

@app.route('/summarize', methods=['POST'])
def summarize():
    data = request.json
    # Implement your text summarization logic here
    summarized_text = "This is a sample summary."
    return jsonify({'summary': summarized_text})

@app.route('/scrape', methods=['POST'])
def scrape_data():
    try:
        data = request.json
        url = data.get('url')  # Assuming the URL is sent in the 'url' field of the JSON request
        if not url:
            return jsonify({'error': 'Missing URL in the request'})

        scraped_data_file = scrape_website(url)
        
        if scraped_data_file:
            # Call the model loading and prediction function
            predictions = load_and_predict_model(scraped_data_file)
            return jsonify({'status': 'Data scraped and predicted successfully', 'predictions': predictions})
        else:
            return jsonify({'error': 'Error during data scraping'})
    except Exception as e:
        error_message = f'Error during scraping and prediction: {str(e)}'
        return jsonify({'error': error_message})

if __name__ == '__main__':
    app.run(port=5000)
