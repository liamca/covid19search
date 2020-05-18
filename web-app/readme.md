### Covid-19 Search Application

This is an MVC based application the provided the code needed to create the Web based UI for the Covid Search application.  All that you should need to do is update the web.config to point to your Azure Cognitive Search service.

<code>
add key="SearchServiceName" value="[Enter Search Service - do not included .search.windows.net"
add key="SearchServiceApiKey" value="[Search Service Query API Key"
add key="SearchServiceIndexName" value="[Search Index Name]"
</code>

If you also created the Semantic Search Server, you will need to update the "SemanticServer" 

<code>
    add key="SemanticServer" value="http://[IP Address of Semantic Server Container]"
</code>

If you wish to enable the document summarization when you click on a document, please reach out to Agolo (sales@agolo.com) and enter the associated server and API Key.

<code>
    add key="AgoloServer" value="https://api.agolo.com/nlp/v0.2/summarize"
    add key="AgoloAPIKey" value="[Send Email to sales@agolo.com to get Key]"
</code>


