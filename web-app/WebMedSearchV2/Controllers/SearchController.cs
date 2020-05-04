using Microsoft.Azure.Search;
using Microsoft.Azure.Search.Models;
using System;
using System.Collections.Generic;
using System.Configuration;
using System.Web.Mvc;
using System.Web.Http;
using WebMedSearchV2.Models;
using System.Text;
using Newtonsoft.Json.Linq;
using System.Net.Http;

using FacetResults = System.Collections.Generic.IDictionary<string, System.Collections.Generic.IList<Microsoft.Azure.Search.Models.FacetResult>>;
using DocumentSearchResult = Microsoft.Azure.Search.Models.DocumentSearchResult<Microsoft.Azure.Search.Models.Document>;
using Newtonsoft.Json;
using System.Linq;
using System.Net;

namespace WebMedSearchV2.Controllers
{
    public class SearchController : Controller
    {
        private static Uri _serviceUri = new Uri("https://" + ConfigurationManager.AppSettings["SearchServiceName"] + ".search.windows.net");
        private static HttpClient _httpClientSearchServer = new HttpClient();
        private static HttpClient _httpClientSemanticServer = new HttpClient();
        private static HttpClient _httpClientAgolo = new HttpClient();

        private static string searchServiceName = ConfigurationManager.AppSettings["SearchServiceName"];
        private static string apiKey = ConfigurationManager.AppSettings["SearchServiceApiKey"];
        private static string indexName = ConfigurationManager.AppSettings["SearchServiceIndexName"];
        private static SearchServiceClient searchClient =
            new SearchServiceClient(searchServiceName, new SearchCredentials(apiKey));

        private static string searchServiceUrl = ConfigurationManager.AppSettings["SearchServiceName"];

        private static string semanticServer = ConfigurationManager.AppSettings["SemanticServer"];
        private static string vectorSearchUrl = semanticServer + "/termVectorSearch";

        private static string agoloServer = ConfigurationManager.AppSettings["AgoloServer"];
        private static string agoloApiKey = ConfigurationManager.AppSettings["AgoloAPIKey"];


        // POST: Search
        [System.Web.Http.HttpPost]
        public ActionResult Docs([FromBody]QueryParameters queryParameters)
        {
            // Perform Azure Search search
            try
            {
                var searchQuery = "";
                if (queryParameters.search == null)
                    searchQuery = "*";
                else
                {
                    JArray terms = JArray.Parse(queryParameters.search);
                    foreach (var term in terms)
                    {
                        searchQuery += term["value"].ToString() + " ";
                    }
                }
                SearchParameters sp = new SearchParameters()
                {
                    HighlightFields = queryParameters.highlights,
                    HighlightPreTag = "<b><em>",
                    HighlightPostTag = "</em></b>",
                    SearchMode = SearchMode.Any,
                    Top = queryParameters.take,
                    Skip = queryParameters.skip,
                    // Limit results
                    Select = queryParameters.select,
                    // Add count
                    IncludeTotalResultCount = true,
                    // Add facets
                    Facets = queryParameters.facets,
                    QueryType = QueryType.Full,
                    ScoringProfile = "date_boost"
                };

                if (queryParameters.filters != null)
                {
                    string filter = String.Join(" and ", queryParameters.filters);
                    sp.Filter = filter;
                }

                if (queryParameters.startPubDate != null)
                {
                    if (sp.Filter != null)
                        sp.Filter += " and ";
                    var dtDateTime = DateTimeOffset.Parse(queryParameters.startPubDate);
                    sp.Filter += " pubDate ge " + dtDateTime.ToString("yyyy-MM-dd") + "T00:00:00Z";
                }

                if (queryParameters.endPubDate != null)
                {
                    if (sp.Filter != null)
                        sp.Filter += " and ";
                    var dtDateTime = DateTimeOffset.Parse(queryParameters.endPubDate);
                    sp.Filter += " pubDate le " + dtDateTime.ToString("yyyy-MM-dd") + "T23:59:59Z";
                }

                // log the actions


                return Json(searchClient.Indexes.GetClient(indexName).Documents.Search(searchQuery, sp),
                    JsonRequestBehavior.AllowGet);
            }
            catch (Exception ex)
            {
                Console.WriteLine("Error querying index: {0}\r\n", ex.Message.ToString());
            }
            return null;
        }

        // POST: MoreLikeThis
        [System.Web.Http.HttpPost]
        public JObject MoreLikeThis([FromBody]QueryParameters queryParameters, string docid)
        {
            // Perform Azure Search search more like this
            var jsonContent = new JObject();
            try
            {
                var selectFieldsAsList = string.Join(",", queryParameters.select.ToArray());
                //string.Join(", ", queryParameters.select.Select(i => i.Value));

                //var selectFieldsAsList = queryParameters.select.ToString().Split(',');
                var jsonPostStr = "{'moreLikeThis': '" + docid + "', 'top': " + queryParameters.take + ", 'count': true, 'select': '" + selectFieldsAsList + "'}  ";

                var jsonObject = JObject.Parse(jsonPostStr);

                var content = new StringContent(jsonObject.ToString(), Encoding.UTF8, "application/json");
                //_httpClientSearchServer.DefaultRequestHeaders.Add("api-key", apiKey);

                var httpRequestMessage = new HttpRequestMessage
                {   
                    Method = HttpMethod.Post,
                    RequestUri = new Uri("https://" + searchServiceUrl + ".search.windows.net/indexes/" + indexName + "/docs/search?api-version=2019-05-06-Preview"),
                    Headers = {
                        { HttpRequestHeader.Accept.ToString(), "application/json" },
                        { HttpRequestHeader.ContentType.ToString(), "application/json" },
                        { "api-key", apiKey }

                    },
                    Content = content
                };

                var result = _httpClientSemanticServer.SendAsync(httpRequestMessage).Result;

                //var resultOld = _httpClientSemanticServer.PostAsync("https://" + searchServiceUrl + ".search.windows.net/indexes/" + indexName + "/docs/search", content).Result;
                if (result.StatusCode.ToString() == "OK")
                {
                    // Pretty sure there is a better way to parse this...
                    jsonContent = JObject.Parse(result.Content.ReadAsStringAsync().Result);
                }
            }
            catch (Exception ex)
            {
                // Todo - do better logging
                Console.WriteLine(ex.Message);
            }

            return jsonContent;


        }

        [System.Web.Http.HttpPost]
        public ActionResult Doc(string docID)
        {
            // Perform Azure Search doc lookup
            try
            {
                return Json(searchClient.Indexes.GetClient(indexName).Documents.Get(docID),
                    JsonRequestBehavior.AllowGet);
                
            }
            catch (Exception ex)
            {
                Console.WriteLine("Error querying index: {0}\r\n", ex.Message.ToString());
            }
            return null;
        }

        [System.Web.Http.HttpPost]
        public JObject GetContentSummary(string query, string title, string body)
        {
            // Call agolo to get a summary
            var agoloSummary = new JObject();

            try
            {
                var termsAsList = query.ToString().Replace("\"", "").Trim().Replace(" ", ", ").Replace("%20", ", ");

                var jsonPost = JObject.Parse("{'coref': 'false','summary_length': '5','query_text': '" + termsAsList + "', 'use_query_sentence_scorer': 'true', 'use_consistent_query_token_weights': 'true', 'use_special_query_weights': 'true'} ");

                var articleJsonArray = new JArray();
                articleJsonArray.Add(new JObject(new JProperty("type", "article")));
                articleJsonArray.Add(new JObject(new JProperty("title", title)));
                articleJsonArray.Add(new JObject(new JProperty("text", body)));

                jsonPost.Add(new JProperty("articles", articleJsonArray));




                //var jsonPostStr = "{'coref': 'false','summary_length': '5','query_text': '" + termsAsList + "', 'use_query_sentence_scorer': 'true', 'use_consistent_query_token_weights': 'true', 'use_special_query_weights': 'true', 'articles': [{";


                //jsonPostStr += "'type': 'article',";
                //jsonPostStr += "'title': '" + title + "',";
                //jsonPostStr += "'text': '" + body + "'}]}";

                //var jsonObject = JObject.Parse(jsonPostStr);

                var content = new StringContent(jsonPost.ToString(), Encoding.UTF8, "application/json");

                _httpClientAgolo.DefaultRequestHeaders.TryAddWithoutValidation("Ocp-Apim-Subscription-Key", agoloApiKey);

                var result = _httpClientAgolo.PostAsync(agoloServer, content).Result;
                if (result.StatusCode.ToString() == "OK")
                {
                    // Pretty sure there is a better way to parse this...
                    agoloSummary = JObject.Parse(result.Content.ReadAsStringAsync().Result);

                   
                    //foreach (var summary in agoloSummary["summary"])
                    //{
                    //    foreach (var sentence in summary["sentences"])
                    //    {

                    //    }

                    //}
                    ////["summary"][0]["sentences"][0]

                    //var jsonContent = Newtonsoft.Json.JsonConvert.DeserializeObject(result.Content.ReadAsStringAsync().Result);
                    //var jsonArray = JArray.Parse(jsonContent.ToString().Replace("\\x", ""));
                }
            }
            catch (Exception ex)
            {
                // Todo - do better logging
                Console.WriteLine(ex.Message);
            }

            return agoloSummary;
        }


        [System.Web.Http.HttpPost]
        public ActionResult GetSemanticTerms([FromBody]QueryParameters queryParameters)
        {
            var semanticTerms = new Dictionary<string, double>();
            try
            {
                var termList = new List<string>();
                var jsonPostStr = "{'terms': [ ";
                if (queryParameters.search != null)
                { 
                    JArray terms = JArray.Parse(queryParameters.search);
                    foreach (var term in terms)
                    {
                        jsonPostStr += "'" + term["value"].ToString().Trim().ToLower() + "',";
                        termList.Add(term["value"].ToString().Trim().ToLower());
                    }
                }

                jsonPostStr += "]}";

                var jsonObject = JObject.Parse(jsonPostStr);

                var content = new StringContent(jsonObject.ToString(), Encoding.UTF8, "application/json");
                var result = _httpClientSemanticServer.PostAsync(vectorSearchUrl, content).Result;
                if (result.StatusCode.ToString() == "OK")
                {
                    // Pretty sure there is a better way to parse this...
                    var jsonContent = Newtonsoft.Json.JsonConvert.DeserializeObject(result.Content.ReadAsStringAsync().Result);
                    var jsonArray = JArray.Parse(jsonContent.ToString().Replace("\\x", "").Replace("b\"", "\""));
                    int counter = 0;
                    foreach (var similarTerm in jsonArray[1])
                    {
                        if (termList.Exists(x => x == similarTerm.ToString()) == false)
                        {
                            semanticTerms[similarTerm.ToString()] = Convert.ToDouble(jsonArray[0][counter]);
                            counter += 1;
                        }
                    }
                }
            }
            catch (Exception ex)
            {
                // Todo - do better logging
                Console.WriteLine(ex.Message);
            }

            return Json(semanticTerms,
                    JsonRequestBehavior.AllowGet);
        }

        public ActionResult AutoComplete(string term)
        {
            // Perform autocomplete

            AutocompleteParameters ap = new AutocompleteParameters()
            {
                UseFuzzyMatching = true,
                Top = 7,
                AutocompleteMode = AutocompleteMode.OneTerm            };
            try
            {
                var response = searchClient.Indexes.GetClient(indexName).Documents.Autocomplete(term, "sg", ap);
                List<string> suggestions = new List<string>();
                foreach (var result in response.Results)
                {
                    suggestions.Add(result.QueryPlusText.ToString());
                }

                return new JsonResult
                {
                    JsonRequestBehavior = JsonRequestBehavior.AllowGet,
                    Data = suggestions
                };
            }
            catch (Exception)
            {
                return null;
            }

        }

        public JObject GetFDNodes(string code, string q, string nodeType)
        {
            // Calculate nodes for 3 levels

            JObject dataset = new JObject();
            int CurrentNodes = 0;

            var FDEdgeList = new List<FDGraphEdges>();
            // Create a node map that will map a facet to a node - nodemap[0] always equals the q term
            var NodeMap = new Dictionary<string, int>();
            NodeMap[q] = CurrentNodes;

            // If blank search, assume they want to search everything
            if (string.IsNullOrWhiteSpace(q))
                q = "*";

            var origTerm = string.Empty;

            var NextLevelTerms = new List<string>();

            // Apply the first level nodes
            int node = CurrentNodes;
            NodeMap[q] = node;

            // Do a query to get the 2nd level nodes
            var response = GetFacets(q, nodeType, 15);
            if (response != null)
            {
                var facetVals = ((FacetResults)response.Facets)[nodeType];
                foreach (var facet in facetVals)
                {
                    node = -1;
                    if (NodeMap.TryGetValue(facet.Value.ToString(), out node) == false)
                    {
                        // This is a new node
                        CurrentNodes++;
                        node = CurrentNodes;
                        NodeMap[facet.Value.ToString()] = node;
                    }
                    // Add this facet to the fd list
                    if (NodeMap[q] != NodeMap[facet.Value.ToString()])
                    {
                        FDEdgeList.Add(new FDGraphEdges { source = NodeMap[q], target = NodeMap[facet.Value.ToString()] });
                        NextLevelTerms.Add(facet.Value.ToString());
                    }
                }
            }

            // Get the 3rd level nodes by going through all the NextLevelTerms
            foreach (var term in NextLevelTerms)
            {
                response = GetFacets(q + " \"" + term + "\"", nodeType, 3);
                if (response != null)
                {
                    var facetVals = ((FacetResults)response.Facets)[nodeType];
                    foreach (var facet in facetVals)
                    {
                        node = -1;
                        if (NodeMap.TryGetValue(facet.Value.ToString(), out node) == false)
                        {
                            // This is a new node
                            CurrentNodes++;
                            node = CurrentNodes;
                            NodeMap[facet.Value.ToString()] = node;
                        }
                        // Add this facet to the fd list
                        if (NodeMap[term] != NodeMap[facet.Value.ToString()])
                        {
                            FDEdgeList.Add(new FDGraphEdges { source = NodeMap[term], target = NodeMap[facet.Value.ToString()] });
                        }
                    }
                }

            }

            JArray nodes = new JArray();
            foreach (var entry in NodeMap)
            {
                nodes.Add(JObject.Parse("{name: \"" + entry.Key.Replace("\"", "") + "\"}"));
            }

            JArray edges = new JArray();
            foreach (var entry in FDEdgeList)
            {
                edges.Add(JObject.Parse("{source: " + entry.source + ", target: " + entry.target + "}"));
            }


            dataset.Add(new JProperty("edges", edges));
            dataset.Add(new JProperty("nodes", nodes));

            // Create the fd data object to return

            return dataset;
        }

        public DocumentSearchResult GetFacets(string searchText, string nodeType, int maxCount = 30)
        {
            // Execute search based on query string
            try
            {
                SearchParameters sp = new SearchParameters()
                {
                    SearchMode = SearchMode.All,
                    Top = 0,
                    Select = new List<String>() { "docID" },
                    Facets = new List<String>() { nodeType + ", count:" + maxCount },
                    QueryType = QueryType.Full
                };

                return searchClient.Indexes.GetClient(indexName).Documents.Search(searchText, sp);
            }
            catch (Exception ex)
            {
                Console.WriteLine("Error querying index: {0}\r\n", ex.Message.ToString());
            }
            return null;
        }


        public class FDGraphEdges
        {
            public int source { get; set; }
            public int target { get; set; }

        }

        public class AutoCompleteItem
        {
            public string id { get; set; }
            public string desc { get; set; }
        }

    }
}