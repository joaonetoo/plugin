import gensim, nltk, re, json, os
from gensim import corpora,similarities, models
from nltk.tokenize import word_tokenize
from datetime import date,datetime
from nltk.stem.snowball import SnowballStemmer
import unicodedata
from utils import DataUtility

notices,body = [],[]
BASEDIR = os.getcwd()
format = "%d/%m/%Y"
FILTER_DEFAULT_DAYS = 7
DataUtility.open_file('blasting.jl', notices,format)
DataUtility.open_file('uol.jl',notices,format)
DataUtility.open_file('globo.jl', notices,format)

# notices = list(filter(lambda x: DataUtility.date_calculate(x['date']) <= FILTER_DEFAULT_DAYS , notices))
# notices = sorted(notices, key = lambda x: x['date'],reverse=True)
body = []
body.extend([re.sub('\xa0','',notice['article']) for notice in notices])

documents = DataUtility.pre_processing_data(body)

dictionary = corpora.Dictionary(documents)
corpus = [dictionary.doc2bow(document) for document in documents]

tf_idf = models.TfidfModel(corpus)
corpus_tfidf = tf_idf[corpus]

lsi = gensim.models.LsiModel(corpus_tfidf, id2word=dictionary,num_topics=300)

index = similarities.Similarity(BASEDIR+"/index",lsi[corpus],num_features=len(dictionary),num_best=10)

dictionary.save(BASEDIR+"/notices_dict.dict")
corpora.MmCorpus.serialize(BASEDIR+"/notices_corpus.mm", corpus)
lsi.save(BASEDIR+"/model_notices.lsi")
index.save(BASEDIR+"/model_similarity.index")
