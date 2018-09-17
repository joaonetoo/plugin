# -*- coding: utf-8 -*-
from flask import Flask, jsonify,request, Response
from flask_cors import CORS
import gensim, nltk, re, json, os
from gensim import corpora,similarities, models
from nltk.tokenize import word_tokenize
from datetime import date,datetime
from nltk.stem.snowball import SnowballStemmer
import unicodedata
from utils import DataUtility

app = Flask(__name__)
CORS(app)

@app.route("/")
def hello():
    return "Root Api"    

@app.route('/notices', methods=['GET'])
def get_notices():
    notices = []
    format = "%d/%m/%Y"
    FILTER_DEFAULT_DAYS = 7
    DataUtility.open_file('blasting.jl', notices,format)
    DataUtility.open_file('uol.jl',notices,format)
    DataUtility.open_file('globo.jl', notices,format)

    BASEDIR = os.getcwd()
    dictionary = corpora.Dictionary.load(BASEDIR+"/notices_dict.dict")
    corpus = corpora.MmCorpus(BASEDIR+"/notices_corpus.mm")
    lsi = models.LsiModel.load(BASEDIR+"/model_notices.lsi")
    index = similarities.Similarity.load(BASEDIR+"/model_similarity.index")
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

    body_notice = [re.sub('\xa0','',notice['article'])]

    documents_notice = DataUtility.pre_processing_data(body_notice)
    
    corpus_notice = [dictionary.doc2bow(document) for document in documents_notice]
    
    vec_lsi = lsi[corpus_notice[0]] 
   
    sims = index[vec_lsi]
    results = []
    for s in sims:
        if s[1] > 0.5:
            try:
                results.append([notices[s[0]]['title'],notices[s[0]]['link'],
                notices[s[0]]['website'], notices[s[0]]['date']])
            except:
                pass
    if (len(results) > 0):
        return jsonify({'url': results})
    else:
        return jsonify({'url': []})


if __name__ == '__main__':
    app.run(host="0.0.0.0")
