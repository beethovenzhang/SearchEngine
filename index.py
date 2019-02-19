#!/usr/bin/python2
import json
import time
from bs4 import BeautifulSoup, Comment
import nltk
from nltk.corpus import stopwords
import math
import os

nltk.download('stopwords')
stop_words = set(stopwords.words('english'))
index_json = {}
field_norms = {}
df_max = 0
df_max_word = ""
tf_idf_max = 0
document_nums = 0


def valid(text):
    if text.parent.name in ["style", "meta", "script", "noscript", "link", "br"]:
        return False
    elif isinstance(text, Comment):
        return False
    elif text == "\n":
        return False
    return True


def encode(text):
    return text.string.encode('utf-8')


def get_term(text):
    terms = []
    for line in text:
        token = ""
        for c in line:
            if c.isalpha() or c.isdigit():
                token += c.lower()
            else:
                if len(token) >= 3 and token not in stop_words:
                    terms.append(token)
                token = ""
        if len(token) >= 3 and token not in stop_words:
            terms.append(token)
    return terms


def index_corpus(path):
    global index_json
    global document_nums

    for i in range(75):
        for j in range(500):
            if i == 74 and j > 496:
                break
            filename = "\%d\%d" % (i, j)

            if j % 50 == 0:
                print "now working " + filename

            with open(path + filename) as f:
                soup = BeautifulSoup(f.read(), "lxml")

                if soup.head is not None and soup.body is not None:
                    document_nums += 1
                else:
                    continue

                terms_len = 0
                if soup.head is not None:
                    all_text = filter(valid, soup.head.find_all(text=True))
                    all_text = map(encode, all_text)
                    terms_head = get_term(all_text)
                    terms_len += len(terms_head)
                    for index, term in enumerate(terms_head):
                        if term not in index_json:
                            index_json[term] = {}
                            index_json[term][filename] = {"tf": 0, "tf-idf": 0, "body": []}
                        if filename not in index_json[term]:
                            index_json[term][filename] = {"tf": 0, "tf-idf": 0, "body": []}
                        index_json[term][filename]["tf"] += 1

                if soup.body is not None:
                    all_text = filter(valid, soup.body.find_all(text=True))
                    all_text = map(encode, all_text)
                    terms_body = get_term(all_text)
                    terms_len += len(terms_body)
                    for index, term in enumerate(terms_body):
                        if term not in index_json:
                            index_json[term] = {}
                            index_json[term][filename] = {"tf": 0, "tf-idf": 0, "body": []}
                        if filename not in index_json[term]:
                            index_json[term][filename] = {"tf": 0, "tf-idf": 0, "body": []}
                        index_json[term][filename]["tf"] += 1
                        index_json[term][filename]["body"].append(index)

                global field_norms
                field_norms[filename] = terms_len

    for term in index_json:
        doc_freq = len(index_json[term])

        global df_max
        global df_max_word
        global tf_idf_max

        if doc_freq > df_max:
            df_max = doc_freq
            df_max_word = term

        for filename in index_json[term]:
            tf = index_json[term][filename]["tf"]
            tf_idf = math.log(document_nums / (doc_freq + 1)) * math.sqrt(tf)
            index_json[term][filename]["tf-idf"] = round(tf_idf, 3)
            if tf_idf > tf_idf_max:
                tf_idf_max = tf_idf


def save():
    with open("index.json", "w") as f:
        f.write(json.dumps(index_json))

    with open("length.json", "w") as f:
        f.write(json.dumps(field_norms))

    with open("summary.txt", "w") as f:
        print >> f, "number of documents =", document_nums, "\n"
        print >> f, "number of words =", len(index_json), "\n"
        print >> f, "max doc freq =", df_max, "is", df_max_word, "\n"
        print >> f, "max tf-idf =", tf_idf_max, "\n"

def main():
    start_time = time.time()
    path_base = "WEBPAGES_RAW"
    index_corpus(path_base)
    end_time = time.time()
    print "index total time %.2f" % (end_time - start_time)
    start_time = time.time()
    save()
    end_time = time.time()
    print "save total time %.2f" % (end_time - start_time)

if __name__ == "__main__":
    main()
