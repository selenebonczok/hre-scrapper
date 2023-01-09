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
    output_props (dict of strings): HTML properties identifying the tag.
    
    ----
    
    e.g. : AmnInternational = Site("article", {"class": "post post--result"})
    
    """
    
    def __init__(self, url_head, site_source_name, 
                 arrangement,
                 output_tag, output_props, 
                 link_tag, link_props,
                 link_prefix,
                 date_tag, date_props,
                 title_tag, title_props,
                 excerpt_tag, excerpt_props):
        self.url_head = url_head
        self.arrangement = arrangement
        self.site_source_name = site_source_name
        self.output_tag = output_tag
        self.output_props = output_props
        self.link_tag = link_tag
        self.link_props = link_props
        self.date_tag = date_tag
        self.date_props = date_props
        self.title_tag = title_tag
        self.title_props = title_props
        self.excerpt_tag = excerpt_tag
        self.excerpt_props = excerpt_props
        self.link_prefix = link_prefix
        
class OutputSiteHTML : 
    def __init__(self, topics_tag, topics_props,
                 pdf_tag, pdf_props):
        self.topics_tag = topics_tag
        self.topics_props = topics_props
        self.pdf_tag = pdf_tag
        self.pdf_props = pdf_props
        

# ~ Helpers ~
# ----------

# AI Main Site (English) ~ https://amnesty.org/ ~ 

MainAI = MainSiteHTML(url_head="https://www.amnesty.org/en/search/page/", 
                      site_source_name="AI", 
                      arrangement = "pages",
                      output_tag="article", 
                  output_props={"class": "post post--result"},
                  link_tag = "a", link_props={"class": "floating-anchor"},
                  link_prefix="",
                  date_tag = "span", date_props={},
                  title_tag="h1", title_props={"class": "post-title"},
                  excerpt_tag="div", excerpt_props={"class" : "post-excerpt"})
OutputAI = OutputSiteHTML(topics_props={"class": "topics-container"}, 
                          topics_tag="div",
                          pdf_tag="a", 
                          pdf_props={"class": "btn btn--download btn--primary customSelect-input"})


# AI Canada (English) ~ https://amnesty.ca/ ~ Main Site Tagging  

MainCanadaEnglish = MainSiteHTML(url_head = "https://www.amnesty.ca/search/a/page/", 
                                 site_source_name="Amnesty Canada (English)", 
                                 arrangement="pages", 
                                 output_tag="article", 
                                 output_props={"class": "post post--result"},
                                 link_tag = "a", link_props={"class": "floating-anchor"},
                                 link_prefix="",
                                 date_tag = "span", date_props={},
                                 title_tag="h1", title_props={"class": "post-title"},
                                 excerpt_tag="div", excerpt_props={"class" : "post-excerpt"})

OutputCanadaEnglish = OutputSiteHTML(topics_props={"class": "topics-container"}, 
                          topics_tag="div",
                          pdf_tag="a", 
                          pdf_props={"class": "btn btn--download btn--dark"})


# AI UK 

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
                             output_tag = "div", output_props= {"class": "views-row"},
                             link_tag = "a", link_props={},
                             link_prefix="https://www.amnesty.org.uk",
                             date_tag=False, date_props={},
                             title_tag = "a", title_props={},
                             excerpt_tag=False, excerpt_props={})

OutputUKEnglish = OutputSiteHTML(topics_tag="ul", topics_props={"class": "tags clearfix"},
                          pdf_tag="a", pdf_props={"class": "pdf"})
