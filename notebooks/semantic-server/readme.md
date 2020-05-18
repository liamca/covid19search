## Semantic Search - Term Embeddings (Optional)

This is an optional step for this search application, but has shown to be an effective way to help people more effectively find what they are looking for and to present a more representative set of relevant contenct (better recall).  This section leverages a method called FastText which will create a set of word embeddings which is a set of vectors that describe this word and makes it easy to find other words that are contextually similar, based on the text in the corpus.  There are many other techniques for creating word embeddings such as Glove and Bert.  In general, each technique generally provides mix of high accuracy at the cost of slow performance (or high CPU costs) and vice versa.  In my testing FastText provided a nice level of "quite good accuracy" while being "relatively fast". 

This section also includes some additional experimentation including the leveraging of the BM25 algorithm to provide more relevancy to words that are deemed to be interesting words (meaning words like "treatment" would be given more weighting than words like "was").  Document embedding are also created, but this is not yet used in the search app.

After the embeddings are created, they are stored into [SPTag](https://github.com/microsoft/SPTAG) which is a vector search library provided by Bing to quickly and efficiently provide a vector and find it's closes match.  Many people use [FAISS](https://github.com/facebookresearch/faiss), although I found SPTag to work well for the purpose of this application.

Please ensure that you have downloaded and installed [FastText](https://github.com/facebookresearch/fastText#requirements) onto this machine.

SQLite is also used to allow the search application to quickly look up the embedding for a search term entered by the user.

It is important that you leverage a Ubuntu based VM as FastText works better on this than Windows.

### Files

* globals.py: This is where you set the parameters that will be used by the subsequent notebooks. It is most important to ensure that you add the Azure Blob Storage credentials and service details. You may also need to change the paths used to suit your machine.

* 00-download-json-blobs-to-terms.ipynb: This first step takes all of the JSON files that contain the research journals and format it in a way that FastText will require.  This also uses lemmatization to map words to a similar root so that words like run, runner and running would be mapped to a single word "run".  We also only include nouns (NN), Verbs (VB) and adjectives (JJ).  This is done to help reduce noise words.

* 02-terms-to-avg-bm25-v2.ipynb: For each term, the releative importance of the term in the corpus is calculated and stored in a SQLite database.  

* 03-fasttext.ipynb: The actual processing of the terms to find the term embeddings is done in this step.

* 04-load-vectors-to-sptag.ipynb: The resulting embeddings are loaded into a SPTag index.

* 05-load-vectors-and-bm25-to-sqlite.ipynb: The terms and their associated embeddings are loaded into a SQLIte database.

* 06-terms-to-avg-vector.ipynb: Using the data calculated in the BM25 algorithm a document embedding is created to define the overall content in the document.

* 07-load-doc-vectors-to-sptag.ipynb:  The resulting embeddings for the document vectors are loaded into a SPTag index.

* 08-load-doc-vectors-to-sqlite.ipynb:  The document ID's and their associated embeddings are loaded into a SQLIte database.

* 09-upload-models-data-to-blob.ipynb: All of the SPTag and SQLite databases created in the previous 4 steps are uploaded to Azure Blob. 
