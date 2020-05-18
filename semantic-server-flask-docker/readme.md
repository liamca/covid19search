## Semantic Search Server (Optional)

This section provides an example of a Flask based web application hosted in a Docker Container that receives a set of terms (search query) and returns back the terms that are most contextually similar.  This application assumes you have created the necessary SPTag and SQLite indexes from [this step](https://github.com/liamca/covid19search/tree/master/notebooks/semantic-server).

This is an optional step for this search application, but has shown to be an effective way to help people more effectively find what they are looking for and to present a more representative set of relevant contenct (better recall). 

### Download SPTag and SQLite indexes

In [this step](https://github.com/liamca/covid19search/tree/master/notebooks/semantic-server) you would have created a set of term and doument embedding and stored them in a set of SPTag and SQLite indexes and uploaded them to Azure Blob Storage.  We will need to download these and place them in the /data directory.  download_latest_model_data_from_blob.py provides some code on how to do this, however, you will need to enter your Azure Blob container details and credentials.

