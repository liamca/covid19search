function fullSearch(q)
{
	// Basically refresh page with new search
	if (q == "")
		q = "*";
	execSearch(q);
	execMultiSelectFacetQuery(q, "city", "cityDiv", "string");
	execMultiSelectFacetQuery(q, "tags", "tagsDiv", "collection");
}

function execSuggest(q, resolve)
{
	// Execute an autocomplete search to populate type ahead
	var searchAPI = baseSearchURL + "/docs/autocomplete?api-version=2019-05-06-Preview&suggesterName=sg&autocompleteMode=twoTerms&search=" + q;
	$.ajax({
		url: searchAPI,
		beforeSend: function (request) {
			request.setRequestHeader("api-key", azureSearchQueryApiKey);
			request.setRequestHeader("Content-Type", "application/json");
			request.setRequestHeader("Accept", "application/json; odata.metadata=none");
		},
		type: "GET",
		success: function (data) {
			availableTags = [];
			for (var item in data.value)
				availableTags.push(data.value[item].queryPlusText);
			resolve(availableTags);

		}
	});
}


function execTypeAhead(q) {
	var searchAPI = "typeahead";
	post_json = "{\"query\": \"" + q + "\"}"
	return new Promise((resolve, reject) => {
		$.ajax({
			url: searchAPI,
			data: post_json,
			dataType: 'json',
			beforeSend: function (request) {
				request.setRequestHeader("Content-Type", "application/json");
			},
			type: "POST",
			success: function(data) {
				//availableTags = eval('(' + data + ')');
				// items = JSON.parse(data)	
				// for (var item in items)
					// availableTags.push(items[item]);
				resolve(data);
			},
			error: function(error) {
				reject(error)
			},
		})
	})

}



function execFindSimilarTerms(q) {
	var searchAPI = "termVectorSearch";
	return new Promise((resolve, reject) => {
		$.ajax({
			url: searchAPI,
			data: JSON.stringify({'terms': q}),
			dataType: 'json',
			beforeSend: function (request) {
				request.setRequestHeader("Content-Type", "application/json");
			},
			type: "POST",
			success: function(data) {
				json_data = eval(data)
				availableTags = json_data[1];
				
				// Add the resulting documents to the search results
				doccounter = 0
				for (docid in json_data[3])
				{
					downloadDoc(json_data[3][docid], "searchResultsDiv" + doccounter)
					doccounter += 1
				}

				resolve(availableTags);
			},
			error: function(error) {
				reject(error)
			},
		})
	})
}

function downloadDoc(docid, div)
{
	var searchAPI = "getdoc";

	$.ajax({
			url: searchAPI,
			data: JSON.stringify({'docid': docid}),
			dataType: 'text',
			beforeSend: function (request) {
				request.setRequestHeader("Content-Type", "application/json");
			},
			type: "POST",
			success: function(data) {
				viewDocHTML = '<a href="javascript:void(0)" onclick="openDoc(\'' + docid + '\');">[View Document]</a>&nbsp;&nbsp;&nbsp;'
				findSimilarHTML = '<a href="javascript:void(0)" onclick="findSimilarDocs(\'' + docid + '\');">[Find Similar]</a>'
				
				$('#' + div).html(data + '<br>' + viewDocHTML + findSimilarHTML)
			},
			error: function(error) {
				console.log(error)
			}
		})
}

function findSimilarDocs(docid)
{
	// Find all the semantically similar docs to this onerror
	console.log(docid)
	var searchAPI = "docVectorSearch";
	$.ajax({
		url: searchAPI,
		data: JSON.stringify({'docid': docid}),
		dataType: 'json',
		beforeSend: function (request) {
			request.setRequestHeader("Content-Type", "application/json");
		},
		type: "POST",
		success: function(data) {
			json_data = eval(data)
			// Add the resulting documents to the search results
			doccounter = 0
			for (docid in json_data[1])
			{
				downloadDoc(json_data[1][docid], "searchResultsDiv" + doccounter)
				doccounter += 1
			}

		},
		error: function(error) {
			console.log(error)
		},
	})
}

function openDoc(docid)
{
	// Find all the semantically similar docs to this onerror
	console.log(docid)
	openInNewTab('document/' + docid)
}


function openInNewTab(url) {
  var win = window.open(url, '_blank');
  win.focus();
}

