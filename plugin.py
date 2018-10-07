# -*- coding: utf-8 -*-
from flask import Flask, jsonify,request, Response
from flask_cors import CORS
import gensim, nltk, re, json, os
from gensim import corpora,similarities, models
from nltk.tokenize import word_tokenize
from datetime import date,datetime
from nltk.stem.snowball import SnowballStemmer
import unicodedata
from scripts.utils import DataUtility
from scripts.models import db, News
# News.query.filter(News.article == None).all()
app = Flask(__name__)
POSTGRES = {
    'user': os.environ.get("USER_POSTGRES"),
    'pw': os.environ.get("PASS_POSTGRES"),
    'db': os.environ.get("DB_NAME"),
    'host': os.environ.get("HOST_DB"),
    'port': '5432',
}

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://%(user)s:\
%(pw)s@%(host)s:%(port)s/%(db)s' % POSTGRES
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)
db.app = app
CORS(app)


@app.route("/")
def hello():
    return "Root Api"    

@app.route('/notices', methods=['GET'])
def get_notices():
    notices = []
    BASEDIR = os.getcwd()

    url = request.args.get('site')

    body_notice =[]

    if(os.path.exists(BASEDIR+"/notice.jl")):
        os.system("rm notice.jl")

    if (re.search("g1.globo.com",url)):
        os.system("scrapy crawl notice_globo -a notice=%s -o notice.jl"%url) 
    elif (re.search("br.blastingnews.com",url)):
        os.system("scrapy crawl notice_blasting -a notice=%s -o notice.jl"%url) 
    elif (re.search("noticias.uol.com.br",url)):
        os.system("scrapy crawl notice_uol -a notice=%s -o notice.jl"%url) 

    with open('notice.jl','r') as f:
        for line in f:
            notice = json.loads(line)
    start = DataUtility.date_increase(notice['date'])
    
    end = DataUtility.date_decrease(notice['date'])
    
    notices = News.query.filter(News.date >= end).filter(News.date <= start).all()
    
    documents = list(map(lambda x: x.processed , notices))
    
    dictionary = corpora.Dictionary(documents)

    corpus = [dictionary.doc2bow(document) for document in documents]

    tf_idf = models.TfidfModel(corpus)

    corpus_tfidf = tf_idf[corpus]

    lsi = gensim.models.LsiModel(corpus_tfidf, id2word=dictionary)
    
    index = similarities.Similarity(BASEDIR+"/index",lsi[corpus],num_features=len(dictionary),num_best=10)
    
    body_notice = [re.sub('\xa0','',notice['article'])]

    documents_notice = DataUtility.pre_processing_data(body_notice)
    
    corpus_notice = [dictionary.doc2bow(document) for document in documents_notice]
    
    vec_lsi = lsi[corpus_notice[0]] 
   
    sims = index[vec_lsi]
    print(sims)
    results = []
    for s in sims:
        if s[1] > 0.5:
            try:
                results.append([notices[s[0]].title,notices[s[0]].link,
                notices[s[0]].website, notices[s[0]].date])
            except:
                pass
    if (len(results) > 1):
        result.pop(0)
        return jsonify({'url': results})
    else:
        return jsonify({'url': []})


if __name__ == '__main__':
    app.config['DEBUG'] = True
    app.run(host="0.0.0.0")
