#!/usr/bin/env python
# coding: utf-8

import os
from os import listdir
from os.path import isfile, join
import glob

from pathlib import Path
import shutil
from shutil import rmtree

files_dir = '/datadrive/processed/content'

#blob 
blob_account_name = [Container Name]
blob_account_key = [Container Key]
blob_container_name = [Container Name]
blob_container_path = 'json/'


#search
endpoint = 'https://' [Search Service Name] '.search.windows.net/'
api_version = '?api-version=2019-05-06'
headers = {'Content-Type': 'application/json',
        'api-key': [Search Admin API Key] }
indexName = 'covid-19-v6'

# TA Endpoint
ta_base_url = "https://" [TA for Health Container] ".azurewebsites.net/text/analytics/v3.0-preview.1/domains/health"

ta_processing_dir = '/datadrive/processed/ta'
ta_processed_json_dir = '/datadrive/processed/ta-json'


# UMLS Concepts
umls_dir = '/datadrive/processed/umls'
conso_url = 'https://' [Location of File] '.blob.core.windows.net/covid-19/umls-2019AB-mrconso.zip'
local_conso_file = os.path.join(umls_dir, 'umls-2019AB-mrconso.zip')
concepts_file = os.path.join(umls_dir, 'MRCONSO.RRF')


################################
#    Global Functions
################################

def getFilesInDir(in_dir):
#     return [f for f in listdir(in_dir) if isfile(join(in_dir, f))]    
    return [os.path.join(dp, f) for dp, dn, filenames in os.walk(in_dir) for f in filenames]


# reset output dir
def resetDir(dir):
    processed_path = Path(dir)
    if processed_path.exists():
        rmtree(processed_path)
    processed_path.mkdir(parents=True)
