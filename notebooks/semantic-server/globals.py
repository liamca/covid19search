#!/usr/bin/env python
# coding: utf-8
import os
from pathlib import Path
import shutil
from shutil import rmtree
from os import listdir
from os.path import isfile, join


# general
max_parallelism = 8
minPhraseLen = 6

#blob 
blob_account_name = [Container Name]
blob_account_key = [Container Key]
blob_container_name = [Container Name]
blob_container_path = 'json/'

root_dir = '/datadrive/processed/corona'

# location where processed text goes (lemmatized, etc)
processed_text_dir = os.path.join(root_dir, 'terms')

# parms for calculating bm25
merged_text_dir = os.path.join(root_dir, 'merged-terms')
merged_text_file_name = 'merged.txt'

bm25_tmp_dir = os.path.join(root_dir, 'tmp')


bm25_dir = os.path.join(root_dir, 'bm25')
bm25_file = 'avg-bm25.txt'
k1 = 1.2
b = 0.75

# fasttext parms
fasttext_bin = '../fastText-0.9.2/fasttext'
vectors_out_dir = '/datadrive/processed/corona/fasttext_vectors'
n_threads = 16
min_count = 10
verbose=2
vector_size= 300

vectors_out_file = 'vectors_w2v_300dim.vec'
sptag_formatted_vectors_out_file = 'vectors_w2v_300dim.sptag'

index_builder = '../SPTAG/Release/indexbuilder'
sptag_term_idx_folder = os.path.join(root_dir, 'sptag_term_idx')

sqlite_term_vec_dir = os.path.join(root_dir, 'sqlite-term-vectors')
sqlite_term_vec_file = "term-vectors.db"

avg_doc_vec_dir = '/datadrive/processed/corona/avg-doc-vec/'
avg_doc_vec_file = 'avg-doc-vec.txt'

sptag_doc_idx_folder = os.path.join(root_dir, 'sptag_doc_idx')

sqlite_doc_vec_dir = os.path.join(root_dir, 'sqlite-doc-vectors')
sqlite_doc_vec_file = 'doc-vectors.db'



################################
#    Global Functions
################################

# reset output dir
def resetDir(dir):
    processed_path = Path(dir)
    if processed_path.exists():
        rmtree(processed_path)
    processed_path.mkdir(parents=True)
    
def getFilesInDir(in_dir):
#     return [f for f in listdir(in_dir) if isfile(join(in_dir, f))]    
    return [os.path.join(dp, f) for dp, dn, filenames in os.walk(in_dir) for f in filenames]
