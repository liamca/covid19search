import io
import os
from os import listdir
from os.path import isfile, join
from pathlib import Path
import shutil
from shutil import rmtree
from azure.storage.blob import BlockBlobService

account_name = [Blob Container Name]
account_key = [Blob API Key]

block_blob_service = BlockBlobService(account_name=account_name, account_key=account_key)

container_name = 'covid-19'
container_path = ''

root_data_dir = './data/'

# reset output dir
def resetDir(dir):
    processed_path = Path(dir)
    if processed_path.exists():
        rmtree(processed_path)
    processed_path.mkdir(parents=True)

def downloadFile(blob_name):
    print ('Downloading:', blob_name)
    fp = open(os.path.join(root_data_dir, blob_name), 'wb')

    b = block_blob_service.get_blob_to_bytes(container_name, container_path + blob_name)
    fp.write(b.content)
    # Or using `get_blob_to_stream`
    # block_blob_service.get_blob_to_stream(container_name, blob.name, fp)

    fp.flush()
    fp.close()


doc_vec_db_files = ['sqlite-doc-vectors/doc-vectors.db']
term_vec_db_files = ['sqlite-term-vectors/term-vectors.db']
doc_vec_sptag_files = ['sptag_doc_idx/deletes.bin', 'sptag_doc_idx/graph.bin', 'sptag_doc_idx/indexloader.ini', 'sptag_doc_idx/metadata.bin', 'sptag_doc_idx/metadataIndex.bin', 'sptag_doc_idx/tree.bin', 'sptag_doc_idx/vectors.bin']
term_vec_sptag_files = ['sptag_term_idx/deletes.bin', 'sptag_term_idx/graph.bin', 'sptag_term_idx/indexloader.ini', 'sptag_term_idx/metadata.bin', 'sptag_term_idx/metadataIndex.bin', 'sptag_term_idx/tree.bin', 'sptag_term_idx/vectors.bin']

resetDir(root_data_dir + 'sqlite-doc-vectors')

for file in doc_vec_db_files:
    downloadFile(file)

for file in term_vec_db_files:
    downloadFile(file)

for file in doc_vec_sptag_files:
    downloadFile(file)

for file in term_vec_sptag_files:
    downloadFile(file)
