# Scripts on this file are dedicated to defining the
# MainSiteHTML and OutputSiteHTML objects.

# Such objects are simply placeholders for site-specific
# HTML tags and their related properties.

# Inconsistent HTML tagging across Amnesty sections made it
# necessary to find a workaround for scrapping different
# sites with different tags without repeating any code.

# The idea is to pre-define a site's Main Site HTML tagging and
# Output Site HTML tagging and have the web scrapping functions
# take such pre-configurations as arguments.  

class MainSiteHTML :
    """This class is intended to hold site-specific 
    HTML tags and attributes.
    
    output_tag (str) : Tag of main entries in an amnesty site.
    output_attrs (dict of strings): HTML properties identifying the tag.
    
    ----
    
    e.g. : AmnInternational = Site("article", {"class": "post post--result"})
    
    """
    
    def __init__(self, url_head, site_source_name, 
                 arrangement,
                 output_tag, output_attrs, 
                 link_in_out_tag,
                 link_tag, link_attrs,
                 link_prefix,
                 date_tag, date_attrs,
                 title_tag, title_attrs,
                 excerpt_tag, excerpt_attrs,
                 sele):
        # Is the search-tool arranged by pages or is it 
        # an infinite scroll. Options: "pages", "scroll".
        self.arrangement = arrangement
        
        # If arrangement is in pages, this should be the
        # Amnesty search-tool link without the page number.
        # Page numbers will be iteratively appended to this string
        # to loop through all pages.
        # If arrangement is an infinite scroll, this should be the
        # search-tool link.
        self.url_head = url_head
        
        # String identifying this site.
        self.site_source_name = site_source_name

        # String with HTML tag that identifies each 
        # output in the search-tool site.
        self.output_tag = output_tag
        # Dictionary identifying HTML attributes of
        # each output in the search-tool site.
        self.output_attrs = output_attrs
        # Same for output link
        self.link_in_out_tag = link_in_out_tag
        self.link_tag = link_tag
        self.link_attrs = link_attrs
        # Same for date
        self.date_tag = date_tag
        self.date_attrs = date_attrs
        # Same for title
        self.title_tag = title_tag
        self.title_attrs = title_attrs
        self.excerpt_tag = excerpt_tag
        self.excerpt_attrs = excerpt_attrs

        # Some sites have incomplete URLs. For example,
        # "/some-output" leading to "https://www.amnesty.x/some-output",
        # where x is a country code. The link_prefix is precisely this 
        # omitted first part of the url string.
        self.link_prefix = link_prefix

        # Some sites (e.g. Amnesty France) contain JS code that 
        # redirects requests from url x to some predetermined site y,
        # thus making it impossible to access the desired URLs using 
        # the requests library. The workaround is to access the URL 
        # via a headless Selenium connection. 
        # Set sele to True for these cases.
        self.sele = sele
        
class OutputSiteHTML : 
    def __init__(self, topics_tag, topics_attrs,
                 pdf_tag, pdf_attrs,
                 date_tag, date_attrs):
        self.topics_tag = topics_tag
        self.topics_attrs = topics_attrs
        self.pdf_tag = pdf_tag
        self.pdf_attrs = pdf_attrs
        self.date_tag = date_tag
        self.date_attrs = date_attrs

# ~ Helpers ~
# ----------

# -----------------------------------------------------------------------------
# AI Main Site (English) ~ https://amnesty.org/ ~ 
# -----------------------------------------------------------------------------

MainAI = MainSiteHTML(
            url_head="https://www.amnesty.org/en/search/page/", 
            site_source_name="AI", 
            arrangement = "pages",
            output_tag="article", 
            output_attrs={"class": "post post--result"},
            link_in_out_tag=False,
            link_tag = "a", link_attrs={"class": "floating-anchor"},
            link_prefix="",
            date_tag = "span", date_attrs={},
            title_tag="h1", title_attrs={"class": "post-title"},
            excerpt_tag="div", excerpt_attrs={"class" : "post-excerpt"},
            sele=False
        )
OutputAI = OutputSiteHTML(topics_attrs={"class": "topics-container"}, 
                          topics_tag="div",
                          pdf_tag="a", 
                          pdf_attrs={"class": "btn btn--download btn--primary customSelect-input"},
                          date_tag=False, date_attrs={}
                    )


# -----------------------------------------------------------------------------
# AI Canada (English) ~ https://amnesty.ca/ ~ Main Site Tagging  
# -----------------------------------------------------------------------------

MainCanadaEnglish = MainSiteHTML(url_head = "https://www.amnesty.ca/search/a/page/", 
                                 site_source_name="Amnesty Canada (English)", 
                                 arrangement="pages", 
                                 output_tag="article", 
                                 output_attrs={"class": "post post--result"},
                                 link_in_out_tag=False,
                                 link_tag = "a", link_attrs={"class": "floating-anchor"},
                                 link_prefix="",
                                 date_tag = "span", date_attrs={},
                                 title_tag="h1", title_attrs={"class": "post-title"},
                                 excerpt_tag="div", excerpt_attrs={"class" : "post-excerpt"},
                                 sele=False
                                 )

OutputCanadaEnglish = OutputSiteHTML(topics_attrs={"class": "topics-container"}, 
                          topics_tag="div",
                          pdf_tag="a", 
                          pdf_attrs={"class": "btn btn--download btn--dark"},
                                    date_tag=False, date_attrs={})


# -----------------------------------------------------------------------------
# AI UK 
# -----------------------------------------------------------------------------

# Search tool of this site divides entries by articles, blogs, resources, etc.
# Each of this divisions entail a different url head. 
# For articles use :
# ~
# https://www.amnesty.org.uk/search/%20a?type=article&sort_by=search_api_relevance&page=
# ~
# For resources use :
# ~ 
# https://www.amnesty.org.uk/search/%20%20a?type=resource&sort_by=search_api_relevance&page=
# ~

MainUKEnglish = MainSiteHTML(url_head = None, #URL varies, see website...
                             site_source_name= "UK (English)",
                             arrangement="pages",
                             output_tag = "div", output_attrs= {"class": "views-row"},
                             link_in_out_tag=False,
                             link_tag = "a", link_attrs={},
                             link_prefix="https://www.amnesty.org.uk",
                             date_tag=False, date_attrs={},
                             title_tag = "a", title_attrs={},
                             excerpt_tag=False, excerpt_attrs={},
                             sele=False
                             )

OutputUKEnglish = OutputSiteHTML(topics_tag="ul", topics_attrs={"class": "tags clearfix"},
                          pdf_tag="a", pdf_attrs={"class": "pdf"},
                                 date_tag = False, date_attrs={})


# -----------------------------------------------------------------------------
# AI USA 
# -----------------------------------------------------------------------------

MainUSA = MainSiteHTML(url_head="https://www.amnestyusa.org/search/+/?fwp_paged=",
                       site_source_name="AI USA",
                       arrangement="pages",
                       title_tag="h4", title_attrs={"role": "heading"},
                       output_tag="a", output_attrs={"class": "row card-group d-flex mb-32"},
                       link_in_out_tag=True,
                       link_tag=False, link_attrs={},
                       date_tag="h5", date_attrs={"role": "heading"}, 
                       link_prefix = "https://www.amnestyusa.org",
                       excerpt_tag = "p", excerpt_attrs={"class": "body-3"},
                       sele=False
                       )


OutputUSA = OutputSiteHTML(topics_tag="att_error_prompter", topics_attrs=False, 
                         pdf_tag="h5", pdf_attrs="mb-24 white-text black-bg padding-8 inline",
                           date_tag=False, date_attrs={}
                         )

# -----------------------------------------------------------------------------
# AI Argentina
# -----------------------------------------------------------------------------

MainARG = MainSiteHTML(url_head="https://amnistia.org.ar/page/",
                       output_tag="article", output_attrs={"class": "article"},
                       title_tag="h1", title_attrs={"class": "title"},
                       excerpt_tag="p", excerpt_attrs={"class": "subtitle"},
                       arrangement="pages",
                       link_in_out_tag=False,
                       link_tag="a", link_attrs={"class": "btn-read-more"},
                       link_prefix="",
                       date_tag=False, date_attrs={},
                       site_source_name="AI Argentina",
                       sele=False
                       )

OutputARG = OutputSiteHTML(topics_tag="attr_error_prompter", topics_attrs={},
                           pdf_tag="attr_error_prompter", pdf_attrs={},
                           date_tag="time", date_attrs={})

# -----------------------------------------------------------------------------
# AI France
# -----------------------------------------------------------------------------

MainFRA = MainSiteHTML(
            url_head="https://www.amnesty.fr/search?keywords=a&page=",
            output_tag="div", output_attrs={"class": "src-client-components-Article-Small-__Small___SmallArticle"},
            title_tag="h1", title_attrs={"class": "src-client-components-Article-Small-__Small___Title"},
            date_tag="span", date_attrs="src-client-components-Article-Small-__Small___Date",
            link_in_out_tag=False, 
            link_tag="a", link_attrs={},
            link_prefix="https://www.amnesty.fr",
            site_source_name="AI France",
            excerpt_tag=False, excerpt_attrs={},
            arrangement="pages",
            sele=True
        )

OutputFRA = OutputSiteHTML(
           topics_tag="attr_error_prompter", topics_attrs={},
           pdf_tag="attr_error_prompter", pdf_attrs={}, # PDFs are raw PDFs.
           date_tag=False, date_attrs={},
        )

