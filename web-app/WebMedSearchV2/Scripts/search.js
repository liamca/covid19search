// State of the Azure Search facets and filters will be stored here
var searchParameters = [];
// This will contain the current search results passed from the controller
var searchResults = [];
// This will contain the facet filters and those facets selected
var facetTypes = { facets: [], selected: [] };

// Intialize the current state of the search parameters
searchParameters["search"] = "";
searchParameters["skip"] = "0";
searchParameters["take"] = "20";
searchParameters["select"] = ['docID', 'pubDate', 'abstractContent', 'title', 'journal', 'contributors', 'bodyStructure', 'conditionQualifier', 'diagnosis',
    'direction', 'examinationName', 'examinationRelation', 'familyRelation',
    'gender', 'gene', 'medicationClass', 'medicationName',
    'routeOrMode', 'symptomOrSign', 'treatmentName', 'variant'
    ];
searchParameters["highlights"] = ['abstractContent', 'body'];
searchParameters["facets"] = ['journal,count:10', 'contributors,count:10', 'pubDate', 'bodyStructure,count:10', 'conditionQualifier,count:10', 'diagnosis,count:10',
    'direction,count:10', 'examinationName,count:10', 'examinationRelation,count:10', 'familyRelation,count:10',
    'gender,count:10', 'gene,count:10', 'medicationClass,count:10', 'medicationName,count:10',
    'routeOrMode,count:10', 'symptomOrSign,count:10', 'treatmentName,count:10', 'variant,count:10'];
searchParameters["filters"] = [];
searchParameters["startPubDate"] = "";
searchParameters["endPubDate"] = "";

