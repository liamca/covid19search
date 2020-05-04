# -*- coding: utf-8 -*-
import logging
from logging.handlers import RotatingFileHandler
# Examples
# app.logger.warning('A warning occurred (%d apples)', 42)
# app.logger.error('An error occurred')
# app.logger.info('Info')

import urllib.request as ur

import os
from flask import Flask, render_template, request, flash, Markup

from flask_wtf import FlaskForm
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy

import json
import requests

import SPTAG
import numpy as np

import sqlite3
from sqlite3 import Error

import spacy
# Initialize spacy 'en' model, keeping only tagger component needed for lemmatization
nlp = spacy.load('en_core_web_sm', disable=['parser', 'ner'])

import nltk.data
from nltk import sent_tokenize, tokenize, word_tokenize
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')
nltk.download('wordnet')

from nltk.stem import WordNetLemmatizer  
lemmatizer = WordNetLemmatizer() 

app = Flask(__name__,
    static_url_path='',
    static_folder='templates')
app.secret_key = 'dev'

bootstrap = Bootstrap(app)
db = SQLAlchemy(app)

# SPTag Config
k = 31

sptag_doc_idx = '/data/sptag_doc_idx'
sptag_doc_idx = SPTAG.AnnIndex.Load(sptag_doc_idx)
sptag_doc_idx.SetSearchParam("MaxCheck", '1024')

sptag_term_idx = '/data/sptag_term_idx'
sptag_term_idx = SPTAG.AnnIndex.Load(sptag_term_idx)
sptag_term_idx.SetSearchParam("MaxCheck", '1024')

# SQLite Config
sqlite_doc_vec_dir = '/data/sqlite-doc-vectors'
sqlite_doc_vec_file = "doc-vectors.db"

sqlite_term_vec_dir = '/data/sqlite-term-vectors'
sqlite_term_vec_file = "term-vectors.db"

# Configure log file location
logging.basicConfig(filename='flask-app.log',level=logging.DEBUG)

    
@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')

    
@app.route('/document/<docid>', methods=['GET', 'POST'])
def document(docid):
    json_file = docid[:docid.find('-')] + ".json"
    data = {'json_file': json_file}
    return render_template('document.html', data=data)


def findTermVector(term):
    # Get the vector based on a term
    app.logger.info('Finding vector for term...')

    sql = "select vector from vectors where term = ? limit 1"
    sqlite_term_conn = sqlite3.connect(os.path.join(sqlite_term_vec_dir,sqlite_term_vec_file))
    cur = sqlite_term_conn.cursor()
    cur.execute(sql, (term,))
 
    app.logger.info('Fetching vectors for term...')

    rows = cur.fetchall()
 
    v = ''
    for row in rows:
        v = str(row[0])
    
    app.logger.info('V: ', v)

    if len(v) > 0:
        vec = v.replace("'", "").replace("|", ",")
        return eval ('[' + vec + ']')
    else:
        return []
    
def findDocVector(docid):
    # Get the vector based on a docid
    app.logger.info('Finding vector for doc...')

    sql = "select vector from vectors where docid = ?"
    sqlite_doc_conn = sqlite3.connect(os.path.join(sqlite_doc_vec_dir,sqlite_doc_vec_file))
    cur = sqlite_doc_conn.cursor()
    cur.execute(sql, (docid,))
 
    rows = cur.fetchall()
 
    v = ''
    for row in rows:
        v = str(row[0])
    
    app.logger.info('V: ', v)

    vec = v.replace("'", "").replace("|", ",")

    return eval ('[' + vec + ']')
    
def findAvgVectorOfTerms(terms):
    query_vectors = []
    app.logger.info('Iterating terms...')

    for t in terms:
        #print ('term', t)
        tv = findTermVector(lemmatizer.lemmatize(t))
        if len(tv) > 0:
            query_vectors.append(tv)

    app.logger.info('Query Vector:', query_vectors)

    avg_query_vector = np.average(query_vectors, axis=0)
    return np.asarray(avg_query_vector, dtype=np.float32)
    
@app.route('/typeahead', methods=['GET', 'POST'])
def typeahead():
    # Type Ahead Search
    app.logger.info('Performing type ahead...')
    content = request.get_json(silent=True)
    app.logger.info('Query: ', content['query'])
    query = content['query']
    
    term_array = []
    
    sql = "select term from vectors where term like ? and vector is not null limit 10"
    sqlite_term_conn = sqlite3.connect(os.path.join(sqlite_term_vec_dir,sqlite_term_vec_file))
    cur = sqlite_term_conn.cursor()
    cur.execute(sql, (query+'%',))
 
    rows = cur.fetchall()
 
    v = ''
    for row in rows:
        term_array.append(str(row[0]))
      
    return json.dumps(term_array)

@app.route('/termVectorSearch', methods=['GET', 'POST'])
def termVectorSearch():
    app.logger.info('Finding similar terms...')
    content = request.get_json(silent=True)
    app.logger.info('Content: ', content)
    
    terms = content['terms']
    
    avg_vec = findAvgVectorOfTerms(terms)

    # Get all the terms that are sematically similar
    terms_result = sptag_term_idx.SearchWithMetaData(avg_vec, k)
    
    # Get all the docs that are sematically similar
    docs_result = sptag_doc_idx.SearchWithMetaData(avg_vec, k)
    
    docs_terms_and_distance = [terms_result[1], terms_result[2], docs_result[1], docs_result[2]]
    

    return json.dumps(str(docs_terms_and_distance).replace("b'", "'")) 
    
    # print (result[0]) # ids
    # print (result[1]) # distances
    # print (result[2]) # metadata

@app.route('/docVectorSearch', methods=['GET', 'POST'])
def docVectorSearch():
    app.logger.info('Finding similar docs...')
    content = request.get_json(silent=True)
    app.logger.info('Content: ', content)
    
    docid = content['docid']
    
    doc_vec = np.asarray(findDocVector(docid), dtype=np.float32)

    # Get all the terms that are sematically similar
    docs_result = sptag_doc_idx.SearchWithMetaData(doc_vec, k)
    
    docs_terms_and_distance = [docs_result[1], docs_result[2]]
    

    return json.dumps(str(docs_terms_and_distance).replace("b'", "'")) 
    
    # print (result[0]) # ids
    # print (result[1]) # distances
    # print (result[2]) # metadata


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=80)
