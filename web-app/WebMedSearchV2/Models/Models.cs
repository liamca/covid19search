using System;
using System.Collections.Generic;
using System.Linq;
using System.Web;

namespace WebMedSearchV2.Models
{
    public class Project
    {
        public string Name { get; set; }
        public List<Task> Tasks { get; set; }
    }

    public class Task
    {
        public string Name { get; set; }
        public DateTime DueDate { get; set; }
    }

    public class QueryParameters
    {
        public string search { get; set; }
        public int skip { get; set; }
        public int take { get; set; }
        public string[] select { get; set; }
        public string[] facets { get; set; }
        public string[] filters { get; set; }
        public string[] highlights { get; set; }
        public string startPubDate { get; set; }
        public string endPubDate { get; set; }
    }
}