import SPTAG
import numpy as np

import json
import requests
from pprint import pprint


# SPTag Config
k = 10
sptag_index_file = 'pubmed'

#Azure Search Config
endpoint = 'https://liamca-ignite.search.windows.net/'
api_version = '?api-version=2019-05-06'
headers = {'Content-Type': 'application/json',
        'api-key': '056FD94507554D1FB97DADE9E11D6503' }
indexName = 'pubmed-term-vectors'

j = SPTAG.AnnIndex.Load(sptag_index_file)
j.SetSearchParam("MaxCheck", '1024')


def findTermVector(term):
    # Get the vector based on a term
    vec = []
    url = endpoint + "indexes/" + indexName + "/docs" + api_version + "&$select=vector&$filter=term eq '" + term + "'"
    response  = requests.get(url, headers=headers)
    index = response.json()
    for t in index["value"]:
        #vec = np.asarray(eval('[' + t["vector"] + ']'), dtype=np.float32)
        vec = eval(t["vector"].replace("'", ""))

    return vec

def findAvgVectorOfTerms(terms):
    query_vectors = []
    for t in terms:
        query_vectors.append(findTermVector(t))

    avg_query_vector = np.average(query_vectors, axis=0)
    return np.asarray(avg_query_vector, dtype=np.float32)


terms = ['liver', 'cancer']
result = j.SearchWithMetaData(findAvgVectorOfTerms(terms), k)
print (result[0]) # ids
print (result[1]) # distances
print (json.dumps(str(result[2]).replace("b'", "'"))) # metadata
