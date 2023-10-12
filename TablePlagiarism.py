import re
from collections import Counter
import math
import subprocess

# Function to preprocess text (lowercase, remove punctuation)
def preprocess_text(text):
    text = text.lower()
    text = re.sub(r'[^\w\s]', '', text)
    return text

# Function to generate n-grams from text
def generate_ngrams(text, n):
    words = text.split()
    ngrams = [tuple(words[i:i + n]) for i in range(len(words) - n + 1)]
    return ngrams

# Function to calculate cosine similarity between two texts
def calculate_cosine_similarity(text1, text2):
    text1 = preprocess_text(text1)
    text2 = preprocess_text(text2)

    n = 2  # You can adjust the size of n-grams as needed
    ngram_text1 = generate_ngrams(text1, n)
    ngram_text2 = generate_ngrams(text2, n)

    count_text1 = Counter(ngram_text1)
    count_text2 = Counter(ngram_text2)

    norm_text1 = math.sqrt(sum(count**2 for count in count_text1.values()))
    norm_text2 = math.sqrt(sum(count**2 for count in count_text2.values()))

    dot_product = sum(count_text1[ngram] * count_text2[ngram] for ngram in ngram_text1 if ngram in ngram_text2)

    similarity = dot_product / (norm_text1 * norm_text2)

    return similarity

# Extract text from PDF 1
pdf1_file = "plagiarism1.pdf"  #this is the path to the pdf file
text1_file = "plagiarism1.txt" #this file will be automatically created 

# Use pdftotext to extract text from PDF 1
conversion_command = f"pdftotext {pdf1_file} {text1_file}"
subprocess.run(conversion_command, shell=True)

# Extracted text from PDF 1
with open(text1_file, 'r', encoding='utf-8') as file:
    extracted_text1 = file.read()

# Extract text from PDF 2
pdf2_file = "plagiarism2.pdf"   #this is the path to the pdf file
text2_file = "plagiarism2.txt"  #this file will be automatically created 

# Use pdftotext to extract text from PDF 2
conversion_command = f"pdftotext {pdf2_file} {text2_file}"
subprocess.run(conversion_command, shell=True)

# Extracted text from PDF 2
with open(text2_file, 'r', encoding='utf-8') as file:
    extracted_text2 = file.read()

# Calculate similarity between the extracted texts
similarity = calculate_cosine_similarity(extracted_text1, extracted_text2)
print(f"Cosine Similarity: {similarity * 100} %")

# Threshold to decide if it's plagiarism or not
plagiarism_threshold = 80  # For example, 80% similarity
if similarity >= plagiarism_threshold / 100:
    print("Plagiarism detected!")
else:
    print("Not plagiarism.")

