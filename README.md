Web Scraping & Sentiment Analysis Project
Project Overview

This project is designed to scrape web articles, process their content, and perform sentiment analysis to extract key metrics like Positive Score, Negative Score, Polarity, Subjectivity, and various text complexity features. The analysis results are exported into an Excel file for further examination.
Key Features

    Web Scraping: Extracts article titles and content from web pages using the requests library and parses the HTML using BeautifulSoup.
    Text Preprocessing: Cleans the extracted text, removes stop words, and tokenizes it into sentences and words.
    Sentiment Analysis: Calculates sentiment scores using predefined positive and negative word lists from a dictionary.
    Text Complexity Metrics: Calculates various text metrics such as Average Sentence Length, Complex Word Count, and Fog Index to assess readability.
    Excel Output: Exports all results to an Excel file, including all sentiment and complexity metrics for each URL.

Sentiment and Text Analysis Metrics

For each article, the following metrics are calculated and stored in the output Excel file:

    Positive Score: The count of positive words.
    Negative Score: The count of negative words.
    Polarity Score: The overall sentiment of the text.
    Polarity Score=Positive Score−Negative ScorePositive Score+Negative Score+0.000001
    Polarity Score=Positive Score+Negative Score+0.000001Positive Score−Negative Score​
    Subjectivity Score: The proportion of subjective words in the text.
    Subjectivity Score=Positive Score+Negative ScoreTotal Words+0.000001
    Subjectivity Score=Total Words+0.000001Positive Score+Negative Score​
    Average Sentence Length: The average number of words per sentence.
    Percentage of Complex Words: The percentage of words that are considered complex (having more than two syllables).
    Fog Index: A readability score to measure how difficult the text is to read.
    Fog Index=0.4×(WordsSentences+Complex WordsWords)
    Fog Index=0.4×(SentencesWords​+WordsComplex Words​)
    Average Number of Words per Sentence
    Complex Word Count: The number of complex words.
    Word Count: The total number of words in the article.
    Syllables per Word: The average number of syllables per word.
    Personal Pronouns: The count of personal pronouns like "I", "we", "my", etc.
    Average Word Length: The average length of words in terms of characters.

Project Structure

    Input.xlsx: Contains the URLs to scrape and analyze.
    StopWords: Folder containing text files with various stop words used for preprocessing.
    MasterDictionary: Folder containing the positive and negative word lists used for sentiment analysis.

Dependencies

To run this project, the following Python packages are required:

    requests
    nltk
    pandas
    BeautifulSoup4
    openpyxl
    chardet

You can install the required dependencies using pip:

pip install requests nltk pandas beautifulsoup4 openpyxl chardet

Running the Project

    Place the URLs to be scraped in the Input.xlsx file under the appropriate columns: URL_ID and URL.
    Run the Python script to scrape the articles, perform sentiment analysis, and generate the Excel output.
    The results will be saved to Output_Data_Structure.xlsx with all calculated metrics.

Example command to run the script:

bash

python sentiment_analysis.py

Error Handling

    The script includes basic error handling for encoding issues. If there is an encoding error when processing a URL, it will log the error and continue to the next URL.




