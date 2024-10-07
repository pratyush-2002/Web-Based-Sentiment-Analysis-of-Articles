import requests
import nltk
from nltk.tokenize import word_tokenize, sent_tokenize
import chardet
from bs4 import BeautifulSoup
import pandas as pd
import re


file_path = "Input.xlsx"
df_input = pd.read_excel(file_path, sheet_name="Sheet1")
url_ids = df_input['URL_ID'].tolist()
urls = df_input['URL'].tolist()
count=0

df_output = pd.DataFrame(columns=[
    "URL_ID", "URL", "POSITIVE SCORE", "NEGATIVE SCORE", "POLARITY SCORE", "SUBJECTIVITY SCORE",
    "AVG SENTENCE LENGTH", "PERCENTAGE OF COMPLEX WORDS", "FOG INDEX","AVG NUMBER OF WORDS PER SENTENCE",
    "COMPLEX WORD COUNT","WORD COUNT", "SYLLABLE PER WORD","PERSONAL PRONOUNS", "AVG WORD LENGTH"
    
])


def get_content(url, filename, headers):
    r = requests.get(url, headers=headers)
    soup = BeautifulSoup(r.text, "html.parser")
    article_title = soup.find("h1", "entry-title").get_text()
    article_txt = soup.find(class_="td-post-content tagdiv-type").get_text()
    article_title_encoded = article_title.encode('ascii', 'ignore').decode('utf-8')
    article_txt_encoded = article_txt.encode('ascii', 'ignore').decode('utf-8')
    with open(f"{filename}.txt", "w", encoding='utf-8') as file:
        file.write("Title : \n")
        file.write(article_title_encoded)
        file.write("\nContent : \n")
        file.write(article_txt_encoded)


def count_personprononus(text):
    pattern = r"\b(I|we|my|ours|us)\b"
    matches = re.findall(pattern, text, re.IGNORECASE)
    filtered_matches = [match for match in matches if not match.isupper()]
    count = len(filtered_matches)
    return count


for index in range(len(url_ids)):
    try:
        filename = url_ids[index]
        url = urls[index]
        if pd.notna(filename) and pd.notna(url):
            headers = {
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,/;q=0.8,application/signed-exchange;v=b3;q=0.9",
                "Accept-Encoding": "gzip, deflate, br",
                "Accept-Language": "en-US,en;q=0.9",
                "Priority": "u=1",
                "Sec-Fetch-Dest": "document",
                "Sec-Fetch-Mode": "navigate",
                "Sec-Fetch-Site": "cross-site",
                "Sec-Fetch-User": "?1",
                "Sec-Gpc": "1",
                "Upgrade-Insecure-Requests": "1",
                "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36",
                "X-Amzn-Trace-Id": "Root=1-667c53fe-22aa4a273644bb2924a2fea4",
            }


            get_content(url, filename, headers)


            stopwords_list = [
                "StopWords\\StopWords_Auditor.txt",
                "StopWords\\StopWords_Currencies.txt",
                "StopWords\\StopWords_DatesandNumbers.txt",
                "StopWords\\StopWords_Generic.txt",
                "StopWords\\StopWords_GenericLong.txt",
                "StopWords\\StopWords_Geographic.txt",
                "StopWords\\StopWords_Names.txt",
            ]
            stopwords = []
            for file in stopwords_list:
                with open(file, "r") as st:
                    s1 = st.read()
                    stopwords.extend(set(s1.split()))


            with open(f"{filename}.txt", "r", encoding="utf-8", errors="replace") as ft:
                uctext = ft.read()
                count_person_pronouns = count_personprononus(uctext)
                sentences = sent_tokenize(uctext)
                lstext = word_tokenize(uctext)
                uncleaned_num_words = len(lstext)
                lstext = [word.upper() for word in lstext]

            pun = ["?", "!", ",", ".",":"]
            filtered_words = [
                word for word in lstext if word not in stopwords and word not in pun
            ]
            filtered_text = " ".join(filtered_words)

            num_sentences = len(sentences)
            with open("cleaned.txt", "w") as ct:
                ct.write(filtered_text)

            with open("MasterDictionary\\negative-words.txt", "rb") as f:
                result = chardet.detect(f.read())

            sentiment = {}
            pos = pd.read_csv(
                "MasterDictionary\\positive-words.txt", sep=" ", names=["word"]
            )
            for word in pos["word"]:
                sentiment[word.upper()] = "pos"
            neg = pd.read_csv(
                "MasterDictionary\\negative-words.txt",
                sep=" ",
                names=["negword"],
                encoding=result["encoding"],
            )
            for word in neg["negword"]:
                sentiment[word.upper()] = "neg"


            pos_score = 0
            neg_score = 0
            with open("cleaned.txt", "r") as c:
                text = c.read()
                words = word_tokenize(text)
                for word in words:
                    if word in sentiment:
                        if sentiment[word] == "pos":
                            pos_score += 1
                        elif sentiment[word] == "neg":
                            neg_score -= 1
            neg_score *= -1
            total_words = len(words)
            syllable = ["a", "e", "i", "o", "u"]
            num_syllable = 0
            complex_word = 0
            for word in lstext:
                char_count = 0
                vowel_found = False
                word = word.lower()
                sy_count = 0
                for char in word:
                    char_count += 1
                    if char in syllable:
                        if not vowel_found:
                            sy_count += 1
                            vowel_found = True
                        if sy_count > 2:
                            complex_word += 1
                    else:
                        vowel_found = False

                if word.endswith("ed") or word.endswith("es"):
                    if sy_count > 0:
                        sy_count -= 1
                num_syllable += sy_count

                if sy_count > 2:
                    complex_word += 1

            row_data = {
                "URL_ID": filename,
                "URL": url,
                "POSITIVE SCORE": pos_score,
                "NEGATIVE SCORE": neg_score,
                "POLARITY SCORE": (pos_score - neg_score) / ((pos_score + neg_score) + 0.000001),
                "SUBJECTIVITY SCORE": (pos_score + neg_score) / (total_words + 0.000001),
                "AVG SENTENCE LENGTH": uncleaned_num_words / num_sentences,
                "PERCENTAGE OF COMPLEX WORDS": (complex_word / uncleaned_num_words),
                "FOG INDEX": 0.4 * ((uncleaned_num_words / num_sentences) + (complex_word / uncleaned_num_words)),
                "AVG NUMBER OF WORDS PER SENTENCE": uncleaned_num_words / num_sentences,
                "COMPLEX WORD COUNT": complex_word,
                "WORD COUNT": total_words,
                "SYLLABLE PER WORD": num_syllable / total_words,
                "PERSONAL PRONOUNS": count_person_pronouns,
                "AVG WORD LENGTH": char_count / uncleaned_num_words,  
                
            }
            
            df_output = pd.concat([df_output, pd.DataFrame([row_data])], ignore_index=True)
            count+=1
            print(count)
    except (UnicodeDecodeError, UnicodeEncodeError) as e:
        print(f"Error processing URL ID {filename}: {e}")
        continue

output_file = 'Output_Data_Structure.xlsx'
df_output.to_excel(output_file, index=False)
