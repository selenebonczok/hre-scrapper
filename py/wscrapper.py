import requests, bs4
import pandas as pd
import misc
import lxml, cchardet
from misc import connect, sconnect, is_raw_pdf

# ----

def crawl_main(url, site):
    """Web crawler. Parse and return all URLs corresponding to 
    Amnesty outputs on a search query.

    Parameters 
    ----------
    url : str
        URL of whichever site displays outputs.
    site : MainSiteHTML
        The HTML configuration of the site as specified on 
        scrapconf.py.
    """

    try:
        data = connect(url).text if site.sele is False else sconnect(url)
        html = bs4.BeautifulSoup(data, 'lxml')
        elements = html.find_all(site.output_tag, site.output_attrs)
        return elements
    except ConnectionError:
        # Prompt "No objects to concatenate"
        return []

def get_property(element, tag, attrs, to_get):
    """Helper function. Flexible wrapper for html.find(). 
    
    Allows to map False tag attributes in Main/Output Site objects
    to None value. Useful to deal with HTML configurations 
    that lack some of the typical properties. 

    For example, Amnesty UK, unlike most sites, has no date tag. 
    See MainUKEnglish at scrapconf.py."""

    if tag is False:
        return None
    if to_get != "text" and to_get != "href":
        raise ValueError
    try:
        x = element.find(tag, attrs)
        y = x.text if to_get == "text" else x.get("href")
        return y
    # Surprisingly, some sites have (rare) outputs with inconsistent 
    # title tagging. It becomes necessary to make the program resilient
    # to such anomalies.
    except AttributeError:
        return "Inspection flag"

def get_post_characteristics(element, site, output_site):
    """Given a bs4 soup, examine its relevant tags in accordance
    to the Main Site and Output Site HTML configurations.
    Return extracted features in data frame format."""
    
    if site.link_in_out_tag:
        link = element.get("href")
    else:
        link = get_property(element, site.link_tag, site.link_attrs, "href")
    #if link.startswith("https") is False:
    link = site.link_prefix + link
    print(link)
    date = get_property(element, site.date_tag, site.date_attrs, "text")
    title = get_property(element, site.title_tag, site.title_attrs, "text")
    excerpt = get_property(element, site.excerpt_tag, site.excerpt_attrs, "text")
    if is_raw_pdf(title, link): 
        props = (None, None, True)
    else:
        props = get_text_pdf_topics(link, output_site)

    topics, text, pdf = props[0], props[1], props[2]
    if not output_site.date_tag is False:
        date = props[3]

    dic = {"Title": title, 
           "Source": site.site_source_name,
           "Link": link,
           "Excerpt": excerpt,
           "RawText": text,
           "Tags": topics,
           "Date": date,
           "PDF": pdf
           }
    
    return(pd.DataFrame([dic]))

# This function works but it's ugly. Consider 
# refactoring it.
def get_text_pdf_topics(url, site, get_date=False):
    """Given the URL of an amnesty output and an Output Site HTML
    configuration, return those features of the output that are 
    only accesible by entering the output."""

    try:
        data = connect(url)
    except ConnectionError:
        print("Unable to connect to ", url, "\nSkipping to next output.")
        return(None, "Inspection flag", False)
    html = bs4.BeautifulSoup(data.text, 'lxml')
    try:
        topics_container = html.find(site.topics_tag, site.topics_attrs)
        a_topics = topics_container.findAll("a")
        topics = [x.text for x in a_topics]
    except AttributeError:
        topics = None
    try:
        paragraphs = html.findAll("p")
        text = " \n".join([x.text for x in paragraphs], )
    except AttributeError:
        text = "Inspection flag"
    try:
        pdf = not(html.find(site.pdf_tag, site.pdf_attrs) is None)
    except AttributeError:
        pdf = False

    # Horrible, fix it..
    date = None
    if not site.date_tag is False:
        try:
            date = get_property(html, site.date_tag, site.date_attrs, "text")
        except AttributeError:
            pass

    return(topics, text, pdf, date)

def df_from_site(url, main_site_conf, output_site_conf):
    """Given the URL of an Amensty search-query page, 
    return the dataframes with the properties of each output in the site.
    
    HTML analysis is done in accordance to the MainSite HTML and 
    OutputSite HTML configurations provided."""
    
    divs = crawl_main(url, main_site_conf) 
    chars = map(lambda x: get_post_characteristics(x, main_site_conf, 
                                                   output_site_conf), divs)
    dfs = pd.concat(list(chars))
    return dfs
    

def main(main_site_conf, output_site_conf, first_page = 1, url_tail = ""):
    """Main function. Given the URL head (.../page/) without specified
    page, loops through all pages extracting features from all 
    Amnesty outputs and returns a data frame with all results
    concatenated."""
 
    dfs, i = [], first_page
    missed = []
    counts = 0

    while True:
        if counts > 3:
            break
        try:
            url = main_site_conf.url_head + str(i) + "/" + url_tail
            print("At page", str(i), " \n URL: ", url)
            df = df_from_site(main_site_conf.url_head + str(i), 
                              main_site_conf, output_site_conf)
            dfs.append(df)
            i += 1
            counts = 0
        except ValueError as e:
            print(f"{e}. This page was omitted.")
            missed.append(main_site_conf.url_head + str(i))
            counts += 1
            i += 1
  
    print("Omitted pages : ")
    for page in missed:
        print(page)
    return(pd.concat(dfs))
    
def create_data_by_pages(s, n, main_site_conf, output_site_conf, url_tail=""):
    dfs, i = [], s
    missed = []
    for i in range (s, n + 1):
        try:
            url = main_site_conf.url_head + str(i) + "/" + url_tail
            print("At page", str(i), " \n URL: ", url)
            df = df_from_site(main_site_conf.url_head + str(i), main_site_conf, output_site_conf)
            dfs.append(df)
            i += 1
        except ValueError as e:
            print(f"{e}. This page was omitted.")
            missed.append(main_site_conf.url_head + str(i))
            i += 1
            continue
  
    print("Missed pages : ")
    for x in missed:
        print(x)

    return(pd.concat(dfs))


