## Semantic Search - Term Embeddings (Optional)

This is an optional step for this search application, but has shown to be an effective way to help people more effectively find what they are looking for and to present a more representative set of relevant contenct (better recall).  This section leverages a method called FastText which will create a set of word embeddings which is a set of vectors that describe this word and makes it easy to find other words that are contextually similar, based on the text in the corpus.  There are many other techniques for creating word embeddings such as Glove and Bert.  In general, each technique generally provides mix of high accuracy at the cost of slow performance (or high CPU costs) and vice versa.  In my testing FastText provided a nice level of "quite good accuracy" while being "relatively fast". 

This section also includes some additional experimentation including the leveraging of the BM25 algorithm to provide more relevancy to words that are deemed to be interesting words (meaning words like "treatment" would be given more weighting than words like "was").  Document embedding are also created, but this is not yet used in the search app.

It is important that you leverage a Ubuntu based VM as FastText works better on this than Windows.

### Files

* 00-download-json-blobs-to-terms.ipynb: 

* 02-terms-to-avg-bm25-v2.ipynb: 

* 03-fasttext.ipynb: 

* 04-load-vectors-to-sptag.ipynb: 

* 05-load-vectors-and-bm25-to-sqlite.ipynb: 

* 06-terms-to-avg-vector.ipynb: 

* 07-load-doc-vectors-to-sptag.ipynb: 

* 08-load-doc-vectors-to-sqlite.ipynb: 

* 09-upload-models-data-to-blob.ipynb: 

