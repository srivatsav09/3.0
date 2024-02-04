from fuzzywuzzy import process

# Sample text
text = "sales"

# List of keywords related to shipping or charges
keywords = ["shipping", "charges", "fee", "cost", "price","tax"]

# Function to check if a word matches any of the keywords
def match_keyword(word):
    highest_match = process.extractOne(word, keywords)
    if highest_match[1] >= 70:  # Adjust the threshold as needed
        return True
    return False

# Tokenize the text and check for matches
words = text.split()
matched_words = [word for word in words if match_keyword(word.lower())]

# Print the matched words
print("Matched words:", matched_words)
