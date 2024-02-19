import re
from nltk import sent_tokenize, pos_tag, word_tokenize, everygrams
from nltk.corpus import wordnet, stopwords

def get_email(text):
    r = re.compile(r'[A-Za-z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+')
    return r.findall(str(text))

def get_name(text):
    name = None
    pattern = r"(\b[A-Z][a-z]+\b)\s(\b[A-Z][a-z]+\b)"
    match = re.search(pattern, text)
    if match:
        name = match.group()
    return name