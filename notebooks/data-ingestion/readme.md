## Alternative Method for Data Ingestion - PUSH API

The main page of this repository explain how to leverage the Azure Search Indexer, which is a mechanism to pull data from an Azure based data source (in this case Azure Blob Storage).  The great part of using the Azure Search Indexer is that you can configure the entire orchestration of data ingestion as well as the execution of "skills" such as TA for Health medical entity extraction which is used here.  

In many cases the Indexer is not viable and a mechanism to allow data to be programatically pushed directly into the index is more appropriate.  Some examples of this include when data sources are not supported by the Azure Cognitive Search idnexer or perhaps on-premise data sources that the Indexer can not access.  

This section of the repository includes a set of notebooks that show how to programatically extract the content from the data source, enrich it and then push it into the data source.

