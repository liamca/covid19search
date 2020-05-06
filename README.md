# Covid-19 Search App - Code Repository

## Overview

Source Code Repository for the Cognitive Search based [Covid-19 Search App](https://covid19search.azurewebsites.net/)

If you simply want to show this code in a running instance, feel free to use <https://covid19search.azurewebsites.net>.  Otherwise, you can follow the [setup instructions](#setup) below to recreate your own instance in your Azure subscription.  

This repository contains:

* AzureCognitiveSearchService: The components to set up the Cognitive Search service
* Concatenator: An Azure Function to reformat names which is invoked as a custom skill
* InvokeHealthEntityExtraction: An Azure Function to call the Text Analytics for Health container which is invoked as a custom skill


## Setup

First, you will need an Azure account.  If you don't already have one, you can start a free trial of Azure [here](https://azure.microsoft.com/free/).  

Secondly, create a new Azure search service using the Azure portal at <https://ms.portal.azure.com/#create/Microsoft.Search>.  Select your Azure subscription.  You may create a new resource group (you can name it something like "covid19-search-rg").  You will need a globally-unique URL as the name of your search service (try something like "covid19-search-" plus your name, organization, or numbers).  Finally, choose a nearby location to host your search service - please remember the location that you chose, as your Cognitive Services instance will need to be based in the same location.  Click "Review + create" to instantiate the service.  

Next, once your search service is deployed in Azure, we will setup the search index, indexers, and skillset.  

