var availableTags = [];
var azureSearchQueryApiKey = "5EBDBE409B9C5D7A4C80A34C48E591FA";	// this is a query key for demo purposes
var baseSearchURL = "https://liamca-ignite.search.windows.net/indexes/pubmed-term-vectors";

var pubmedSearchQueryApiKey = "EEE37AC65E8F11707D01BA2E7F6C43BF";	
var pubmedSearchURL = "https://azs-docsearch-s3.search.windows.net/indexes/semanticscholar";

var facetFiltersString = [];
var facetFiltersCollection = [];
var currentPage = 1;
var documentsToRetrieve = 15;	// This is the maximum documents to retrieve / page
