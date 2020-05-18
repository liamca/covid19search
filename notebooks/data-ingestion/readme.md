## Alternative Method for Data Ingestion - PUSH API

The main page of this repository explain how to leverage the Azure Search Indexer, which is a mechanism to pull data from an Azure based data source (in this case Azure Blob Storage).  The great part of using the Azure Search Indexer is that you can configure the entire orchestration of data ingestion as well as the execution of "skills" such as TA for Health medical entity extraction which is used here.  
In many cases the Indexer is not viable and a mechanism to allow data to be programatically pushed directly into the index is more appropriate.  Some examples of this include when data sources are not supported by the Azure Cognitive Search idnexer or perhaps on-premise data sources that the Indexer can not access.  

This section of the repository includes a set of notebooks that show how to programatically extract the content from the data source, enrich it and then push it into the data source.  

This set of notebooks was run on a Ubuntu based Azure Data Science VM.

### Notebook Details

* globals.py: This is where you set the parameters that will be used by the subsequent notebooks.  It is most important to ensure that you add the Azure Cognitive Search as well as the Azure Blob Storage credentials and service details.  It is important that you have created a Text Analytics for Health container and updated the details of where this can be called.  You can test this with the test-ta-health-container.ipynb.  You may also need to change the paths used to suit your machine.  

* 01-Download latest publications.ipynb: This notebook downloads and extracts the .tar.gz JSON files that contain the research journal information as well as a metadata.csv file that contains additional details about the journals such as contributor names.

* 02-Create-Search-Index.ipynb: This notebook will create a new search index with a defined schema to be used for this search application.

* 03-Upload-JSON-to-Azure-Search.ipynb: This will upload the content stored in the extracted JSON files into Azure Cognitive Search.  This is done in batches to make ingestion more efficient.

* 04-Apply-Metadata.ipynb: This will merge the contributor and journal information in the metadata.csv into the search index created in the previous step.

* 05-download-umls-concepts.ipynb: The TA for Health container that will be used in the next step will identify UMLS Concept ID's, but it does not provide the textual representation of these concept ID's.  This will create a dictionary that maps these ID's to the associated textual name so that we can store in Azure Cognitive Search the names which will then be used as facets and filters in the search app.

* 06-Upload-Concepts-to-Azure-Search.ipynb:  This will go through the Azure Cog Search index and and pass the title as well as up to 5000 characters of the abstract (or body if there is no abstract) to the TA for Health container to get the associated medical entities.  These medical entities are then added to the document in the index.   
