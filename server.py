# # server.py

from flask import Flask, request, jsonify,render_template
from scraper import scrape_website
from model_loader import load_and_predict_model  # Import the model loader function

app = Flask(__name__)


# @app.route('/scrape', methods=['POST'])
# def scrape_data():
#     try:
#         data = request.json
#         url = data.get('url')  # Assuming the URL is sent in the 'url' field of the JSON request
#         if not url:
#             return jsonify({'error': 'Missing URL in the request'})

#         scraped_data_file = scrape_website(url)
        
#         if scraped_data_file:
#             # Call the model loading and prediction function
#             predictions = load_and_predict_model(scraped_data_file)

#             # Format predictions for better readability
#             formatted_predictions = [{'text': entry['text'], 'prediction': entry['prediction']} for entry in predictions]

#             return jsonify({'status': 'Data scraped and predicted successfully', 'predictions': formatted_predictions})
#         else:
#             return jsonify({'error': 'Error during data scraping'})
#     except Exception as e:
#         error_message = f'Error during scraping and prediction: {str(e)}'
#         return jsonify({'error': error_message})
# @app.route('/summarizer')
# def summarizer():
#     # Redirect to the summarizer HTML page
#     return render_template('summarizer.html')


# if __name__ == '__main__':
#     app.run(port=5000)

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

if __name__ == '__main__':
    app.run(port=5000)
