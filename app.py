# encoding=utf8
from flask import Flask, jsonify,request, Response
from flask_cors import CORS
import gensim, nltk, re, json, os
from gensim import corpora,similarities, models
from nltk.tokenize import word_tokenize
from datetime import date,datetime
from nltk.stem.snowball import SnowballStemmer
import unicodedata

app = Flask(__name__)
CORS(app)


@app.route('/notices', methods=['GET'])
def get_notices():
    notices,body = [],[]
    format = "%d/%m/%Y"
    FILTER_DEFAULT_DAYS = 7

    def remover_combinantes(string):
        string = unicodedata.normalize('NFD', string)
        return u''.join(ch for ch in string if unicodedata.category(ch) != 'Mn')

    def open_file(name_file):
        with open(name_file,'r') as file:
            for line in file:
                notice = json.loads(line)
                if notice['date'] and notice['article'] and notice['article'] != ' ':
                    notice['date'] = datetime.strptime(notice['date'],format).date()
                    notices.append(notice)
                    
    def date_calculate(dateNotice):    
        today = date.today()
        return abs((today - dateNotice).days)

    open_file('blasting.jl')
    open_file('uol.jl')
    open_file('globo.jl')

    notices = list(filter(lambda x: date_calculate(x['date']) <= FILTER_DEFAULT_DAYS , notices))
    notices = sorted(notices, key = lambda x: x['date'],reverse=True)

    body = []

    body.extend([re.sub('\xa0','',notice['article']) for notice in notices])

    BASEDIR = os.getcwd()
    stopwords = nltk.corpus.stopwords.words("portuguese")
    stemmer = SnowballStemmer("portuguese")

    regex = "[a-zA-ZçÇãÃõÕáÁéÉíÍóÓúÚâÂêÊîÎôÔûÛàÀ]+"

    if (os.path.exists(BASEDIR+"/notices_dict.dict")):
        dictionary = corpora.Dictionary.load(BASEDIR+"/notices_dict.dict")
        corpus = corpora.MmCorpus(BASEDIR+"/notices_corpus.mm")
        lsi = models.LsiModel.load(BASEDIR+"/model_notices.lsi")

    else:

        documents_without_stopwords = [[stemmer.stem(remover_combinantes(w.lower())) for w in word_tokenize(text) if w.lower() not in stopwords] 
                    for text in body]
        documents = []
        for document in documents_without_stopwords:
            filtered_tokens = []
            for token in document:
                if re.search(regex, token):
                    filtered_tokens.append(token)
            documents.append(filtered_tokens)

        dictionary = corpora.Dictionary(documents)

        dictionary.save(BASEDIR+"/notices_dict.dict")

        corpus = [dictionary.doc2bow(document) for document in documents]

        corpora.MmCorpus.serialize(BASEDIR+"/notices_corpus.mm", corpus)

        tf_idf = models.TfidfModel(corpus)

        corpus_tfidf = tf_idf[corpus]

        lsi = gensim.models.LsiModel(corpus_tfidf, id2word=dictionary,num_topics=100)
        
        lsi.save(BASEDIR+"/model_notices.lsi") 

    index = similarities.Similarity(BASEDIR+"/index",lsi[corpus],num_features=len(dictionary),num_best=10)

    url = request.args.get('site')
    print(url)
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
        notice = json.load(f)
    body_notice = [re.sub('\xa0','',notice['article'])]

    documents_notice_without_stopwords = [[stemmer.stem(remover_combinantes(w.lower())) for w in word_tokenize(text) if w.lower() not in stopwords] 
                for text in body_notice]
    documents_notice = []
    for document in documents_notice_without_stopwords:
        filtered_tokens = []
        for token in document:
            if re.search(regex, token):
                filtered_tokens.append(token)
        documents_notice.append(filtered_tokens)
    corpus_notice = [dictionary.doc2bow(document) for document in documents_notice]
    vec_lsi = lsi[corpus_notice[0]] 
    sims = index[vec_lsi]
    results =[]
    for s in sims:
        if s[1] > 0.5:
            results.append([notices[s[0]]['title'],notices[s[0]]['link']])
    return jsonify({'url': results})

if __name__ == '__main__':
    app.run(debug=True)
