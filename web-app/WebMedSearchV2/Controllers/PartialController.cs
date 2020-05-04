using System;
using System.Collections.Generic;
using System.Linq;
using System.Web;
using System.Web.Mvc;

namespace WebMedSearchV2.Controllers
{
    public class PartialController : Controller
    {
        public ActionResult SearchBox()
        {
            return View();
        }

        public ActionResult SearchResults()
        {
            return View();
        }


        public ActionResult CheckBoxFacet()
        {
            return View();
        }

        public ActionResult MultiLevelFacet()
        {
            return View();
        }

    }
}