## Semantic Search Server (Optional)

This section provides an example of a Flask based web application hosted in a Docker Container that receives a set of terms (search query) and returns back the terms that are most contextually similar.  This application assumes you have created the necessary SPTag and SQLite indexes from [this step](https://github.com/liamca/covid19search/tree/master/notebooks/semantic-server).

This is an optional step for this search application, but has shown to be an effective way to help people more effectively find what they are looking for and to present a more representative set of relevant contenct (better recall). 

### Requirements

* Docker Desktop
* Azure Container Registry with associcated password


### Download SPTag and SQLite indexes

In [this step](https://github.com/liamca/covid19search/tree/master/notebooks/semantic-server) you would have created a set of term and doument embedding and stored them in a set of SPTag and SQLite indexes and uploaded them to Azure Blob Storage.  We will need to download these and place them in the /data directory.  download_latest_model_data_from_blob.py provides some code on how to do this, however, you will need to enter your Azure Blob container details and credentials.

### Building the Container

The (Linux) container can be built using the command: docker build -t vector-search-flask-sptag-covid19:latest .

### Tag the Image

We will tag the image as "vector-search-flask-sptag-covid19:latest" with the command: docker tag vector-search-flask-sptag-covid19:latest [Azure Container Registry].azurecr.io/containers/vector-search-flask-sptag-covid19

### Upload Images to Azure Container Registry 

Before you do this, you will need to connect to your Azure Container Registry.  For more details on how to do this, [visit](https://docs.microsoft.com/en-us/azure/container-registry/container-registry-get-started-docker-cli).

Upload the image using the command: docker push [Azure Container Registry Name].azurecr.io/containers/vector-search-flask-sptag-covid19

### Create the Azure Container Instance

Once the container image has been uploaded, we can create the container instance using the following command:

az container create -g [Resource Group] --name vector-search-flask-sptag-covid19 --image [Azure Container Registry].azurecr.io/containers/vector-search-flask-sptag-covid19 --ip-address public --cpu 2 --memory 16 --registry-username [Registry UserName] --registry-password [Registry Password]
