from flask import Flask, render_template, request
from transformers import pipeline

app = Flask(__name__)

# Load the summarization pipeline
summarizer = pipeline("summarization")

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
    app.run(debug=True)
