import gensim, nltk, re, json, os
from gensim import corpora,similarities, models
from nltk.tokenize import word_tokenize
from datetime import date,datetime
from nltk.stem.snowball import SnowballStemmer
import unicodedata

class DataUtility(object):

    @staticmethod
    def remover_combinantes(string):
        string = unicodedata.normalize('NFD', string)
        return u''.join(ch for ch in string if unicodedata.category(ch) != 'Mn')

    @staticmethod            
    def date_calculate(dateNotice):    
        today = date.today()
        return abs((today - dateNotice).days)

    @staticmethod
    def open_file(name_file,notices, format):
        with open(name_file,'r') as file:
            for line in file:
                notice = json.loads(line)
                if notice['date'] and notice['article'] and notice['article'] != ' ':
                    notice['date'] = datetime.strptime(notice['date'],format).date()
                    notices.append(notice)

    @staticmethod
    def pre_processing_data(body):
        stopwords = nltk.corpus.stopwords.words("portuguese")
        stemmer = SnowballStemmer("portuguese")

        regex = "[a-zA-ZçÇãÃõÕáÁéÉíÍóÓúÚâÂêÊîÎôÔûÛàÀ]+"

        documents_without_stopwords = [[stemmer.stem(DataUtility.remover_combinantes(w.lower())) for w in word_tokenize(text) if w.lower() not in stopwords] 
                    for text in body]
        documents = []
        for document in documents_without_stopwords:
            filtered_tokens = []
            for token in document:
                if re.search(regex, token):
                    filtered_tokens.append(token)
            documents.append(filtered_tokens)
        return documents
